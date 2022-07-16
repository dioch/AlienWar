import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_game):
        """在飞船当前位置建立一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在（0.0）处创建一个子弹矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        # 存储子弹位置
        self.y = float(self.rect.y)

    def update(self):
        """子弹向上移动"""
        self.y -= self.settings.bullet_speed
        # 更新表示子弹位置rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
