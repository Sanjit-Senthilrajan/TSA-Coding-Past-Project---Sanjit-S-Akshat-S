from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from game import SnakeTrainingEnvironment
import sys

steps = 1000000
if len(sys.argv) > 1:
    steps = sys.argv[1]
print(f"Training with: {steps}")

env = SnakeTrainingEnvironment()
check_env(env)  

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=1000000)
model.save(f"ppo_snake_1000000")
