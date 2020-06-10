# Author: Sullivan Myer
# Date: 5/25/20
# Description: Program which allows users to play Gess (Chess combined with Go)


class InvalidPieceException(Exception):
    """
    Exception which is raised when a player
    attempts to make a move with an invalid piece
    """
    pass


class InvalidMoveException(Exception):
    """
    Exception which is raised when a player
    attempts to make an invalid move
    """
    pass


class Piece:
    """
    Piece class which will be called by the
    make_move method of the Board class
    """
    def __init__(self, center, board_state, player, opponent, own_rings, opponent_rings):
        """
        initializes a piece class when called by
        Board class's make_move method
        takes as params the coordinate of the
        proposed piece's center, the complete
        board state, and the player making the move
        """
        try:
            self._board_state = board_state
            self._player = player
            self._opponent = opponent
            # check if piece is centered on valid column, initialize center letter if so
            if center[0] == 'a' or center[0] == 't':
                raise InvalidPieceException
            else:
                self._center_letter = center[0]
            # check if piece is centered on valid row, initialize center number if so
            if center[1:] == '1' or center[1:] == '20':
                raise InvalidPieceException
            else:
                self._center_number = center[1:]
            # dictionary matching letters with an index for piece construction purposes
            self._letter_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
                                  'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
                                  'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14,
                                  'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19}
            # set the letters for eastern and western columns of the piece
            self._west_letter = list(self._letter_index.items())[self._letter_index[self._center_letter] - 1][0]
            self._east_letter = list(self._letter_index.items())[self._letter_index[self._center_letter] + 1][0]
            # set then numbers of the northern and southern rows of the the piece
            self._north_number = str(int(self._center_number) + 1)
            self._south_number = str(int(self._center_number) - 1)
            # create piece map dictionary
            self._piece = {'NW': self._board_state[self._west_letter][self._north_number],
                           'N': self._board_state[self._center_letter][self._north_number],
                           'NE': self._board_state[self._east_letter][self._north_number],
                           'W': self._board_state[self._west_letter][self._center_number],
                           'C': self._board_state[self._center_letter][self._center_number],
                           'E': self._board_state[self._east_letter][self._center_number],
                           'SW': self._board_state[self._west_letter][self._south_number],
                           'S': self._board_state[self._center_letter][self._south_number],
                           'SE': self._board_state[self._east_letter][self._south_number]}
            # create piece address dictionary
            self._address = {'NW': self._west_letter + self._north_number,
                             'N': self._center_letter + self._north_number,
                             'NE': self._east_letter + self._north_number,
                             'W': self._west_letter + self._center_number,
                             'C': self._center_letter + self._center_number,
                             'E': self._east_letter + self._center_number,
                             'SW': self._west_letter + self._south_number,
                             'S': self._center_letter + self._south_number,
                             'SE': self._east_letter + self._south_number}
            # invalidate the piece if it contains black and white stones, otherwise create valid moves
            if 'w' in self._piece.values() and 'b' in self._piece.values():
                raise InvalidPieceException
            else:
                self._valid_moves = list(set([i[0] for i in self._piece.items() if i[1] != ' ']))
                if 'C' in self._valid_moves:
                    self._valid_moves = {i: 17 for i in self._piece}
                else:
                    self._valid_moves = {i: 3 for i in self._valid_moves}
            # if piece belongs to current player, initialize center
            if self._player[0].lower() not in list(set(self._piece.values())):
                raise InvalidPieceException
            else:
                self._center = center
                self._opponent_rings = opponent_rings
                self._own_rings = own_rings
                if len(own_rings) == 1:
                    self._invalid_centers = list(self.get_invalid_centers(self._own_rings[0]).values())
                else:
                    self.invalid_centers = None
                if self._center in self._invalid_centers:
                    raise InvalidPieceException
                else:
                    self._valid_piece = True
        except InvalidPieceException:
            self._valid_piece = False

    def get_validity(self):
        """returns the validity of the piece"""
        return self._valid_piece

    def get_own_rings(self):
        """returns the rings of the current player"""
        return self._own_rings

    def get_opponent_rings(self):
        """returns opponent rings"""
        return self._opponent_rings

    def get_invalid_centers(self, ring_center):
        """
        given the center coordinate of a ring,
        return a list of invalid centers which
        cannot be the cordinate of a piece
        without breaking the ring
        """
        ring_center_letter = ring_center[0]
        ring_center_number = ring_center[1:]
        far_west_letter = list(self._letter_index.items())[self._letter_index[ring_center_letter] - 2][0]
        far_east_letter = list(self._letter_index.items())[self._letter_index[ring_center_letter] + 2][0]
        far_north_number = str(int(ring_center_number) + 2)
        far_south_number = str(int(ring_center_number) - 2)
        near_west_letter = list(self._letter_index.items())[self._letter_index[ring_center_letter] - 1][0]
        near_east_letter = list(self._letter_index.items())[self._letter_index[ring_center_letter] + 1][0]
        near_north_number = str(int(ring_center_number) + 1)
        near_south_number = str(int(ring_center_number) - 1)
        invalid_centers = {'n11': far_west_letter + far_north_number,
                           'n21': near_west_letter + far_north_number,
                           'n31': ring_center_letter + far_north_number,
                           'n41': near_east_letter + far_north_number,
                           'n51': far_east_letter + far_north_number,
                           'w11': far_west_letter + near_north_number,
                           'w21': far_west_letter + ring_center_number,
                           'w31': far_west_letter + near_south_number,
                           'e11': far_east_letter + near_north_number,
                           'e21': far_east_letter + ring_center_number,
                           'e31': far_east_letter + near_south_number,
                           's11': far_west_letter + far_south_number,
                           's21': near_west_letter + far_south_number,
                           's31': ring_center_letter + far_south_number,
                           's41': near_east_letter + far_south_number,
                           's51': far_east_letter + far_south_number,
                           'n22': near_west_letter + near_north_number,
                           'n32': ring_center_letter + near_north_number,
                           'n42': near_east_letter + near_north_number,
                           'w22': near_west_letter + ring_center_number,
                           'e22': near_east_letter + ring_center_number,
                           's22': near_west_letter + near_south_number,
                           's32': ring_center_letter + near_south_number,
                           's42': near_east_letter + near_south_number}
        return invalid_centers

    def update_rings(self):
        """
        Method which updates the location of
        a ring if it is the moving piece. It
        returns True if the ring remains intact
        and False if the opponents ring is broken
        """
        if self._center in self._own_rings:
            self._own_rings[0] = self._address['C']
            self._center = self._own_rings[0]
        ring_center_letter = self.get_opponent_rings()[0][0]
        ring_center_number = self.get_opponent_rings()[0][1:]
        west_letter = list(self._letter_index.items())[self._letter_index[ring_center_letter] - 1][0]
        east_letter = list(self._letter_index.items())[self._letter_index[ring_center_letter] + 1][0]
        north_number = str(int(ring_center_number) + 1)
        south_number = str(int(ring_center_number) - 1)
        supposed_loc = {'NW': self._board_state[west_letter][north_number],
                        'N': self._board_state[ring_center_letter][north_number],
                        'NE': self._board_state[east_letter][north_number],
                        'W': self._board_state[west_letter][ring_center_number],
                        'C': self._board_state[ring_center_letter][ring_center_number],
                        'E': self._board_state[east_letter][ring_center_number],
                        'SW': self._board_state[west_letter][south_number],
                        'S': self._board_state[ring_center_letter][south_number],
                        'SE': self._board_state[east_letter][south_number]}
        ring_template = {'NW': self._opponent[0].lower(),
                         'N': self._opponent[0].lower(),
                         'NE': self._opponent[0].lower(),
                         'W': self._opponent[0].lower(),
                         'C': ' ',
                         'E': self._opponent[0].lower(),
                         'SW': self._opponent[0].lower(),
                         'S': self._opponent[0].lower(),
                         'SE': self._opponent[0].lower()}
        intact = True
        for i in supposed_loc.keys():
            if supposed_loc[i] == ring_template[i]:
                continue
            else:
                intact = False
        if intact is False:
            print('ring broken', ring_center_letter + ring_center_number)
            return False
        else:
            print('ring intact', ring_center_letter + ring_center_number)
            return True

    def get_valid_moves(self):
        """
        returns a collection of the valid
        moves available to the piece
        """
        return self._valid_moves

    def get_board_state(self):
        """
        returns the board state kept
        internally by the piece.
        Will be returned to the game
        once piece is done moving
        """
        return self._board_state

    def display_piece(self):
        """Displays the piece specified"""
        if self._piece is not None:
            print(self._piece['NW'], self._piece['N'], self._piece['NE'])
            print(self._piece['W'], self._piece['C'], self._piece['E'])
            print(self._piece['SW'], self._piece['S'], self._piece['SE'])
        else:
            print('Not a piece')

    def display_address(self):
        """Displays the address of the piece"""
        if self._address is not None:
            print(self._address['NW'], self._address['N'], self._address['NE'])
            print(self._address['W'], self._address['C'], self._address['E'])
            print(self._address['SW'], self._address['S'], self._address['SE'])
        else:
            print('Not a piece')

    def update_address(self, direction):
        """
        Updates the address of the piece
        as it moves across the board.
        Does not change the piece itself
        """
        if direction == 'N':
            self._center_number = str(int(self._center_number) + 1)
        elif direction == 'NE':
            self._center_number = str(int(self._center_number) + 1)
            self._center_letter = list(self._letter_index.items())[self._letter_index[self._center_letter] + 1][0]
        elif direction == 'E':
            self._center_letter = list(self._letter_index.items())[self._letter_index[self._center_letter] + 1][0]
        elif direction == 'SE':
            self._center_number = str(int(self._center_number) - 1)
            self._center_letter = list(self._letter_index.items())[self._letter_index[self._center_letter] + 1][0]
        elif direction == 'S':
            self._center_number = str(int(self._center_number) - 1)
        elif direction == 'SW':
            self._center_number = str(int(self._center_number) - 1)
            self._center_letter = list(self._letter_index.items())[self._letter_index[self._center_letter] - 1][0]
        elif direction == 'W':
            self._center_letter = list(self._letter_index.items())[self._letter_index[self._center_letter] - 1][0]
        elif direction == 'NW':
            self._center_number = str(int(self._center_number) + 1)
            self._center_letter = list(self._letter_index.items())[self._letter_index[self._center_letter] - 1][0]
        else:
            print('Not a direction')
        self._west_letter = list(self._letter_index.items())[self._letter_index[self._center_letter] - 1][0]
        self._east_letter = list(self._letter_index.items())[self._letter_index[self._center_letter] + 1][0]
        self._north_number = str(int(self._center_number) + 1)
        self._south_number = str(int(self._center_number) - 1)
        self._address = {'NW': self._west_letter + self._north_number,
                         'N': self._center_letter + self._north_number,
                         'NE': self._east_letter + self._north_number,
                         'W': self._west_letter + self._center_number,
                         'C': self._center_letter + self._center_number,
                         'E': self._east_letter + self._center_number,
                         'SW': self._west_letter + self._south_number,
                         'S': self._center_letter + self._south_number,
                         'SE': self._east_letter + self._south_number}

    def update_board_state(self, direction):
        """
        Completes one step in the move of a
        piece by updating the board to reflect
        the new location of the piece, and by
        removing and trailing pieces in its wake
        """
        # place piece layout down on its new footprint
        self._board_state[self._address['NW'][0]][self._address['NW'][1:]] = self._piece['NW']
        self._board_state[self._address['N'][0]][self._address['N'][1:]] = self._piece['N']
        self._board_state[self._address['NE'][0]][self._address['NE'][1:]] = self._piece['NE']
        self._board_state[self._address['W'][0]][self._address['W'][1:]] = self._piece['W']
        self._board_state[self._address['C'][0]][self._address['C'][1:]] = self._piece['C']
        self._board_state[self._address['E'][0]][self._address['E'][1:]] = self._piece['E']
        self._board_state[self._address['SW'][0]][self._address['SW'][1:]] = self._piece['SW']
        self._board_state[self._address['S'][0]][self._address['S'][1:]] = self._piece['S']
        self._board_state[self._address['SE'][0]][self._address['SE'][1:]] = self._piece['SE']

        # collect garbage in the wake of piece's move
        north_front = str(int(self._north_number) + 1)
        south_front = str(int(self._south_number) - 1)
        east_front = list(self._letter_index.items())[self._letter_index[self._east_letter] + 1][0]
        west_front = list(self._letter_index.items())[self._letter_index[self._west_letter] - 1][0]
        if direction == 'N':
            self._board_state[self._address['SW'][0]][south_front] = ' '
            self._board_state[self._address['S'][0]][south_front] = ' '
            self._board_state[self._address['SE'][0]][south_front] = ' '
        elif direction == 'NE':
            self._board_state[west_front][self._address['W'][1:]] = ' '
            self._board_state[west_front][self._address['SW'][1:]] = ' '
            self._board_state[west_front][south_front] = ' '
            self._board_state[self._address['SW'][0]][south_front] = ' '
            self._board_state[self._address['S'][0]][south_front] = ' '
        elif direction == 'E':
            self._board_state[west_front][self._address['NW'][1:]] = ' '
            self._board_state[west_front][self._address['W'][1:]] = ' '
            self._board_state[west_front][self._address['SW'][1:]] = ' '

        elif direction == 'SE':
            self._board_state[west_front][self._address['W'][1:]] = ' '
            self._board_state[west_front][self._address['NW'][1:]] = ' '
            self._board_state[west_front][north_front] = ' '
            self._board_state[self._address['NW'][0]][north_front] = ' '
            self._board_state[self._address['N'][0]][north_front] = ' '

        elif direction == 'S':
            self._board_state[self._address['NW'][0]][north_front] = ' '
            self._board_state[self._address['N'][0]][north_front] = ' '
            self._board_state[self._address['NE'][0]][north_front] = ' '
        elif direction == 'SW':
            self._board_state[east_front][self._address['E'][1:]] = ' '
            self._board_state[east_front][self._address['NE'][1:]] = ' '
            self._board_state[east_front][north_front] = ' '
            self._board_state[self._address['NE'][0]][north_front] = ' '
            self._board_state[self._address['N'][0]][north_front] = ' '
        elif direction == 'W':
            self._board_state[east_front][self._address['NE'][1:]] = ' '
            self._board_state[east_front][self._address['E'][1:]] = ' '
            self._board_state[east_front][self._address['SE'][1:]] = ' '
        elif direction == 'NW':
            self._board_state[east_front][self._address['E'][1:]] = ' '
            self._board_state[east_front][self._address['SE'][1:]] = ' '
            self._board_state[east_front][south_front] = ' '
            self._board_state[self._address['SE'][0]][south_front] = ' '
            self._board_state[self._address['S'][0]][south_front] = ' '
        else:
            print('Not a direction')

    def frontier_scan(self, direction):
        """
        scans the frontier of the move,
        returning True if there are stones,
        False if there are no stones, and
        None if the direction is invalid
        """
        collection_status = None
        north_front = str(int(self._north_number) + 1)
        south_front = str(int(self._south_number) - 1)
        east_front = list(self._letter_index.items())[self._letter_index[self._east_letter] + 1][0]
        west_front = list(self._letter_index.items())[self._letter_index[self._west_letter] - 1][0]
        if direction == 'N':
            frontier = [self._board_state[self._west_letter][north_front],
                        self._board_state[self._center_letter][north_front],
                        self._board_state[self._east_letter][north_front]]
        elif direction == 'NE':
            frontier = [self._board_state[self._center_letter][north_front],
                        self._board_state[self._east_letter][north_front],
                        self._board_state[east_front][north_front],
                        self._board_state[east_front][self._north_number],
                        self._board_state[east_front][self._center_number]]
        elif direction == 'E':
            frontier = [self._board_state[east_front][self._north_number],
                        self._board_state[east_front][self._center_number],
                        self._board_state[east_front][self._south_number]]

        elif direction == 'SE':
            frontier = [self._board_state[self._center_letter][south_front],
                        self._board_state[self._east_letter][south_front],
                        self._board_state[east_front][south_front],
                        self._board_state[east_front][self._south_number],
                        self._board_state[east_front][self._center_number]]
        elif direction == 'S':
            frontier = [self._board_state[self._west_letter][south_front],
                        self._board_state[self._center_letter][south_front],
                        self._board_state[self._east_letter][south_front]]
        elif direction == 'SW':
            frontier = [self._board_state[self._center_letter][south_front],
                        self._board_state[self._west_letter][south_front],
                        self._board_state[west_front][south_front],
                        self._board_state[west_front][self._south_number],
                        self._board_state[west_front][self._center_number]]
        elif direction == 'W':
            frontier = [self._board_state[west_front][self._north_number],
                        self._board_state[west_front][self._center_number],
                        self._board_state[west_front][self._south_number]]
        elif direction == 'NW':
            frontier = [self._board_state[self._center_letter][north_front],
                        self._board_state[self._west_letter][north_front],
                        self._board_state[west_front][north_front],
                        self._board_state[west_front][self._north_number],
                        self._board_state[west_front][self._center_number]]
        else:
            print('Not a direction')
            return collection_status

        if 'b' in frontier or 'w' in frontier:
            print("field of view:", frontier)
            collection_status = True
        else:
            print("field of view:", frontier)
            collection_status = False
        return collection_status

    def move_piece(self, location):
        """validates and coordinates the movement of the piece"""
        success = True
        # if final and initial position are identical
        if location[0] == self._center_letter and location[1:] == self._center_number:
            print('No move made: Final == Initial')
            success = False
            return success
        # if not identical, but in same column, i.e. same letter
        elif location[0] == self._center_letter:
            # sign of difference will determine whether move is north or south
            diff = int(self._center_number) - int(location[1:])
            # if move is north, and north is valid for this piece
            if diff < 0 and 'N' in self._valid_moves.keys():
                if abs(diff) > self._valid_moves['N']:
                    print('proposed move invalid')
                    success = False
                    return success
                desired_distance = min(abs(diff), self._valid_moves['N'])
                direction = 'N'
            # if move is south, and south is valid for this piece
            elif diff > 0 and 'S' in self._valid_moves.keys():
                if abs(diff) > self._valid_moves['S']:
                    print('proposed move invalid')
                    success = False
                    return success
                desired_distance = min(abs(diff), self._valid_moves['S'])
                direction = 'S'
            # if the proposed direction is not a valid move
            else:
                raise InvalidMoveException
        # if not identical, but in same row, i.e. same number
        elif location[1:] == self._center_number:
            # sign of difference will determine whether move is east or west
            diff = self._letter_index[self._center_letter] - self._letter_index[location[0]]
            # if move is east, and east is valid for this piece
            if diff < 0 and 'E' in self._valid_moves.keys():
                if abs(diff) > self._valid_moves['E']:
                    print('proposed move invalid')
                    success = False
                    return success
                desired_distance = min(abs(diff), self._valid_moves['E'])
                direction = 'E'
            # if move is west, and west is valid for this piece
            elif diff > 0 and 'W' in self._valid_moves.keys():
                if abs(diff) > self._valid_moves['W']:
                    print('proposed move invalid')
                    success = False
                    return success
                desired_distance = min(abs(diff), self._valid_moves['W'])
                direction = 'W'
            # if the proposed direction is not a valid move
            else:
                raise InvalidMoveException
        # if neither columns nor rows matches, we look for diagonal matches
        else:
            # signs of differences will determine whether move is nw,ne,se,sw
            row_diff = int(self._center_number) - int(location[1:])
            col_diff = self._letter_index[self._center_letter] - self._letter_index[location[0]]
            # if magnitudes of differences are unequal, the move is not diagonal
            if abs(col_diff) != abs(row_diff):
                raise InvalidMoveException
            # magnitudes are equal, now check which direction
            else:
                # if northeast, and northeast is valid
                if (row_diff < 0 > col_diff) and 'NE' in self._valid_moves:
                    if abs(row_diff) > self._valid_moves['NE']:
                        print('proposed move invalid')
                        success = False
                        return success
                    desired_distance = min(abs(row_diff), self._valid_moves['NE'])
                    direction = 'NE'
                # if northwest, and northwest is valid
                elif (row_diff < 0 < col_diff) and 'NW' in self._valid_moves:
                    if abs(row_diff) > self._valid_moves['NW']:
                        print('proposed move invalid')
                        success = False
                        return success
                    desired_distance = min(abs(row_diff), self._valid_moves['NW'])
                    direction = 'NW'
                # if southeast, and southeast is valid
                elif row_diff > 0 > col_diff and 'SE' in self._valid_moves:
                    if abs(row_diff) > self._valid_moves['SE']:
                        print('proposed move invalid')
                        success = False
                        return success
                    desired_distance = min(abs(row_diff), self._valid_moves['SE'])
                    direction = 'SE'
                # if southwest, and southwest is valid
                elif row_diff > 0 < col_diff and 'SW' in self._valid_moves:
                    if abs(row_diff) > self._valid_moves['SW']:
                        print('proposed move invalid')
                        success = False
                        return success
                    desired_distance = min(abs(row_diff), self._valid_moves['SW'])
                    direction = 'SW'
                # if invalid direction or move is entered
                else:
                    print('something went wrong')
                    success = False
                    return success
        for i in range(desired_distance):
            print("--")
            print("beginning of iteration", i)
            if self.frontier_scan(direction):
                self.update_address(direction)
                self.update_rings()
                self.update_board_state(direction)
                print('pieces recognized, board will be updated, but players will switch and movement ended')
                break
            else:
                self.update_address(direction)
                self.update_rings()
                self.update_board_state(direction)
                print('no pieces recognized')
                self.display_piece()
                self.display_address()
            print("end of iteration", i)
        return success


