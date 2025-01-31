import pygame
from settings import Settings
from player import Player

def run_game():
    pygame.init()
    gm_settings = Settings()
    
    screen = pygame.display.set_mode([gm_settings.screen_width, gm_settings.screen_height])
    pygame.display.set_caption(gm_settings.caption)
    
    player = Player(screen)
    
    running = True
    while running:
        screen.fill(gm_settings.bg_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        player.blit_me()
    
        pygame.display.flip()

    pygame.quit()

run_game()