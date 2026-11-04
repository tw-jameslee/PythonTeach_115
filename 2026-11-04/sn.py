import pygame
import sys, os, random
import music
from dataclasses import dataclass


# 遊戲常數設定
WIDTH = 32      # 0~31 共32格
HEIGHT = 24     # 0~23 共24格
CELL_SIZE = 20  # 每格大小: 20像素
FPS = 7         # 遊戲更新頻率(每秒幀數)

# 顏色定義(RGB)
BACKGROUND_COLOR = pygame.Color(175, 215, 70)   # R=175,G=215,B=70 綠色
GRASS_COLOR = pygame.Color(167, 209, 61)        # R=167,G=209,B=61 草地色
HEAD_COLOR = pygame.Color(51, 51, 255)          # R=51,G=51,B=255 藍色
BODY_COLOR = pygame.Color(91, 123, 249)         # R=91,G=123,B=249 藍色
FRUIT_COLOR = pygame.Color(255, 0, 0)           # R=255,G=0,B=0 紅色

# 取得本程式檔所在的資料夾路徑，以便存取上一層 assets 資料夾中的音效檔案
pardir = os.path.dirname(__file__)
assets_dir = os.path.join(pardir, "assets")   # assets資料夾路徑

# 變數/類別宣告
@dataclass
class Point:    # 表示座標上的一個點(有x屬性、y屬性，資料型態都是整數)
    x: int
    y: int


# 遊戲初始化
pygame.init()

# 創建遊戲視窗
screen = pygame.display.set_mode(  (WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE)  )   # 640 x 480
pygame.display.set_caption("我的貪食蛇遊戲")    # 設定視窗抬頭
clock = pygame.time.Clock()   # 建立一個時鐘，等一下用來控制遊戲速度

# 音樂初始化與載入
pygame.mixer.init()
music.load_sounds(assets_dir)   # 傳入assets資料夾路徑，載入音樂、音效
pygame.mixer.music.play(-1)     # 開始播放背景音樂，-1代表無限迴圈


# 暫停遊戲的函數定義(宣告)
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

# 取得新的果實位置，且不與蛇身重疊
def get_new_fruit():
  while True:
    # 果實位置(隨機產生)
    pos = Point(   
       random.randint(0, WIDTH-1), 
       random.randint(0, HEIGHT-1) 
    )
    if pos not in snake_body: # 如果新位置不在蛇身上，則回傳該位置
      return pos


# 遊戲變數
direction = '右'    # 初始方向
head = Point(WIDTH//2 , HEIGHT//2)    # 產生一個頭，位置在畫面正中央(16, 12)
snake_body = [head]     # 記錄蛇身每一節的位置，一開始只有一個頭
fruit = get_new_fruit() # 取得初始果實位置

# 遊戲主迴圈
while True:

    # 處理使用者事件
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()   # 遊戲結束，關閉pygame視窗
            sys.exit()      # 結束程式

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and direction != "左":   # 按下右鍵而且不是正往左走
                direction = '右'
            elif event.key == pygame.K_LEFT and direction != '右':  # 按下左鍵而且不是正往右走
                direction = '左'
            elif event.key == pygame.K_UP and direction != '下':    # 按下上鍵而且不是正往下走
                direction = '上'
            elif event.key == pygame.K_DOWN and direction != '上':  # 按下下鍵而且不是正往上走
                direction = '下'
            elif event.key == pygame.K_ESCAPE:  # 按下ESC鍵
                pause_game()    # 暫停遊戲

    # 取得目前的頭(now_head)，它在蛇身的第1節（索引是0）
    now_head = snake_body[0]

    # 算出新的頭(new_head)的位置
    if direction == "右":
       new_head = Point(now_head.x + 1 , now_head.y)
    elif direction == "左":
       new_head = Point(now_head.x - 1 , now_head.y)
    elif direction == "下":
       new_head = Point(now_head.x , now_head.y + 1)
    elif direction == "上":
       new_head = Point(now_head.x , now_head.y - 1)

    # 把新的頭塞進(insert)蛇身的最前面(索引0)
    snake_body.insert(0, new_head)

    # 判斷是否吃到果實
    
    # 是否撞牆或撞到自己身體

    # 繪製背景圖

    # 繪製果實

    # 繪製蛇身

    # 顯示分數

    # 更新畫面顯示
    pygame.display.update()

    # 控制遊戲速度為每秒FPS幀
    clock.tick(FPS)