from constants import CELL_SIZE, WIDTH, HEIGHT
import random
import pygame
import gymnasium as gym
from gymnasium import spaces
import numpy as np

def load_cell_sized_image(path):
    return pygame.transform.scale(pygame.image.load(f"graphics/{path}"), (CELL_SIZE, CELL_SIZE))

class Snake:
    def __init__(self):
        self.body = [(WIDTH/CELL_SIZE * 5, HEIGHT/CELL_SIZE * 5), (WIDTH/CELL_SIZE * 4, HEIGHT/CELL_SIZE * 5)]  
        self.x_dir = 1 
        self.y_dir = 0
        self.grow = False

        self.prev_body = self.body[:]
        self.step_time = 200  
        self.last_step = pygame.time.get_ticks()
        
        self.head_sprites = {(0,-1):load_cell_sized_image("head_up.png"), 
                             (0,1):load_cell_sized_image("head_down.png"), 
                             (-1,0):load_cell_sized_image("head_left.png"), 
                             (1,0):load_cell_sized_image("head_right.png")}
        self.tail_sprites = {(0,1):load_cell_sized_image("tail_up.png"), 
                             (0,-1):load_cell_sized_image("tail_down.png"), 
                             (1,0):load_cell_sized_image("tail_left.png"), 
                             (-1,0):load_cell_sized_image("tail_right.png")}
        self.body_sprites = {
            "horizontal": load_cell_sized_image("body_horizontal.png"),
            "vertical": load_cell_sized_image("body_vertical.png"),
            "topleft": load_cell_sized_image("body_topleft.png"),
            "topright": load_cell_sized_image("body_topright.png"),
            "bottomleft": load_cell_sized_image("body_bottomleft.png"),
            "bottomright": load_cell_sized_image("body_bottomright.png")
        }
        
    def draw(self, screen):
        # HEAD
        head_rect = pygame.Rect(*self.body[0], CELL_SIZE, CELL_SIZE)
        screen.blit(self.head_sprites[(self.x_dir, self.y_dir)], head_rect)
        
        # BODY
        for i in range(1, len(self.body) - 1):
            x, y = self.body[i]
            prev_x, prev_y = self.body[i - 1]
            next_x, next_y = self.body[i + 1]

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if prev_y == y and next_y == y:
                sprite = self.body_sprites["horizontal"]
            elif prev_x == x and next_x == x:
                sprite = self.body_sprites["vertical"]
            elif (prev_x < x and next_y < y) or (next_x < x and prev_y < y):
                sprite = self.body_sprites["topleft"]
            elif (prev_x > x and next_y < y) or (next_x > x and prev_y < y):
                sprite = self.body_sprites["topright"]
            elif (prev_x < x and next_y > y) or (next_x < x and prev_y > y):
                sprite = self.body_sprites["bottomleft"]
            elif (prev_x > x and next_y > y) or (next_x > x and prev_y > y):
                sprite = self.body_sprites["bottomright"]
            else:
                sprite = self.body_sprites["horizontal"] 

            screen.blit(sprite, rect)

        # TAIL
        tail_x, tail_y = self.body[-1]
        prev_x, prev_y = self.body[-2]
        dx, dy = prev_x - tail_x, prev_y - tail_y
        dx, dy = (0 if dx == 0 else dx // abs(dx)), (0 if dy == 0 else dy // abs(dy))
        screen.blit(self.tail_sprites[(dx, dy)], pygame.Rect(tail_x, tail_y, CELL_SIZE, CELL_SIZE))
        
    def update(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.x_dir * CELL_SIZE, head_y + self.y_dir * CELL_SIZE)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False  

    def check_collision(self):
        return self.check_future_collision_with_direction(0, 0)
    
    def check_future_collision_with_direction(self, x_dir, y_dir):
        head = self.body[0]
        head_x, head_y = head
        new_head_x = (head_x + x_dir * CELL_SIZE)
        new_head_y = (head_y + y_dir * CELL_SIZE)

        if (new_head_x < 0 or new_head_x >= WIDTH or new_head_y < 0 or new_head_y >= HEIGHT):
            return True

        if head in self.body[1:]:
            return True
        return False
    
    def check_food_collision(self, food):
        if self.body[0][0] == food.position[0] and  self.body[0][1] == food.position[1]:
            food.move_to_random_position()
            self.grow = True
    
    def set_direction(self, new_x_dir, new_y_dir):
        self.x_dir = new_x_dir
        self.y_dir = new_y_dir

class Food:
    def __init__(self):
        self.move_to_random_position()
        self.apple_sprite = load_cell_sized_image("apple.png")

    def move_to_random_position(self):
        self.position = (random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE)

    def draw(self, screen):
        screen.blit(self.apple_sprite, (*self.position, CELL_SIZE, CELL_SIZE))

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.checkerboard= None

    def draw(self, screen):
        if self.checkerboard == None:
            self.checkerboard = self.make_checkerboard()
            
        screen.blit(self.checkerboard, (0, 0))
        self.snake.draw(screen)
        self.food.draw(screen)
        
    def update(self):
        self.snake.update()

        if self.snake.check_food_collision(self.food):
            self.food.move_to_random_position()

        if self.snake.check_collision():
            return False

        return True
    
    def make_checkerboard(self, cell_size=CELL_SIZE):
        color_a = (23,23,23)
        color_b = (25,25,25)
        surf = pygame.Surface((WIDTH, HEIGHT)).convert()   
        for gy in range(0, HEIGHT, cell_size):
            row = (gy // cell_size)
            for gx in range(0, WIDTH, cell_size):
                col = (gx // cell_size)
                color = color_a if ((row + col) % 2 == 0) else color_b
                surf.fill(color, (gx, gy, cell_size, cell_size))
        return surf

    def get_state(self):
        food_x, food_y = self.food.position
        head_x, head_y = self.snake.body[0]

        head_x_norm = head_x / WIDTH
        head_y_norm = head_y / HEIGHT
        food_dx = (food_x - head_x) / WIDTH
        food_dy = (food_y - head_y) / HEIGHT

        danger_left = int(self.snake.check_future_collision_with_direction(-1, 0))
        danger_up = int(self.snake.check_future_collision_with_direction(0, -1))
        danger_right = int(self.snake.check_future_collision_with_direction(1, 0))

        return np.array([
            head_x_norm, head_y_norm,
            self.snake.x_dir, self.snake.y_dir,
            food_dx, food_dy,
            danger_left, danger_up, danger_right
        ], dtype=np.float32)

    
class SnakeTrainingEnvironment(gym.Env):
    def __init__(self):
        super().__init__()

        self.action_space = spaces.Discrete(4)

        self.observation_space = spaces.Box(
            low=-1.0, high=1.0, shape=(9,), dtype=np.float32
        )

        self.game = Game()
        self.prev_dist = None  

    def render(self, screen):
        self.game.draw(screen)

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.game = Game()

        food_x, food_y = self.game.food.position
        head_x, head_y = self.game.snake.body[0]
        self.prev_dist = abs(food_x - head_x) + abs(food_y - head_y)

        obs = self.game.get_state()
        info = {}
        return obs, info

    def step(self, action):
        if action == 0:  
            self.game.snake.set_direction(-1, 0)
        elif action == 1: 
            self.game.snake.set_direction(0, -1)
        elif action == 2: 
            self.game.snake.set_direction(1, 0)
        elif action == 3: 
            self.game.snake.set_direction(0, 1)

        alive = self.game.update()

        reward = 0
        terminated = not alive

        if not alive:
            reward = -10  
        if self.game.snake.grow:
            reward = 50   
            self.prev_dist = 1000

        food_x, food_y = self.game.food.position
        head_x, head_y = self.game.snake.body[0]
        new_dist = abs(food_x - head_x) + abs(food_y - head_y)

        if new_dist < self.prev_dist:
            reward += 0.2
            self.prev_dist = new_dist
        else:
            reward -= 0.2


        obs = self.game.get_state()
        info = {}

        return obs, reward, terminated, False, info

