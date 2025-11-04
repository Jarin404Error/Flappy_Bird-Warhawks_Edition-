import pygame
import sys
import random

def draw_floor():
    """This function, it draws the floor. I make it scroll by drawing two times."""
    screen.blit(floor_surface, (floor_x_pos, 700))
    screen.blit(floor_surface, (floor_x_pos + 448, 700))

def create_pipe():
    """Make new pipe. This is for make game hard. Use random for height."""
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - PIPE_GAP))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    """Move all pipes to left. This make hawk look like flying forward."""
    for pipe in pipes:
        pipe.centerx -= PIPE_SPEED
    # if pipe go off screen, i must remove it.
    # This is list... comprehension? My teacher say it is fast. 
    # a normal 'for' loop also work but maybe slow? i will learn later.
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    """This function draw all the pipes from the list onto the game screen."""
    for pipe in pipes:
        if pipe.bottom >= 800:
            # This is bottom pipe
            screen.blit(pipe_surface, pipe)
        else:
            # This is top pipe. must flip it.
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    """Check for crash. If hawk hit pipe or ground, game over. Very important!"""
    global game_active
    
    # check if hawk hit pipe
    # This check all pipes. maybe slow if many pipes? 
    # my friend say use 'quadtree' but i not know this. for later.
    for pipe in pipes:
        if hawk_rect.colliderect(pipe):
            # death_sound.play() <-- REMOVED
            game_active = False
            return
            
    # check if hawk hit floor or fly too high
    if hawk_rect.top <= -50 or hawk_rect.bottom >= 700:
        # death_sound.play() <-- REMOVED
        game_active = False
        return

def rotate_hawk(hawk_surface_to_rotate, velocity):
    """Make hawk look like flying up or down. this part is math."""
    # rotate the hawk picture, not the box.
    # clamp is... like min/max?
    new_hawk = pygame.transform.rotozoom(hawk_surface_to_rotate, -velocity * 3, 1)
    return new_hawk

def display_score(game_state):
    """Show the score number. two times: one for game, one for game over."""
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255)) # white color
        score_rect = score_surface.get_rect(center=(224, 100))
        screen.blit(score_surface, score_rect)
    
    if game_state == 'game_over':
        # show final score
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(224, 100))
        screen.blit(score_surface, score_rect)
        
        # show best score
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(224, 650))
        screen.blit(high_score_surface, high_score_rect)
        
        # message for play again
        game_over_surface = game_font.render('Press Space to Play', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(224, 384))
        screen.blit(game_over_surface, game_over_rect)

def update_high_score(current_score, current_high_score):
    """Check if score is new high score. very simple function."""
    if current_score > current_high_score:
        current_high_score = current_score
    return current_high_score

def reset_game():
    """Reset all things to start again. new game."""
    global hawk_y, hawk_velocity, score, game_active
    hawk_y = 384
    hawk_velocity = 0
    pipe_list.clear() # empty the pipe list
    score = 0
    game_active = True
    hawk_rect.center = (100, hawk_y)


# --- Pygame Initialization ---
# Start pygame. Mixer is for sounds. Must do this first.
# pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512) <-- REMOVED
pygame.init()

# --- Game Constants ---
# Numbers for game. like settings.
SCREEN_WIDTH = 448
SCREEN_HEIGHT = 800
GRAVITY = 0.25 # how fast hawk fall
FLAP_STRENGTH = -7 # how high hawk jump
PIPE_SPEED = 4 # how fast pipe move
PIPE_GAP = 200 # space for hawk to fly

# --- Setup Display ---
# Make the game window.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hawk Flapper') # window title
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 60) # font for score

# --- Game Assets (Created with Pygame) ---
# Make all pictures for game. i use color block, no image file.

# Background
bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_surface.fill((28, 182, 224)) # blue sky

# Floor
floor_surface = pygame.Surface((448, 112))
floor_surface.fill((220, 200, 140)) # sand color

# Hawk (ULM Warhawk inspired - trying to match the mascot image!)
HAWK_WIDTH = 70  # Make it a bit wider to match the head shape
HAWK_HEIGHT = 50 # Make it a bit taller
hawk_base_surface = pygame.Surface((HAWK_WIDTH, HAWK_HEIGHT), pygame.SRCALPHA) # Transparent background

# Colors from the mascot image
COLOR_DARK_GREY = (50, 50, 50) # The main body color
COLOR_MAROON = (128, 0, 32)   # The red part
COLOR_GOLD = (212, 175, 55)   # The gold outline/beak
COLOR_WHITE = (255, 255, 255) # White for the eye/head stripe

# Body and Head Shape (like a curved shape)
# I remove 'border_radius=15' because it not work on older pygame.
pygame.draw.ellipse(hawk_base_surface, COLOR_DARK_GREY, (0, 0, HAWK_WIDTH - 5, HAWK_HEIGHT))

# The maroon "feather" part on the side
pygame.draw.polygon(hawk_base_surface, COLOR_MAROON, [
    (HAWK_WIDTH * 0.2, HAWK_HEIGHT * 0.1),
    (HAWK_WIDTH * 0.8, HAWK_HEIGHT * 0.05),
    (HAWK_WIDTH * 0.9, HAWK_HEIGHT * 0.4),
    (HAWK_WIDTH * 0.3, HAWK_HEIGHT * 0.5)
])

