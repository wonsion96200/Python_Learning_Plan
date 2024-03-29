import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载外星人图像并设置rect属性
        self.sourceimage = pygame.image.load('images/alien.bmp')
        ratio = 0.1
        self.sourceimagerect = self.sourceimage.get_rect()
        self.image = pygame.transform.scale(self.sourceimage, (
        int(self.sourceimagerect.width * ratio), int(self.sourceimagerect.height * ratio)))
        self.rect = self.image.get_rect()
        # 外星人最初在左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 存储准确位置
        self.x = float(self.rect.x)

    def bliteme(self):
        """指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """向右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """外星人位于屏幕边缘，返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
