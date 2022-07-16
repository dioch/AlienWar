class Settings:
    """储存游戏中所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.width = 1200
        self.height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        self.ship_limit = 1
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        self.alien_speed = 0.5
        self.fleet_drop_speed = 5        # fleet_direction=1表示往右移动
        self.fleet_direction = 1
        self.speedup_scale=1.1
        self.initialize_dynamic_settings()
        self.alien_points=50
        self.score_scale=1.5


    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed=1.5
        self.bullet_speed=3.0
        self.alien_speed=1.0

        #fleet_direction=1
        self.fleet_direction=1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)
        print(self.alien_points)

