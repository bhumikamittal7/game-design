import pygame
import random
import math

board_size = 16
adjust_size = 50
WINDOW_WIDTH = (board_size + 2) * adjust_size
WINDOW_HEIGHT = board_size * adjust_size
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 10)
selection = True
first_click = True
turn = 'player1'
counter = 0
ctpb = ''
duplicate = []
pieces = []
places = [
    (adjust_size * 8, adjust_size, 0, [2, 28]),
    (adjust_size * 8, adjust_size * 15, 1, [30, 33]),
    (adjust_size, adjust_size, 2, [0, 3]),
    (adjust_size, adjust_size * 3, 3, [2, 26, 4]),
    (adjust_size, adjust_size * 5, 4, [3, 5, 7]),
    (adjust_size * 4.5, adjust_size * 5, 5, [4, 6]),
    (adjust_size * 4.5, adjust_size * 7, 6, [7, 5, 18]),
    (adjust_size, adjust_size * 8, 7, [4, 10, 6, 8]),
    (adjust_size * 4.5, adjust_size * 9, 8, [7, 20, 9]),
    (adjust_size * 4.5, adjust_size * 11, 9, [8, 10]),
    (adjust_size, adjust_size * 11, 10, [9, 7, 29]),
    (adjust_size * 15 - 1, adjust_size * 5, 11, [12, 27, 14]),
    (adjust_size * 11.5, adjust_size * 5, 12, [13, 11]),
    (adjust_size * 11.5, adjust_size * 7, 13, [12, 18, 14]),
    (adjust_size * 15 - 1, adjust_size * 8, 14, [13, 15, 11, 17]),
    (adjust_size * 11.5, adjust_size * 9, 15, [20, 16, 14]),
    (adjust_size * 11.5, adjust_size * 11, 16, [15, 17]),
    (adjust_size * 15 - 1, adjust_size * 11, 17, [16, 14, 32]),
    (adjust_size * 8, adjust_size * 6, 18, [6, 23, 24, 13, 26, 20]),
    (adjust_size, adjust_size * 8, 19, []),
    (adjust_size * 8, adjust_size * 10, 20, [8, 23, 24, 15, 18, 31]),
    (adjust_size * 15 - 1, adjust_size * 8, 21, []),
    (adjust_size * 8, adjust_size * 6, 22, []),
    (adjust_size * 6, adjust_size * 8, 23, [18, 24, 20]),
    (adjust_size * 10, adjust_size * 8, 24, [23, 18, 20]),
    (adjust_size * 8, adjust_size * 10, 25, []),
    (adjust_size * 8, adjust_size * 3, 26, [3, 27, 18]),
    (adjust_size * 15, adjust_size * 3, 27, [26, 28, 11]),
    (adjust_size * 15, adjust_size, 28, [0, 27]),
    (adjust_size, adjust_size * 13, 29, [10, 30, 31]),
    (adjust_size, adjust_size * 15, 30, [29, 1]),
    (adjust_size * 8, adjust_size * 13, 31, [29, 20, 32]),
    (adjust_size * 15, adjust_size * 13, 32, [31, 17, 33]),
    (adjust_size * 15, adjust_size * 15, 33, [1, 32])
]


def game():
    global SCREEN
    pygame.display.set_caption("COIN JUMPERS")
    SCREEN.fill("WHITE")

    run = True
    draw_grid()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                check_move(pygame.mouse.get_pos())
        for i in pieces:
            if [400, 50] == i[0] and i[1] == "2":
                print("player 2 wins")
                return
            if [400, 750] == i[0] and i[1] == "1":
                print("player 1 wins")
                return
        pygame.display.update()


