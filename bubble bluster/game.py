import pygame
from settings import Settings
from player import Player
from bubble import Bubble
import game_functions as gf

def run_game():
    pygame.init()
    gm_settings = Settings()
    
    screen = pygame.display.set_mode([gm_settings.screen_width, gm_settings.screen_height])
    pygame.display.set_caption(gm_settings.caption)
    
    player = Player(screen)
    bubble = Bubble(screen, gm_settings)
    
    while True:
        gf.check_events()
        player.update()
        gf.update_screen(gm_settings, screen, player)
    
run_game()