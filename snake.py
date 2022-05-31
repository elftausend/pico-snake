import random
import st7789
import utime
from pimoroni import Button
from pimoroni import RGBLED

WIDTH, HEIGHT = 320, 240  # Pico Display 2.0

display = st7789.ST7789(WIDTH, HEIGHT, rotate180=False)
display.set_backlight(0.8)

led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

def check_snake_collision(coords, x, y):
    for coord in coords:
        collision_x, collision_y = coord
        if collision_x == x and collision_y == y:
            return True
    return False

def rand_pos():
    food_x = random.randrange(0, WIDTH, 20)
    food_y = random.randrange(0, HEIGHT, 20)
    return (food_x, food_y)

def spawn_food(coords):
    food_x, food_y = rand_pos()
    while check_snake_collision(coords, food_x, food_y):
        food_x, food_y = rand_pos()
    
    display.set_pen(255, 0, 0)
    display.rectangle(food_x, food_y, 20, 20)
    
    display.set_pen(255, 255, 255)
    return (food_x, food_y)
    

def check_game_over(coords, x, y):
    if x+20 > WIDTH or y+20 > HEIGHT or x < 0 or y < 0:
        return True;
    
    return check_snake_collision(coords, x, y)

def lost_game():
    display.set_pen(0, 255, 0)
    display.text("Snake ist wohl nicht deine Staerke..", 6, 6, 6, 3)
    display.text("press 'x' to restart", 200, 6, 6, 3)
    display.update()
    
    while True:
        if button_x.read():
            display.set_pen(0, 0, 0)
            display.clear()
            game_loop()



def game_loop():
    
    # setup values
    food_x, food_y = spawn_food([])

    x = 160
    y = 120

    last_x = x
    last_y = y

    y_dir = 0
    x_dir = 1

    last_x = x
    last_y = y

    snake_len = 3

    coords = []
    
    # move loop
    while True:
        if x == food_x and y == food_y:
            snake_len += 1
            food_x, food_y = spawn_food(coords)
            
        
        if y_dir != 0:
            if button_a.read():
                x_dir = -1
                y_dir = 0
            if button_x.read():
                x_dir = 1
                y_dir = 0
                
        if x_dir != 0:
            if button_b.read():
                y_dir = -1
                x_dir = 0
            if button_y.read():
                y_dir = 1
                x_dir = 0
                
        
        # following figures will be in this color:
        display.set_pen(255, 255, 255)
        
        
        x += 20 * x_dir
        y += 20 * y_dir
        
        game_over = check_game_over(coords, x, y)
        if game_over:
            lost_game()
        
        display.rectangle(x, y, 20, 20)

        
        # despawn the last segement
        # using a list in order to save the last segment's position
        if len(coords) == snake_len:
            # black -> 'despawn' the segment
            display.set_pen(0, 0, 0)
            last_x, last_y = coords[0]
            display.rectangle(last_x, last_y, 20, 20)
            coords.pop(0)
        
        coords.append((x, y))


        
        # show changes
        display.update()
        
        # wait till next move
        utime.sleep(0.45)

    
game_loop()

 