def draw_grid():
    outer = pygame.Rect(adjust_size, adjust_size, 700, 700)
    pygame.draw.rect(SCREEN, 'BLACK', outer, 1)
    inner = pygame.Rect(adjust_size, adjust_size * 3, 700, 500)
    pygame.draw.rect(SCREEN, 'BLACK', inner, 1)
    pygame.draw.circle(SCREEN, 'RED', (adjust_size * 8, adjust_size), 20, 20)
    pygame.draw.circle(SCREEN, 'RED', (adjust_size * 8, adjust_size * 15), 20, 20)
    pygame.draw.line(SCREEN, 'BLACK', (adjust_size * 8, adjust_size * 3), (adjust_size * 8, (adjust_size * 13) - 1), 1)
    pygame.draw.polygon(SCREEN, 'BLACK', ((adjust_size, adjust_size * 5),
                                          (adjust_size * 4.5, adjust_size * 5),
                                          (adjust_size * 4.5, adjust_size * 7),
                                          (adjust_size, adjust_size * 8),
                                          (adjust_size * 4.5, adjust_size * 9),
                                          (adjust_size * 4.5, adjust_size * 11),
                                          (adjust_size, adjust_size * 11),
                                          ), 1)
    pygame.draw.polygon(SCREEN, 'BLACK', ((adjust_size * 15 - 1, adjust_size * 5),
                                          (adjust_size * 11.5, adjust_size * 5),
                                          (adjust_size * 11.5, adjust_size * 7),
                                          (adjust_size * 15 - 1, adjust_size * 8),
                                          (adjust_size * 11.5, adjust_size * 9),
                                          (adjust_size * 11.5, adjust_size * 11),
                                          (adjust_size * 15 - 1, adjust_size * 11),
                                          ), 1)
    pygame.draw.polygon(SCREEN, 'BLACK', ((adjust_size * 8, adjust_size * 6),
                                          (adjust_size, adjust_size * 8),
                                          (adjust_size * 8, adjust_size * 10),
                                          (adjust_size * 15 - 1, adjust_size * 8)), 1)
    pygame.draw.polygon(SCREEN, 'BLACK', ((adjust_size * 8, adjust_size * 6),
                                          (adjust_size * 6, adjust_size * 8),
                                          (adjust_size * 8, adjust_size * 10),
                                          (adjust_size * 10, adjust_size * 8)), 1)
    pygame.draw.line(SCREEN, 'BLACK', (adjust_size * 6, adjust_size * 8), (adjust_size * 10, adjust_size * 8), 1)
    pygame.draw.circle(SCREEN, 'BLUE', (adjust_size * 8, adjust_size), 30, 10)
    pygame.draw.circle(SCREEN, 'BLUE', (adjust_size * 8, adjust_size * 15), 30, 10)
    pygame.draw.circle(SCREEN, 'BLACK', (adjust_size * 8, adjust_size), 32, 2)
    pygame.draw.circle(SCREEN, 'BLACK', (adjust_size * 8, adjust_size * 15), 32, 2)

    pygame.draw.circle(SCREEN, 'GREY', (adjust_size, adjust_size), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size, adjust_size * 3), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size, adjust_size * 5), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 4.5, adjust_size * 5), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 4.5, adjust_size * 7), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size, adjust_size * 8), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 4.5, adjust_size * 9), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 4.5, adjust_size * 11), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size, adjust_size * 11), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 15 - 1, adjust_size * 5), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 11.5, adjust_size * 5), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 11.5, adjust_size * 7), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 15 - 1, adjust_size * 8), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 11.5, adjust_size * 9), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 11.5, adjust_size * 11), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 15 - 1, adjust_size * 11), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 8, adjust_size * 6), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size, adjust_size * 8), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 8, adjust_size * 10), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 15 - 1, adjust_size * 8), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 8, adjust_size * 6), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 6, adjust_size * 8), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 8, adjust_size * 10), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 10, adjust_size * 8), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 8, adjust_size * 3), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 15, adjust_size * 3), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 15, adjust_size), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size, adjust_size * 13), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size, adjust_size * 15), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 8, adjust_size * 13), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 15, adjust_size * 13), 16, 16)
    pygame.draw.circle(SCREEN, 'GREY', (adjust_size * 15, adjust_size * 15), 16, 16)

    prect = pygame.Rect(800, 0, 200, 800)
    pygame.draw.rect(SCREEN, 'BLACK', prect)

    pygame.draw.circle(SCREEN, 'PINK', (adjust_size * 17, adjust_size * 2), 40, 40)
    pygame.draw.circle(SCREEN, 'ORANGE', (adjust_size * 17, adjust_size * 6), 40, 40)
    pygame.draw.circle(SCREEN, 'GREEN', (adjust_size * 17, adjust_size * 10), 40, 40)
    pygame.draw.circle(SCREEN, 'BROWN', (adjust_size * 17, adjust_size * 14), 40, 40)


