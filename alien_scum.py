from gameplay import Gameplay
from main_menu import MainMenu
while True:
    MainMenu().run_menu()
    currentGameplay = Gameplay()
    currentGameplay.run_gameplay()
