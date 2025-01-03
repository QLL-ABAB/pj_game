import pygame
from pygame.locals import *
import copy
import time

from Collections import *
from Settings import *


pygame.init()


font1 = pygame.font.Font(Game_Path.word_path, TextSettings.font_size)
font2 = pygame.font.Font(Game_Path.word_path, TextSettings.font_size_plus)
box_rect = pygame.Rect(
    0,
    WindowSettings.height - TextSettings.box_height,
    WindowSettings.width,
    TextSettings.box_height,
)
box_surface = pygame.Surface(box_rect.size)
box_surface.fill(TextSettings.box_color)


class Scene_Fight(Listener):
    def __init__(self, player, type):
        super().__init__()
        self.attribute_size = SceneSettings.attribute_size
        self.player_real = player
        self.enemy_attack = [2, 1]
        self.enemy_hp = [13, 8]
        self.coin_add = [5, 2]
        self.enemy_pos = (1000, 600)
        self.player_pos = (200, 600)

        self.player_right = True
        self.enemy_left = True
        self.player_act = True
        self.enemy_act = False

        self.animation_num = 0
        self.animation_speed = 1

        self.player_hp_showings = []
        self.enemy_hp_showings = []

        for i in range(20):
            self.player_hp_showings.append(
                Attribute_showing(
                    0,
                    pygame.Rect(
                        i * 25 + 10, 30, self.attribute_size, self.attribute_size
                    ),
                )
            )

        for i in range(14):
            self.enemy_hp_showings.append(
                Attribute_showing(
                    11,
                    pygame.Rect(
                        1340 - i * 25,
                        30,
                        self.attribute_size,
                        self.attribute_size,
                    ),
                )
            )

        self.background = pygame.transform.scale(
            pygame.image.load(Game_Path.background_path[4]),
            (
                WindowSettings.width,
                WindowSettings.height,
            ),
        )
        self.attribute_size = SceneSettings.attribute_size

        self.player = Fixed_object(
            pygame.transform.scale(
                pygame.image.load(Game_Path.player_run_path1[0]), (200, 200)
            ),
            pygame.Rect(200, 600, 200, 200),
        )

        self.enemy1 = Fixed_object(
            pygame.transform.scale(
                pygame.image.load(Game_Path.enemy_path[3]), (200, 200)
            ),
            pygame.Rect(1000, 600, 200, 200),
        )

        self.enemy2 = Fixed_object(
            pygame.transform.scale(
                pygame.image.load(Game_Path.enemy_path[2]), (200, 200)
            ),
            pygame.Rect(1000, 600, 200, 200),
        )

        self.type = type

    def listen(self, event: Event):
        super().listen(event)
        if (self.player_right == False and self.player_act == True) or (
            self.enemy_left == False and self.enemy_act == True
        ):
            self.animation_num += 2

        else:
            self.animation_num += 1

        if event.code == Event_Code.DRAW:

            if self.player_real.hp <= 0:
                self.post(Event(Scene_Code.GAME_OVER))

                self.enemy_hp = [13, 8]

            if self.enemy_hp[self.type - 1] <= 0:
                self.player_real.coin += self.coin_add[self.type - 1]
                self.post(Event(Scene_Code.FOREST))
                self.player_real.speed = PlayerSettings.player_Speed
                self.enemy_hp = [13, 8]
                # self.post(Event(Event_Code.WHETHER_TO_FIGHT_FALSE))

            window.blit(self.background, (0, 0))

            for i in range(self.player_real.hp):
                hp = self.player_hp_showings[i]
                window.blit(hp.image, hp.rect)

            for i in range(self.enemy_hp[self.type - 1]):
                hp = self.enemy_hp_showings[i]
                window.blit(hp.image, hp.rect)

            if self.player_right and self.player_act:
                self.player.rect = (
                    self.player_pos[0]
                    + (self.enemy_pos[0] - 100 - self.player_pos[0])
                    * self.animation_num
                    / 400,
                    self.player_pos[1]
                    + (self.enemy_pos[1] - self.player_pos[1])
                    * self.animation_num
                    / 400,
                    200,
                    200,
                )

            if (not self.player_right) and self.player_act:
                self.player.rect = (
                    self.enemy_pos[0]
                    - 100
                    - (self.enemy_pos[0] - 100 - self.player_pos[0])
                    * self.animation_num
                    / 400,
                    self.enemy_pos[1]
                    - (self.enemy_pos[1] - self.player_pos[1])
                    * self.animation_num
                    / 400,
                    200,
                    200,
                )

            if self.type == 1:
                if self.enemy_act:
                    if self.enemy_left:
                        self.enemy1.rect = (
                            self.enemy_pos[0]
                            - (self.enemy_pos[0] - 100 - self.player_pos[0])
                            * self.animation_num
                            / 400,
                            self.enemy_pos[1]
                            - (self.enemy_pos[1] - self.player_pos[1])
                            * self.animation_num
                            / 400,
                            200,
                            200,
                        )

                    if not self.enemy_left:
                        self.enemy1.rect = (
                            self.player_pos[0]
                            + 100
                            + (self.enemy_pos[0] - 100 - self.player_pos[0])
                            * self.animation_num
                            / 400,
                            self.enemy_pos[1]
                            - (self.enemy_pos[1] - self.player_pos[1])
                            * self.animation_num
                            / 400,
                            200,
                            200,
                        )

                self.enemy1.draw()

            if self.type == 2:

                if self.enemy_act:
                    if self.enemy_left:
                        self.enemy2.rect = (
                            self.enemy_pos[0]
                            - (self.enemy_pos[0] - 100 - self.player_pos[0])
                            * self.animation_num
                            / 400,
                            self.enemy_pos[1]
                            - (self.enemy_pos[1] - self.player_pos[1])
                            * self.animation_num
                            / 400,
                            200,
                            200,
                        )

                    if not self.enemy_left:
                        self.enemy2.rect = (
                            self.player_pos[0]
                            + 100
                            + (self.enemy_pos[0] - 100 - self.player_pos[0])
                            * self.animation_num
                            / 400,
                            self.player_pos[1]
                            + (self.enemy_pos[1] - self.player_pos[1])
                            * self.animation_num
                            / 400,
                            200,
                            200,
                        )

                self.enemy2.draw()

            self.player.draw()

        if self.animation_num >= 400:
            self.animation_num = 0
            if self.player_act:
                if self.player_right:

                    self.player_right = False
                    self.enemy_hp[self.type - 1] -= self.player_real.attack

                elif not self.player_right:
                    self.player_act = False
                    self.enemy_act = True
                    self.player_right = True

            elif self.enemy_act:
                if self.enemy_left:
                    self.enemy_left = False
                    self.player_real.hp -= self.enemy_attack[self.type - 1]

                elif not self.enemy_left:
                    self.enemy_act = False
                    self.player_act = True
                    self.enemy_left = True

            time.sleep(1)