def check_move(position):
    global piece_to_move
    global location
    global selection
    global counter
    global turn
    global first_click
    global ctpb
    if selection:
        if first_click:
            if 800 <= position[0] <= 900 and 50 <= position[1] <= 150:
                ctpb = 'PINK'
            elif 800 <= position[0] <= 900 and 250 <= position[1] <= 350:
                ctpb = 'ORANGE'
            elif 800 <= position[0] <= 900 and 450 <= position[1] <= 550:
                ctpb = 'GREEN'
            elif 800 <= position[0] <= 900 and 650 <= position[1] <= 750:
                ctpb = 'BROWN'
            else:
                return
            first_click = False
        else:
            if turn == 'player1':
                if adjust_size - 8 <= position[0] <= adjust_size + 8 and adjust_size - 8 <= \
                        position[1] <= adjust_size + 8 and [adjust_size, adjust_size] not in duplicate:
                    pygame.draw.circle(SCREEN, ctpb, (adjust_size, adjust_size), 10, 10)
                    duplicate.append([adjust_size, adjust_size])
                    pieces.append([[adjust_size, adjust_size], "1", ctpb])
                elif (adjust_size * 15) - 8 <= position[0] <= (adjust_size * 15) + 8 and adjust_size - 8 <= \
                        position[1] <= adjust_size + 8 and [adjust_size * 15, adjust_size] not in duplicate:
                    pygame.draw.circle(SCREEN, ctpb, (adjust_size * 15, adjust_size), 10, 10)
                    duplicate.append([adjust_size * 15, adjust_size])
                    pieces.append([[adjust_size * 15, adjust_size], "1", ctpb])
                elif (adjust_size * 15) - 8 <= position[0] <= (adjust_size * 15) + 8 and (adjust_size * 3) - 8 <= \
                        position[1] <= (adjust_size * 3) + 8 and [adjust_size * 15, adjust_size * 3] not in duplicate:
                    pygame.draw.circle(SCREEN, ctpb, (adjust_size * 15, adjust_size * 3), 10, 10)
                    duplicate.append([adjust_size * 15, adjust_size * 3])
                    pieces.append([[adjust_size * 15, adjust_size * 3], "1", ctpb])
                elif (adjust_size * 8) - 8 <= position[0] <= (adjust_size * 8) + 8 and (adjust_size * 3) - 8 <= \
                        position[1] <= (adjust_size * 3) + 8 and [adjust_size * 8, adjust_size * 3] not in duplicate:
                    pygame.draw.circle(SCREEN, ctpb, (adjust_size * 8, adjust_size * 3), 10, 10)
                    duplicate.append([adjust_size * 8, adjust_size * 3])
                    pieces.append([[adjust_size * 8, adjust_size * 3], "1", ctpb])
                elif adjust_size - 8 <= position[0] <= adjust_size + 8 and (adjust_size * 3) - 8 <= position[1] <= (
                        adjust_size * 3) + 8 and [adjust_size, adjust_size * 3] not in duplicate:
                    pygame.draw.circle(SCREEN, ctpb, (adjust_size, adjust_size * 3), 10, 10)
                    duplicate.append([adjust_size, adjust_size * 3])
                    pieces.append([[adjust_size, adjust_size * 3], "1", ctpb])

                else:
                    return
                text = font.render("1", True, "BLACK")
                text_rect = text.get_rect()
                text_rect.center = tuple(duplicate[-1])
                SCREEN.blit(text, text_rect)
                first_click = True
                turn = 'player2'
                counter += 1
                if counter == 10:
                    selection = False

            else:
                if adjust_size - 8 <= position[0] <= adjust_size + 8 and (adjust_size * 15) - 8 <= \
                        position[1] <= (adjust_size * 15) + 8 and [adjust_size, adjust_size * 15] not in duplicate:
                    pygame.draw.circle(SCREEN, ctpb, (adjust_size, adjust_size * 15), 10, 10)
                    duplicate.append([adjust_size, adjust_size * 15])
                    pieces.append([[adjust_size, adjust_size * 15], "2", ctpb])
                elif (adjust_size * 15) - 8 <= position[0] <= (adjust_size * 15) + 8 and (adjust_size * 15) - 8 <= \
                        position[1] <= (adjust_size * 15) + 8 and [adjust_size * 15, adjust_size * 15] not in duplicate:
                    pygame.draw.circle(SCREEN, ctpb, (adjust_size * 15, adjust_size * 15), 10, 10)
                    duplicate.append([adjust_size * 15, adjust_size * 15])
                    pieces.append([[adjust_size * 15, adjust_size * 15], "2", ctpb])
                elif (adjust_size * 15) - 8 <= position[0] <= (adjust_size * 15) + 8 and (adjust_size * 13) - 8 <= \
                        position[1] <= (adjust_size * 13) + 8 and [adjust_size * 15, adjust_size * 13] not in duplicate:
                    pygame.draw.circle(SCREEN, ctpb, (adjust_size * 15, adjust_size * 13), 10, 10)
                    duplicate.append([adjust_size * 15, adjust_size * 13])
                    pieces.append([[adjust_size * 15, adjust_size * 13], "2", ctpb])
                elif (adjust_size * 8) - 8 <= position[0] <= (adjust_size * 8) + 8 and (adjust_size * 13) - 8 <= \
                        position[1] <= (adjust_size * 13) + 8 and [adjust_size * 8, adjust_size * 13] not in duplicate:
                    pygame.draw.circle(SCREEN, ctpb, (adjust_size * 8, adjust_size * 13), 10, 10)
                    duplicate.append([adjust_size * 8, adjust_size * 13])
                    pieces.append([[adjust_size * 8, adjust_size * 13], "2", ctpb])
                elif adjust_size - 8 <= position[0] <= adjust_size + 8 and (adjust_size * 13) - 8 <= position[1] <= (
                        adjust_size * 13) + 8 and [adjust_size, adjust_size * 13] not in duplicate:
                    pygame.draw.circle(SCREEN, ctpb, (adjust_size, adjust_size * 13), 10, 10)
                    duplicate.append([adjust_size, adjust_size * 13])
                    pieces.append([[adjust_size, adjust_size * 13], "2", ctpb])

                else:
                    return
                text = font.render("2", True, "BLACK")
                text_rect = text.get_rect()
                text_rect.center = tuple(duplicate[-1])
                SCREEN.blit(text, text_rect)
                first_click = True
                turn = 'player1'
                counter += 1
                if counter == 10:
                    selection = False
    else:
        if first_click:
            piece_pos = check_clicked(position)
            if piece_pos is None:
                return
            for piece in pieces:
                if piece[0] == [piece_pos[0], piece_pos[1]]:
                    if (turn == "player1" and piece[1] == "1") or (turn == "player2" and piece[1] == "2"):
                        location = piece_pos
                        piece_to_move = piece
                        first_click = False
                        return
            return
        else:
            first_click = True
            piece_pos = check_clicked(position)
            if piece_pos is None:
                return
            if piece_pos[2] in location[3]:
                temp = [piece_pos[0], piece_pos[1]]
                for piece in pieces:
                    if temp == piece[0]:
                        if piece_to_move[1] != piece[1]:
                            attack, defence = kill(piece_to_move[2], piece[2])
                            print(attack)
                            print(defence)
                            if attack == defence:
                                if turn == "player1":
                                    turn = "player2"
                                else:
                                    turn = "player1"
                            elif attack == "miss":
                                if location[2] in [0, 1]:
                                    colour = "RED"
                                else:
                                    colour = "GREY"
                                pygame.draw.circle(SCREEN, colour, (location[0], location[1]), 16, 16)
                                piece[0] = [999, 999]
                                if turn == "player1":
                                    turn = "player2"
                                else:
                                    turn = "player1"
                            elif attack == "hit":
                                print("hi")
                                for j in pieces:
                                    if j[0] == [piece_pos[0], piece_pos[1]]:
                                        j[0] = [999, 999]
                                piece[0] = [piece_pos[0], piece_pos[1]]
                                if location[2] in [0, 1]:
                                    colour = "RED"
                                else:
                                    colour = "GREY"
                                pygame.draw.circle(SCREEN, colour, (location[0], location[1]), 16, 16)
                                pygame.draw.circle(SCREEN, piece_to_move[2], (piece_pos[0], piece_pos[1]), 10, 10)
                                text = font.render(piece_to_move[1], True, "BLACK")
                                text_rect = text.get_rect()
                                text_rect.center = (piece_pos[0], piece_pos[1])
                                SCREEN.blit(text, text_rect)
                                if turn == "player1":
                                    turn = "player2"
                                else:
                                    turn = "player1"
                            else:
                                print("hi")
                                for j in pieces:
                                    if j[0] == [piece_pos[0], piece_pos[1]]:
                                        j[0] = [999, 999]
                                piece[0] = [piece_pos[0], piece_pos[1]]
                                if location[2] in [0, 1]:
                                    colour = "RED"
                                else:
                                    colour = "GREY"
                                pygame.draw.circle(SCREEN, colour, (location[0], location[1]), 16, 16)
                                pygame.draw.circle(SCREEN, piece_to_move[2], (piece_pos[0], piece_pos[1]), 10, 10)
                                text = font.render(piece_to_move[1], True, "BLACK")
                                text_rect = text.get_rect()
                                text_rect.center = (piece_pos[0], piece_pos[1])
                                SCREEN.blit(text, text_rect)
                            pygame.display.update()
                            return
                        return
                for piece in pieces:
                    if piece == piece_to_move:
                        piece[0] = [piece_pos[0], piece_pos[1]]
                        if location[2] in [0, 1]:
                            colour = "RED"
                        else:
                            colour = "GREY"
                        pygame.draw.circle(SCREEN, colour, (location[0], location[1]), 16, 16)
                        pygame.draw.circle(SCREEN, piece_to_move[2], (piece_pos[0], piece_pos[1]), 10, 10)
                        text = font.render(piece_to_move[1], True, "BLACK")
                        text_rect = text.get_rect()
                        text_rect.center = (piece_pos[0], piece_pos[1])
                        SCREEN.blit(text, text_rect)
                        if turn == "player1":
                            turn = "player2"
                        else:
                            turn = "player1"
            else:
                return


