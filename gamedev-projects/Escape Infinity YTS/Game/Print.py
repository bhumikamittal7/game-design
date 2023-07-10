pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((lvlsize * boxsize + 300, lvlsize * boxsize))
pygame.display.set_caption('Escape Infinity')
window.fill((0, 0, 0))

input_rect = pygame.Rect(lvlsize * boxsize, 0, 300, lvlsize * boxsize)
base_font = pygame.font.Font(None, 22)
user_text = ['']

C_pos = []
gameOn = True
win = False
def update():
    global grid, C_pos, player, lvlsize, win, frame, dir
    if len(C_pos) > 0:
        for x in [0]:
            if C_pos[0][0] in ['+','-','=']:
                if C_pos[0][0] == '=':
                    dir = C_pos[0][1]
                elif  C_pos[0][0] == '+':
                    dir = (dir + C_pos[0][1]) % 360
                elif C_pos[0][0] == '-':
                    dir = (dir - C_pos[0][1]) % 360
                C_pos.pop(0)
                break
            try:
                if C_pos[0][0] != 0:
                    grid[player + int(C_pos[0][0] / abs(C_pos[0][0]))]
                else:
                    grid[player + int(C_pos[0][1] / abs(C_pos[0][1]) * lvlsize)]
            except:
                break
            player = grid.index('O')
            if C_pos[0][0] != 0:
                if grid[player + int(C_pos[0][0]/abs(C_pos[0][0]))] in ['-','@']:
                    grid[player] = '-'
                    if grid[player + int(C_pos[0][0]/abs(C_pos[0][0]))] == '@':
                        win = True
                    grid[player + int(C_pos[0][0]/abs(C_pos[0][0]))] = 'O'
                    C_pos[0][0] -= int(C_pos[0][0]/abs(C_pos[0][0]))
                    if C_pos[0] == [0,0]:
                        C_pos.pop(0)
                else:
                    C_pos.pop(0)
                    break
            else:
                if grid[player + int(C_pos[0][1]/abs(C_pos[0][1])*lvlsize)] in ['-','@']:
                    grid[player] = '-'
                    if grid[player + int(C_pos[0][1]/abs(C_pos[0][1])*lvlsize)] == '@':
                        win = True
                    grid[player + int(C_pos[0][1]/abs(C_pos[0][1])*lvlsize)] = 'O'
                    C_pos[0][1] -= int(C_pos[0][1] / abs(C_pos[0][1]))
                    if C_pos[0] == [0,0]:
                        C_pos.pop(0)
                else:
                    C_pos.pop(0)
                    break
        if C_pos == []:
            frame = 100
    pygame.display.flip()
grid = level[i].copy()
activate = False
frame = 0
while True:
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
            break
        if (event.type == MOUSEBUTTONDOWN) and (input_rect.collidepoint(pygame.mouse.get_pos())):
            activate = True
            frame = 60
        if (event.type == MOUSEBUTTONUP) and (activate == True):
            if (C_pos == []) and (frame >= 0):
                try:
                    tmp = '\n'.join(user_text) + '\n'
                    try:
                        tmp = tmp.replace(' ' + For.findall(tmp)[0] + ' ',' var ')
                    except:
                        pass
                    exec(tmp)
                except:
                    print('Error!! Some error in the code!!')
                    user_text = ['']
                    C_pos = []
                    dir = 270
                    grid = level[i].copy()
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                if len(user_text[-1]) == 0:
                    if len(user_text) > 1:
                        user_text.pop(-1)
                else:
                    user_text[-1] = user_text[-1][:-1]
            else:
                if event.key == K_RETURN:
                    user_text += ['']
                else:user_text[-1] += event.unicode
    if gameOn == False:
        pygame.quit()
        break
    for y in range(0, lvlsize * boxsize, boxsize):
        for x in range(0, lvlsize * boxsize, boxsize):
            window.blit(box[grid[int((y * lvlsize + x)/boxsize)]], [x, y])
            if grid[int((y * lvlsize + x)/boxsize)] == 'O':
                if dir == 90:
                    pygame.draw.polygon(window,(0, 0, 0), [(x + boxsize/2, y), (x + boxsize, y + boxsize/2), (x, y + boxsize/2)])
                elif dir == 270:
                    pygame.draw.polygon(window,(0, 0, 0), [(x + boxsize/2, y + boxsize), (x + boxsize, y + boxsize/2), (x, y + boxsize/2)])
                elif dir == 0:
                    pygame.draw.polygon(window,(0, 0, 0), [(x + boxsize, y + boxsize/2), (x + boxsize/2, y + boxsize), (x + boxsize/2, y)])
                elif dir == 180:
                    pygame.draw.polygon(window,(0, 0, 0), [(x, y + boxsize/2), (x + boxsize/2, y + boxsize), (x + boxsize/2, y)])
    pygame.draw.rect(window, (50, 50, 50), input_rect)
    for y in range(0,len(user_text),1):
        if y == len(user_text) -1:
            text_surface = base_font.render(user_text[y] + '|', True, (255, 255, 255))
        else:
            text_surface = base_font.render(user_text[y], True, (255, 255, 255))
        window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5 + y * 25))
    update()
    if (win == False) and (C_pos == []) and (activate == True) and (frame == 0):
        activate = False
        user_text = ['']
        C_pos = []
        dir = 270
        grid = level[i].copy()
    elif frame != 0:
        frame -= 1
    clock.tick(60)
    if win == True:
        print('Completed Level!!')
        wait(3)
        pygame.quit()
        break