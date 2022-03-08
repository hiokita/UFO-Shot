'''
UFOが左右に動くUFOに弾を当てるゲームサンプルです。
極力最低限の実装にしてあります。
2022/2/22 置田宏幸
'''

'''
以下、自分でコンピュータゲームを組む際、わかりずらいかなと思う点のコメントを書きました。

・画面の構成と、位置の指定方法
画面の大きさや、場所は、縦と横の数（値）で表します。 
横方向をX（X軸、X座標）と呼び、縦方向をY（Y軸、Y座標）と呼ぶ事が多いです。
コンピュータでは画面の左上が最初の場所（原点）で、X=0, Y=0 です。
X=0, Y=0 と毎回書くのは面倒なので（Xの数、Yの数で表します。例えば原点は（0,0）と書きます
画面の右に行くほどXが増えます。
画面の下に行くほどYが増えます。（算数で習うグラフは上に行くほど数増えるので、コンピュータの画面は逆です）

・rectとは
rectangleの略で、長方形、矩形を表現します。
画面に書きたい物体の領域や場所を管理するのに使います。
以下の座標を持っています
横方向（X軸）は
    x（長方形の左端）
    left（長方形の左端 leftと同じ）
    right（長方形の右端）
縦方向（Y軸）は
    y（長方形の上端）
    top（長方形の左端 topと同じ）
    bottom（長方形の下端）
'''

from pathlib import Path
from posixpath import abspath, dirname
import sys
import time
import pygame
from pygame.locals import *

# pygameしょきか
pygame.init()

#
#-- がめんや とうじょうキャラクタの データを よういします
#

# がめんの こうせい
rectScreen = Rect(0, 0, 640, 400)
screen = pygame.display.set_mode(rectScreen.size) # ゲームがめん

# はいけいの さくせいと びょうが
backgroud = pygame.Surface(rectScreen.size)
backgroud.fill((0, 150, 0))  # はいけいしょく

# がぞうの よみこみ
baseDirPath = Path(__file__).parent.resolve()
imageFighter =  pygame.image.load(baseDirPath/"fighter.png").convert_alpha() # じき
imageMissile = pygame.image.load(baseDirPath/"missile.png").convert_alpha() # ミサイル
imageEnemy = pygame.image.load(baseDirPath/"UFO.png").convert_alpha() # てき

# ひょうじする くけいの ようい
rectFighter = Rect(0, 250, imageFighter.get_width(), imageFighter.get_height()) # じき
rectMissile = Rect(0, 0, imageMissile.get_width(), imageMissile.get_height()) # ミサイル
rectEnemy = Rect(0, 50, imageEnemy.get_width(), imageEnemy.get_height()) # てき

# いどうする はやさ
speedFighter = 15 # じき
speedMissile = 10 # ミサイル
speedEnemy = 5 # てき

# てきを やっつけたときの メッセージ
font = pygame.font.Font(None, 55)   
textBang = font.render("Hit!", True, (255,255,255)) 

