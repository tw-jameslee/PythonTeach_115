import pygame
import sys, os, random
import music
from dataclasses import dataclass


# 遊戲常數設定
WIDTH = 32      # 0~31 共32格
HEIGHT = 24     # 0~23 共24格
CELL_SIZE = 30  # 每格大小: 20像素
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

# 某一點的座標(物件類別)宣告(定義)
@dataclass
class Point:    # 表示座標上的一個點(有x屬性、y屬性，資料型態都是整數)
    x: int
    y: int


#### 副程式（函數）####

# 暫停遊戲的副程式(函數)定義(宣告)
def pause_game():
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
    if pos not in snake_body: # 如果新果實的位置不在蛇身上(合法)，則回傳該位置
      return pos

# 繪製背景圖案函式
def draw_background():
  # 使用純色填滿背景(綠色)
  screen.fill(BACKGROUND_COLOR)
  
  # 畫上草地(grass)顏色圖案
  for y in range(HEIGHT):   # 0~23(共24列)
    
    if y % 2 == 0:  # 偶數列
      for x in range(WIDTH):  # 0~31(共32行)
        if x % 2 == 0:  # 偶數行
          grass_rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) # 定義矩形區域
          pygame.draw.rect(screen, GRASS_COLOR, grass_rect) # 繪製矩形
    
    else: # 奇數列
      for x in range(WIDTH):  # 0~31(共32行)
        if x % 2 != 0:  # 奇數行
          grass_rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) # 定義矩形區域
          pygame.draw.rect(screen, GRASS_COLOR, grass_rect) # 繪製矩形

# 繪製果實
def draw_fruit():
    fruit_rect = (fruit.x * CELL_SIZE, fruit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, FRUIT_COLOR, fruit_rect)

# 繪製蛇身
def draw_snake():
    # 繪製蛇頭
    head = snake_body[0]
    head_rect = (head.x * CELL_SIZE, head.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, HEAD_COLOR, head_rect)

    # 繪製蛇身(不含蛇頭)
    for seg in snake_body[1:]: 
        seg_rect = (seg.x * CELL_SIZE, seg.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BODY_COLOR, seg_rect)

# 顯示分數
def draw_score():
    font = pygame.font.SysFont('microsoftjhenghei', int(CELL_SIZE*1.2))  # 使用系統字型，字型大小1.2倍CELL_SIZE
    score_surf = font.render(f"分數: {score}", True, (0, 0, 0))  # 黑色文字
    screen.blit(score_surf, (10, 5))  # 繪製在左上角(10,5)位置

# 遊戲結束處理函式
def game_over():
    pygame.mixer.music.stop()  # 停止背景音樂
    music.die_sound.play()  # 播放遊戲結束音效
    # 顯示遊戲結束訊息
    font = pygame.font.SysFont('microsoftjhenghei', int(CELL_SIZE*1.8))  # 使用系統字型，字型大小1.8倍CELL_SIZE
    txtSurf = font.render(f"遊戲結束！你的得分是: {score} 分", True, (0, 100, 0))  # 綠色文字
    txtRect = txtSurf.get_rect()  # 取得文字矩形物件
    txtRect.midbottom  = (screen.get_width()//2 , screen.get_height()//2)  # 置中位置
    screen.blit(txtSurf, txtRect) # 繪製在置中位置
    pygame.display.update()    # 更新畫面顯示
    pygame.time.delay(3000)  # 暫停4秒鐘讓玩家聽完音效

    pygame.quit()   # 結束遊戲
    sys.exit()      # 離開系統


#### 遊戲中的變數 ####

direction = '右'    # 初始方向
head = Point(WIDTH//2 , HEIGHT//2)    # 產生一個頭，位置在畫面正中央(16, 12)
snake_body = [head]     # 記錄蛇身每一節的位置，一開始只有一個頭
fruit = get_new_fruit() # 取得初始果實位置
score = 0  # 設定啟始分數為0

#### 遊戲主迴圈 ####
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
                pause_game()    # 暫停遊戲副程式（函數）


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

    ##### 處理遊戲邏輯 #####
    # 判斷是否吃到果實
    ate_food = (new_head == fruit)

    if ate_food:  # 吃到果實
        music.eat_sound.play()  # 播放吃到果實音效
        score += 1  # 增加分數
        fruit = get_new_fruit() # 並取得新果實位置
    
    else: # 沒有吃到果實   
        snake_body.pop() # 移除蛇尾 
    
    # 是否撞牆或撞到自己身體

    if new_head.x < 0 or new_head.x > WIDTH-1 or \
        new_head.y < 0 or new_head.y > HEIGHT-1 or \
        new_head in snake_body[1:]:  # 頭如果在 從第2節到最後一節 之中的話(表示吃到身體)

        game_over() # 播放遊戲結束音效並結束遊戲

    # 繪製背景圖
    draw_background()
    # 繪製果實
    draw_fruit()
    # 繪製蛇身
    draw_snake()
    # 顯示分數
    draw_score()
    # 更新畫面顯示
    pygame.display.update()

    # 控制遊戲速度為每秒FPS幀
    clock.tick(FPS)