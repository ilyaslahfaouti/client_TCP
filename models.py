from abc import ABC, abstractmethod
import random

class Game:

    def __init__(self, nb_max_turn, width, height):
        self.__nb_max_turn = nb_max_turn # dunder => double underscore ?
        self.__current_turn = 0
        self.__gameboard = GameBoard(height, width)
        self.__actions = {}

    @property
    def nb_max_turn(self):
        return self.__nb_max_turn

    # action: (width, height) (-1,0), (1,0), (0,1),(0,-1)
    # TODO: use Thread to wait until timeout is reached for action
    def register_action(self, player, action):
        self.__actions[player] = action

    def process_action(self):
        for player, action in self.__actions.items():
            self.__gameboard.move_player(player, action)
        self.__actions.clear()


class Player(ABC):

    # pseudo only 1 letter length
    def __init__(self, pseudo : str, field_distance):
        if len(pseudo) != 1:
            raise ValueError('Max length of pseudo is 1')
        self.__pseudo = pseudo
        self.__field_distance = field_distance
        self.__position_width = None
        self.__position_height = None

    @property
    def position(self):
        return (self.__position_width, self.__position_height)

    @position.setter
    def position(self, value):
        self.__position_width, self.__position_height = value

    @property
    def pseudo(self):
        return self.__pseudo

    @property
    def field_distance(self):
        return self.__field_distance

    def __str__(self):
        return self.__pseudo

    def __eq__(self, object):
        return isinstance(object, self.__class__)

class Wolf(Player):

    def __init__(self, pseudo):
        super().__init__(pseudo, field_distance = 2)

    def __str__(self):
        return 'W'

    def __gt__(self, object):
        return isinstance(object, Villager) or isinstance(object, CellEmpty)


class Villager(Player):
    def __init__(self, pseudo):
        super().__init__(pseudo, field_distance = 1)

    def __gt__(self, object):
        return not isinstance(object, Wolf) or isinstance(object, CellEmpty)

    def __str__(self):
        return 'O'

class CellEmpty(Player):

    def __init__(self, pseudo = '.'):
        super().__init__(pseudo, field_distance = 0)

    def __gt__(self, object):
        return False

    def __str__(self):
        return '.'

class GameBoard:

    def __init__(self, width, height):
        self.__height = height
        self.__width = width
        self.__content = [[CellEmpty()] * width for _ in range(height)]
        self.__next_content = [[CellEmpty()] * self.__width for _ in range(self.__height)]
        # init a list of positions
        self.__available_start_positions = GameBoard.init_start_positions(width, height)

    @classmethod
    def init_start_positions(cls, width, height):
        start_positions = []
        for idx_height in range(height):
            for idx_width in range(width):
                start_positions.append((idx_width, idx_height))
        return start_positions

    def subscribe_player(self, player: Player):
        if len(self.__available_start_positions) > 0:
            player_width, player_height = random.choice(self.__available_start_positions)
            player.position = player_width, player_height
            self.__available_start_positions.remove(player.position)
            self.__content[player_height][player_width] = player
        else:
            print('No more space to play')

    def move_player(self, player: Player, action):
        width_delta, height_delta = action
        if -1 <= width_delta <= 1 and -1 <= height_delta <= 1:
            current_width, current_height = player.position
            next_width, next_height = current_width + width_delta, current_height + height_delta
            if 0 <= next_width < self.__width and 0 <= next_height < self.__height:
                existing_character = self.__next_content[next_height][next_width]
                if existing_character < player:
                    player.position = (next_width, next_height)
                    self.__next_content[next_height][next_width] = player

    def end_round(self):
        for idx_h, h in enumerate(self.__next_content):
            for idx_w, w in enumerate(self.__next_content[idx_h]):
                self.__content[idx_h][idx_w] = self.__next_content[idx_h][idx_w]
        self.__next_content = [[CellEmpty()] * self.__width for _ in range(self.__height)]


    def __repr__(self):
        result = ''
        for row in self.__content:
            result += ' '.join(map(str, row)) + '\n'
        return result


if __name__ == '__main__':
    g = GameBoard(10, 5)
    print(g)
    p1 = Wolf('A')
    p2 = Wolf('B')
    p3 = Villager('V')
    p4 = Villager('X')
    for i in range(53):
        g.subscribe_player(p1)
#    g.subscribe_player(p2)
#    g.subscribe_player(p3)
#    g.subscribe_player(p4)
    print(g)
    # print(p1, p2, 'p1 == p2', p1 == p2)
    # print(p3, p4, 'p3 == p4', p3 == p4)
    # print(p1, p2, 'p1 < p2', p1 < p2)
    # print(p1, p2, 'p1 > p2', p1 > p2)
    # print(p1, p3, 'p1 < p3', p1 < p3)
    # print(p1, p3, 'p1 > p3', p1 > p3)
    # print(p1, p3, 'p1 == p3', p1 == p3)
    # print(p2, p4, 'p2 == p4', p2 == p4)
    # print(p2, CellEmpty(), 'p2 == .', p2 == CellEmpty())
    # print(p2, CellEmpty(), 'p2 > .', p2 > CellEmpty())
    # g.move_player(p1, (0,1))
    # g.move_player(p3, (1,0))
    # g.end_round()
    # print(g)
