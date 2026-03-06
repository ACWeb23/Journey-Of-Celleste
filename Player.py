import pygame
import random
import math
# =========================
# PLAYER
# =========================
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None):
        super().__init__()
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 5
        self.health = 100
        self.experience = 0
        self.equipment = []
        self.inventory = {}

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def move_logic(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_d]:
            dx = 1

        self.velocity = pygame.Vector2(dx, dy)

        if self.velocity.length() != 0:
            self.velocity = self.velocity.normalize()

        self.move(self.velocity.x, self.velocity.y)

    def change_health(self, amount):
        self.health = max(0, min(100, self.health + amount))

    def equip(self, item):
        self.equipment.append(item)
        item.owner = self
    
    def get_XP(self, amount):
        self.experience += amount
    
    def check_XP(self):
        return self.experience
        # =========================
        # Player Inventory
        # =========================
    def add_to_inventory(self, item_name, quantity=1):
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity

    def remove_from_inventory(self, item_name, quantity=1):
        if item_name in self.inventory:
            self.inventory[item_name] -= quantity
            if self.inventory[item_name] <= 0:
                del self.inventory[item_name]
    def draw_inventory(self, Item):
        x, y = 10, HEIGHT - 50
        for item_name, quantity in self.inventory.items():
            text = f"{item_name} x{quantity}"
            font = pygame.font.Font(None, 24)
            img = font.render(text, True, (255, 255, 255))
            self.screen.blit(img, (x, y))
            y -= 30
    def use_item(self, item_name):
        if item_name in self.inventory and self.inventory[item_name] > 0:
            # Example: Using a health potion
            self.remove_from_inventory(item_name)
        else:
            print(f"No {item_name} left in inventory!")

class Item(pygame.sprite.Sprite):
    def __init__(self, name, image=None):
        super().__init__()
        self.name = name

        if image:
            self.image = image
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()