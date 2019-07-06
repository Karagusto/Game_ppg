import pygame
from pygame.locals import *
import numpy as np
import sys


class Board:
    def __init__(self, width, height):
        pygame.init()

        self.width = width
        self.height = height
        self.wstep = self.width / 8
        self.hstep = self.height / 8

        self.whitePlays = True

        self.screen = pygame.display.set_mode((width, height), 0, 32)
        self.colors = [(255, 255, 255), (0, 0, 0), (255, 178, 102), (80, 40, 0)]
        self.empty_board = [[0, 0], [0, 3], [0, 6],
                            [1, 1], [1, 3], [1, 5],
                            [2, 2], [2, 3], [2, 4],
                            [3, 0], [3, 1], [3, 2], [3, 4], [3, 5], [3, 6],
                            [4, 2], [4, 3], [4, 4],
                            [5, 1], [5, 3], [5, 5],
                            [6, 0], [6, 3], [6, 6]]

        self.board = np.ones((7, 7))*3

        for coords in self.empty_board:
                self.board[coords[0], coords[1]] = 0

    def draw_board(self):
        wstep = self.width / 8
        hstep = self.height / 8

        self.screen.fill(self.colors[0])

        for i in range(1, 4):
            pygame.draw.rect(self.screen, self.colors[1], [wstep*i, hstep*i, wstep*(6-2*(i-1)), hstep*(6-2*(i-1))], 3)

        pygame.draw.line(self.screen, self.colors[1], [wstep, hstep*4], [wstep*3, hstep*4], 3)
        pygame.draw.line(self.screen, self.colors[1], [wstep*5, hstep*4], [wstep*7, hstep*4], 3)
        pygame.draw.line(self.screen, self.colors[1], [wstep*4, hstep], [wstep*4, hstep*3], 3)
        pygame.draw.line(self.screen, self.colors[1], [wstep*4, hstep*5], [wstep*4, hstep*7], 3)

        for coord in self.empty_board:
            self.draw_coord(coord, 4, self.colors[1])

    # draws to the coordinates [row, column] (starts by 1)
    def draw_coord(self, coords, radius, col):
        y = coords[0]
        x = coords[1]

        h = (y+1) * self.hstep
        w = (x+1) * self.wstep

        pygame.draw.circle(self.screen, col, [w, h], radius)
        pygame.draw.circle(self.screen, (0, 0, 0), [w, h], radius, 1)

    def set_pawn(self, coords):
        if self.whitePlays:
            player = 1
        else:
            player = 2

        col = self.colors[player+1]

        self.draw_coord(coords, 15, col)

        self.board[coords[0], coords[1]] = player

        self.whitePlays = not self.whitePlays

    def play_move(self):
        self.dummy_thinking()

    def dummy_thinking(self):
        for i, row in enumerate(self.board):
            for j, spot in enumerate(row):
                if spot == 0:
                    self.set_pawn([i, j])
                    return

    def start(self):
        self.draw_board()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    # detect clicked positions and set pawns
                    for coords in self.empty_board:
                        w = (coords[1]+1) * self.wstep
                        h = (coords[0]+1) * self.hstep

                        if w-self.wstep/3 < pos[0] < w+self.wstep/3 and h-self.hstep/3 < pos[1] < h+self.hstep/3:
                            self.set_pawn(coords)

                            # reply
                            self.play_move()
                            print("ok")
                            break


                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()


