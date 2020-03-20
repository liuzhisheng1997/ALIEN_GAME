import game_function as gf

class GameStatus():
    """跟踪游戏的统计信息"""
    def __init__(self,ai_settings):
        self.ai_settings=ai_settings
        self.reset_status()
        self.game_active=False
        self.high_score=gf.read_high_score()
    def reset_status(self):
        self.ships_left=self.ai_settings.ship_limit
        self.score=0
        self.level=1