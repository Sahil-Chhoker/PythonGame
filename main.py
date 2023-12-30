import pygame

def initialize_game(screen_size):
    pygame.init()
    screen = pygame.display.set_mode((screen_size.x, screen_size.y))
    clock = pygame.time.Clock()
    return screen, clock

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  # Signal to stop the game
    return True

def update_player_position():
    player_pos.x, player_pos.y = pygame.mouse.get_pos()
    player_pos.x -= player_size.x / 2
    player_pos.y = 650

    if(player_pos.x + player_size.x >= 940):
        player_pos.x = 870
    elif(player_pos.x <= 60):
        player_pos.x = 60

def draw_player():
    pygame.draw.rect(screen, "white", (player_pos.x, player_pos.y, player_size.x, player_size.y), 10)

def draw_boundaryLines():
    pygame.draw.line(screen, "white", (60, 0), (60, 720), 5)
    pygame.draw.line(screen, "white", (940, 0), (940, 720), 5)

def draw_ball(screen_size):
    pygame.draw.circle(screen, "white", screen_size/2, 10)

def main():
    screen_size = pygame.Vector2(1000, 720)

    global screen, player_pos, player_size

    screen, clock = initialize_game(screen_size)
    
    player_size = pygame.Vector2(70, 10)
    player_pos = pygame.Vector2(screen.get_width() / 2 - player_size.x / 2, 650)

    running = True
    dt = 0

    while running:
        running = handle_events()
    
        screen.fill("black")
        
        draw_ball(screen_size)
        update_player_position()
        draw_player()
        draw_boundaryLines()

        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
