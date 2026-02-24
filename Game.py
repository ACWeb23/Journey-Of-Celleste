import random
import pygame
import math

WIDTH, HEIGHT = 1920, 1080
FRAME_RATE = 60
TITLE = "I Can"


# =========================
# PLAYER
# =========================
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 5
        self.health = 100
        self.equipment = []

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


# =========================
# ORBITING SWORD
# =========================
class Sword(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.original_image = pygame.Surface((60, 10), pygame.SRCALPHA)
        self.original_image.fill((0, 255, 0))
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.owner = None
        self.damage = 10
        self.radius = 100
        self.angle = 0
        self.angular_speed = 5

    def update(self):
        if not self.owner:
            return

        self.angle = (self.angle + self.angular_speed) % 360
        radians = math.radians(self.angle)

        center = self.owner.rect.center
        x = center[0] + math.cos(radians) * self.radius
        y = center[1] + math.sin(radians) * self.radius

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(x, y))


# =========================
# DIRECTIONAL SWORD
# =========================
class SwordDirectional(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

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


# =========================
# PROJECTILE
# =========================
class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()

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
# ENEMY BASE
# =========================
class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, x, y, player, projectile_group, health):
        super().__init__()

        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))

        self.player = player
        self.projectile_group = projectile_group

        self.speed = random.uniform(1.0, 2.5)
        self.health = health
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
        orb = Projectile(self.rect.center, self.player.rect.center)
        self.projectile_group.add(orb)

    def take_damage(self, amount):
        if self.hit_cooldown > 0:
            return

        self.health -= amount
        self.hit_cooldown = 20

        if self.health <= 0:
            self.kill()


class EnemySlime(EnemyBase):
    def __init__(self, x, y, player, projectile_group):
        super().__init__(x, y, player, projectile_group, 50)


class EnemySlimeBoss(EnemyBase):
    def __init__(self, x, y, player, projectile_group):
        super().__init__(x, y, player, projectile_group, 250)
        self.image.fill((128, 0, 255))


# =========================
# GAME
# =========================
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.velocity = pygame.Vector2(1, 0)  # default facing right

        self.player = Player(WIDTH // 2, HEIGHT // 2)

        self.sword = Sword()
        self.weap2 = SwordDirectional()

        self.player.equip(self.sword)
        self.player.equip(self.weap2)

        self.enemies = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        for _ in range(5):
            self.spawn_enemy()

        self.spawn_boss()

        self.font = pygame.font.Font(None, 36)

    def spawn_enemy(self):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        self.enemies.add(EnemySlime(x, y, self.player, self.projectiles))

    def spawn_boss(self):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        self.bosses.add(EnemySlimeBoss(x, y, self.player, self.projectiles))

    def run(self):
        while self.running:
            self.clock.tick(FRAME_RATE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.player.move_logic()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.weap2.start_attack()

            self.sword.update()
            self.weap2.update()
            self.enemies.update()
            self.bosses.update()
            self.projectiles.update()

            if pygame.sprite.spritecollide(self.player, self.projectiles, True):
                self.player.change_health(-10)

            # Weapon damage loop
            for weapon in [self.sword, self.weap2]:
                if weapon == self.weap2 and not self.weap2.swinging:
                    continue

                for group in [self.enemies, self.bosses]:
                    hits = pygame.sprite.spritecollide(weapon, group, False)
                    for enemy in hits:
                        enemy.take_damage(weapon.damage)

            # DRAW
            self.screen.fill((0, 0, 0))

            self.screen.blit(self.player.image, self.player.rect)
            self.screen.blit(self.sword.image, self.sword.rect)
            self.screen.blit(self.weap2.image, self.weap2.rect)

            self.enemies.draw(self.screen)
            self.bosses.draw(self.screen)
            self.projectiles.draw(self.screen)

            text = self.font.render(
                f"Health: {self.player.health}  Enemies: {len(self.enemies)}  Bosses: {len(self.bosses)}",
                True, (255, 255, 255)
            )
            self.screen.blit(text, (1400, 1000))

            if self.player.health <= 0:
                self.screen.blit(self.font.render("Game Over", True, (255, 0, 0)),
                                 (WIDTH // 2 - 60, HEIGHT // 2))

            elif len(self.enemies) == 0 and len(self.bosses) == 0:
                self.screen.blit(self.font.render("You Win!", True, (0, 255, 0)),
                                 (WIDTH // 2 - 60, HEIGHT // 2))

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Game().run()