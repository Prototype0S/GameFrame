class Globals:
    """
    A class to store global variables and configuration constants for the game.

    Attributes:
        running (bool): Indicates if the game loop is running.
        FRAMES_PER_SECOND (int): The target frames per second for the game.
        SCREEN_WIDTH (int): The width of the game window.
        SCREEN_HEIGHT (int): The height of the game window.
        SCORE (int): The player's current score.
        LIVES (int): The starting number of lives for the player.
        window_name (str): The display name of the game window.
        levels (list): The ordered list of level names.
        start_level (int): The index of the starting level.
        end_game_level (int): The index of the level to jump to when the game ends.
        next_level (int): The index of the next level to load.
        exiting (bool): Indicates if the game is exiting.
        total_count (int): User-defined global variable for total count.
        destroyed_count (int): User-defined global variable for destroyed count.
    """

    running = True
    FRAMES_PER_SECOND = 30

    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080

    SCORE = 0

    # - Set the starting number of lives - #
    LIVES = 3

    # - Set the Window display name - #
    window_name = 'CyberSocial Butterfly'

    # - Set the order of the rooms - #
    levels = ["WelcomeScreen", "SchoolRoom"]

    # - Set the starting level - #
    start_level = 0

    # - Set this number to the level you want to jump to when the game ends - #
    end_game_level = 4

    # - This variable keeps track of the room that will follow the current room - #
    # - Change this value to move through rooms in a non-sequential manner - #
    next_level = 0

    # - Change variable to True to exit the program - #
    exiting = False

# ############################################################# #
# ###### User Defined Global Variables below this line ######## #
# ############################################################# #

    total_count = 0
    destroyed_count = 0
