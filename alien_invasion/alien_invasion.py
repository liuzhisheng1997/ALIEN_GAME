import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from music import MusicPlay
import game_function as gf
import game_status as gs
from button import Button
from scoreboard import Scoreboard

def run_game():
	# 初始化游戏并创建一个屏幕对象
	pygame.init()
	pygame.mixer.init()
	ai_settings=Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	play_button=Button(ai_settings,screen,'play')
	#创建一艘飞船
	ship=Ship(ai_settings,screen)
	#创建一个用于存储游戏统计信息的实例
	status=gs.GameStatus(ai_settings)
	#创建一个用于存储子弹的编组
	bullets=Group()
	#创建一个外星人编组
	aliens=Group()
	#创建外星人群
	gf.create_fleet(ai_settings,screen,aliens,ship)
	#创建分数
	sb=Scoreboard(ai_settings,screen,status)
	#创建音乐
	music_game=MusicPlay()
	# 开始游戏的主循环
	while True:
			# 监视键盘和鼠标事件
			gf.check_events(ai_settings,screen,ship,bullets,status,play_button,aliens,sb,music_game)
			if status.game_active:
				music_game.background_music_play()
				ship.update()
				gf.update_bullets(bullets,aliens,ai_settings,screen,ship,status,sb)
				gf.update_alien(aliens,ai_settings,ship,status,bullets,screen,sb)
				#每次循环时都重绘屏幕
			gf.update_screen(ai_settings,screen,ship,bullets,aliens,play_button,status,sb)
run_game()