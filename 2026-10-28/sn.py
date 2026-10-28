import pygame
import sys


#常數宣告
WIDTH = 32      # 0~31 共32格
HEIGHT = 24     # 0~23 共24格
CELL_SIZE = 20  # 每格大小: 20像素


# 遊戲初始化
pygame.init()


# 創建遊戲視窗
screen = pygame.display.set_mode(( WIDTH*CELL_SIZE,HEIGHT*CELL_SIZE ))
pygame.display.set_caption("我的貪食蛇遊戲")    #設定視窗抬頭
#clock = pygame.time.Clock()   #設定遊戲時鐘

# 音樂初始化與載入
#
# 還沒寫
#

# 主遊戲迴圈
while True:

    # 處理使用者事件
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit(); 
            sys.exit()

