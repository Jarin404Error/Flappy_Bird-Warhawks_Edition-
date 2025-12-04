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
    """Check for crash. If hawk hit pipe or ground, game over."""
    global game_active
    
    for pipe in pipes:
        if hawk_rect.colliderect(pipe):
            game_active = False
            return
            
    # check if hawk hit floor or fly too high
    if hawk_rect.top <= -50 or hawk_rect.bottom >= 700:
        game_active = False
        return

def rotate_hawk(hawk_surface_to_rotate, velocity):
    """Make hawk look like flying up or down. this part is math."""
    new_hawk = pygame.transform.rotozoom(hawk_surface_to_rotate, -velocity * 3, 1)
    return new_hawk

def display_score(game_state):
    """Show the score number."""
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(224, 100))
        screen.blit(score_surface, score_rect)
    
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(224, 100))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(224, 650))
        screen.blit(high_score_surface, high_score_rect)
        
        game_over_surface = game_font.render('Press Space to Play', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(224, 384))
        screen.blit(game_over_surface, game_over_rect)

def update_high_score(current_score, current_high_score):
    if current_score > current_high_score:
        current_high_score = current_score
    return current_high_score

def reset_game():
    """Reset all things to start again."""
    global hawk_y, hawk_velocity, score, game_active
    hawk_y = 384
    hawk_velocity = 0
    pipe_list.clear() 
    score = 0
    game_active = True
    hawk_rect.center = (100, hawk_y)


# --- Pygame Initialization ---
pygame.init()

# --- Game Constants ---
SCREEN_WIDTH = 448
SCREEN_HEIGHT = 800
GRAVITY = 0.25 
FLAP_STRENGTH = -7 
PIPE_SPEED = 4 
PIPE_GAP = 200 

# --- Setup Display ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('ULM Hawk Flapper')
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 60)

# --- Game Assets ---

# Background
bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_surface.fill((28, 182, 224)) 

# Floor
floor_surface = pygame.Surface((448, 112))
floor_surface.fill((220, 200, 140)) 

# --- HAWK GRAPHICS (REDONE FOR ULM MASCOT LOOK) ---
HAWK_WIDTH = 80  
HAWK_HEIGHT = 60 
hawk_base_surface = pygame.Surface((HAWK_WIDTH, HAWK_HEIGHT), pygame.SRCALPHA)

# ULM Official Brand Colors
ULM_MAROON = (132, 0, 41)   # Official ULM Maroon
ULM_GOLD = (253, 185, 19)   # Official ULM Gold
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

# 1. Back Feathers (Maroon) - Spiky hair at the back
pygame.draw.polygon(hawk_base_surface, ULM_MAROON, [
    (0, 20), (20, 10), (10, 30), (25, 25), (15, 45)
])

# 2. Main Head Shape (Maroon) - More angular
pygame.draw.polygon(hawk_base_surface, ULM_MAROON, [
    (20, 5),    # Top back
    (55, 5),    # Top forehead
    (65, 20),   # Brow
    (50, 45),   # Jaw
    (20, 50)    # Neck
])

# 3. The Beak (Gold) - Sharp and Hooked
pygame.draw.polygon(hawk_base_surface, ULM_GOLD, [
    (60, 20),   # Top connection
    (80, 28),   # Tip of beak
    (60, 35),   # Bottom connection
    (55, 25)    # Middle connection
])

# 4. White Cheek/Eye Patch (Signature Warhawk look)
pygame.draw.polygon(hawk_base_surface, WHITE, [
    (45, 15),   # Top
    (60, 18),   # Front near eye
    (55, 30),   # Bottom
    (35, 25)    # Back
])

# 5. The Eye (Fierce angle)
# Eye Background
pygame.draw.polygon(hawk_base_surface, BLACK, [
    (48, 18), (58, 20), (52, 26)
])
# Eye Glint
pygame.draw.circle(hawk_base_surface, WHITE, (52, 21), 2)


hawk_rect = hawk_base_surface.get_rect(center=(100, SCREEN_HEIGHT // 2))

# Pipes
PIPE_WIDTH = 80
pipe_surface = pygame.Surface((PIPE_WIDTH, 500))
pipe_surface.fill((34, 139, 34)) 
pipe_height = [300, 400, 500, 600] 

# --- Game Variables ---
hawk_y = SCREEN_HEIGHT // 2
hawk_velocity = 0
game_active = False 
score = 0
high_score = 0
floor_x_pos = 0
pipe_list = [] 
score_pipe_check = True
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)


# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    hawk_velocity = 0 
                    hawk_velocity += FLAP_STRENGTH
                else:
                    reset_game()

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
            score_pipe_check = True 

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Hawk Physics
        hawk_velocity += GRAVITY
        hawk_y += hawk_velocity
        hawk_rect.centery = hawk_y
        
        # Draw Hawk
        rotated_hawk = rotate_hawk(hawk_base_surface, hawk_velocity)
        screen.blit(rotated_hawk, hawk_rect)
        
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        # Collision
        check_collision(pipe_list)
        
        # Scoring
        next_pipe = None
        for pipe in pipe_list:
            if pipe.right > hawk_rect.left and pipe.bottom >= 800:
                next_pipe = pipe
                break
        
        if next_pipe and score_pipe_check:
            if hawk_rect.left > next_pipe.centerx: 
                score += 1
                score_pipe_check = False 
                
        display_score('main_game')
        
    else:
        # Game Over
        high_score = update_high_score(score, high_score)
        draw_pipes(pipe_list)
        screen.blit(hawk_base_surface, hawk_rect) 
        display_score('game_over')

    # Floor Logic
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -448: 
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)