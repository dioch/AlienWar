import sys
import pygame
from ship import Ship
from settings import Settings
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    '''管理游戏资源和行为的类'''

    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.width = self.screen.get_rect().width
        self.settings.height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.stats = GameStats(self)
        self.play_button = Button(self,"PLAY")
        self.sb=Scoreboard(self)


    def run_game(self):
        """开始游戏主循环"""
        while True:
            # 设置监视鼠标和键盘的事件
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            # 移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collections = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                 True, True)

        if collections:
            for aliens in collections.values():
                self.stats.score+=self.settings.alien_points*len(aliens)
                self.sb.prep_score()
                self.sb.prep_high_score()
                self.sb.prep_level()
                self.sb.prep_ships()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.stats.level+=1
            self.sb.prep_level()

    def _create_fleet(self):
        # 创建外星人
        alien = Alien(self)
        # alien.width,alien_height=alien.rect.size
        alien_width = alien.rect.width
        alien.height = alien.rect.height
        available_space_x = self.settings.width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可以容纳多少外星人
        ship_height = self.ship.rect.height
        available_space_y = self.settings.height - 3 * alien.height - ship_height
        number_rows = available_space_y // (2 * alien.height)

        # 创建第一行外星人
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.height = alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检查是否有外星人撞到底端
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """检查外星人到达边缘的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移动并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        '''相应被外行星人撞到'''
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            # 清空子弹和外星人
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新外星人，飞船位置重置,并暂停一会
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.6)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查外星人是否到达屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self,mouse_pos):
        """在玩家按下PLAY时开始游戏"""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #重置游戏统计信息
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()

            #清空外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            #创建新的外星人
            self._create_fleet()
            self.ship.center_ship()
            #隐藏鼠标光标
            pygame.mouse.set_visible(False)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()