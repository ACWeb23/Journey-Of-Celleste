import pygame
import math
import random
# =========================
# ORBITING SWORD
# =========================
class OrbitingSword(pygame.sprite.Sprite):
    def __init__(self, owner = None, image=None, dmg=10, rad=100, ang=5, col=(0, 255, 0), blades=2):
        super().__init__()

        self.owner = owner  # Require owner at construction
        self.damage = dmg
        self.radius = rad
        self.angular_speed = ang
        self.color = col
        self.num_blades = max(1, min(blades, 32))  # Clamp safely
        
        self.angle = 0
        self.level = 0
        self.experience = 0
        
        # Pre-create blade template
        if image:
            self.blade_template = image
        else:
            self.blade_template = pygame.Surface((60, 10), pygame.SRCALPHA)
            self.blade_template.fill(self.color)

        self.blade_images = []
        self.blade_rects = []

    def update(self):
        if not self.owner:
            return

        self.angle = (self.angle + self.angular_speed) % 360
        self._update_blades()

    def _update_blades(self):
        """Recalculate blade positions"""
        self.blade_images.clear()
        self.blade_rects.clear()

        center = self.owner.rect.center
        angle_step = 360 / self.num_blades

        for i in range(self.num_blades):
            blade_angle = self.angle + i * angle_step
            radians = math.radians(blade_angle)

            x = center[0] + math.cos(radians) * self.radius
            y = center[1] + math.sin(radians) * self.radius

            rotated = pygame.transform.rotate(self.blade_template, -blade_angle)
            rect = rotated.get_rect(center=(x, y))

            self.blade_images.append(rotated)
            self.blade_rects.append(rect)

    def draw(self, surface):
        for img, rect in zip(self.blade_images, self.blade_rects):
            surface.blit(img, rect)

    def check_collision(self, enemies):
        """Damage enemies that collide with blades"""
        for enemy in enemies:
            for blade_rect in self.blade_rects:
                if blade_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.damage)
    def gain_experience(self):
        """
        if self.game.level_Cleared():
            self.experience += self.owner.check_XP()/2
        """
        pass