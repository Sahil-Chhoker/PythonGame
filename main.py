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

# Ball variables
ball_speed = 30
ball_radius = 10
can_launch_ball = True
initialized_ball_pos = pygame.Vector2(player_pos.x + player_size.x / 2, player_pos.y - player_size.y)
ball_pos = pygame.Vector2(10, 10)

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

    # Fill the screen
    screen.fill((0, 0, 0))

    # Draw ball
    launch_dir = pygame.Vector2()
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_pos.x), int(ball_pos.y)), ball_radius)

    # Draw player and boundaries
    pygame.draw.rect(screen, (255, 255, 255), (player_pos.x - player_size.x / 2, player_pos.y, player_size.x, player_size.y), 10)
    pygame.draw.line(screen, (255, 255, 255), (60, 0), (60, 720), 5)
    pygame.draw.line(screen, (255, 255, 255), (940, 0), (940, 720), 5) 

    # Disable Arrows After Click
    if(can_launch_ball):
        if(clicking):
            can_launch_ball = False

        # Get Launch Direction
        launch_dir = mouse_pos - player_pos
        launch_dir.normalize_ip()
        if(launch_dir.magnitude != 0):
            new_launch_dir = launch_dir

        # Rotate and draw arrow image
        modified_arrow_image = pygame.transform.rotate(arrow_image, angle - 90)
        modified_arrow_image = pygame.transform.scale_by(modified_arrow_image, 3)
        arrow_rect = modified_arrow_image.get_rect(center=(player_pos.x, player_pos.y - 15))
        screen.blit(modified_arrow_image, arrow_rect)

    # Launch Ball
    if can_launch_ball:
        ball_pos = initialized_ball_pos
    else:
        ball_pos += new_launch_dir * ball_speed

    # Bounce Back
    if ball_pos.x + ball_radius >= 940 or ball_pos.x - ball_radius <= 60:
        new_launch_dir.x = -new_launch_dir.x

    # Bounce off Striker
    if (player_pos.x - player_size.x / 2 <= ball_pos.x <= player_pos.x + player_size.x / 2 and player_pos.y <= ball_pos.y <= player_pos.y + player_size.y):
        new_launch_dir.y = -new_launch_dir.y


    # Refresh the screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
