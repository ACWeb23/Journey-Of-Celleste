import random
import pygame
import math

class GameSettings:
    def __init__(self):
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.FRAME_RATE = 60
        self.TITLE = "Journey of Celleste"
    def return_settings(self):
        return self.WIDTH, self.HEIGHT, self.FRAME_RATE, self.TITLE

game_settings = GameSettings()
WIDTH, HEIGHT, FRAME_RATE, TITLE = game_settings.return_settings()

from Player import Player
from Weapons.OrbitingSword import OrbitingSword as Sword
from Weapons.DirectionalSword import SwordDirectional
from Enemys.Enemys import EnemySlime, EnemySlimeBoss

class Round:
    def __init__(self, Round_Number, Round_Type, Round_ID, Difficulty) -> None:
        self.Round_Number = Round_Number
        self.Round_Type = Round_Type
        self.Round_ID = Round_ID
        self.Difficulty = Difficulty
        self.round_level = 0
        
    def Set_Round_Level(self, Round_Number: int = 0, Round_Type: str = "Normal", Difficulty: str = "Easy") -> int:
        ###########################################
        # Parameters:
        # Round_Number: The number of the round (int, default=0)
        # Round_Type: The type of the round (str, default="Normal")
        # Difficulty: The difficulty of the round (str, default="Easy")
        # Description:
        # This functiuon sets the round level based on the number of rounds and the type of round. 
        # The round level is calculated by applying a floor function to a difficulty mulitplier that increases with the number of rounds, 
        # and then multiplying that by a round type multiplier that increases based on the type of round (Normal, Boss, Elite).
        ###########################################
        Round_Difficulty = {"Easy": 0.33, "Medium": 0.66, "Hard": 1.25}
        Round_Type_Multiplier = {"Normal": 1, "Boss": 1.5, "Elite": 2}
        self.round_level =  (math.floor(1 + (Round_Number * Round_Difficulty[Difficulty]))) * Round_Type_Multiplier[Round_Type]
        self.round_level = int(self.round_level)
        return self.round_level
    
    def fetch_enemy_list(self, Round_ID: int = 0) -> list:
        ###########################################
        # Description:
        # This function calls a database to fetch a list of enemies based on the round ID. 
        # The round ID is used to determine which enemies should be included in the round and their spawn times, allowing for a dynamic and varied gameplay experience as the player progresses through different rounds.
        ###########################################
        enemy_list = []
        return enemy_list


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
        self.message_queue = []

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
    
    def Load_message(self, text, type="info", duration=5):
        if type == "info":
            color = (255, 255, 255)
            position = (WIDTH // 2, HEIGHT // 4)
        elif type == "warning":
            color = (255, 255, 0)
            position = (WIDTH // 2, HEIGHT // 4 + 40)
        elif type == "error":
            color = (255, 0, 0)
            position = (WIDTH // 2, HEIGHT // 4 + 80)
        self.message_queue.append([text, color, position, duration])
    
    def draw_messages(self):
        message = self.message_queue[0] if self.message_queue else None
        if message:
            text, color, position, duration = message
            img = self.font.render(text, True, color)
            self.screen.blit(img, (position[0] - img.get_width() // 2, position[1]))
            message[3] -= 1
            if message[3] <= 0:
                self.message_queue.pop(0)

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
            self.sword.check_collision(self.enemies)
            self.weap2.check_collision(self.enemies)
            self.sword.check_collision(self.bosses)
            self.weap2.check_collision(self.bosses)

            # DRAW
            self.screen.fill((0, 0, 0))

            self.screen.blit(self.player.image, self.player.rect)
            self.sword.draw(self.screen)
            self.screen.blit(self.weap2.image, self.weap2.rect)

            self.enemies.draw(self.screen)
            self.bosses.draw(self.screen)
            self.projectiles.draw(self.screen)

            text = self.font.render(
                f"Health: {self.player.health}  Enemies: {len(self.enemies)}  Bosses: {len(self.bosses)}    XP: {self.player.experience}",
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