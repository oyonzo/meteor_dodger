import pygame
import random

# Specify the width and height of the screen for the game
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 600

# Frames-Per-Second for game updates
FPS = 60

# Amount to move the player with each key press
DELTA_X = 50
DELTA_Y = 50


class Box():
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def collide(self, other):
        return self.rect.colliderect(other.rect)

class Obstacle(Box):
    def __init__(self):
        super().__init__(
            random.randint(100, SCREEN_WIDTH-50),
            random.randint(100 , SCREEN_HEIGHT-50),
            50, 50,
            (0, 0, 255)
        )
        self.velocity = [random.randint(20 , 100), random.randint(20 , 100)]
        
    def update(self, dt):
        self.rect.x += self.velocity[0]*dt
        self.rect.y += self.velocity[1]*dt
        
        # check if rectangle has hit the edges
        if (self.rect.left < 0 or self.rect.right > SCREEN_WIDTH):
            self.velocity[0] *= -1
        if (self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT):
            self.velocity[1] *= -1

class Player(Box):
    def __init__(self):
        super().__init__(0, 0, 50, 50, (255, 0, 0)) 

    def shift_x(self, shift):
        self.rect.x += shift
    
    def shift_y(self, shift):
        self.rect.y += shift

def play_game(num_boxes=5):
    # Initialize pygame
    pygame.init()
    pygame.font.init()

    # Initialize the screen
    screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )

    # Initialize game elements
    player = Player()
    obstacles = []
    for _ in range(num_boxes):
        obstacles.append(Obstacle())
    
    # Initialize some game variables
    time = 0
    delta_t = 1/FPS

    # Setup the font and clock
    font  = pygame.font.SysFont('Arial',14)
    clock = pygame.time.Clock()

    # Main game loop
    playing = True
    while playing:
        
        # Get the event corresponding to user input
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT):
                player.shift_x(DELTA_X)
            elif (event.key == pygame.K_LEFT):
                player.shift_x(-DELTA_X)
            elif (event.key == pygame.K_UP):
                player.shift_y(-DELTA_Y)
            elif (event.key == pygame.K_DOWN):
                player.shift_y(DELTA_Y)

        for obstacle in obstacles:
            obstacle.update(delta_t) # Update the position of the box
            if obstacle.collide(player):
                playing = False # End game if there is a collision

        # Draw the scene
        screen.fill((255,255,255)) # Fill the scene with white (specified by RGB tuple)
        player.render(screen)
        for obstacle in obstacles:
            obstacle.render(screen)

        # Update and draw the current time in the bottom left corner
        time += delta_t
        text = font.render('Time=' + str(round(time,1)) + ' seconds',True,(0,0,0))
        screen.blit(text,(10,0.95*SCREEN_HEIGHT))

        # Update the screen
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    print("Game over!")

play_game()