import pygame
import random
import math

# =========================
# ENEMY BASE
# =========================
class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, x, y, player, projectile_group, health, experience_value = 1, image=None):
        super().__init__()

        if image:
            self.image = image
        else:
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))

        self.player = player
        self.projectile_group = projectile_group

        self.speed = random.uniform(1.0, 2.5)
        self.health = health
        self.experience = experience_value
        self.hit_cooldown = 0

        self.state = "wander"
        self.state_timer = random.randint(60, 180)

        self.set_new_wander_dir()

        self.shoot_cooldown = random.randint(120, 240)
        self.timer = 0

    def set_new_wander_dir(self):
        vec = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if vec.length() == 0:
            vec = pygame.Vector2(1, 0)
        self.wander_dir = vec.normalize()

    def update(self):
        self.update_state()
        self.move()
        self.shoot_logic()

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

    def update_state(self):
        self.state_timer -= 1
        if self.state_timer <= 0:
            self.state_timer = random.randint(60, 180)
            self.state = "chase" if self.state == "wander" else "wander"
            self.set_new_wander_dir()

    def move(self):
        if self.state == "chase":
            direction = pygame.Vector2(
                self.player.rect.centerx - self.rect.centerx,
                self.player.rect.centery - self.rect.centery
            )
            if direction.length() != 0:
                direction = direction.normalize()
        else:
            direction = self.wander_dir

        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

    def shoot_logic(self):
        self.timer += 1
        if self.timer >= self.shoot_cooldown:
            self.timer = 0
            self.shoot()

    def shoot(self):
        from Projectile import Projectile
        orb = Projectile(self.rect.center, self.player.rect.center)
        self.projectile_group.add(orb)

    def take_damage(self, amount):
        if self.hit_cooldown > 0:
            return

        self.health -= amount
        self.hit_cooldown = 20

        if self.health <= 0:
            self.player.get_XP(self.experience)
            self.kill()


class EnemySlime(EnemyBase):
    def __init__(self, x, y, player, projectile_group):
        super().__init__(x, y, player, projectile_group, 50)


class EnemySlimeBoss(EnemyBase):
    def __init__(self, x, y, player, projectile_group):
        super().__init__(x, y, player, projectile_group, 20)
        self.image.fill((128, 0, 255))
