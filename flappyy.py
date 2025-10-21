import pygame
from pygame.locals import *  # Import Pygame constants like QUIT, MOUSEBUTTONDOWN, etc.
import random  # For generating random pipe heights

# Initialize Pygame
pygame.init()

# Set up the game clock and frame rate
clock = pygame.time.Clock()
fps = 20  # Frames per second

# Screen dimensions
screen_height = 400
screen_width = 400

# Game variables
ground_scroll = 0  # Tracks ground movement for scrolling effect
scroll_speed = 4  # Speed of ground and pipes
flying = False  # Whether the bird is flying
game_over = False  # Game state
pipe_gap = 70  # Space between top and bottom pipes
pipe_freq = 1500  # Time (ms) between pipe spawns
last_pipe = pygame.time.get_ticks() - pipe_freq  # Time since the last pipe spawned
score = 0  # Current score
pass_pipe = False  # Checks if the bird passed a pipe
high_score = 0  # Tracks the highest score

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Load images
bg = pygame.image.load("images/bg1.png")  # Background image
ground = pygame.image.load("images/ground1.png")  # Ground image
button_image = pygame.image.load("images/restart1.png")  # Restart button image

# Function to render text on the screen
def draw_text(text, font, txt_col, x, y):
    img = font.render(text, True, txt_col)  # Render the text
    screen.blit(img, (x, y))  # Draw the text on the screen

# Function to reset the game state
def reset_game():
    pipe_group.empty()  # Remove all pipes
    flappy.rect.x = 47  # Reset bird's x position
    flappy.rect.y = int(screen_height / 2)  # Reset bird's y position
    score = 0  # Reset score
    return score

# Bird class: Handles bird animation, movement, and physics
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []  # List to store bird animation frames
        self.index = 0  # Current frame index
        self.counter = 0  # Counter for animation timing
        # Load bird animation frames
        for i in range(1, 4):
            img = pygame.image.load(f"images/bird{i}.png")
            self.images.append(img)
        self.image = self.images[self.index]  # Set initial image
        self.rect = self.image.get_rect()  # Get the rectangle for collision detection
        self.rect.center = [x, y]  # Set initial position
        self.vel = 0  # Vertical velocity
        self.clicked = False  # Track mouse clicks for flapping

    def update(self):
        # Apply gravity if the bird is flying
        if flying:
            self.vel += 1  # Increase velocity (gravity)
            if self.vel > 10:  # Limit maximum falling speed
                self.vel = 8
            if self.rect.bottom < 325:  # Keep bird within screen bounds
                self.rect.y += int(self.vel)  # Move bird down

        # Handle flapping if the game is not over
        if not game_over:
            # Flap on mouse click
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.vel = -10  # Set upward velocity (flap)
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

            # Animate the bird
            self.counter += 1
            flap_cooldown = 5  # Controls animation speed
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):  # Loop back to the first frame
                    self.index = 0
                self.image = self.images[self.index]  # Update the bird's image

# Pipe class: Handles pipe creation and movement
class pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/pipe1.png")  # Load pipe image
        self.rect = self.image.get_rect()  # Get the rectangle for collision detection
        # Position the pipe (top or bottom)
        if position == 1:  # Top pipe
            self.image = pygame.transform.flip(self.image, False, True)  # Flip vertically
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]  # Position above the gap
        if position == -1:  # Bottom pipe
            self.rect.topleft = [x, y + int(pipe_gap / 2)]  # Position below the gap

    def update(self):
        self.rect.x -= scroll_speed  # Move pipe left
        if self.rect.right < 0:  # Remove pipe if it's off-screen
            self.kill()

# Button class: Handles restart button creation and interaction
class Button():
    def __init__(self, x, y, image):
        self.image = image  # Button image
        self.rect = self.image.get_rect()  # Get the rectangle for collision detection
        self.rect.topleft = (x, y)  # Set button position

    def draw(self):
        action = False  # Track if the button is clicked
        pos = pygame.mouse.get_pos()  # Get mouse position
        if self.rect.collidepoint(pos):  # Check if mouse is over the button
            if pygame.mouse.get_pressed()[0]:  # Check if mouse is clicked
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))  # Draw the button
        return action  # Return whether the button was clicked

# Create sprite groups
bird_group = pygame.sprite.Group()  # Group for the bird
pipe_group = pygame.sprite.Group()  # Group for pipes

# Create the bird and button
flappy = Bird(47, int(screen_height / 2))  # Initialize the bird
bird_group.add(flappy)  # Add bird to the group
button = Button((screen_width // 2) - 45, (screen_height // 2) - 30, button_image)  # Initialize the restart button

# Main game loop
run = True
while run:
    clock.tick(fps)  # Limit the frame rate

    # Draw the background
    screen.blit(bg, (0, 0))

    # Draw and update the bird
    bird_group.draw(screen)
    bird_group.update()

    # Draw the pipes
    pipe_group.draw(screen)

    # Draw the ground
    screen.blit(ground, (ground_scroll, 325))

    # Score logic: Check if the bird passed a pipe
    if len(pipe_group) > 0:
        if (bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and
            bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and
            not pass_pipe):
            pass_pipe = True  # Bird is between the pipes
        if pass_pipe and bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
            score += 1  # Increment score
            pass_pipe = False  # Reset for the next pipe

    # Draw the current score
    draw_text(str(score), pygame.font.SysFont('Arial', 30), white, int(screen_width / 2), 17)

    # Update high score
    if score > high_score:
        high_score = score
    # Draw the high score
    draw_text("High score: " + str(high_score), pygame.font.SysFont('Arial', 20), black, 10, int((screen_height / 2) + 150))

    # Collision detection: Check if the bird hits a pipe or the ground
    if (pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or
        flappy.rect.top < 0 or
        flappy.rect.bottom >= 325):
        game_over = True  # End the game on collision

    # Game logic for when the game is not over and the bird is flying
    if not game_over and flying:
        time_now = pygame.time.get_ticks()  # Get current time
        if time_now - last_pipe > pipe_freq:  # Check if it's time to spawn a new pipe
            pipe_height = random.randint(-60, 60)  # Randomize pipe height
            btm_pipe = pipe(screen_width, int(((screen_height + 25) / 2) + pipe_height), -1)  # Bottom pipe
            top_pipe = pipe(screen_width, int(((screen_height - 25) / 2) + pipe_height), 1)  # Top pipe
            pipe_group.add(btm_pipe)  # Add pipes to the group
            pipe_group.add(top_pipe)
            last_pipe = time_now  # Update the last pipe spawn time

        # Scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 10:  # Reset ground position to create a looping effect
            ground_scroll = 0

        # Update pipes
        pipe_group.update()

    # Game over logic: Show restart button and handle clicks
    if game_over:
        if button.draw():  # If the restart button is clicked
            game_over = False
            score = reset_game()  # Reset the game

    # Event handling: Quit the game or start flying
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close the game window
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:  # Start flying on mouse click
            flying = True

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
