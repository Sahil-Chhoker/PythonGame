import pygame
import math

pygame.init()

# Initialize game
screen_size = pygame.Vector2(1000, 720)
screen = pygame.display.set_mode((int(screen_size.x), int(screen_size.y)))
clock = pygame.time.Clock()

# Player variables
player_size = pygame.Vector2(70, 10)
player_pos = pygame.Vector2(screen.get_width() / 2 - player_size.x / 2, 650)

# Enemy AI variables
enemy_size = pygame.Vector2(70, 10)
enemy_pos = pygame.Vector2(screen.get_width() / 2 - enemy_size.x / 2, 50)
enemy_speed = 8  # Adjust the speed for more responsiveness

# Ball variables
ball_speed = 20
ball_radius = 10
can_launch_ball = True
initialized_ball_pos = pygame.Vector2(player_pos.x + player_size.x / 2, player_pos.y - player_size.y)
ball_pos = pygame.Vector2(10, 10)
ball_direction = pygame.Vector2(1, 1)  # Initial direction

# Arrow image
arrow_image = pygame.image.load("launch_arrow.png")
arrow_rect = arrow_image.get_rect(center=(player_pos.x + player_size.x / 2, player_pos.y))

# Track Mouse clicks
clicking = False

running = True
dt = 0

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicking = False

    # Get Mouse Position
    mouse_pos = pygame.mouse.get_pos()

    # Calculate angle
    x_dis = mouse_pos[0] - arrow_rect.centerx
    y_dis = -(mouse_pos[1] - arrow_rect.centery)
    angle = math.degrees(math.atan2(y_dis, x_dis))

    # Update player position
    initial_player_pos = pygame.Vector2(screen_size.x / 2, 650)
    if can_launch_ball:
        player_pos = initial_player_pos
    else:
        player_pos.x, player_pos.y = mouse_pos
        player_pos.y = 650

        if player_pos.x + player_size.x >= 980:
            player_pos.x = 905
        elif player_pos.x <= 100:
            player_pos.x = 95

    if enemy_pos.x + enemy_size.x >= 980:
            enemy_pos.x = 905
    elif enemy_pos.x <= 100:
            enemy_pos.x = 95

    # Update enemy AI position based on the ball position
    target_x = ball_pos.x - enemy_size.x / 2
    enemy_pos.x += (target_x - enemy_pos.x) * 1

    # Apply boundary conditions for enemy
    if enemy_pos.x + enemy_size.x / 2 >= 980:
        enemy_pos.x = 1000 - enemy_size.x / 2
    elif enemy_pos.x - enemy_size.x / 2 <= 60:
        enemy_pos.x = 60 + enemy_size.x / 2

    # Calculate player direction
    player_direction = pygame.Vector2(mouse_pos[0] - player_pos.x, mouse_pos[1] - player_pos.y)
    player_direction.normalize_ip()  # Normalize the vector

    # Calculate enemy direction
    enemy_direction = pygame.Vector2(ball_pos.x - enemy_pos.x, ball_pos.y - enemy_pos.y)
    enemy_direction.normalize_ip()  # Normalize the vector

    # Fill the screen
    screen.fill((0, 0, 0))

    # Draw ball
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_pos.x), int(ball_pos.y)), ball_radius)
    # Draw player and enemy paddles and boundaries
    pygame.draw.rect(screen, (255, 255, 255), (player_pos.x - player_size.x / 2, player_pos.y, player_size.x, player_size.y), 10)
    pygame.draw.rect(screen, (255, 0, 0), (enemy_pos.x - enemy_size.x / 2, enemy_pos.y, enemy_size.x, enemy_size.y), 10)
    pygame.draw.line(screen, (255, 255, 255), (60, 0), (60, 720), 5)
    pygame.draw.line(screen, (255, 255, 255), (940, 0), (940, 720), 5)

    # Disable Arrows After Click
    if can_launch_ball:
        if clicking:
            can_launch_ball = False

        # Get Launch Direction
        launch_dir = mouse_pos - player_pos
        launch_dir.normalize_ip()
        if launch_dir.magnitude != 0:
            ball_direction = launch_dir

        # Rotate and draw arrow image
        modified_arrow_image = pygame.transform.rotate(arrow_image, angle - 90)
        modified_arrow_image = pygame.transform.scale_by(modified_arrow_image, 3)
        arrow_rect = modified_arrow_image.get_rect(center=(player_pos.x, player_pos.y - 15))
        screen.blit(modified_arrow_image, arrow_rect)

    # Launch Ball
    if can_launch_ball:
        ball_pos = initialized_ball_pos
    else:
        ball_pos += ball_direction * ball_speed

    # Bounce Back
    if ball_pos.x + ball_radius >= 940 or ball_pos.x - ball_radius <= 60:
        ball_direction.x = -ball_direction.x

    # Bounce off Striker
    player_rect = pygame.Rect(player_pos.x - player_size.x / 2, player_pos.y, player_size.x, player_size.y)
    if player_rect.colliderect(ball_pos.x - ball_radius, ball_pos.y - ball_radius, 2 * ball_radius, 2 * ball_radius):
        relative_velocity = ball_direction - player_direction
        ball_direction -= 2 * relative_velocity.dot(pygame.Vector2(0, -1)) * pygame.Vector2(0, -1)
        ball_direction.normalize_ip()  # Ensure the ball direction is normalized

        ball_pos.y = player_pos.y - ball_radius - 1  # Adjust the ball's position to prevent repeated collisions

    # Bounce off Enemy Paddle
    enemy_rect = pygame.Rect(enemy_pos.x - enemy_size.x / 2, enemy_pos.y - enemy_size.y / 2, enemy_size.x, enemy_size.y)
    if enemy_rect.colliderect(ball_pos.x - ball_radius, ball_pos.y - ball_radius, 2 * ball_radius, 2 * ball_radius):
        relative_velocity = ball_direction - enemy_direction
        ball_direction -= 2 * relative_velocity.dot(pygame.Vector2(0, -1)) * pygame.Vector2(0, -1)
        ball_direction.normalize_ip()  # Ensure the ball direction is normalized

        ball_pos.y = enemy_pos.y + enemy_size.y + ball_radius + 1  # Adjust the ball's position to prevent repeated collisions

    # To check the collision area of enemy
    pygame.draw.rect(screen, (0, 255, 0), (enemy_rect.x, enemy_rect.y, enemy_rect.width, enemy_rect.height), 2)

    # Refresh the screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