def check_clicked(position):
    for place in places:
        if abs(place[0] - position[0]) <= 8 and abs(place[1] - position[1]) <= 8:
            return place
    return None


def kill(attack_colour, defence_colour):
    map = SCREEN.subsurface(0, 0, 900, 800)
    map = map.copy()
    SCREEN.fill("WHITE")
    pygame.display.update()
    x1 = random.randint(0, 360)
    x = (2 * math.pi * x1) / 360
    pygame.draw.line(SCREEN, 'BLUE', (225, 400), (225 + 100 * math.cos(x), 400 + 100 * math.sin(x)), 1)
    y1 = random.randint(0, 360)
    y = (2 * math.pi * y1) / 360
    pygame.draw.line(SCREEN, 'BLUE', (675, 400), (675 + 100 * math.cos(y), 400 + 100 * math.sin(y)), 1)
    if attack_colour == "PINK":
        pygame.draw.circle(SCREEN, "BLACK", (225, 400), 225, 1)
        pygame.draw.line(SCREEN, 'BLACK', (225, 400), (225, 175), 1)
        pygame.draw.line(SCREEN, 'BLACK', (225, 400), (225, 625), 1)
        pygame.draw.line(SCREEN, 'BLACK', (225, 400), (68, 241), 1)
        if 90 <= x1 <= 135:
            attack = "double"
        elif 135 < x1 <= 270:
            attack = "miss"
        else:
            attack = "hit"
    if attack_colour == "ORANGE":
        pygame.draw.circle(SCREEN, "BLACK", (225, 400), 225, 1)
        pygame.draw.line(SCREEN, 'BLACK', (225, 400), (450, 400), 1)
        pygame.draw.line(SCREEN, 'BLACK', (225, 400), (225, 175), 1)
        pygame.draw.line(SCREEN, 'BLACK', (225, 400), (68, 241), 1)
        if 0 <= x1 <= 90:
            attack = "double"
        elif 90 < x1 <= 135:
            attack = "hit"
        else:
            attack = "miss"
    if attack_colour == "GREEN":
        pygame.draw.circle(SCREEN, "BLACK", (225, 400), 225, 1)
        pygame.draw.line(SCREEN, 'BLACK', (225, 400), (225, 175), 1)
        pygame.draw.line(SCREEN, 'BLACK', (225, 400), (225, 625), 1)
        if 90 <= x1 <= 270:
            attack = "miss"
        else:
            attack = "hit"
    if attack_colour == "BROWN":
        pygame.draw.circle(SCREEN, "BLACK", (225, 400), 225, 1)
        pygame.draw.line(SCREEN, 'BLACK', (225, 400), (373, 569), 1)
        pygame.draw.line(SCREEN, 'BLACK', (225, 400), (225, 175), 1)
        if 90 <= x1 <= 315:
            attack = "miss"
        else:
            attack = "double"
    if defence_colour == 'PINK' or defence_colour == 'ORANGE' or defence_colour == 'GREEN' or defence_colour == 'BROWN':
        pygame.draw.circle(SCREEN, "BLACK", (675, 400), 225, 1)
        pygame.draw.line(SCREEN, 'BLACK', (675, 175), (675, 625), 1)
        if 90 <= x1 <= 270:
            defence = "miss"
        else:
            defence = "hit"
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                SCREEN.blit(map, (0, 0))
                return [attack, defence]


game()
