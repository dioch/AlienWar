

class GameStats:
    def __init__(self,ai_game):
        self.settings=ai_game.settings
        self.reset_stats()
        #让游戏一开始处于非活跃状态
        self.game_active=False
        self.high_score=0
        self.level=1

    def reset_stats(self):
        """初始化游戏运行期间可能变化的统计信息"""
        self.ship_left=self.settings.ship_limit
        self.score = 0