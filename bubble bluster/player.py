import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Player, self).__init__()
        
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        self.player = pygame.Surface((75, 25))
        self.player.fill((255, 0, 0))
        self.rect = self.player.get_rect()
        
    def blit_me(self):
        self.screen.blit(self.player, self.rect)