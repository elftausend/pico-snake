import random
import st7789
import utime
from pimoroni import Button
from pimoroni import RGBLED

WIDTH, HEIGHT = 320, 240  # Pico Display 2.0
WAIT_UNTIL_NEXT_MOVE = 0.45 # the duration in seconds waited until the next move is performed
GRID_CONSTANT = 20 # integrally divisible (WIDTH / GRID_CONSTANT and HEIGHT / GRID_CONSTANT) to create a grid
START_SNAKE_LEN = 3 # the length of the snake without eating any food
START_POS = 160, 120 # the first snake segment spawns at this position

display = st7789.ST7789(WIDTH, HEIGHT, rotate180=False)
display.set_backlight(0.5)

led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# check if the snake collided with itself
def check_snake_collision(coords, x, y):
    for coord in coords:
        collision_x, collision_y = coord
        if collision_x == x and collision_y == y:
            return True
    return False

# generates a random position located on the grid
def rand_pos():
    food_x = random.randrange(0, WIDTH, GRID_CONSTANT)
    food_y = random.randrange(0, HEIGHT, GRID_CONSTANT)
    return (food_x, food_y)

def spawn_food(coords):
    food_x, food_y = rand_pos()
    
    # repeat until a free location for the food is found
    while check_snake_collision(coords, food_x, food_y):
        food_x, food_y = rand_pos()
    
    # set color of the pen to red
    display.set_pen(255, 0, 0)
    display.rectangle(food_x, food_y, GRID_CONSTANT, GRID_CONSTANT)
    # change the color to white
    display.set_pen(255, 255, 255)
    
    return (food_x, food_y)
    

def check_game_over(coords, x, y):
    # check if the snake touches the border of the screen
    if x+GRID_CONSTANT > WIDTH or y+GRID_CONSTANT > HEIGHT or x < 0 or y < 0:
        return True;
    
    return check_snake_collision(coords, x, y)

def lost_game():
    # set the color to green
    display.set_pen(0, 255, 0)
    display.text("Snake ist wohl nicht deine Staerke..", 6, 6, 6, 3)
    display.text("press 'x' to restart", 200, 6, 6, 3)
    display.update()
    
    # restart the game if the button 'x' is pressed
    while True:
        if button_x.read():
            display.set_pen(0, 0, 0)
            display.clear()
            game_loop()



def game_loop():
    
    # setup values
    food_x, food_y = spawn_food([])

    x, y = START_POS

    y_dir = 0
    x_dir = 1

    snake_len = START_SNAKE_LEN

    coords = []
    
    # move loop
    while True:
        # if the head of the snake touches the food, a new apple is spawned at a random position
        if x == food_x and y == food_y:
            # if this value grows, the last segment will despawn later thus making the snake longer by one segment
            snake_len += 1
            food_x, food_y = spawn_food(coords)
            
        # controll system
        # if the snake is moving up or down, the x direction can be updated 
        if y_dir != 0:
            # move left
            if button_a.read():
                x_dir = -1
                y_dir = 0
            # move right
            if button_x.read():
                x_dir = 1
                y_dir = 0
                
        # if the snake is moving right or left, the y direction can be updated 
        if x_dir != 0:
            # move up
            if button_b.read():
                y_dir = -1
                x_dir = 0
            # move down
            if button_y.read():
                y_dir = 1
                x_dir = 0
                
        
        # following figures will be in this color (white):
        display.set_pen(255, 255, 255)
        
        # update the snake's position
        x += GRID_CONSTANT * x_dir
        y += GRID_CONSTANT * y_dir
        
        # if the snake intersects with it's body or the border of the screen, the game is lost.
        if check_game_over(coords, x, y):
            lost_game()
        
        display.rectangle(x, y, GRID_CONSTANT, GRID_CONSTANT)

        
        # despawn the last segement
        # using a list in order to save the last segment's position
        if len(coords) == snake_len:
            # black -> 'despawn' the segment
            display.set_pen(0, 0, 0)
            last_x, last_y = coords[0]
            display.rectangle(last_x, last_y, GRID_CONSTANT, GRID_CONSTANT)
            # delete the first element of the array, which represents the last segment
            coords.pop(0)
        
        coords.append((x, y))
        
        # show changes
        display.update()
        
        # wait till next move
        utime.sleep(WAIT_UNTIL_NEXT_MOVE)


if __name__ == "__main__":
    game_loop()

 

