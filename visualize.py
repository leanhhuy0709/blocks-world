import pygame as pg, sys
from run import *

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

init, goal, moves, numTableSlot = main()

for i in range(numTableSlot):
    init.append([])
    goal.append([])

from pygame.locals import *
pg.init()
if NUM_CELL > 20:
    size = SCREEN_WIDTH / len(init)
else:
    size = SCREEN_WIDTH / 20
pg.display.set_caption("Blocks World")
font = pg.font.SysFont("cambria", int(size/2), True)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
COLORS = [(127, 0, 0), (255, 0, 0), (0, 127, 0), (0, 255, 0), (255, 0, 127), (255, 0, 255), (127, 127, 0), 
        (127, 255, 0), (127, 0, 127), (127, 0, 255), (127, 127, 127), (127, 255, 127), (127, 255, 255), (255, 127, 127)]
def draw(arr, step):
    x = SCREEN_WIDTH/2 - len(arr) * size / 2
    y = SCREEN_HEIGHT/2
    text = font.render(f'STEP: {step}/{len(moves)}', 1, (0, 0, 0))
    text_rect = text.get_rect(center=(200, 100))
    screen.blit(text, text_rect)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            pg.draw.rect(screen, arr[i][j].color, ((x + i * size, y - j * size), (size, size)))
            text = font.render(f'{arr[i][j].name}', 1, (0, 0, 0))
            text_rect = text.get_rect(center=(x + i * size + size/2, y - j * size + size/2))
            screen.blit(text, text_rect)
    for i in range(len(arr)):
        pg.draw.rect(screen, (0, 0, 0), ((x + i * size, y + size), (size, size)))
        text = font.render(f'{i}', 1, (255, 255, 255))
        text_rect = text.get_rect(center=(x + i * size + size/2, y + size + size/2))
        screen.blit(text, text_rect)

curr = []
for i in range(len(init)):
    curr.append([])
    for j in range(len(init[i])):
        curr[i].append(init[i][j])
        init[i][j].color = COLORS[rd.randint(0, len(COLORS) - 1)]

step = 0
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                if step < len(moves):
                    move(curr, moves[step][0], moves[step][1], False)
                    step += 1
            elif event.key == K_LEFT: 
                if step > 0:
                    step -= 1
                    move(curr, moves[step][1], moves[step][0], False)
    screen.fill((255, 255, 255))
    draw(curr, step)
    if step >= 0 and step < len(moves):
        text = font.render(f'MOVE {moves[step][0]} to {moves[step][1]}', 1, (0, 0, 0))
        text_rect = text.get_rect(center=(400, SCREEN_HEIGHT/2 + size + 100))
        screen.blit(text, text_rect)
    time.sleep(0.035)
    pg.display.update()
