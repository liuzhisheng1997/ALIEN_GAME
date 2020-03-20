import sys
import os
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,ship,bullets,status,music_game):
    """响应按键"""
    if event.key==pygame.K_RIGHT:
        ship.moving_right=True
    if event.key==pygame.K_LEFT:
        ship.moving_left=True
    if event.key==pygame.K_SPACE and status.game_active:
        fire_bullet(ai_settings,bullets,screen,ship,music_game)
    if event.key==pygame.K_q:
        write_high_score(status.high_score)
        sys.exit()
def check_keyup_events(event,ship):
    """响应松开"""
    if event.key==pygame.K_RIGHT:
        ship.moving_right=False
    if event.key==pygame.K_LEFT:
        ship.moving_left=False
def check_events(ai_settings, screen, ship, bullets,status,play_button,aliens,sb,music_game):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,status,music_game)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(status,play_button,mouse_x,mouse_y,aliens,bullets,ai_settings,screen,ship,sb)
def check_play_button(status,play_button,mouse_x,mouse_y,aliens,bullets,ai_settings,screen,ship,sb):
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not status.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        status.reset_status()
        status.game_active=True
        aliens.empty()
        bullets.empty()
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()
        create_fleet(ai_settings,screen,aliens,ship)
def update_screen(ai_settings, screen, ship,bullets,aliens,play_button,status,sb):
    """更新屏幕上的图像并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not status.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()
def update_bullets(bullets,aliens,ai_settings,screen,ship,status,sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    check_bullets_alien_collisions(bullets,aliens,ai_settings,screen,ship,status,sb)
def check_bullets_alien_collisions(bullets,aliens,ai_settings,screen,ship,status,sb):
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            status.score+=ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(status,sb)
    if len(aliens)==0:
        ai_settings.increase_speed()
        status.level+=1
        sb.prep_level()
        bullets.empty()
        create_fleet(ai_settings,screen,aliens,ship)
def fire_bullet(ai_settings,bullets,screen,ship,music_game):
    if len(bullets)<ai_settings.bullets_allowed:
        new_bullet=Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
        music_game.shoot_music_play()
def get_number_aliens_x(ai_settings,alien_width):
    available_space_x=ai_settings.screen_width-2*alien_width
    number_aliens_x=int(available_space_x/(2*alien_width))
    return number_aliens_x
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien_height=alien.rect.height
    alien.x=alien_width+2*alien_width*alien_number
    alien.y=alien_height+2*alien_height*row_number
    alien.rect.x=alien.x
    alien.rect.y=alien.y
    aliens.add(alien)
def get_number_rows(ai_settings,alien_height,ship_height):
    available_space_y=ai_settings.screen_height-3*alien_height-ship_height
    number_aliens_y=int(available_space_y/(2*alien_height))
    return number_aliens_y
def update_alien(aliens,ai_settings,ship,status,bullets,screen,sb):
    aliens.update()
    check_fleet_edges(ai_settings,aliens)
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(aliens,status,ship,bullets,ai_settings,screen,sb)
    check_aliens_bottom(ai_settings,status,screen,ship,aliens,bullets,sb)
def ship_hit(aliens,status,ship,bullets,ai_settings,screen,sb):
    if status.ships_left>0:
        aliens.empty()
        bullets.empty()
        status.ships_left-=1
        sb.prep_ships()
        create_fleet(ai_settings,screen,aliens,ship)
        ship.center_ship()
        sleep(0.5)
    else:
        pygame.mouse.set_visible(True)
        status.game_active=False
def check_high_score(status,sb):
    if status.score>status.high_score:
        status.high_score=status.score
        sb.prep_high_score()
def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def check_aliens_bottom(ai_settings,status,screen,ship,aliens,bullets,sb):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(aliens,status,ship,bullets,ai_settings,screen,sb)
            break
def change_fleet_direction(ai_settings,aliens):
    ai_settings.fleet_direction*=-1
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
def create_fleet(ai_settings,screen,aliens,ship):
    """创建外星人群"""
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_aliens_y=get_number_rows(ai_settings,alien.rect.height,ship.rect.height)
    #创建第一行外星人
    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)
def read_high_score():
    """从文件夹读取最高分"""
    file_path=os.getcwd()+"\\high_score.txt"
    try:
        with open(file_path,'r') as high_score_file:
            high_score=high_score_file.read()
            high_score=int(high_score)
    except FileNotFoundError:
        with open(file_path,'w') as high_score_file:
            high_score_file.write('0')
            high_score=0
    return high_score
def write_high_score(high_score):
    """向文件写入最高分"""
    file_path=os.getcwd()+"\\high_score.txt"
    with open(file_path,'w') as high_score_file:
        high_score_file.write(str(high_score))