class GessGame:
    """
    Class allowing users the
    ability to play go virtually.
    Takes no parameters
    """
    def __init__(self):
        self._board = {'a': {'1': ' ', '2': ' ', '3': ' ', '4': ' ', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': ' ', '18': ' ', '19': ' ', '20': ' '},
                       'b': {'1': ' ', '2': ' ', '3': 'b', '4': ' ', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': ' ', '18': 'w', '19': ' ', '20': ' '},
                       'c': {'1': ' ', '2': 'b', '3': 'b', '4': 'b', '5': ' ',
                             '6': ' ', '7': 'b', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': 'w', '15': ' ',
                             '16': ' ', '17': 'w', '18': 'w', '19': 'w', '20': ' '},
                       'd': {'1': ' ', '2': ' ', '3': 'b', '4': ' ', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': ' ', '18': 'w', '19': ' ', '20': ' '},
                       'e': {'1': ' ', '2': 'b', '3': ' ', '4': 'b', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': 'w', '18': ' ', '19': 'w', '20': ' '},
                       'f': {'1': ' ', '2': ' ', '3': 'b', '4': ' ', '5': ' ',
                             '6': ' ', '7': 'b', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': 'w', '15': ' ',
                             '16': ' ', '17': ' ', '18': 'w', '19': ' ', '20': ' '},
                       'g': {'1': ' ', '2': 'b', '3': ' ', '4': 'b', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': 'w', '18': ' ', '19': 'w', '20': ' '},
                       'h': {'1': ' ', '2': 'b', '3': 'b', '4': 'b', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': 'w', '18': 'w', '19': 'w', '20': ' '},
                       'i': {'1': ' ', '2': 'b', '3': 'b', '4': 'b', '5': ' ',
                             '6': ' ', '7': 'b', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': 'w', '15': ' ',
                             '16': ' ', '17': 'w', '18': 'w', '19': 'w', '20': ' '},
                       'j': {'1': ' ', '2': 'b', '3': 'b', '4': 'b', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': 'w', '18': 'w', '19': 'w', '20': ' '},
                       'k': {'1': ' ', '2': 'b', '3': 'b', '4': 'b', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': 'w', '18': 'w', '19': 'w', '20': ' '},
                       'l': {'1': ' ', '2': 'b', '3': ' ', '4': 'b', '5': ' ',
                             '6': ' ', '7': 'b', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': 'w', '15': ' ',
                             '16': ' ', '17': 'w', '18': ' ', '19': 'w', '20': ' '},
                       'm': {'1': ' ', '2': 'b', '3': 'b', '4': 'b', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': 'w', '18': 'w', '19': 'w', '20': ' '},
                       'n': {'1': ' ', '2': 'b', '3': ' ', '4': 'b', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': 'w', '18': ' ', '19': 'w', '20': ' '},
                       'o': {'1': ' ', '2': ' ', '3': 'b', '4': ' ', '5': ' ',
                             '6': ' ', '7': 'b', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': 'w', '15': ' ',
                             '16': ' ', '17': ' ', '18': 'w', '19': ' ', '20': ' '},
                       'p': {'1': ' ', '2': 'b', '3': ' ', '4': 'b', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': 'w', '18': ' ', '19': 'w', '20': ' '},
                       'q': {'1': ' ', '2': ' ', '3': 'b', '4': ' ', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': ' ', '18': 'w', '19': ' ', '20': ' '},
                       'r': {'1': ' ', '2': 'b', '3': 'b', '4': 'b', '5': ' ',
                             '6': ' ', '7': 'b', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': 'w', '15': ' ',
                             '16': ' ', '17': 'w', '18': 'w', '19': 'w', '20': ' '},
                       's': {'1': ' ', '2': ' ', '3': 'b', '4': ' ', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': ' ', '18': 'w', '19': ' ', '20': ' '},
                       't': {'1': ' ', '2': ' ', '3': ' ', '4': ' ', '5': ' ',
                             '6': ' ', '7': ' ', '8': ' ', '9': ' ', '10': ' ',
                             '11': ' ', '12': ' ', '13': ' ', '14': ' ', '15': ' ',
                             '16': ' ', '17': ' ', '18': ' ', '19': ' ', '20': ' '}
                       }
        self._current_player = 'BLACK'
        self._non_current_player = 'WHITE'
        self._ring_addresses = {'BLACK': ['l3'], 'WHITE': ['l18']}
        self._game_state = 'UNFINISHED'

    def print_board(self):
        """
        prints out the present state of the board,
        which is invaluable when debugging.
        """
        print(' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
              'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
              sep='  ')
        for number in range(20, 0, -1):
            if int(number) >= 10:
                print(number, end=' ')
            else:
                print(f' {number}', end=' ')
            for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']:
                if letter != 't':
                    print(self._board[letter][str(number)], end='  ')
                else:
                    print(self._board[letter][str(number)], number, end='\n')
        print(' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
              'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', sep='  ')

    def get_board(self):
        """returns the current state of the gess board"""
        return self._board

    def get_current_player(self):
        """returns the player whose turn it is"""
        return self._current_player

    def get_non_current_player(self):
        """returns the player whose turn it is not"""
        return self._non_current_player

    def get_game_state(self):
        """returns the current game state"""
        return self._game_state

    def switch_players(self):
        """swap current and non_current players"""
        temp = self.get_non_current_player()
        self._non_current_player = self.get_current_player()
        self._current_player = temp

    def resign_game(self):
        """
        Allows a player to cede victory
        """
        if self._current_player == 'BLACK':
            self._game_state = 'WHITE_WON'
        else:
            self._game_state = 'BLACK_WON'
        print(self._game_state)
        self.print_board()

    def update_game_state(self, status, current_player):
        """updates game state"""
        if status:
            self._game_state = 'UNFINISHED'
        else:
            if current_player == 'WHITE':
                self._game_state = 'WHITE_WON'
            else:
                self._game_state = 'BLACK_WON'

    def make_move(self, initial, final):
        """
        Not yet complete method which will update the board, current_player,
        and game state if called with valid initial and final conditions
        :param initial: proposed moving piece center coordinate
        :param final: proposed final location of center coordinate
        :return: Not sure yet
        """
        if self.get_game_state() != 'UNFINISHED':
            return False
        moving_piece = Piece(initial,
                             self.get_board(),
                             self.get_current_player(),
                             self.get_non_current_player(),
                             self._ring_addresses[self.get_current_player()],
                             self._ring_addresses[self.get_non_current_player()])
        if moving_piece.get_validity():
            results = moving_piece.move_piece(final)
            if results:
                self._board = moving_piece.get_board_state()
                self.print_board()
                self.update_game_state(moving_piece.update_rings(), self._current_player)
                if self.get_game_state() == 'UNFINISHED':
                    self.switch_players()
                    print('CURRENT PLAYER:', self.get_current_player())
                    print('GAME STATE:', self.get_game_state())
                else:
                    print('GAME STATE:', self.get_game_state())
                move_status = True
            else:
                move_status = False
        else:
            move_status = False
        return move_status
