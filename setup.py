from pip._internal import main
import os
dependencies = ["pynput","bs4","pyautogui"]

def install_dependencies():
    for i in dependencies:
        install(i)
    os._exit(0)

def install(package):
    main(['install', package])

if __name__ == "__main__":
    install_dependencies()
