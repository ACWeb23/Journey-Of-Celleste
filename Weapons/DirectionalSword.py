import pygame
import math
import random
# =========================
# DIRECTIONAL SWORD
# =========================
class SwordDirectional(pygame.sprite.Sprite):
    def __init__(self, image=None, owner=None):
        super().__init__()
        if image:
            self.original_image = image
        else:
            self.original_image = pygame.Surface((60, 10), pygame.SRCALPHA)
            self.original_image.fill((255, 0, 0))
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.owner = None
        self.damage = 15
        self.range = 60

        self.angle = 0
        self.swinging = False
        self.swing_speed = 10
        self.max_swing_angle = 120
        self.current_swing = 0

    def start_attack(self):
        if not self.swinging:
            self.swinging = True
            self.current_swing = -self.max_swing_angle // 2

    def update(self):
        if not self.owner:
            return

        center = self.owner.rect.center

        # Base angle from player movement
        base_angle = 0
        if self.owner.velocity.length() != 0:
            base_angle = math.degrees(
                math.atan2(-self.owner.velocity.y, self.owner.velocity.x)
            )

        # Apply swing offset
        if self.swinging:
            self.current_swing += self.swing_speed
            if self.current_swing >= self.max_swing_angle // 2:
                self.swinging = False
            swing_offset = self.current_swing
        else:
            swing_offset = 0

        self.angle = base_angle + swing_offset

        radians = math.radians(self.angle)
        offset_x = math.cos(radians) * self.range
        offset_y = -math.sin(radians) * self.range

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(
            center=(center[0] + offset_x, center[1] + offset_y)
    )
    
    def check_collision(self, enemies):
        """Damage enemies that collide with the sword"""
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(self.damage)