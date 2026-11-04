import pygame
import sys
from dataclasses import dataclass


# 常數宣告
WIDTH = 32      # 0~31 共32格
HEIGHT = 24     # 0~23 共24格
CELL_SIZE = 20  # 每格大小: 20像素
FPS = 7         # 遊戲更新頻率(每秒幀數)

# 變數/類別宣告
@dataclass
class Point:    # 表示座標上的一個點(有x屬性、y屬性，資料型態都是整數)
    x: int
    y: int


# 遊戲初始化
pygame.init()

# 創建遊戲視窗
screen = pygame.display.set_mode(( WIDTH*CELL_SIZE,HEIGHT*CELL_SIZE ))
pygame.display.set_caption("我的貪食蛇遊戲")    # 設定視窗抬頭
clock = pygame.time.Clock()   # 設定遊戲時鐘

# 音樂初始化與載入
#
# 還沒寫
#

# 暫停遊戲
def pause_game():
    print("遊戲暫停中,按ESC鍵繼續遊戲")

    paused = True
    while paused:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 如果按「X」關閉視窗
          pygame.quit(); sys.exit()

        # 如果有按鍵被按下 而且 按下的是 ESC鍵
        elif event.type == pygame.KEYDOWN and \
             event.key == pygame.K_ESCAPE:
          paused = False
          break



# 遊戲變數
direction = '右'   # 初始方向

# 遊戲主迴圈
while True:

    # 處理使用者事件
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()   # 遊戲結束，關閉pygame視窗
            sys.exit()      # 結束程式
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and direction != '左':  # 按下右鍵
                print("按下右鍵")
                direction = '右'
            elif event.key == pygame.K_LEFT and direction != '右':  # 按下左鍵
                print("按下左鍵")
                direction = '左'
            elif event.key == pygame.K_UP and direction != '下':    # 按下上鍵
                print("按下上鍵")
                direction = '上'
            elif event.key == pygame.K_DOWN and direction != '上':  # 按下下鍵
                print("按下下鍵")
                direction = '下'
            elif event.key == pygame.K_ESCAPE:  # 按下ESC鍵
                print("按下ESC鍵")
                pause_game()    # 暫停遊戲


    # 更新畫面顯示
    pygame.display.flip()
    # 控制遊戲速度為每秒FPS幀
    clock.tick(FPS)