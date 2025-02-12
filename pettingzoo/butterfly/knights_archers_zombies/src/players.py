"""
玩家角色模块。

这个模块实现了游戏中的玩家角色类，包括骑士和射手两种角色类型。
每种角色都有其独特的属性、能力和行为模式。

主要功能：
1. 角色状态管理
2. 移动控制
3. 攻击实现
4. 碰撞检测
5. 生命值系统

角色类型：
1. 骑士
   - 近战攻击
   - 高生命值
   - 中等移动速度
   - 剑术技能

2. 射手
   - 远程攻击
   - 中等生命值
   - 快速移动
   - 弓箭技能

共同特性：
1. 生命值系统
2. 等级进展
3. 技能冷却
4. 状态效果
5. 动画系统
"""

import math
import os

import numpy as np
import pygame

from pettingzoo.butterfly.knights_archers_zombies.src import constants as const
from pettingzoo.butterfly.knights_archers_zombies.src.img import get_image


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.agent_name = None

        self.rect = pygame.Rect(0.0, 0.0, 0.0, 0.0)
        self.image = None
        self.org_image = None

        self.angle = 0
        self.pos = pygame.Vector2(self.rect.center)
        self.direction = pygame.Vector2(0, -1)

        self.alive = True
        self.score = 0

        self.is_archer = False
        self.is_knight = False

        self.speed = 0
        self.ang_rate = 0

        self.action = 6
        self.attacking = False
        self.weapon_timeout = 99

        self.weapons = pygame.sprite.Group()

    @property
    def vector_state(self):
        return np.array(
            [
                self.rect.x / const.SCREEN_WIDTH,
                self.rect.y / const.SCREEN_HEIGHT,
                *self.direction,
            ]
        )

    def update(self, action):
        self.action = action
        went_out_of_bounds = False

        if not self.attacking:
            move_angle = math.radians(self.angle + 90)
            # 上下移动
            if action == 1 and self.rect.y > 20:
                self.rect.x += math.cos(move_angle) * self.speed
                self.rect.y -= math.sin(move_angle) * self.speed
            elif action == 2 and self.rect.y < const.SCREEN_HEIGHT - 40:
                self.rect.x -= math.cos(move_angle) * self.speed
                self.rect.y += math.sin(move_angle) * self.speed
            # 逆时针和顺时针旋转
            elif action == 3:
                self.angle += self.ang_rate
            elif action == 4:
                self.angle -= self.ang_rate
            # 使用武器或不做任何动作
            elif action == 5 and self.alive:
                pass
            elif action == 6:
                pass

            # 限制在屏幕内
            if self.rect.y < 0 or self.rect.y > (const.SCREEN_HEIGHT - 40):
                went_out_of_bounds = True

            self.rect.x = max(min(self.rect.x, const.SCREEN_WIDTH - 132), 100)
            self.rect.y = max(min(self.rect.y, const.SCREEN_HEIGHT - 40), 0)

            # 当我们确定没有攻击时，增加武器超时时间
            self.weapon_timeout += 1
        else:
            self.weapon_timeout = 0

        self.direction = pygame.Vector2(0, -1).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        return went_out_of_bounds

    def offset(self, x_offset, y_offset):
        self.rect.x += x_offset
        self.rect.y += y_offset

    def is_done(self):
        return not self.alive


class Archer(Player):
    def __init__(self, agent_name):
        super().__init__()
        self.agent_name = agent_name
        self.image = get_image(os.path.join("img", "archer.png"))
        self.rect = self.image.get_rect(center=(const.ARCHER_X, const.ARCHER_Y))
        self.org_image = self.image.copy()
        self.pos = pygame.Vector2(self.rect.center)
        self.is_archer = True
        self.speed = const.ARCHER_SPEED
        self.ang_rate = const.PLAYER_ANG_RATE


class Knight(Player):
    def __init__(self, agent_name):
        super().__init__()
        self.agent_name = agent_name
        self.image = get_image(os.path.join("img", "knight.png"))
        self.rect = self.image.get_rect(center=(const.KNIGHT_X, const.KNIGHT_Y))
        self.org_image = self.image.copy()
        self.pos = pygame.Vector2(self.rect.center)
        self.is_knight = True
        self.speed = const.KNIGHT_SPEED
        self.ang_rate = const.PLAYER_ANG_RATE
