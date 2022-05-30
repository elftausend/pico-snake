import random
import st7789
import utime
from pimoroni import Button
from pimoroni import RGBLED

WIDTH, HEIGHT = 320, 240  # Pico Display 2.0

display = st7789.ST7789(WIDTH, HEIGHT, rotate180=False)
display.set_backlight(0.5)

led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

def spawn_food():
    # TODO: Prevent spawning of the food inside the snake
    # -> check coords list
    
    food_x = random.randrange(0, WIDTH, 20)
    food_y = random.randrange(0, HEIGHT, 20)
    display.set_pen(255, 0, 0)
    display.rectangle(food_x, food_y, 20, 20)
    
    pix = display.pixel(food_x+1, food_y+1)
    
    display.set_pen(255, 255, 255)
    return (food_x, food_y)

def check_game_over(coords, x, y, snake_len):
    if x+20 > WIDTH or y+20 > HEIGHT:
        return True;
    
    for coord in coords:
        collision_x, collision_y = coord
        if collision_x == x and collision_y == y:
            return True

    return False

food_x, food_y = spawn_food()

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
    
    print(food_x)
    if x == food_x and y == food_y:
        snake_len += 1
        food_x, food_y = spawn_food()
        
    
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
    
    game_over = check_game_over(coords, x, y, snake_len)
    if game_over:
        break
    
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
    utime.sleep(0.6)


display.set_pen(255, 255, 255)
display.text("Snake ist wohl nicht deine Staerke..", 6, 6, 6, 3)
display.update()


 

