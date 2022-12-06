class Board:
    def __init__(self):
        self.__board = [[" " for _ in range(3)] for i in range(3)]

    @property
    def board(self):
        return self.__board
    
    @board.setter
    def board(self, val):
        self.__board = val

    def move(self, n:str, nut:str):
        """ n: a number between 0-8
        nut: X or O
        """
        indexMap = {
            0:0,
            1:1,
            2:2,
            3:0,
            4:1,
            5:2,
            6:0,
            7:1,
            8:2,
        }
        if 0 <= n <= 2:
            if self.__board[0][indexMap[n]] == " ":
                self.__board[0][indexMap[n]] = nut

        elif 3 <= n <= 5:
            if self.__board[1][indexMap[n]] == " ":
                self.__board[1][indexMap[n]] = nut
                print(self.__board)
        
        elif 6 <= n <= 8:
            if self.__board[2][indexMap[n]] == " ":
                self.__board[2][indexMap[n]] = nut
                print(self.__board)


    @staticmethod # check if all of the list item similar, return True
    def __similarItem(li:list):
        for i in range(2):
            if li[i] != li[i + 1]:
                return False
        return True

    def winner(self):
        # check rows
        rows = [r for r in self.__board if " " not in r]
        if rows != []:
            for r in rows:
                if self.__similarItem(r):
                    return 1
        
        # check columns
        columns = [[self.__board[j][i] for j in range(3)] for i in range(3)]
        columns = [c for c in columns if " " not in c]
        if columns != []:
            for c in columns:
                if self.__similarItem(c):
                    return 1
        
        # check diameters
        for _ in range(2):
            diameter = [self.__board[i][i] for i in range(3)]
            if " " not in diameter and self.__similarItem(diameter):
                return 1
            self.__board = self.__board[::-1]
        
        # check filled the board
        check = [r for r in self.__board if " " not in r]
        if len(check) == 3:
            return 2

    def reset(self):
        self.__board = [[" " for _ in range(3)] for i in range(3)]