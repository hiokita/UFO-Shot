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

from curses import KEY_CLOSE, KEY_LEFT, KEY_RIGHT
from select import KQ_FILTER_TIMER
import sys
import time
import pygame
from pygame.locals import *

# pygame初期化
pygame.init()

#
#-- 画面や登場キャラクタのデータを用意します
#

# 画面を構成する
rectScreen = Rect(0, 0, 640, 400)
screen = pygame.display.set_mode(rectScreen.size) # ゲーム画面

# 背景の作成と描画
backgroud = pygame.Surface(rectScreen.size)
backgroud.fill((0, 150, 0))  # 画面の背景色

# 画像の読み込み
imageFighter = pygame.image.load("fighter.png").convert_alpha() # 自機
imageMissile = pygame.image.load("missile.png").convert_alpha() # ミサイル
imageEnemy = pygame.image.load("UFO.png").convert_alpha() # 敵

# 表示する矩形の用意
rectFighter = Rect(0, 250, imageFighter.get_width(), imageFighter.get_height()) # 自機
rectMissile = Rect(0, 0, imageMissile.get_width(), imageMissile.get_height()) # ミサイル
rectEnemy = Rect(0, 50, imageEnemy.get_width(), imageEnemy.get_height()) # 敵

# 移動する速さ
speedFighter = 15 # 自機
speedMissile = 10 # ミサイル
speedEnemy = 5 # 敵

# 敵をやっつけた時のメッセージ
font = pygame.font.Font(None, 55)   
textBang = font.render("Hit!", True, (255,255,255))   # 描画する文字列の設定

# メイン関数の定義
def main():
    flagEnemyBang = False # 敵をやっつけた（True）か、やっつけてない（False）かを表す
    flagEnemyMoveRight = True # 敵が右に移動中（True）か、左に移動中（False）かを表す
    flagMissileFire = False # ミサイルが発射した（True）か、発射していない（False）かを表す

    while True:
        #
        #-- 最初に背景を描きます（ここでは画面全体を塗りつぶします）
        #
        screen.blit(backgroud, (0, 0))

        #
        #-- 自機の操作と描写
        #
        pressed = pygame.key.get_pressed() # 今押されているキーを取得します
        
        if pressed[K_RIGHT]: # →　キーの場合
            rectFighter.x = rectFighter.x + speedFighter # 右に移動します
            if rectFighter.right > rectScreen.width: # 自機の右位置(right)が画面の右端（画面幅）より大きい場合
                rectFighter.right = rectScreen.width # 画面からはみ出さないいように、画面幅に修正します
        
        if pressed[K_LEFT]: # ←　キーの場合
            rectFighter.x = rectFighter.x - speedFighter # 左に移動します
            if rectFighter.x < 0: # 自機の左位置が画面の左端（0）より小さい場合
                rectFighter.x = 0 # 画面からはみ出さないいように、0に修正します

        if pressed[K_SPACE]: # スペースキーの場合
            if flagMissileFire == False: # ミサイルを発射してなければ
                # ミサイルの場所を自機と同じにして、発射！
                rectMissile.x = rectFighter.x 
                rectMissile.y = rectFighter.y
                flagMissileFire = True

        screen.blit(imageFighter, rectFighter) # 自機をゲーム画面に書きます

        #
        #-- ミサイルの移動と描写
        #
        if flagMissileFire == True: # 発射状態の場合
            if rectMissile.y <= 0: # 画面上端(Y=0)に届いた場合（敵に当たらなかった、残念）
                flagMissileFire = False # 無効（未発射）にします
            else: # そうでない場合
                rectMissile.y = rectMissile.y - speedMissile # 上に移動します
                screen.blit(imageMissile, rectMissile) # ミサイルをゲーム画面に書きます
 
        #
        #-- 敵の移動と描写
        #
        if flagEnemyBang == False: # 敵にミサイルが当たっていない場合
            if flagEnemyMoveRight == True: # 右に移動中の場合
                rectEnemy.x = rectEnemy.x + speedEnemy # 右に移動
                if rectEnemy.right > rectScreen.width: # 画面右端に届いた場合
                    flagEnemyMoveRight = False # 左移動に切り替える
            else : # 左に移動中の場合
                rectEnemy.x = rectEnemy.x - speedEnemy # 左に移動
                if rectEnemy.right < 0: # 画面左端に届いた場合
                    flagEnemyMoveRight = True # 右移動に切り替える

            screen.blit(imageEnemy, rectEnemy) # 敵をゲーム画面に書きます

        #
        #-- 敵のミサイルのあたり判定
        #
        if flagMissileFire == True: # ミサイルが発射している場合
            if rectMissile.colliderect(rectEnemy) : # ミサイルと敵の座標が重なっている場合
                screen.blit(textBang, [rectMissile.x, rectMissile.y]) # メッセージ表示
                pygame.display.update()  # 作ったゲーム画面で、Windowsの画面を更新します
                time.sleep(2) # 3秒待ちます
                exit() # 終了関数を呼び出す
        #
        #-- ゲーム画面の更新
        #
        pygame.display.update()  # 作ったゲーム画面で、Windowsの画面を更新します
        pygame.time.Clock().tick(30)        # 更新速度は5fps

        #
        #-- ゲーム画面が閉じられた場合などに対して、システムの後処理を行います
        # ※この部分は直接ゲームに関係ありません
        for event in pygame.event.get(): # 今キューに溜まっている全てのイベントを順に取得
            if event.type == QUIT:    # イベントが強制終了の場合
                exit() # 終了関数を呼び出す

# 終了関数の定義
def exit():
    pygame.quit() # pyGame終了処理
    sys.exit()    # Python終了

# このファイルがpython起動時に指定されたファイルであるかを判定します
if __name__ == '__main__': # importで呼ばれた場合、__name__ には import xxx の xxx　という文字が入ります
    main() # メイン関数を呼び出します