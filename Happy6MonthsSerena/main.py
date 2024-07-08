import pygame
import random
import math
import os
import sys

# Initialize Pygame
pygame.init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Load and resize images
def load_and_resize_image(filepath, scale=1):
    image = pygame.image.load(resource_path(filepath))
    width, height = image.get_size()
    print(width, height)
    new_size = (width // scale, height // scale)
    return pygame.transform.scale(image, new_size)

images = [load_and_resize_image('imgs/image1.png')]
images.append(load_and_resize_image('imgs/image2.png', 4))
images.append(load_and_resize_image('imgs/image3.png', 1.5))
images.append(load_and_resize_image('imgs/image4.png', 3))
images.append(load_and_resize_image('imgs/image5.PNG'))
images.append(load_and_resize_image('imgs/image6.png', 2.7))
for i in [7, 8, 10, 16]:
    images.append(load_and_resize_image(f'imgs/image{i}.png', 3))
images.append(load_and_resize_image('imgs/image9.png', 3.2))
images.append(load_and_resize_image('imgs/image11.png', 2.5))
images.append(load_and_resize_image('imgs/image12.png', 2))
images.append(load_and_resize_image('imgs/image13.png', 2))
images.append(load_and_resize_image('imgs/image14.png', 2))
images.append(load_and_resize_image('imgs/image15.png', 5))
images.append(load_and_resize_image('imgs/image17.png'))

pygame.mixer.init()
pygame.mixer.music.load(resource_path('music/Minecraft - Full [Classic] Soundtrack-[AudioTrimmer.com].mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy 6 Months!")

title_font = pygame.font.Font(resource_path(os.path.join("fonts", "DancingScript-VariableFont_wght.ttf")), 58)
subtitle_font = pygame.font.Font(resource_path(os.path.join("fonts", "DancingScript-VariableFont_wght.ttf")), 45)

# Colors
SKY_BLUE = (173, 216, 230)
LIGHT_BROWN = (101, 67, 33)
DARK_BROWN = (67, 38, 0)
PINK = (255, 192, 203)
DARK_PINK = (255, 162, 182)
WHITE = (255, 255, 255)
GRASS_GREEN = (34, 139, 34)
LIGHT_GRASS_GREEN = (144, 238, 144)
RED = (255, 0, 0)

# Tree parameters
TRUNK_WIDTH = 80
TRUNK_HEIGHT = HEIGHT * 0.4
LEAF_SIZE = 30
TREE_WIDTH = 800
TREE_HEIGHT = 600

# Petal parameters
NUM_PETALS = 100
PETAL_SIZE = 0.3

# Flower parameters
NUM_FLOWERS = 50
FLOWER_STEM_HEIGHT = 30
FLOWER_SIZE = 10
FLOWER_HEART_SIZE = 0.04

NUM_BRANCHES = 5
BRANCH_WIDTH = 20

# Image display parameters
current_image = None
current_image_index = -1
image_position = None
image_display_time = 0
IMAGE_DISPLAY_DURATION = 1000

class Branch:
    def __init__(self, start_x, start_y, angle, length):
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle
        self.length = length

    def draw(self, surface):
        end_x = self.start_x + math.cos(math.radians(self.angle)) * self.length
        end_y = self.start_y - math.sin(math.radians(self.angle)) * self.length
        pygame.draw.line(surface, DARK_BROWN, (self.start_x, self.start_y), (end_x, end_y), BRANCH_WIDTH)

class Flower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stem_height = random.randint(20, FLOWER_STEM_HEIGHT)
        self.color = random.choice([PINK, DARK_PINK])

class BigFlower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stem_height = 0
        self.target_height = 100
        self.growing = False

    def start_growing(self):
        self.growing = True

    def update(self):
        if self.growing and self.stem_height < self.target_height:
            self.stem_height += 1

    def draw(self, surface):
        if self.stem_height > 0:
            pygame.draw.line(surface, GRASS_GREEN, (self.x, self.y), (self.x, self.y - self.stem_height), 3)
            if self.stem_height >= self.target_height:
                draw_heart(surface, self.x, self.y - self.stem_height, 2, PINK)

def draw_flower(surface, flower):
    pygame.draw.line(surface, GRASS_GREEN, (flower.x, flower.y), (flower.x, flower.y - flower.stem_height), 2)
    pygame.draw.circle(surface, flower.color, (flower.x, flower.y - flower.stem_height), FLOWER_SIZE)
    draw_heart(surface, flower.x, flower.y - flower.stem_height - FLOWER_SIZE, FLOWER_HEART_SIZE, DARK_PINK)

class Petal:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = random.uniform(2, 5)
        self.angle = random.uniform(0, 360)
        self.angular_speed = random.uniform(-1, 1)

    def fall(self):
        self.y += self.speed
        self.x += math.sin(math.radians(self.angle)) * 0.3
        self.angle += self.angular_speed
        if self.y > HEIGHT - 20:
            self.y = HEIGHT - TRUNK_HEIGHT - random.randint(0, TREE_HEIGHT)
            self.x = WIDTH // 2 + random.randint(-TREE_WIDTH // 2, TREE_WIDTH // 2)

def draw_heart(surface, x, y, size, color):
    points = []
    for i in range(360):
        angle = math.radians(i)
        heart_x = size * (16 * math.sin(angle) ** 3)
        heart_y = size * (13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle))
        points.append((x + heart_x, y - heart_y))
    pygame.draw.polygon(surface, color, points)

def create_trunk_surface():
    trunk_surface = pygame.Surface((TRUNK_WIDTH, TRUNK_HEIGHT), pygame.SRCALPHA)
    trunk_surface.fill(DARK_BROWN)
    for _ in range(20):  # Add light brown streaks
        start_x = random.randint(0, TRUNK_WIDTH)
        start_y = random.randint(0, TRUNK_HEIGHT)
        end_x = start_x + random.randint(-10, 10)
        end_y = start_y + random.randint(20, 50)
        pygame.draw.line(trunk_surface, LIGHT_BROWN, (start_x, start_y), (end_x, end_y), random.randint(2, 5))
    return trunk_surface

def create_tree_blocks():
    blocks = []
    for x in range(WIDTH // 2 - TREE_WIDTH // 2, WIDTH // 2 + TREE_WIDTH // 2, LEAF_SIZE):
        for y in range(int(HEIGHT - TRUNK_HEIGHT - TREE_HEIGHT), int(HEIGHT - TRUNK_HEIGHT), int(LEAF_SIZE)):
            distance = math.hypot(x - WIDTH // 2, y - (HEIGHT - TRUNK_HEIGHT))
            if distance <= TREE_WIDTH // 2:
                size = random.randint(LEAF_SIZE - 5, LEAF_SIZE + 5)
                color = PINK if random.random() > 0.25 else DARK_PINK
                rx = x + random.randint(-5, 5)
                ry = y + random.randint(-5, 5)
                blocks.append((rx, ry, size, color))
    return blocks

def create_underlayer():
    blocks = []
    for x in range(WIDTH // 2 - TREE_WIDTH // 2, WIDTH // 2 + TREE_WIDTH // 2, LEAF_SIZE):
        for y in range(int(HEIGHT - TRUNK_HEIGHT - TREE_HEIGHT), int(HEIGHT - TRUNK_HEIGHT), int(LEAF_SIZE)):
            distance = math.hypot(x - WIDTH // 2, y - (HEIGHT - TRUNK_HEIGHT))
            if distance <= TREE_WIDTH // 2 + LEAF_SIZE:
                blocks.append((x, y, LEAF_SIZE, DARK_PINK))
    return blocks

def main():
    global current_image, current_image_index, image_position, image_display_time

    # Create tree blocks (static) and petals
    petals = []
    trunk_surface = create_trunk_surface()
    tree_blocks = []
    branches = []

    # Create branches
    for _ in range(NUM_BRANCHES):
        start_x = WIDTH // 2 + random.randint(-TRUNK_WIDTH // 4, TRUNK_WIDTH // 4)
        start_y = HEIGHT - TRUNK_HEIGHT + random.randint(0, TRUNK_HEIGHT // 4)
        angle = random.uniform(30, 150)
        length = random.randint(TRUNK_WIDTH, TRUNK_WIDTH * 2)
        branches.append(Branch(start_x, start_y, angle, length))

    # Create tree blocks
    tree_blocks = create_tree_blocks()

    # Create petals (starting from under the canopy)
    for _ in range(NUM_PETALS):
        x = WIDTH // 2 + random.randint(-TREE_WIDTH // 2, TREE_WIDTH // 2)
        y = HEIGHT - TRUNK_HEIGHT - random.randint(0, TREE_HEIGHT)
        color = PINK if random.random() > 0.25 else DARK_PINK
        petals.append(Petal(x, y, color))

    # Create flowers
    flowers = [Flower(random.randint(0, WIDTH), HEIGHT - 5) for _ in range(NUM_FLOWERS)]

    # Create grass blades
    grass_blades = []
    for _ in range(6000):
        x = random.randint(0, WIDTH)
        y = random.randint(HEIGHT - 20, HEIGHT)
        color = random.choice([GRASS_GREEN, LIGHT_GRASS_GREEN])
        grass_blades.append((x, y, color))

    # Create underlayer
    underlayer = create_underlayer()

    # Create big flower
    big_flower = BigFlower(WIDTH - 100, HEIGHT)
    big_flower_click_time = 0

    # Main game loop
    running = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if big_flower.growing and big_flower.stem_height >= big_flower.target_height:
                        flower_rect = pygame.Rect(big_flower.x - 50, big_flower.y - big_flower.stem_height - 50, 100, 100)
                        if flower_rect.collidepoint(event.pos):
                            big_flower_click_time = current_time
                            current_image_index = (current_image_index + 1) % len(images)
                            current_image = images[current_image_index]
                elif event.button == 3:  # Right mouse button
                    big_flower_click_time = current_time
                    current_image_index = (current_image_index - 1) % len(images)
                    current_image = images[current_image_index]

        # Clear the screen
        screen.fill(SKY_BLUE)

        # Draw grass blades
        for blade in grass_blades:
            pygame.draw.line(screen, blade[2], (blade[0], HEIGHT), (blade[0], blade[1]), 1)

        # Draw trunk
        screen.blit(trunk_surface, (WIDTH // 2 - TRUNK_WIDTH // 2, HEIGHT - TRUNK_HEIGHT))

        # Draw branches
        for branch in branches:
            branch.draw(screen)

        # Draw flowers
        for flower in flowers:
            draw_flower(screen, flower)

        # Update and draw petals (heart-shaped)
        for petal in petals:
            petal.fall()
            draw_heart(screen, int(petal.x), int(petal.y), PETAL_SIZE, petal.color + (230,))

        # Draw underlayer
        underlayer_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for block in underlayer:
            block_color = block[3] + (230,)
            pygame.draw.rect(underlayer_surface, block_color, (block[0], block[1], block[2], block[2]))
        screen.blit(underlayer_surface, (0, 0))

        # Draw tree top (static blocks)
        canopy_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for block in tree_blocks:
            block_color = block[3] + (230,)
            pygame.draw.rect(canopy_surface, block_color, (block[0], block[1], block[2], block[2]))
        screen.blit(canopy_surface, (0, 0))

        # Draw title
        title_text = title_font.render("Happy 6 Month Anniversary!", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        screen.blit(title_text, title_rect)

        # Draw subtitle
        subtitle_text = subtitle_font.render("I love you Serena :)", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(subtitle_text, subtitle_rect)

        # Draw big flower if it's time
        if current_time - start_time > 5000:  # 5 seconds
            big_flower.start_growing()
        big_flower.update()
        big_flower.draw(screen)

        # Draw the current image if one is selected and the display time hasn't expired
        if current_image and (current_time - big_flower_click_time < IMAGE_DISPLAY_DURATION):
            # Center the image in the screen
            image_rect = current_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(current_image, image_rect.topleft)
        else:
            current_image = None

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()