import pygame
from pygame.sprite  import Sprite

class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_game):
        '''初始化飞船并设置其初始位置'''
        super().__init__()
        self.sreen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获得其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 对于每艘新飞船，都把他放在底部中央位置
        self.rect.midbottom = self.screen_rect.midbottom
        # 移动标志
        self.moving_right = False
        self.moving_left = False

        # 在飞船属性x中储存最小值
        self.x = float(self.rect.x)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        '''在指定位置画飞船'''
        self.sreen.blit(self.image, self.rect)

    def center_ship(self):
        """飞船居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
