import pygame
import sys
from world import World
from player import Player
from camera import Camera
from menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Block Survival")
        self.world = World()
        self.player = Player(0, 0)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.camera = Camera(800, 600)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    item = self.player.inventory[self.player.item_held]
                    self.world.handle_click(self.player, self.camera, event.pos, item, event.button)

                elif event.button == 3:
                    if self.player.is_tool_selected:
                        continue
                    else:
                        selected_block = list(self.player.block_inventory.keys())[self.player.item_held]
                        self.world.handle_click(self.player, self.camera, event.pos, selected_block, event.button)
        return True

    def update(self):
        self.player.update(self.camera, self.world)
        self.camera.update(self.player)

        if self.player.lives <= 0:
            self.game_over()
            return False
        else:
            return True

    def render(self):
        self.screen.fill((255, 255, 255))
        self.world.render(self.screen, self.camera, self.player)
        self.player.render(self.screen, self.camera)
        pygame.display.flip()
    
    def game_over(self):
        """Handles game over logic."""
        font = pygame.font.Font("assets/gui/menu_font.ttf", 50)
        text = font.render("Game Over", True, (0, 0, 0))
        text_rect = text.get_rect(center=(400, 300))
        screen = pygame.display.get_surface()
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.quit()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            if running:
                running = self.update()
            if running:
                self.render()
            self.clock.tick(60)

if __name__ == "__main__":
    menu = Menu()
    game_run = menu.main_menu()
    if game_run:
        game = Game()
        game.run()
    pygame.quit()
    sys.exit()