# メインかんすうの ていぎ
def main():
    flagEnemyBang = False # てきをやっつけた（True）か やっつけてない（False）か
    flagEnemyMoveRight = True # てきが右にいどう中（True）か 左にいどう中（False）か
    flagMissileFire = False # ミサイルがはっしゃした（True）か はっしゃしていない（False）か

    while True:
        #
        #-- さいしょに はいけいを かきます（ここでは がめんぜんたい をぬりつぶします）
        #
        screen.blit(backgroud, (0, 0))

        #
        #-- じきの そうさと びょうしゃ
        #
        pressed = pygame.key.get_pressed() # いま おされているキーを しゅとくします
        
        if pressed[K_RIGHT]: # →　キーのばあい
            rectFighter.x = rectFighter.x + speedFighter # 右に いどうします
            if rectFighter.right > rectScreen.width: # じきの右いち(right)が がめんの右はし（がめんはば）より 大きいばあい
                rectFighter.right = rectScreen.width # がめんから はみ出さないように がめんはばに しゅうせいします
        
        if pressed[K_LEFT]: # ←　キーのばあい
            rectFighter.x = rectFighter.x - speedFighter # 左に いどうします
            if rectFighter.x < 0: # じきの左いちが がめんの左はし（0）より 小さいばあい
                rectFighter.x = 0 # がめんから はみ出さないいように 0にしゅうせいします

        if pressed[K_SPACE]: # スペースキーの ばあい
            if flagMissileFire == False: # ミサイルを はっしゃしてなければ
                # ミサイルのばしょを じきと同じにして、はっしゃ！
                rectMissile.x = rectFighter.x 
                rectMissile.y = rectFighter.y
                flagMissileFire = True

        screen.blit(imageFighter, rectFighter) # じきを ゲームがめんに かきます

        #
        #-- ミサイルのいどうと びょうしゃ
        #
        if flagMissileFire == True: # はっしゃじょうたいの ばあい
            if rectMissile.y <= 0: # がめんうえはじ(Y=0)に とどいたばあい（てき にあたらなかった、ざんねん！）
                flagMissileFire = False # はっしゃしていない じょうたいに します
            else: # そうでないばあい
                rectMissile.y = rectMissile.y - speedMissile # うえに いどうします
                screen.blit(imageMissile, rectMissile) # ミサイルを ゲームがめんに かきます
 
        #
        #-- てきのいどうと びょうしゃ
        #
        if flagEnemyBang == False: # てきに ミサイルが あたっていない ばあい
            if flagEnemyMoveRight == True: # 右にいどう中の ばあい
                rectEnemy.x = rectEnemy.x + speedEnemy # 右にいどう
                if rectEnemy.right > rectScreen.width: # がめんみぎはしに とどいたいたばあい
                    flagEnemyMoveRight = False # 左いどうに きりかえる
            else : # 左にいどう中の ばあい
                rectEnemy.x = rectEnemy.x - speedEnemy # 左にいどう
                if rectEnemy.right < 0: # がめんひだりはしに とどいたばあい
                    flagEnemyMoveRight = True # 右いどうに きりかえる

            screen.blit(imageEnemy, rectEnemy) # てきを ゲームがめんに かきます

        #
        #-- てきと ミサイルの あたりはんてい
        #
        if flagMissileFire == True: # ミサイルが はっしゃしているばあい
            if rectMissile.colliderect(rectEnemy) : # ミサイルと てきのざひょうが かさなっているばあい
                screen.blit(textBang, [rectMissile.x, rectMissile.y]) # メッセージひょうじ
                pygame.display.update()  # つくったゲームがめんで、Windowsのがめんを こうしんします
                time.sleep(2) # 3びょう まちます
                exit() # しゅうりょうかんすうを よびだす
        #
        #-- ゲームがめんのこうしん
        #
        pygame.display.update()  # つくったゲームがめんで、Windowsのがめんを こうしんします
        pygame.time.Clock().tick(30) # こうしんそくどは 5fps[frame per second]

        #
        #-- ゲームがめんが とじられたばあい、システムの あとしょりを おこないます
        # ※このぶぶんは ちょくせつゲームに かんけいありません
        for event in pygame.event.get(): # いま キューにたまっている すべてのイベントを じゅんに しゅとく
            if event.type == QUIT:    # イベントが きょうせいしゅうりょうの ばあい
                exit() # しゅうりょうかんすうを よびだす

# しゅうりょうかんすうの ていぎ
def exit():
    pygame.quit() # pyGameしゅうりょう
    sys.exit()    # Pythonしゅうりょう

# このファイルが pythonきどうじに していされたファイルであるかを はんていします
if __name__ == '__main__': # importでよばれたばあい、__name__ には import xxx の xxx　というもじがはいります
    main() # メインかんすうを よびだします