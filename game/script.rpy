# The script of the game goes in this file.

# Declare characters used by this game.
# Set up a tile size and boundaries (assuming standard 1920x1080 resolution)
init python:
    STEP_SIZE = 60
    MAP_WIDTH = 1920
    MAP_HEIGHT = 1080

screen rpg_movement():
    # Capture keyboard inputs and trigger the move label
    key "K_UP" action Jump("move_up")
    key "w" action Jump("move_up")
    
    key "K_DOWN" action Jump("move_down")
    key "s" action Jump("move_down")
    
    key "K_LEFT" action Jump("move_left")
    key "a" action Jump("move_left")
    
    key "K_RIGHT" action Jump("move_right")
    key "d" action Jump("move_right")

    # Interactive Object / Talk button
    key "K_SPACE" action Jump("interact_check")

    # Render the background map
    add "bg_map.png"

    # Render the player sprite at their current X and Y coordinates
    add "player_sprite.png":
        xpos player_x
        ypos player_y
        xanchor 0.5
        yanchor 0.5
while true:
    print(1)
