import os

command = input("Choose one (train, manual, test): ")

if command == "train":
    os.system("python train.py")
elif command == "manual":
    os.system("python manual.py")
elif command == "test":
    os.system("python test.py")
else:
    print(f"Unknown command: {command}")