import pygame
import sys
import random

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 600))

# Initialize snake and food positions
snake = [(200, 200), (200, 210), (200, 220)]
snake_direction = 'up'
food = (random.randint(0, 59) * 10, random.randint(0, 59) * 10)  # Generate food at a multiple of 10

# Set the snake's speed
snake_speed = 10

clock = pygame.time.Clock()

food_eaten = 0  # To keep track of the number of food items eaten

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_direction = 'up'
            elif event.key == pygame.K_DOWN:
                snake_direction = 'down'
            elif event.key == pygame.K_LEFT:
                snake_direction = 'left'
            elif event.key == pygame.K_RIGHT:
                snake_direction = 'right'

    # Update the snake's position.
    new_head = list(snake[0])
    if snake_direction == 'up':
        new_head[1] -= snake_speed
    elif snake_direction == 'down':
        new_head[1] += snake_speed
    elif snake_direction == 'left':
        new_head[0] -= snake_speed
    elif snake_direction == 'right':
        new_head[0] += snake_speed

    # Check if the snake has hit the boundary.
    if new_head[0] < 0 or new_head[0] >= 600 or new_head[1] < 0 or new_head[1] >= 600:
        pygame.quit()
        sys.exit()

    snake.insert(0, tuple(new_head))  # Insert new head at the beginning

    # Check if the snake has hit the food.
    if snake[0] == food:
        # Increase the snake's length.
        snake.append((0, 0))  # Add a new segment at the end of the snake

        # Generate new food coordinates.
        food = (random.randint(0, 59) * 10, random.randint(0, 59) * 10)  # Generate food at a multiple of 10
        
        # Increase the count of food eaten
        food_eaten += 1

    else:
        # Remove the tail segment
        snake.pop()

    # Draw everything.
    screen.fill((0, 0, 0))  # Clear the screen
    pygame.draw.rect(screen, (255, 0, 0), (*food, 10, 10))  # Draw the food
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*segment, 10, 10))  # Draw the snake segments

    # Display the food eaten count
    font = pygame.font.Font(None, 36)
    text = font.render(f"Food Eaten: {food_eaten}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Update the display.
    pygame.display.update()

    clock.tick(15)  # Control the frame rate
