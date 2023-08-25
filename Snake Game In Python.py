import pygame
import sys
import random
import time

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 600))

# Initialize snake and food positions
snake = [(200, 200), (200, 210), (200, 220)]
snake_direction = 'up'
food = (random.randint(0, 59) * 10, random.randint(0, 59) * 10)  # Generate food at a multiple of 10

# Set the starting and current snake speed
starting_snake_speed = 5
snake_speed = starting_snake_speed

clock = pygame.time.Clock()

food_eaten = 0  # To keep track of the number of food items eaten
normal_food_eaten = 0  # Count of normal food items eaten
bonus_food_eaten = 0  # Count of bonus food items eaten
bonus_diamond = None  # Coordinates of the bonus diamond
bonus_timer = None  # Timer for the bonus diamond
current_level = 1  # Current level

# Define colors for the glowing effect
bonus_colors = [(255, 255, 0), (255, 255, 128)]
current_bonus_color = 0  # Index of the current bonus color

def generate_bonus_diamond():
    return (random.randint(0, 59) * 10, random.randint(0, 59) * 10)  # Generate at a multiple of 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'down':
                snake_direction = 'up'
            elif event.key == pygame.K_DOWN and snake_direction != 'up':
                snake_direction = 'down'
            elif event.key == pygame.K_LEFT and snake_direction != 'right':
                snake_direction = 'left'
            elif event.key == pygame.K_RIGHT and snake_direction != 'left':
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

    # Check if the snake has hit its own tail.
    if new_head in snake[1:]:
        pygame.quit()
        sys.exit()

    # Check if the snake has hit the bonus diamond.
    if bonus_diamond is not None and snake[0] == bonus_diamond:
        bonus_diamond = None
        bonus_food_eaten += 1
        snake.append((0, 0))  # Increase the snake's length

    # Check if the snake has hit the food.
    if snake[0] == food:
        # Generate new food coordinates.
        food = (random.randint(0, 59) * 10, random.randint(0, 59) * 10)  # Generate food at a multiple of 10
        
        # Increase the count of normal food eaten
        normal_food_eaten += 1
        food_eaten += 1

        # Check for bonus diamond appearance
        if normal_food_eaten >= 5 and bonus_diamond is None:
            bonus_diamond = generate_bonus_diamond()
            bonus_timer = time.time() + 10  # Bonus diamond lasts for 10 seconds

        # Check for level up
        if normal_food_eaten >= 30 and current_level < 100:
            current_level += 1
            snake_speed += 1

    else:
        # Remove the tail segment only if not leveling up
        if normal_food_eaten < 30:
            snake.pop()

    # Draw everything.
    screen.fill((0, 0, 0))  # Clear the screen
    pygame.draw.rect(screen, (255, 0, 0), (*food, 10, 10))  # Draw the food
    for i, segment in enumerate(snake):
        if i == 0:
            pygame.draw.circle(screen, (255, 255, 0), (segment[0] + 5, segment[1] + 5), 8)  # Draw the snake head as smaller yellow circle
        else:
            pygame.draw.circle(screen, (0, 255, 0), (segment[0] + 5, segment[1] + 5), 5)  # Draw the snake tail as small green circle
    
    # Draw bonus diamond if available and within the time limit
    if bonus_diamond is not None and time.time() < bonus_timer:
        pygame.draw.polygon(screen, bonus_colors[current_bonus_color], [(bonus_diamond[0] + 5, bonus_diamond[1]), (bonus_diamond[0], bonus_diamond[1] + 5), (bonus_diamond[0] + 10, bonus_diamond[1] + 5), (bonus_diamond[0] + 5, bonus_diamond[1] + 10)])  # Draw the bonus diamond
    
    # Display the food eaten count and current level
    font = pygame.font.Font(None, 36)
    text_food = font.render(f"Food Eaten: {food_eaten}", True, (255, 255, 255))
    text_level = font.render(f"Level: {current_level}", True, (255, 255, 255))
    screen.blit(text_food, (10, 10))
    screen.blit(text_level, (450, 10))

    # Display the bonus eaten count
    text_bonus = font.render(f"Bonus Eaten: {bonus_food_eaten}", True, (255, 255, 255))
    screen.blit(text_bonus, (10, 40))

    # Display the bonus timer countdown
    if bonus_diamond is not None and time.time() < bonus_timer:
        bonus_countdown = int(bonus_timer - time.time())
        text_countdown = font.render(f"Bonus Time: {bonus_countdown}", True, (255, 255, 255))
        screen.blit(text_countdown, (10, 570))  # Display at the bottom left corner

    # Update the display.
    pygame.display.update()

    # Change the bonus diamond color index for glowing effect
    current_bonus_color = (current_bonus_color + 1) % len(bonus_colors)

    clock.tick(15)  # Control the frame rate
