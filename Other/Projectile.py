# =========================
# PROJECTILES
# =========================
import pygame
import math
import random
from Game import game_settings
WIDTH, HEIGHT, FRAME_RATE, TITLE = game_settings.return_settings()
class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, image=None):
        super().__init__()
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (6, 6), 6)
        self.rect = self.image.get_rect(center=start_pos)

        self.speed = 3

        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        dist = math.hypot(dx, dy)

        if dist != 0:
            dx /= dist
            dy /= dist

        self.velocity = (dx * self.speed, dy * self.speed)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if (
            self.rect.right < 0 or
            self.rect.left > WIDTH or
            self.rect.bottom < 0 or
            self.rect.top > HEIGHT
        ):
            self.kill()
# =========================
# PROJECTILE Arrow
# =========================

class ProjectileArrow(Projectile):
    def __init__(self, start_pos, target_pos, image=None):
        super().__init__(start_pos, target_pos)
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((20, 5), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 255, 0), (0, 0, 20, 5))
        self.rect = self.image.get_rect(center=start_pos)

        # Recalculate velocity for arrow speed
        self.speed = 5
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        dist = math.hypot(dx, dy)

        if dist != 0:
            dx /= dist
            dy /= dist

        self.velocity = (dx * self.speed, dy * self.speed)