# Beak (gold color)
pygame.draw.polygon(hawk_base_surface, COLOR_GOLD, [
    (HAWK_WIDTH * 0.8, HAWK_HEIGHT * 0.2), # Tip of beak
    (HAWK_WIDTH * 0.6, HAWK_HEIGHT * 0.3), # Top back of beak
    (HAWK_WIDTH * 0.6, HAWK_HEIGHT * 0.5), # Bottom back of beak
    (HAWK_WIDTH * 0.8, HAWK_HEIGHT * 0.4)  # Bottom front of beak
])

# White eye area
pygame.draw.polygon(hawk_base_surface, COLOR_WHITE, [
    (HAWK_WIDTH * 0.65, HAWK_HEIGHT * 0.15),
    (HAWK_WIDTH * 0.75, HAWK_HEIGHT * 0.1),
    (HAWK_WIDTH * 0.85, HAWK_HEIGHT * 0.2),
    (HAWK_WIDTH * 0.75, HAWK_HEIGHT * 0.25)
])

# Eye (small dark grey/black circle)
pygame.draw.circle(hawk_base_surface, COLOR_DARK_GREY, (int(HAWK_WIDTH * 0.75), int(HAWK_HEIGHT * 0.18)), 4)


hawk_rect = hawk_base_surface.get_rect(center=(100, SCREEN_HEIGHT // 2))

# Pipes
# green pipes
PIPE_WIDTH = 80
pipe_surface = pygame.Surface((PIPE_WIDTH, 500))
pipe_surface.fill((34, 139, 34)) # green
pipe_height = [300, 400, 500, 600] # possible heights for pipe

# --- Game Variables ---
# I need to remember these things when game is playing.
hawk_y = SCREEN_HEIGHT // 2
hawk_velocity = 0
game_active = False # game not start yet
score = 0
high_score = 0
floor_x_pos = 0
pipe_list = [] # list to hold all pipes
score_pipe_check = True # This check is so i not get many points for one pipe. Only one point.

# --- Timers ---
# This is timer. It make a new pipe every 1.2 second. (1200 millisecond)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# --- Sound (Generated placeholder sounds if mixer fails) ---
# (ENTIRE SOUND BLOCK REMOVED)


# --- Main Game Loop ---
# Main loop. Game runs here. Forever loop until i close window.
while True:
    # --- Event Handling ---
    # Check if player do something. like press key or close window.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    # make hawk fly
                    hawk_velocity = 0 # reset fall speed
                    hawk_velocity += FLAP_STRENGTH
                    # flap_sound.play() <-- REMOVED
                else:
                    # if game over, space bar mean play again.
                    reset_game()

        if event.type == SPAWNPIPE and game_active:
            # timer say time for new pipe
            pipe_list.extend(create_pipe())
            score_pipe_check = True # ready to score for this new pipe

    # --- Draw Background ---
    # Draw blue sky first. So it is in back.
    screen.blit(bg_surface, (0, 0))

    if game_active:
        # --- Game Active Logic ---
        # This code run only when game is playing.
        
        # --- Hawk Physics ---
        # Gravity pull hawk down. math for falling.
        hawk_velocity += GRAVITY
        hawk_y += hawk_velocity
        hawk_rect.centery = hawk_y
        
        # --- Hawk Graphics ---
        # draw the hawk
        rotated_hawk = rotate_hawk(hawk_base_surface, hawk_velocity) # Use hawk_base_surface for rotation
        screen.blit(rotated_hawk, hawk_rect)
        
        # --- Pipe Logic ---
        # move pipes and draw them
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        # --- Collision Check ---
        # check if hawk crash
        check_collision(pipe_list)
        
        # --- Scoring ---
        # This loop for score check. it check pipes list every frame. 
        # maybe there is better way? for now is ok.
        next_pipe = None
        for pipe in pipe_list:
            if pipe.right > hawk_rect.left and pipe.bottom >= 800: # find next bottom pipe
                next_pipe = pipe
                break
        
        # if hawk pass the pipe, add score. 
        if next_pipe and score_pipe_check:
            if hawk_rect.left > next_pipe.centerx: # <-- This line is fixed
                score += 1
                # score_sound.play() <-- REMOVED
                score_pipe_check = False # only one score per pipe
                
        display_score('main_game')
        
    else:
        # --- Game Over Logic ---
        # this run when game is not active (game over screen)
        high_score = update_high_score(score, high_score)
        draw_pipes(pipe_list) # show pipes where they stop
        screen.blit(hawk_base_surface, hawk_rect) # show hawk where it crash (not rotated)
        display_score('game_over')

    # --- Floor Logic (runs in all states) ---
    # Floor move all time. make look like flying.
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -448: # loop the floor
        floor_x_pos = 0

    # --- Update Display ---
    # Show everything on screen. very important.
    pygame.display.update()
    clock.tick(120) # game speed. 120 is fast.

