import pygame

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
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

def draw_player():
    pygame.draw.rect(screen, "white", (player_pos.x, player_pos.y, player_size.x, player_size.y), 10)

def main():
    global screen, player_pos, player_size

    screen, clock = initialize_game()
    
    player_size = pygame.Vector2(70, 10)
    player_pos = pygame.Vector2(screen.get_width() / 2 - player_size.x / 2, 650)

    running = True
    dt = 0

    while running:
        running = handle_events()

        screen.fill("black")
        
        update_player_position()
        draw_player()

        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
