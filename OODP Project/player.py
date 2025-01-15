import pygame
import pygame.gfxdraw

class Player:
    def __init__(self, x, y):
        self.block_inventory = {}
        self.__max_block_slots__ = 7
        self.load_textures()
        self.__image__ = pygame.transform.scale(self.textures['player'], (32, 32))
        self.rect = self.__image__.get_rect(topleft=(x, y))

        # Movement attributes
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.5
        self.jump_strength = -8
        self.base_speed = 3
        self.sprint_speed = 7
        self.speed = self.base_speed

        # Stamina attributes
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.stamina_regeneration_rate = 0.5
        self.stamina_consumption_rate = 1

        # Tools and inventory
        self.inventory = ['axe', 'pickaxe', 'shovel']
        self.item_held = 0
        self.is_tool_selected = True

        # Falling attributes
        self.is_falling = False
        self.fall_distance = 0
        self.fall_damage_threshold = 7
        self.lives = 5

    def load_textures(self):
        self.textures = {
            'player': pygame.transform.scale(pygame.image.load('assets/player.png'), (33, 48)),
            'axe': pygame.image.load('assets/tools/axe.png'),
            'pickaxe': pygame.image.load('assets/tools/pickaxe.png'),
            'shovel': pygame.image.load('assets/tools/shovel.png'),
            'dirt': pygame.image.load('assets/blocks/dirt.png'),
            'stone': pygame.image.load('assets/blocks/stone.png'),
            'grass': pygame.image.load('assets/blocks/grass.png'),
            'wood': pygame.image.load('assets/blocks/wood.png'),
            'cobblestone': pygame.image.load('assets/blocks/cobblestone.png'),
            'bomb':pygame.image.load('assets/blocks/shrooms.png'),
            'flower1':pygame.image.load('assets/blocks/flower1.png'),
            'flower2':pygame.image.load('assets/blocks/flower2.png'),
            'gem':pygame.image.load('assets/blocks/diamond.png'),
            'granite': pygame.image.load('assets/blocks/granite.png'),
            'andesite': pygame.image.load('assets/blocks/andesite.png'),
        }

    def get_pos(self):
        return (self.rect.centerx // 32, self.rect.centery // 32)

    def update(self, camera, world):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity.x = -self.speed
        elif keys[pygame.K_d]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0

        if keys[pygame.K_LSHIFT] and (keys[pygame.K_a] or keys[pygame.K_d]):
            if self.stamina > self.max_stamina * 0.3:
                self.speed = self.sprint_speed
                self.stamina -= self.stamina_consumption_rate
        else:
            self.speed = self.base_speed
            if self.stamina < self.max_stamina:
                self.stamina += self.stamina_regeneration_rate

        self.stamina = min(self.stamina, self.max_stamina)

        # Handle jumping
        if keys[pygame.K_SPACE] and self.is_on_ground(world):
            self.velocity.y = self.jump_strength

        # Apply gravity
        self.velocity.y = min(self.velocity.y + self.gravity, 10)

        # Update player position
        self.rect.x += self.velocity.x
        self.handle_collisions(camera, world, axis='x')
        self.rect.y += self.velocity.y
        self.handle_collisions(camera, world, axis='y')

        combined_inventory = self.inventory + list(self.block_inventory.keys())
        for i in range(0, 10):
            if keys[getattr(pygame, f'K_{i}')] and i <= len(combined_inventory):
                self.switch_item(i)

        # Fall damage
        if not self.is_on_ground(world):
            if not self.is_falling:
                self.is_falling = True
                self.fall_distance = 0
            else:
                self.fall_distance += abs(self.velocity.y) / 32
        else:
            self.is_falling = False
            self.fall_distance = 0
        
    def is_on_ground(self, world):
        self.rect.y += 1
        on_ground = pygame.sprite.spritecollideany(self, world.tiles, collided=pygame.sprite.collide_rect)
        self.rect.y -= 1
        return on_ground

    def handle_collisions(self, camera, world, axis):
        collided_tiles = pygame.sprite.spritecollide(self, world.tiles, False, collided=pygame.sprite.collide_rect)


        for tile in collided_tiles:
            if tile.tile_type not in ['flower1', 'flower2', 'bomb']:
                if self.rect.top == 0:
                    self.is_falling = False
                    self.fall_distance = 0
                    continue

                if axis == 'x':
                    if self.velocity.x > 0:
                        self.rect.right = tile.rect.left
                    elif self.velocity.x < 0:
                        self.rect.left = tile.rect.right
                    self.velocity.x = 0
                elif axis == 'y':
                    if self.velocity.y > 0:
                        if self.is_falling:
                            terrain_height_diff = abs(self.rect.bottom - tile.rect.top)
                            effective_fall_distance = max(self.fall_distance, terrain_height_diff / 32)

                            if effective_fall_distance > self.fall_damage_threshold:
                                self.take_damage()

                            self.fall_distance = 0
                        self.rect.bottom = tile.rect.top
                        self.velocity.y = 0
                        self.is_falling = False
                    elif self.velocity.y < 0:
                        self.rect.top = tile.rect.bottom
                        self.velocity.y = 0

    def render(self, screen, camera):
        screen_x = self.rect.x - camera.offset.x
        screen_y = self.rect.y - camera.offset.y
        screen.blit(self.__image__, (screen_x, screen_y))

        self.render_stamina(screen)
        self.render_health(screen)
        self.render_inventory(screen)

        # Render the tool or block on the player's hand
        if self.is_tool_selected:
            current_tool = self.inventory[self.item_held]
            if current_tool:
                tool_x = screen_x + self.rect.width // 2 + 8
                tool_y = screen_y + self.rect.height // 2 + -12
                tool_image = pygame.transform.scale(self.textures[current_tool], (20, 20))
                screen.blit(tool_image, (tool_x, tool_y))
        else:
            try:
                current_block = list(self.block_inventory.keys())[self.item_held]
                if current_block:
                    block_offset_x = 8
                    block_offset_y = -15
                    block_x = screen_x + self.rect.width // 2 + block_offset_x
                    block_y = screen_y + self.rect.height // 2 + block_offset_y

                    block_image = pygame.transform.scale(self.textures[current_block], (23, 23))
                    screen.blit(block_image, (block_x, block_y))
            except:
                pass

    def render_stamina(self, screen):
        stamina_bar_width = 200
        stamina_bar_height = 10
        stamina_percentage = self.stamina / self.max_stamina
        current_stamina_bar_width = stamina_bar_width * stamina_percentage
        bar_x, bar_y = 10, 35

        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, stamina_bar_width, stamina_bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, current_stamina_bar_width, stamina_bar_height))
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, stamina_bar_width, stamina_bar_height), 2)


    def take_damage(self):
        self.lives -= 1
        if self.lives > 0:
            font = pygame.font.Font("assets/gui/menu_font.ttf", 20)
            text = font.render("One Life Lost", True, (255, 0, 0))
            screen = pygame.display.get_surface()
            
            text_rect = text.get_rect(center=(400, 450))

            shadow_offset = 3
            shadow_text = font.render("One Life Lost", True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(center=(400 + shadow_offset, 450 + shadow_offset))
            screen.blit(shadow_text, shadow_rect)
            
            screen.blit(text, text_rect)
            pygame.display.flip()

            pygame.time.wait(750)

    def render_health(self, screen):
        health_image = pygame.image.load('assets/gui/lifeline.png')
        health_image = pygame.transform.scale(health_image, (15, 15))
        health_x1, health_y1 = 75, 10

        for i in range(self.lives):
            screen.blit(health_image, (health_x1 - (i * 16), health_y1))

    def add_block_to_inventory(self, block_type, count=1):
        if block_type in self.block_inventory:
            self.block_inventory[block_type] += count
        elif len(self.block_inventory) < self.__max_block_slots__:
            self.block_inventory[block_type] = count

    def remove_block_from_inventory(self, block_type, count=1):
        if block_type in self.block_inventory:
            if self.block_inventory[block_type] > count:
                self.block_inventory[block_type] -= count
            elif self.block_inventory[block_type] == 1 and len(self.block_inventory) != 0:
                del self.block_inventory[block_type]
                self.item_held=0
                self.is_tool_selected = True
            else:
                del self.block_inventory[block_type]
                if len(self.block_inventory) == 0:
                    self.item_held = 0
                    self.is_tool_selected = True

    def render_inventory(self, screen):
        inventory_bar_width = 450
        inventory_bar_height = 50
        slot_width = inventory_bar_width // (self.__max_block_slots__ + len(self.inventory))
        screen_width, screen_height = screen.get_size()

        inventory_x = (screen_width - inventory_bar_width) // 2
        inventory_y = screen_height - inventory_bar_height - 20

        background_rect = pygame.Rect(inventory_x, inventory_y, inventory_bar_width, inventory_bar_height)
        pygame.gfxdraw.box(screen, background_rect, (0, 0, 0, 150))

        combined_inventory = self.inventory + list(self.block_inventory.keys())

        for i, item in enumerate(combined_inventory):
            slot_x = inventory_x + i * slot_width

            box_color = (0, 0, 0)
            if self.is_tool_selected and i < len(self.inventory) and i == self.item_held:
                box_color = (200, 200, 200)
            elif not self.is_tool_selected and i >= len(self.inventory) and (i - len(self.inventory)) == self.item_held:
                box_color = (200, 200, 200)
            pygame.draw.rect(screen, box_color, (slot_x, inventory_y, slot_width, inventory_bar_height), 2)

            item_texture = self.textures.get(item)
            if item_texture:
                screen.blit(item_texture,
                            (slot_x + (slot_width - slot_width // 2) // 2, inventory_y + (inventory_bar_height - 5 - inventory_bar_height // 2) // 2))

            if item in self.block_inventory:
                self.render_block_count(screen, slot_x + slot_width - 10, inventory_y + inventory_bar_height - 20, self.block_inventory[item])

    def render_block_count(self, screen, x, y, count):
        font = pygame.font.Font(None, 24)
        count_text = font.render(str(count), True, (255, 255, 255))
        screen.blit(count_text, (x, y))
        
    def switch_item(self, item_index):
        item_index -= 1
        if item_index == -1:
            if len(self.block_inventory) > 0:
                self.item_held = len(self.block_inventory) - 1
                self.is_tool_selected = False
        if item_index < len(self.inventory):
            self.item_held = item_index
            self.is_tool_selected = True
        else:
            block_index = item_index - len(self.inventory)
            block_keys = list(self.block_inventory.keys())

            if block_index < len(block_keys):
                self.item_held = block_index
                self.is_tool_selected = False
            else:
                self.item_held = 0
                self.is_tool_selected = True

    def get_selected_block(self):
        if not self.is_tool_selected:
            selected_block_index = self.item_held
            block_types = list(self.block_inventory.keys())
            if selected_block_index < len(block_types):
                return block_types[selected_block_index]
        return None

    def has_block_in_inventory(self, block_type):
        return block_type in self.block_inventory