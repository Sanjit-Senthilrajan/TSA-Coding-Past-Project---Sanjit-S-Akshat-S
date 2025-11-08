import pygame
import sys
from stable_baselines3 import PPO
from constants import FPS, WIDTH, HEIGHT
from game import SnakeTrainingEnvironment
import sys

model_name = "models/ppo_snake_1000000.zip"
if len(sys.argv) > 1:
    model_name = sys.argv[1]
print(f"Using model: {model_name}")
    
# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
    
model = PPO.load(model_name) 
env = SnakeTrainingEnvironment()

# Unpack correctly: Gymnasium returns (obs, info)
obs, _ = env.reset()
done = False

while not done:
    action, _ = model.predict(obs)
    
    # Gymnasium returns 5 values, convert to SB3 format
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated

    # Render
    screen.fill((30, 30, 30))
    env.render(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
