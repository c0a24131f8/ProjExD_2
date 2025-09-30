import os
import time
import random
import sys
import pygame as pg



WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0),}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    • 引数：こうかとんRect or 爆弾Rect
    • 戻り値：横方向・縦方向の真理値タプル（True：画面内/False：画面外）
    • Rectオブジェクトのleft, right, top, bottomの値から画面内・外を判断する
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top <0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    こうかとんに爆弾が衝突すると「Game Over」「こうかとんの画像」が5秒間表示される関数
    黒い画面に「Game Over」「こうかとんの画像」をそれぞれ載せ、time.sleep()で5秒間表示させる
    """
    tannkei = pg.Surface((WIDTH, HEIGHT))
    tannkei.set_alpha(255)
    fonto = pg.font.Font(None, 100)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    tannkei.blit(txt, [350, 300])
    kkgo_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    tannkei.blit(kkgo_img, [300, 300])
    tannkei.blit(kkgo_img, [735, 300])
    screen.blit(tannkei, [0, 0])
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() ->tuple[list[pg.Surface], list[int]]:
    """
    時間とともに爆弾を拡大、加速させる
    大きさを変えた爆弾Surfaceのリストと加速度のリストを準備する
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return (bb_imgs, bb_accs)

#途中
# def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
#     kk_dict = {
#         ( 0  0): rotozoom(kk_img, 0, 0),
#         (+5  0): rotozoom(flip(kk_img, True, False), 0, 0),
#         (+5 +5): rotozoom(flip(kk_img, True, False), -45, 0),
#         ( 0 +5): rotozoom(flip(kk_img, True, False), -90, 0),
#         (-5 +5): rotozoom(kk_img, 45, 0),
#         (-5  0): rotozoom(kk_img, 0, 0),
#         (-5 -5): rotozoom(kk_img, -45, 0),
#         ( 0 -5): rotozoom(flip(kk_img, True, False), 90, 0),
#         (+5 -5): rotozoom(flip(kk_img, True, False), 45, 0),
#     }
#     return kk_dict
    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0

    bbimgs, bbaccs =  init_bb_imgs()
    # kk_imgs = get_kk_imgs()　#途中

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:                
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # kk_img = kk_imgs[tuple(sum_mv)]　#途中

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        avx = vx*bbaccs[min(tmr//500, 9)]
        avy = vy*bbaccs[min(tmr//500, 9)]
        bb_img = bbimgs[min(tmr//500, 9)]

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
