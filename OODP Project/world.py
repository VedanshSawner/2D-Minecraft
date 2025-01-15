import pygame
import pygame.gfxdraw
import random
import time
import math

class World:
    def __init__(self):
        self.tile_size = 32
        self.tiles = pygame.sprite.Group()
        self.tile_map = {}
        self.world_width = 200
        self.world_height = 200
        self.render_distance = 25
        self.load_textures()
        self.clouds = self.generate_clouds()
        self.generate_world()

        self.start_time = time.time()
        self.day_night_duration = 60

    def load_textures(self):
        self.textures = {
            'dirt': pygame.image.load('assets/blocks/dirt.png'),
            'grass': pygame.image.load('assets/blocks/grass.png'),
            'cobblestone': pygame.image.load('assets/blocks/cobblestone.png'),
            'wood': pygame.image.load('assets/blocks/wood.png'),
            'flower1': pygame.image.load('assets/blocks/flower1.png'),
            'flower2': pygame.image.load('assets/blocks/flower2.png'),
            'bomb': pygame.image.load('assets/blocks/shrooms.png'),
            'cloud': pygame.image.load('assets/gui/cloud2.png'),
            'gem': pygame.image.load('assets/blocks/diamond_ore.png'),
            'leaves': pygame.image.load('assets/blocks/leaves.png'),
            'granite': pygame.image.load('assets/blocks/granite.png'),
            'andesite': pygame.image.load('assets/blocks/andesite.png'),
        }

    def generate_world(self):
        world_data = []
        cliff_height = self.world_height // 2

        for y in range(self.world_height):
            world_data.append([])

        for x in range(0, self.world_width):        # Horizontal terrain generation
            if x > 0:
                change = random.choice([-1, 0, 1])
                cliff_height += change
            for y in range(0, self.world_height):   # Vertical terrain generation
                if y > 0 and world_data[y - 1][x] == 'wood' and y < cliff_height:
                    block = 'wood'
                elif y == cliff_height - 3:
                    block = 'wood' if random.random() < 0.15 else 'air'
                elif y < cliff_height:
                    block = 'air'
                elif y == cliff_height:
                    block = 'grass'
                    if world_data[y - 1][x] != 'wood':
                        if random.random() < 0.08:
                            world_data[y - 1][x] = 'flower1' if random.random() < 0.5 else 'flower2'
                        elif random.random() < 0.15:
                            world_data[y - 1][x] = 'bomb'
                else:
                    if y in [cliff_height + 1, cliff_height + 2, cliff_height + 3]:
                        block = 'dirt'
                    elif y > cliff_height + 3 and y < cliff_height + 8:
                        if random.random() < 0.8:
                            block = 'cobblestone'
                        else:
                            block = 'dirt'
                    else:
                        ran = random.random()
                        if ran <= 0.05:
                            block = 'gem'
                        elif ran > 0.05 and ran <= 0.4:
                            block = 'cobblestone'
                        elif ran > 0.4 and ran <= 0.7:
                            block = 'granite'
                        else:
                            block = 'andesite'
                world_data[y].append(block)

        for x in range(self.world_width):
            for y in range(self.world_height):
                if world_data[y][x] == 'wood':
                    if y - 2 >= 0 and world_data[y - 2][x] == 'air':
                        world_data[y - 2][x] = 'leaves'

                    for dx, dy in [(0, -1), (-1, -1), (1, -1), (-1, 0), (1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.world_width and 0 <= ny < self.world_height:
                            if world_data[ny][nx] == 'air':
                                world_data[ny][nx] = 'leaves'
                    break
        
        for y in range(0, self.world_height):
            for x in range(0, self.world_width):
                if world_data[y][x] != 'air':
                    tile = Tile(x - (self.world_width // 2), y - (self.world_height // 2), world_data[y][x], self.textures[world_data[y][x]], self.tile_size)
                    self.tiles.add(tile)
                    self.tile_map[(x - (self.world_width // 2), y - (self.world_height // 2))] = tile

    def generate_clouds(self):
        clouds = []
        for _ in range(5):
            x = random.randint(0, 800)
            y = random.randint(0, 100)
            cloud_width = random.randint(100, 200)
            cloud_height = random.randint(40, 70)
            clouds.append((x, y, cloud_width, cloud_height))
        return clouds

    def update_day_night_cycle(self):
        elapsed_time = time.time() - self.start_time
        cycle_progress = (elapsed_time % self.day_night_duration) / self.day_night_duration
        transition_progress = cycle_progress**2

        light_blue = (135, 206, 235)
        dark_blue = (25, 25, 112)

        r = int(light_blue[0] * (1 - transition_progress) + dark_blue[0] * transition_progress)
        g = int(light_blue[1] * (1 - transition_progress) + dark_blue[1] * transition_progress)
        b = int(light_blue[2] * (1 - transition_progress) + dark_blue[2] * transition_progress)

        self.sky_color = (r, g, b)

    def render(self, screen, camera, player):
        self.update_day_night_cycle()
        pygame.draw.rect(screen, self.sky_color, (0, 0, 800, 600))

        for cloud in self.clouds:
            screen.blit(self.textures['cloud'], (cloud[0], cloud[1]))

        player_tile_x, player_tile_y = player.get_pos()

        start_x = player_tile_x - self.render_distance
        end_x = player_tile_x + self.render_distance
        start_y = player_tile_y - self.render_distance
        end_y = player_tile_y + self.render_distance

        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if (x, y) in self.tile_map:
                    tile = self.tile_map[(x, y)]
                    screen_x = tile.rect.x - camera.offset.x
                    screen_y = tile.rect.y - camera.offset.y
                    screen.blit(tile.image, (screen_x, screen_y))

    def render_block_count(self, screen, x, y, count):
        font = pygame.font.Font(None, 24)
        count_text = font.render(str(count), True, (255, 255, 255))
        screen.blit(count_text, (x + 2, y + 2))

    def place_block(self, camera, player, x, y, block_type):
        block_x = x + camera.offset.x
        block_y = y + camera.offset.y
        tile_x = block_x // self.tile_size
        tile_y = block_y // self.tile_size
        tile_pos = (tile_x, tile_y)

        if abs(player.get_pos()[0] - tile_x) <= 2 and abs(player.get_pos()[1] - tile_y) <= 3:
            if tile_pos not in self.tile_map:
                if player.has_block_in_inventory(block_type):
                    player.remove_block_from_inventory(block_type)
                    tile = Tile(tile_x, tile_y, block_type, self.textures[block_type], self.tile_size)
                    self.tiles.add(tile)
                    self.tile_map[tile_pos] = tile

    def break_block(self, camera, player, x, y, tool):
        block_x = x + camera.offset.x
        block_y = y + camera.offset.y
        tile_x = block_x // self.tile_size
        tile_y = block_y // self.tile_size
        tile_pos = (tile_x, tile_y)

        block_broken = False
        if (abs(player.get_pos()[0] - tile_x) <= 2 and abs(player.get_pos()[1] - tile_y) <= 3):
            if tile_pos in self.tile_map:
                tile_sprite = self.tile_map[tile_pos]
                block_type = tile_sprite.tile_type

                if (tool == 'pickaxe'):
                    if block_type in ['cobblestone', 'andesite', 'granite', 'gem', 'flower1', 'flower2'] and block_type != 'leaves':
                        block_broken = True
                elif (tool == 'axe'):
                    if block_type in ['wood', 'leaves', 'flower1', 'flower2'] and block_type != 'leaves':
                        block_broken = True
                elif (tool == 'shovel'):
                    if block_type in ['grass', 'dirt', 'flower1', 'flower2'] and block_type != 'leaves':
                        block_broken = True
                if block_broken:
                    player.add_block_to_inventory(block_type)
                    tile_sprite.kill()
                    del self.tile_map[tile_pos]
                elif block_type == 'leaves':
                    tile_sprite.kill()
                    del self.tile_map[tile_pos]
    
    def handle_click(self, player, camera, pos, tool, button):
        x, y = pos
        self.break_block(camera, player, x, y, tool)

        if button == 3:
            block_type = player.get_selected_block()
            if block_type:
                self.place_block(camera, player, x, y, block_type)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type, texture, tile_size):
        super().__init__()
        self.image = texture
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))
        self.tile_type = tile_type