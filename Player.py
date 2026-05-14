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

        self.level = 0
        self.speed = 5
        self.health = 100
        self.experience = 0
        self.atk = 10
        self.defense = 10
        self.atkSpeed = 1 # Base attack speed multiplier
        self.critChance = 0.05 # Base critical hit chance (5%)
        self.critDamage = 0.5 # Base critical damage multiplier (50%) This is addtive damage.
        self.lifeSteal = 0
        self.damage = 0 # This is addtive damage that is added to the player's final damage after atk and crit are calculated.
        self.defensePercent = 0 # This is a flat percentage that damage is reduced before defense is calcutatec.
        self.equipment = []
        self.inventory = {}
        self.buffs = {
            "Speed": 0,
            "Health": 0,
            "Experience": 0,
            "ATK": 0,
            "DEF": 0,
            "ATKspd": 0,
            "Crit Chance": 0,
            "Crit Damage": 0,
            "Lifesteal": 0,
            "Damage": 0,
            "Defense%": 0
        }
        self.cards = []
    
    def apply_static_buffs(self):
        #############################################
        # Description:
        # Applies static buffs to the player's
        #############################################
        for buff, value in self.buffs.items():
            if buff == "Speed":
                self.speed *= value # Speed buffs are multiplicative.
            elif buff == "Health":
                self.health *= value # Health buffs are multiplicative.
            elif buff == "Experience":
                self.experience *= value
            elif buff == "ATK":
                self.atk += value
            elif buff == "DEF":
                self.defense += value
            elif buff == "ATKspd":
                self.atkSpeed *= value
            elif buff == "Crit Chance":
                self.critChance += value
            elif buff == "Crit Damage":
                self.critDamage += value
            elif buff == "Lifesteal":
                self.lifeSteal += value
            elif buff == "Damage":
                self.damage += value
            elif buff == "Defense%":
                self.defensePercent += value

    def move(self, dx, dy):
        #############################################
        # Parameters:
        # dx: Change in x-direction (float)
        # dy: Change in y-direction (float)
        # Description:
        # Moves the player by updating its position based on the provided directional inputs (dx, dy) and the player's speed.
        # The method first calculates the velocity vector from the directional inputs, normalizes it to maintain consistent movement speed in all directions, and then updates the player's position accordingly.
        #############################################
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def move_logic(self):
        #############################################
        # Description:
        # Handles the player's movement logic based on keyboard input.
        # The method checks for pressed keys and updates the player's velocity accordingly.
        # It then calls the move method to update the player's position.
        #############################################
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
        ###########################################
        # Parameters:
        # amount: The amount to change the player's health by (int)
        # Description:
        # Modifies the player's health by a specified amount, ensuring that it remains within the bounds of 0 and 100. This method can be used to apply damage or healing to the player.
        ###########################################
        self.health = max(0, min(100, self.health + amount))

    def equip(self, item):
        ###########################################
        # Parameters:
        # item: The item to equip (Item)
        # Description:
        # Equips the specified item, adding it to the player's equipment and setting the item's owner to the player.
        ###########################################
        self.equipment.append(item)
        item.owner = self
    
    def get_XP(self, amount):
        ###########################################
        # Parameters:
        # amount: The amount of experience points to add (int)
        # Description:
        # Increases the player's experience points by the specified amount.
        ###########################################
        self.experience += amount
    
    def check_XP(self):
        ###########################################
        # Description:
        # Returns the player's current experience points.
        ###########################################
        return self.experience
        # =========================
        # Player Inventory
        # =========================
    def add_to_inventory(self, item_name, quantity=1):
        ###########################################
        # Parameters:
        # item_name: The name of the item to add (str)
        # quantity: The quantity of the item to add (int, default=1)
        # Description:
        # Adds a specified quantity of an item to the player's inventory. If the item already exists in the inventory, it increments the quantity; otherwise, it adds the item with the specified quantity.
        ###########################################
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity

    def remove_from_inventory(self, item_name, quantity=1):
        ###########################################
        # Parameters:
        # item_name: The name of the item to remove (str)
        # quantity: The quantity of the item to remove (int, default=1)
        # Description:
        # Removes a specified quantity of an item from the player's inventory. If the quantity reaches zero or below, the item is removed entirely.
        ###########################################
        if item_name in self.inventory:
            self.inventory[item_name] -= quantity
            if self.inventory[item_name] <= 0:
                del self.inventory[item_name]
    def draw_inventory(self, Item):
        ###########################################
        # Parameters:
        # Item: The item to draw (Item)
        # Description:
        # Draws the player's inventory on the screen.
        ###########################################
        x, y = 10, HEIGHT - 50
        for item_name, quantity in self.inventory.items():
            text = f"{item_name} x{quantity}"
            font = pygame.font.Font(None, 24)
            img = font.render(text, True, (255, 255, 255))
            self.screen.blit(img, (x, y))
            y -= 30
    def use_item(self, item_name):
        ###########################################
        # Parameters:
        # item_name: The name of the item to use (str)
        # Description:
        # Uses the specified item from the player's inventory.
        ###########################################
        if item_name in self.inventory and self.inventory[item_name] > 0:
            # Example: Using a health potion
            self.remove_from_inventory(item_name)
        else:
            print(f"No {item_name} left in inventory!")

class Item(pygame.sprite.Sprite):
    ###########################################
    # This class represents an item that can be equipped or used by the player. It inherits from pygame.sprite.Sprite, allowing it to be treated as a sprite in the game.
    # The Item class has a name and an optional image. If no image is provided, it creates a default surface filled with yellow color. The class also includes methods for equipping the item to a player and using the item, which can be overridden by specific item types to implement unique behaviors.
    ###########################################
    def __init__(self, name, image=None):
        super().__init__()
        self.name = name

        if image:
            self.image = image
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()

class Card(Item):
    ###########################################
    # This class represents a card that is equipped by the player at the end of a round. 
    # By equipping a card, the player can gain various benefits or effects that enhance their abilities or provide strategic advantages in the game.
    ###########################################
    def __init__(self, name, image=None):
        super().__init__(name, image)
        if not image:
            self.image.fill((0, 0, 255))

    def use(self, player):
        ###########################################
        # Parameters:
        # player: The player using the card (Player)
        # Description:
        # Defines the effect of using the card. This method can be overridden to implement specific behaviors when the card is used by the player.
        ###########################################
        pass