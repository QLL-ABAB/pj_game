import copy
import pygame
import random

from Collections import *
from Settings import *
from Wild_scene_entityLike import *
from Portals import *
from City_scene_entityLike import *
from Add_windows import *

pygame.init()


class Scene_Forest(Listener):  # 场景类
    def __init__(self, player):
        super().__init__()
        self.trees = []
        self.tiles = []
        self.fires = []
        self.hp_showings = []
        self.burn_showings = []
        self.enemy2s = []
        self.enemy1s = []
        self.player = player
        self.window_scale = (
            WindowSettings.width,
            WindowSettings.height,
        )
        self.map_range = SceneSettings.map_size  # 实际地图的大小
        self.carema = SceneSettings.camara_0  # 镜头的初始位置
        self.update_camera()  # 更新镜头的位置
        self.attribute_size = SceneSettings.attribute_size  # 属性显示的大小
        self.b_attribute_size = (
            SceneSettings.burn_attribute_size[0],
            SceneSettings.burn_attribute_size[1],
        )  # 火焰显示的大小

        self.portal1 = Portals(SceneSettings.portal_speed, 0)
        self.portal3 = Portals(SceneSettings.portal_speed, 1)

        self.coin = 0
        self.coin_image = pygame.transform.scale(
            pygame.image.load(Game_Path.coin_path),
            (self.attribute_size * 2, self.attribute_size * 2),
        )

        self.attack_showing = Attribute_showing(
            10, pygame.Rect(10, 100, self.attribute_size * 2, self.attribute_size * 2)
        )

        self.blood_eat = Attribute_showing(
            6, pygame.Rect(10, 140, self.attribute_size * 2, self.attribute_size * 2)
        )
        self.skill = Attribute_showing(
            14, pygame.Rect(10, 140, self.attribute_size * 2, self.attribute_size * 2)
        )
        self.through = Attribute_showing(
            12, pygame.Rect(10, 140, self.attribute_size * 2, self.attribute_size * 2)
        )
        self.add_bullet_speed = Attribute_showing(
            13, pygame.Rect(10, 140, self.attribute_size * 2, self.attribute_size * 2)
        )
        self.skills = []
        self.first_add1 = True
        self.first_add2 = True
        self.first_add3 = True
        self.first_add4 = True

        self.rect_proof = pygame.Surface((100, 100))
        self.rect_proof.fill((255, 255, 255))
        self.rect_proof.set_alpha(
            200
        )  # 电风扇发的范德萨发顺丰方法说法fnjsfkfjmkfslfflfsfsldfsdk
        self.rect_proof_rect = self.rect_proof.get_rect()
        self.rect_proof_rect.center = (
            self.player.rect.centerx,
            self.player.rect.centery,
        )

        """
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        """
        self.whether_fight = False
        self.judege_window = False
        self.judege_window_image = pygame.Surface((1000, 500))
        self.judege_window_image.fill((20, 20, 20))
        # self.judege_window_image.set_alpha(220)
        self.judege_window_rect = self.judege_window_image.get_rect()
        self.judege_window_rect.center = (
            WindowSettings.width // 2,
            WindowSettings.height // 2,
        )

        self.button_image1 = pygame.Surface((250, 125))
        self.button_image1.fill((50, 50, 50))
        self.button_rect1 = self.button_image1.get_rect()
        self.button_rect1.center = (350, 600)

        self.button_image1_clicked = pygame.Surface((250, 125))
        self.button_image1_clicked.fill((100, 100, 100))

        self.button_image2 = pygame.Surface((250, 125))
        self.button_image2.fill((50, 50, 50))
        self.button_rect2 = self.button_image2.get_rect()
        self.button_rect2.center = (1050, 600)

        self.button_image2_clicked = pygame.Surface((250, 125))
        self.button_image2_clicked.fill((100, 100, 100))

        self.text1 = font1.render(
            "Wanna Fight? Press Fight!!!!!", True, (255, 255, 255)
        )
        self.text2 = font1.render("Escape? Coward!（╬￣皿￣）", True, (255, 255, 255))
        self.text3 = font1.render(
            "Say Goodbye to your money and get beaten up !", True, (255, 255, 255)
        )

        self.text1_rect = self.text1.get_rect()
        self.text2_rect = self.text2.get_rect()
        self.text3_rect = self.text3.get_rect()
        self.text1_rect.center = (WindowSettings.width // 2, 300)
        self.text2_rect.center = (WindowSettings.width // 2, 400)
        self.text3_rect.center = (WindowSettings.width // 2, 500)

        self.button_text1 = font1.render("Fight", True, (255, 255, 255))
        self.button_text2 = font1.render("Escape", True, (255, 255, 255))
        self.button_text1_rect = self.button_text1.get_rect()
        self.button_text2_rect = self.button_text2.get_rect()
        self.button_text1_rect.center = (350, 600)
        self.button_text2_rect.center = (1050, 600)

        """
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        """

        # 根据地图的尺寸每行每列逐个生成地图方块
        for i in range(self.map_range[0] // 40 + 1):
            for j in range(self.map_range[1] // 40 + 1):
                self.tiles.append(
                    Forest_Tile(
                        random.randint(0, 5), pygame.Rect(i * 40, j * 40, 40, 40)
                    )
                )

        # 在地图里随机生成一些障碍物
        for _ in range(20):
            tree = Tree(
                pygame.Rect(
                    random.randint(0, self.map_range[0]),
                    random.randint(0, self.map_range[1]),
                    40,
                    40,
                )
            )
            if (
                not tree.rect.colliderect(self.rect_proof_rect)
                and not tree.rect.colliderect(self.portal1.rect)
                and not tree.rect.colliderect(self.portal3.rect)
            ):
                self.trees.append(tree)

        for _ in range(10):
            fire = Fire(
                pygame.Rect(
                    random.randint(0, self.map_range[0]),
                    random.randint(0, self.map_range[1]),
                    40,
                    40,
                ),
                self.player,
            )

            collide_with_tree = False
            for tree in self.trees:
                if fire.rect.colliderect(tree.rect):
                    collide_with_tree = True

            if (
                not fire.rect.colliderect(self.rect_proof_rect)
                and not fire.rect.colliderect(self.portal1.rect)
                and not fire.rect.colliderect(self.portal3.rect)
                and not collide_with_tree
            ):
                self.fires.append(fire)

        """
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        """
        self.enemy1_num = EnemySettings.enemy1_num
        self.enemy2_num = EnemySettings.enemy2_num

        for _ in range(self.enemy2_num):
            enemy2 = Enemy(
                1,
                pygame.Rect(
                    random.randint(
                        0, self.map_range[0] - EnemySettings.enemy_width[1] * 2
                    ),
                    random.randint(
                        0, self.map_range[1] - EnemySettings.enemy_height[1] * 2
                    ),
                    EnemySettings.enemy_width[1],
                    EnemySettings.enemy_height[1],
                ),
            )

            collide_with_obstacles = False
            for tree in self.trees:
                if enemy2.rect.colliderect(tree.rect):
                    collide_with_obstacles = True

            for fire in self.fires:
                if enemy2.rect.colliderect(fire.rect):
                    collide_with_obstacles = True

            collide_with_enemy2 = False
            for e2 in self.enemy2s:
                if enemy2.rect.colliderect(e2.rect):
                    collide_with_enemy2 = True

            if (
                not enemy2.rect.colliderect(self.rect_proof_rect)
                and not enemy2.rect.colliderect(self.portal1.rect)
                and not enemy2.rect.colliderect(self.portal3.rect)
                and not collide_with_obstacles
                and not collide_with_enemy2
            ):
                self.enemy2s.append(enemy2)

        while len(self.enemy2s) < 2:
            enemy2 = Enemy(
                1,
                pygame.Rect(
                    random.randint(
                        0, self.map_range[0] - EnemySettings.enemy_width[1] * 2
                    ),
                    random.randint(
                        0, self.map_range[1] - EnemySettings.enemy_height[1] * 2
                    ),
                    EnemySettings.enemy_width[1],
                    EnemySettings.enemy_height[1],
                ),
            )

            collide_with_obstacles = False
            for tree in self.trees:
                if enemy2.rect.colliderect(tree.rect):
                    collide_with_obstacles = True

            for fire in self.fires:
                if enemy2.rect.colliderect(fire.rect):
                    collide_with_obstacles = True

            collide_with_enemy2 = False
            for e2 in self.enemy2s:
                if enemy2.rect.colliderect(e2.rect):
                    collide_with_enemy2 = True

            if (
                not enemy2.rect.colliderect(self.rect_proof_rect)
                and not enemy2.rect.colliderect(self.portal1.rect)
                and not enemy2.rect.colliderect(self.portal3.rect)
                and not collide_with_obstacles
                and not collide_with_enemy2
            ):
                self.enemy2s.append(enemy2)

        for _ in range(self.enemy1_num):
            enemy1 = Enemy(
                0,
                pygame.Rect(
                    random.randint(
                        0, self.map_range[0] - EnemySettings.enemy_width[0] * 2
                    ),
                    random.randint(
                        0, self.map_range[1] - EnemySettings.enemy_height[0] * 2
                    ),
                    EnemySettings.enemy_width[0],
                    EnemySettings.enemy_height[0],
                ),
            )

            collide_with_obstacles = False
            for tree in self.trees:
                if enemy1.rect.colliderect(tree.rect):
                    collide_with_obstacles = True

            for fire in self.fires:
                if enemy1.rect.colliderect(fire.rect):
                    collide_with_obstacles = True

            for e2 in self.enemy2s:
                if enemy1.rect.colliderect(e2.rect):
                    collide_with_obstacles = True

            collide_with_enemy1 = False
            for e1 in self.enemy1s:
                if enemy1.rect.colliderect(e1.rect):
                    collide_with_enemy1 = True

            if (
                not enemy1.rect.colliderect(self.rect_proof_rect)
                and not enemy1.rect.colliderect(self.portal1.rect)
                and not collide_with_obstacles
                and not collide_with_enemy1
            ):
                self.enemy1s.append(enemy1)

        while len(self.enemy1s) < 2:
            enemy1 = Enemy(
                1,
                pygame.Rect(
                    random.randint(
                        0, self.map_range[0] - EnemySettings.enemy_width[1] * 2
                    ),
                    random.randint(
                        0, self.map_range[1] - EnemySettings.enemy_height[1] * 2
                    ),
                    EnemySettings.enemy_width[1],
                    EnemySettings.enemy_height[1],
                ),
            )

            collide_with_obstacles = False
            for tree in self.trees:
                if enemy1.rect.colliderect(tree.rect):
                    collide_with_obstacles = True

            for fire in self.fires:
                if enemy1.rect.colliderect(fire.rect):
                    collide_with_obstacles = True

            collide_with_enemy1 = False
            for e1 in self.enemy1s:
                if enemy1.rect.colliderect(e1.rect):
                    collide_with_enemy1 = True

            if (
                not enemy1.rect.colliderect(self.rect_proof_rect)
                and not enemy1.rect.colliderect(self.portal1.rect)
                and not collide_with_obstacles
                and not collide_with_enemy1
            ):
                self.enemy1s.append(enemy1)

        """
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        """

        for i in range(20):
            hp = Attribute_showing(
                0,
                pygame.Rect(i * 25 + 10, 30, self.attribute_size, self.attribute_size),
            )
            self.hp_showings.append(hp)

        for i in range(31):
            burn = Attribute_showing(
                2,
                pygame.Rect(
                    i * 5 + 10, 10, self.b_attribute_size[0], self.b_attribute_size[1]
                ),
            )
            self.burn_showings.append(burn)

        """
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        """

    def update_camera(self):
        player_center_cord = self.player.rect.center
        self.camera = Compute_tuple.tuple_sub(
            player_center_cord, Compute_tuple.tuple_mul(self.window_scale, 0.5)
        )

        left_top = (0, 0)

        right_down = Compute_tuple.tuple_sub(self.map_range, self.window_scale)
        self.camera = Compute_tuple.tuple_min(right_down, self.camera)
        self.camera = Compute_tuple.tuple_max(left_top, self.camera)

    def listen(self, event: Event):  # 场景所监听的事件
        super().listen(event)

        keys = pygame.key.get_pressed()

        # if event.code == Event_Code.WHETHER_TO_FIGHT_FALSE:  # 监听玩家按下键盘事件
        #     self.whether_fight = False

        if event.code == Event_Code.REQUEST_MOVE:  # 监听玩家的移动请求事件
            can_move = 1
            target_rect = pygame.Rect(
                event.body["POS"][0],
                event.body["POS"][1],
                self.player.width,
                self.player.height,
            )
            for tree in self.trees:
                if tree.rect.colliderect(target_rect):
                    can_move = 0
                    break

            if can_move:
                self.post(Event(Event_Code.CAN_MOVE, event.body))

        """
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        """
        if event.code == Event_Code.CHECK_PORTAL1:
            if self.portal1.rect.colliderect(self.player.rect) and keys[pygame.K_e]:
                self.post(Event(Scene_Code.CITY))

            if self.portal3.rect.colliderect(self.player.rect) and keys[pygame.K_e]:
                self.post(Event(Scene_Code.BOSS))

        """
        》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
        """

        if event.code == Event_Code.CHECK_FIRE:
            if self.player.burn > 0:
                self.player.burn -= 1
            for fire in self.fires:
                if fire.rect.colliderect(self.player.rect):
                    self.post(Event(Event_Code.BURN))

        if event.code == Event_Code.STEP:  # STEP是每次游戏周期刷新时会被触发的事件
            self.update_camera()  # 更新镜头的位置

        if event.code == Event_Code.DRAW:  # DRAW事件，用于描绘场景中的实体

            for tile in self.tiles:  # 遍历所有地图背景图块并描绘
                tile.draw(self.camera)

            # window.blit(self.rect_proof, self.rect_proof_rect)

            for tree in self.trees:  # 遍历所有障碍物并描绘
                tree.draw(self.camera)

            for fire in self.fires:  # 遍历所有火焰并描绘
                fire.draw(self.camera)
            for enemy2 in self.enemy2s:  # 遍历所有敌人并描绘
                enemy2.draw(self.camera)
            for enemy1 in self.enemy1s:  # 遍历所有敌人并描绘
                enemy1.draw(self.camera)

            self.portal1.update()
            self.portal1.draw(self.camera)

            self.portal3.update()
            self.portal3.draw(self.camera)

            self.player.draw(self.camera)  # 描绘玩家图像

            for i in range(self.player.hp):
                hp = self.hp_showings[i]
                window.blit(hp.image, hp.rect)

            for i in range(self.player.burn):
                burn = self.burn_showings[i]
                window.blit(burn.image, burn.rect)

            window.blit(self.coin_image, (10, 60))
            coin_num = font1.render(str(self.player.coin), True, (255, 255, 255))
            window.blit(coin_num, (50, 60))

            window.blit(self.attack_showing.image, self.attack_showing.rect)
            attack_num = font1.render(str(self.player.attack), True, (255, 255, 255))
            window.blit(attack_num, (50, 100))

            if self.player.skill == True and self.first_add1 == True:
                self.skills.append(self.skill)
                self.first_add1 = False
            if self.player.through == True and self.first_add2 == True:
                self.skills.append(self.through)
                self.first_add2 = False
            if self.player.add_bullet_speed == True and self.first_add3 == True:
                self.skills.append(self.add_bullet_speed)
                self.first_add3 = False
            if self.player.blood_eat == True and self.first_add4 == True:
                self.skills.append(self.blood_eat)
                self.first_add4 = False

            for i in range(len(self.skills)):
                window.blit(
                    pygame.transform.scale(
                        self.skills[i].image,
                        (self.attribute_size * 2, self.attribute_size * 2),
                    ),
                    pygame.Rect(
                        10 + i * 50,
                        140,
                        self.attribute_size * 2,
                        self.attribute_size * 2,
                    ),
                )

            for enemy2 in self.enemy2s:
                if self.player.rect.colliderect(enemy2.rect):
                    self.judege_window = True

                    if self.whether_fight == True:
                        self.post(Event(Scene_Code.FIGHT1))
                        self.enemy2s.remove(enemy2)
                        self.whether_fight = False
                        self.judege_window = False

                    if self.judege_window == True:
                        self.player.speed = 0
                        mouse_pos = pygame.mouse.get_pos()
                        mouse_get_pressed = pygame.mouse.get_pressed()

                        window.blit(self.judege_window_image, self.judege_window_rect)

                        window.blit(self.text1, self.text1_rect)
                        window.blit(self.text2, self.text2_rect)
                        window.blit(self.text3, self.text3_rect)

                        if self.button_rect1.collidepoint(mouse_pos):
                            window.blit(self.button_image1_clicked, self.button_rect1)
                            if mouse_get_pressed[0]:
                                self.whether_fight = True
                                self.judege_window = False

                        else:
                            window.blit(self.button_image1, self.button_rect1)

                        if self.button_rect2.collidepoint(mouse_pos):

                            window.blit(self.button_image2_clicked, self.button_rect2)
                            if mouse_get_pressed[0]:
                                self.whether_fight = False
                                self.enemy2s.remove(enemy2)
                                self.judege_window = False
                                self.player.speed = PlayerSettings.player_Speed
                                if self.player.coin >= 5:
                                    self.player.coin -= 5
                                else:
                                    self.player.coin = 0
                                    self.player.hp -= 3
                                    if self.player.hp <= 0:
                                        self.post(Event(Scene_Code.GAME_OVER))
                                self.player.hp -= 2
                                if self.player.hp <= 0:
                                    self.post(Event(Scene_Code.GAME_OVER))

                        else:
                            window.blit(self.button_image2, self.button_rect2)

                        window.blit(self.button_text1, self.button_text1_rect)
                        window.blit(self.button_text2, self.button_text2_rect)

            for enemy1 in self.enemy1s:
                if self.player.rect.colliderect(enemy1.rect):
                    self.judege_window = True

                    if self.whether_fight == True:
                        self.post(Event(Scene_Code.FIGHT2))
                        self.enemy1s.remove(enemy1)
                        self.whether_fight = False
                        self.judege_window = False

                    if self.judege_window == True:
                        self.player.speed = 0
                        mouse_pos = pygame.mouse.get_pos()
                        mouse_get_pressed = pygame.mouse.get_pressed()

                        window.blit(self.judege_window_image, self.judege_window_rect)

                        window.blit(self.text1, self.text1_rect)
                        window.blit(self.text2, self.text2_rect)
                        window.blit(self.text3, self.text3_rect)

                        if self.button_rect1.collidepoint(mouse_pos):
                            window.blit(self.button_image1_clicked, self.button_rect1)
                            if mouse_get_pressed[0]:
                                self.whether_fight = True
                                self.judege_window = False

                        else:
                            window.blit(self.button_image1, self.button_rect1)

                        if self.button_rect2.collidepoint(mouse_pos):

                            window.blit(self.button_image2_clicked, self.button_rect2)
                            if mouse_get_pressed[0]:
                                if self.player.coin >= 2:
                                    self.player.coin -= 2
                                else:
                                    self.player.coin = 0
                                    self.player.hp -= 1
                                    if self.player.hp == 0:
                                        self.post(Event(Scene_Code.GAME_OVER))
                                self.player.hp -= 1
                                if self.player.hp == 0:
                                    self.post(Event(Scene_Code.GAME_OVER))
                                self.whether_fight = False
                                self.enemy1s.remove(enemy1)
                                self.judege_window = False
                                self.player.speed = PlayerSettings.player_Speed

                        else:
                            window.blit(self.button_image2, self.button_rect2)

                        window.blit(self.button_text1, self.button_text1_rect)
                        window.blit(self.button_text2, self.button_text2_rect)


class Scene_City(Listener):  # 场景类
    def __init__(self, player):
        super().__init__()
        self.tiles = []
        self.hp_showings = []
        self.player = player
        self.window_scale = (
            WindowSettings.width,
            WindowSettings.height,
        )
        self.map_range = SceneSettings.map_size  # 实际地图的大小
        self.carema = SceneSettings.camara_0  # 镜头的初始位置
        self.update_camera()  # 更新镜头的位置
        self.attribute_size = SceneSettings.attribute_size  # 属性显示的大小

        self.portal2 = Portals(SceneSettings.portal_speed, 0)

        # 根据地图的尺寸每行每列逐个生成地图方块
        for i in range(self.map_range[0] // 40 + 1):
            for j in range(self.map_range[1] // 40 + 1):
                self.tiles.append(
                    # 方块的种类是随机的，即随机选取一张素材作为该方块
                    # 方块的大小是40*40，根据当前的行数和列数来算出位置
                    City_Tile(random.randint(0, 5), pygame.Rect(i * 40, j * 40, 40, 40))
                )

        self.game_machine1 = Game_machine(
            pygame.Rect(
                SceneSettings.game_machine_pos[0][0],
                SceneSettings.game_machine_pos[0][1],
                SceneSettings.game_machine_size[0],
                SceneSettings.game_machine_size[1],
            )
        )
        self.game_machine2 = Game_machine(
            pygame.Rect(
                SceneSettings.game_machine_pos[1][0],
                SceneSettings.game_machine_pos[1][1],
                SceneSettings.game_machine_size[0],
                SceneSettings.game_machine_size[1],
            )
        )

        self.shop = Shop_icon(
            pygame.Rect(
                SceneSettings.shop_pos[0],
                SceneSettings.shop_pos[1],
                SceneSettings.tile_size * 4,
                SceneSettings.tile_size * 4,
            )
        )

        self.hotel = Hotel_icon(
            pygame.Rect(
                SceneSettings.hotel_pos[0],
                SceneSettings.hotel_pos[1],
                SceneSettings.tile_size * 4,
                SceneSettings.tile_size * 4,
            )
        )

        self.coin_image = pygame.transform.scale(
            pygame.image.load(Game_Path.coin_path),
            (self.attribute_size * 2, self.attribute_size * 2),
        )

        self.attack_showing = Attribute_showing(
            10, pygame.Rect(10, 100, self.attribute_size * 2, self.attribute_size * 2)
        )

        self.blood_eat = Attribute_showing(
            6, pygame.Rect(10, 140, self.attribute_size * 2, self.attribute_size * 2)
        )
        self.skill = Attribute_showing(
            14, pygame.Rect(10, 140, self.attribute_size * 2, self.attribute_size * 2)
        )
        self.through = Attribute_showing(
            12, pygame.Rect(10, 140, self.attribute_size * 2, self.attribute_size * 2)
        )
        self.add_bullet_speed = Attribute_showing(
            13, pygame.Rect(10, 140, self.attribute_size * 2, self.attribute_size * 2)
        )
        self.skills = []
        self.first_add1 = True
        self.first_add2 = True
        self.first_add3 = True
        self.first_add4 = True

        for i in range(20):
            hp = Attribute_showing(
                0,
                pygame.Rect(i * 25 + 10, 30, self.attribute_size, self.attribute_size),
            )
            self.hp_showings.append(hp)
        """
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        """
        self.whether_hotel = False

        self.whether_sleep = False

        self.judege_window_image = pygame.Surface((1000, 500))
        self.judege_window_image.fill((20, 20, 20))
        # self.judege_window_image.set_alpha(220)
        self.judege_window_rect = self.judege_window_image.get_rect()
        self.judege_window_rect.center = (
            WindowSettings.width // 2,
            WindowSettings.height // 2,
        )

        self.button_image1 = pygame.Surface((250, 125))
        self.button_image1.fill((50, 50, 50))
        self.button_rect1 = self.button_image1.get_rect()
        self.button_rect1.center = (350, 600)

        self.button_image1_clicked = pygame.Surface((250, 125))
        self.button_image1_clicked.fill((100, 100, 100))

        self.button_image2 = pygame.Surface((250, 125))
        self.button_image2.fill((50, 50, 50))
        self.button_rect2 = self.button_image2.get_rect()
        self.button_rect2.center = (1050, 600)

        self.button_image2_clicked = pygame.Surface((250, 125))
        self.button_image2_clicked.fill((100, 100, 100))

        self.text1 = font2.render("Press Yes to sleep !", True, (255, 255, 255))
        self.text2 = font1.render(
            "(hp add 2 if hp <= 8 , cost 3 coins and refresh the enemies)",
            True,
            (255, 255, 255),
        )

        self.text1_rect = self.text1.get_rect()
        self.text2_rect = self.text2.get_rect()
        self.text1_rect.center = (WindowSettings.width // 2, 300)
        self.text2_rect.center = (WindowSettings.width // 2, 450)

        self.button_text1 = font1.render("YES", True, (255, 255, 255))
        self.button_text2 = font1.render("NO", True, (255, 255, 255))
        self.button_text1_rect = self.button_text1.get_rect()
        self.button_text2_rect = self.button_text2.get_rect()
        self.button_text1_rect.center = (350, 600)
        self.button_text2_rect.center = (1050, 600)

        """
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        """

    def update_camera(self):
        player_center_cord = self.player.rect.center
        self.camera = Compute_tuple.tuple_sub(
            player_center_cord, Compute_tuple.tuple_mul(self.window_scale, 0.5)
        )

        left_top = (0, 0)

        right_down = Compute_tuple.tuple_sub(self.map_range, self.window_scale)
        self.camera = Compute_tuple.tuple_min(right_down, self.camera)
        self.camera = Compute_tuple.tuple_max(left_top, self.camera)

    def listen(self, event: Event):  # 场景所监听的事件
        super().listen(event)

        keys = pygame.key.get_pressed()

        if event.code == Event_Code.REQUEST_MOVE:  # 监听玩家的移动请求事件
            can_move = 1
            target_rect = pygame.Rect(
                event.body["POS"][0],
                event.body["POS"][1],
                self.player.width,
                self.player.height,
            )
            # for tree in self.trees:
            #     if tree.rect.colliderect(target_rect):
            #         can_move = 0
            #         break

            if can_move:
                self.post(Event(Event_Code.CAN_MOVE, event.body))

        if event.code == Event_Code.CHECK_PORTAL2:

            if self.portal2.rect.colliderect(self.player.rect) and keys[pygame.K_e]:
                self.post(Event(Scene_Code.FOREST))
                # print("go to forest")

            if self.shop.rect.colliderect(self.player.rect) and keys[pygame.K_e]:
                self.post(Event(Scene_Code.SHOP))

            if (
                self.hotel.rect.colliderect(self.player.rect)
                and keys[pygame.K_e]
                and self.can_enter_hotel
            ):
                self.whether_hotel = True
                self.can_enter_hotel = False

            if not self.hotel.rect.colliderect(self.player.rect):
                self.can_enter_hotel = True

            if (
                self.game_machine1.rect.colliderect(self.player.rect)
                and keys[pygame.K_e]
            ):
                self.post(Event(Scene_Code.GAME_GREEDY_SNAKE))

            if (
                self.game_machine2.rect.colliderect(self.player.rect)
                and keys[pygame.K_e]
            ):
                self.post(Event(Scene_Code.GAME_MINE_SWEEPING))

        """
        》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
        """

        # if event.code == Event_Code.CHECK_FIRE:
        #     for fire in self.fires:
        #         if fire.rect.colliderect(self.player.rect):
        #             self.post(Event(Event_Code.BURN))

        if event.code == Event_Code.STEP:  # STEP是每次游戏周期刷新时会被触发的事件
            self.update_camera()  # 更新镜头的位置

        if event.code == Event_Code.DRAW:  # DRAW事件，用于描绘场景中的实体

            if self.player.skill == True and self.first_add1 == True:
                self.skills.append(self.skill)
                self.first_add1 = False
            if self.player.through == True and self.first_add2 == True:
                self.skills.append(self.through)
                self.first_add2 = False
            if self.player.add_bullet_speed == True and self.first_add3 == True:
                self.skills.append(self.add_bullet_speed)
                self.first_add3 = False
            if self.player.blood_eat == True and self.first_add4 == True:
                self.skills.append(self.blood_eat)
                self.first_add4 = False

            for tile in self.tiles:  # 遍历所有地图背景图块并描绘
                tile.draw(self.camera)
            self.game_machine1.draw(self.camera)
            self.game_machine2.draw(self.camera)

            self.player.draw(self.camera)  # 描绘玩家图像

            for i in range(self.player.hp):
                hp = self.hp_showings[i]
                window.blit(hp.image, hp.rect)

            window.blit(self.coin_image, (10, 60))
            coin_num = font1.render(str(self.player.coin), True, (255, 255, 255))
            window.blit(coin_num, (50, 60))

            self.shop.draw(self.camera)
            self.hotel.draw(self.camera)

            window.blit(self.attack_showing.image, self.attack_showing.rect)
            attack_num = font1.render(str(self.player.attack), True, (255, 255, 255))
            window.blit(attack_num, (50, 100))

            for i in range(len(self.skills)):
                window.blit(
                    pygame.transform.scale(
                        self.skills[i].image,
                        (self.attribute_size * 2, self.attribute_size * 2),
                    ),
                    pygame.Rect(
                        10 + i * 50,
                        140,
                        self.attribute_size * 2,
                        self.attribute_size * 2,
                    ),
                )

            self.portal2.update()
            self.portal2.draw(self.camera)

            """
            >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            """
            if self.whether_hotel == True:
                self.player.speed = 0
                mouse_pos = pygame.mouse.get_pos()
                mouse_get_pressed = pygame.mouse.get_pressed()

                window.blit(self.judege_window_image, self.judege_window_rect)

                window.blit(self.text1, self.text1_rect)
                window.blit(self.text2, self.text2_rect)

                if self.button_rect1.collidepoint(mouse_pos):
                    window.blit(self.button_image1_clicked, self.button_rect1)
                    if mouse_get_pressed[0] and self.player.coin >= 3:
                        self.whether_sleep = True
                        self.whether_hotel = False
                        self.player.speed = PlayerSettings.player_Speed
                        self.player.coin -= 3
                        if self.player.hp <= 8:
                            self.player.hp += 2

                        self.post(Event(Scene_Code.FRESH_ENEMY))

                else:
                    window.blit(self.button_image1, self.button_rect1)

                if self.button_rect2.collidepoint(mouse_pos):

                    window.blit(self.button_image2_clicked, self.button_rect2)
                    if mouse_get_pressed[0]:
                        self.whether_sleep = False
                        self.whether_hotel = False
                        self.player.speed = PlayerSettings.player_Speed

                else:
                    window.blit(self.button_image2, self.button_rect2)

                window.blit(self.button_text1, self.button_text1_rect)
                window.blit(self.button_text2, self.button_text2_rect)


class Scene_Beginning(Listener):
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.scale(
            pygame.image.load(Game_Path.background_path[0]),
            (
                WindowSettings.width,
                WindowSettings.height,
            ),
        )

    def listen(self, event: Event):
        super().listen(event)

        if event.code == Event_Code.DRAW:
            window.blit(self.background, (0, 0))

            text_surface = font2.render(
                "Press Q to enter", True, TextSettings.text_color
            )
            text_rect = text_surface.get_rect(
                center=(300, WindowSettings.height - TextSettings.box_height)
            )
            window.blit(text_surface, text_rect)


class Scene_Ending(Listener):
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.scale(
            pygame.image.load(Game_Path.background_path[1]),
            (
                WindowSettings.width,
                WindowSettings.height,
            ),
        )

    def listen(self, event: Event):
        super().listen(event)

        keys = pygame.key.get_pressed()

        if event.code == Event_Code.DRAW:
            window.blit(self.background, (0, 0))

            text_surface2 = font2.render("菜", True, (255, 0, 0))
            text_rect = text_surface2.get_rect(center=(1100, 450))
            window.blit(text_surface2, text_rect)

            text_surface1 = font2.render("Press R to restart", True, (0, 0, 0))
            text_rect1 = text_surface1.get_rect(center=(1000, 600))
            window.blit(text_surface1, text_rect1)

            if keys[pygame.K_r]:
                self.post(Event(Scene_Code.GAME_BEGIN))


class Scene_Winning(Listener):
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.scale(
            pygame.image.load(Game_Path.background_path[2]),
            (
                WindowSettings.width,
                WindowSettings.height,
            ),
        )

    def listen(self, event: Event):
        super().listen(event)
        keys = pygame.key.get_pressed()
        if event.code == Event_Code.DRAW:
            window.blit(self.background, (0, 0))

            text_surface3 = font2.render("YOU WIN!!!!!", True, (0, 0, 0))
            text_rect = text_surface3.get_rect(
                center=(WindowSettings.width / 2, (WindowSettings.height / 2) + 200)
            )
            window.blit(text_surface3, text_rect)

            text_surface4 = font1.render("(Press R to restart)", True, (0, 0, 0))
            text_rect1 = text_surface4.get_rect(
                center=(WindowSettings.width / 2, (WindowSettings.height / 2) + 300)
            )
            window.blit(text_surface4, text_rect1)

            if keys[pygame.K_r]:
                self.post(Event(Scene_Code.GAME_BEGIN))
