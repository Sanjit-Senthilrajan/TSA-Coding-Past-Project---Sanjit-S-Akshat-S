import pygame
import sys
from constants import FPS, WIDTH, HEIGHT
from game import Game

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Manual Mode")
clock = pygame.time.Clock()

game = Game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.snake.y_dir != 1:
                game.snake.x_dir, game.snake.y_dir = 0, -1
            elif event.key == pygame.K_DOWN and game.snake.y_dir != -1:
                game.snake.x_dir, game.snake.y_dir = 0, 1
            elif event.key == pygame.K_LEFT and game.snake.x_dir != 1:
                game.snake.x_dir, game.snake.y_dir = -1, 0
            elif event.key == pygame.K_RIGHT and game.snake.x_dir != -1:
                game.snake.x_dir, game.snake.y_dir = 1, 0

    if not game.update():
        running = False

    screen.fill((30, 30, 30))
    game.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
