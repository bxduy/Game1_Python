import pygame as pg
import os
import tkinter

pg.font.init()
pg.mixer.init()

WIDTH, HEIGHT = 900, 500 #width, height cho frame
WIN = pg.display.set_mode((WIDTH, HEIGHT)) #tạo frame
ICON = pg.image.load(os.path.join('Assets', 'icon.png')) #icon
pg.display.set_caption('Game 1') #tên frame
pg.display.set_icon(ICON)

WHITE = (255, 255, 255) #mau trang trong bang mau rgb
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pg.Rect(WIDTH//2-5, 0, 10, HEIGHT)

# BULLET_HIT_SOUND = pg.mixer.Sound('/Assets/Sound1.mp3')

HEALTH_FONT = pg.font.SysFont('comicsans', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)

FPS = 60 #thiết lập cấu hình /1s

VEL = 5 #van toc spaceship
BULLET_VEL = 7 #vantoc vien dan
MAX_BULLETS = 3
YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMG = pg.image.load(os.path.join('Assets', 'spaceship_yellow.png')) #ấy hình ảnh tàu vàng
YELLOW_SPACESHIP = pg.transform.rotate(pg.transform.scale(YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) #scale xác định kích thước, rotate quay hình ảnh
RED_SPACESHIP_IMG = pg.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pg.transform.rotate(pg.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)


SPACE = pg.transform.scale(pg.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pg.draw.rect(WIN,BLACK, BORDER)

    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #cho hình ảnh vào frame
    WIN.blit(RED_SPACESHIP, (red.x, red.y))



    for bullet in red_bullets:
        pg.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pg.draw.rect(WIN, YELLOW, bullet)

    pg.display.update() #update để hiển thị hình ảnh

def yellow_handle_movement(keys, yellow_position):
    if keys[pg.K_a] and yellow_position.x - VEL > 0:  # left va khong cho spaceship di chuyen ra ngoai frame
        yellow_position.x -= VEL
    if keys[pg.K_d] and yellow_position.x + VEL + yellow_position.width < BORDER.x + 12:  # right va ... ko vuot qua border
        yellow_position.x += VEL
    if keys[pg.K_w] and yellow_position.y - VEL > 0:  # up
        yellow_position.y -= VEL
    if keys[pg.K_s] and yellow_position.y + VEL + yellow_position.height < HEIGHT - 13:  # down
        yellow_position.y += VEL

def red_handle_movement(keys, red_position):
    if keys[pg.K_LEFT] and red_position.x - VEL > BORDER.x + BORDER.width:  # left
        red_position.x -= VEL
    if keys[pg.K_RIGHT] and red_position.x + VEL + red_position.width < WIDTH + 12:  # right
        red_position.x += VEL
    if keys[pg.K_UP] and red_position.y - VEL > 0:  # up
        red_position.y -= VEL
    if keys[pg.K_DOWN] and red_position.y + VEL + red_position.height < HEIGHT - 13:  # down
        red_position.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): #vien dan co va cham voi red spaceship hay khong
            pg.event.post(pg.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH: #kiem tra vien dan co ra khoi frame khong
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pg.display.update()
    pg.time.delay(5000)

def main():
    red_position = pg.Rect(750, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) #vi tri spaceship tren frame
    yellow_position = pg.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS) #fps
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(yellow_position.x + yellow_position.width, yellow_position.y + yellow_position.height // 2 - 2, 10, 5) #toa do vien dan: x ở phía trước của tàu, y là điểm chính giữa con tàu, viên đạn dài 10, cao 5
                    yellow_bullets.append(bullet)
                    #BULLET_HIT_SOUND.play()
                if event.key == pg.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(red_position.x, red_position.y + red_position.height // 2 - 2, 10, 5)  # toa do vien dan: x ở phía trước của tàu, y là điểm chính giữa con tàu, viên đạn dài 10, cao 5
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ''
        if red_health <= 0:
            winner_text = 'Yellow Wins'
        if yellow_health <= 0:
            winner_text = 'Red Wins'
        if winner_text != '':
            draw_winner(winner_text)
            break

        keys = pg.key.get_pressed()
        yellow_handle_movement(keys, yellow_position)
        red_handle_movement(keys, red_position)
        handle_bullets(yellow_bullets, red_bullets, yellow_position, red_position)
        draw_window(red_position, yellow_position, red_bullets, yellow_bullets, red_health, yellow_health)
    main()

if __name__ == '__main__':
    main()