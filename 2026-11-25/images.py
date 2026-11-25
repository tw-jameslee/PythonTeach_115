"""
載入音樂、音效的模組
"""
import pygame
import os

# 載入圖片
def load_pictures(assets_dir):

  images_dir = "images"# 圖片檔在images資料夾裡

  # pygame.image.load().convert_alpha()   # 用來載入圖片檔案，並且保留透明背景(Alpha通道)，以便在遊戲中使用

  # 載入圖片

  # 載入蛇的圖片
  global snake_imgs
  snake_imgs = {}

  # for img_name in ["head_up", "head_down", "head_left", "head_right",   # 蛇頭圖片
  #                  "tail_up", "tail_down", "tail_left", "tail_right",   # 蛇尾圖片
  #                  "body_vertical", "body_horizontal",                  # 蛇身圖片
  #                  "body_tr", "body_tl", "body_br", "body_bl"]:         # 蛇身轉角圖片
  #   image_file = os.path.join(assets_dir, images_dir, f"{img_name}.png")
  #   snake_imgs[img_name] = pygame.image.load(image_file).convert_alpha()


  # 載入果實圖片
  global apple

  image_file = os.path.join(assets_dir, images_dir, f"apple.png")
  apple = pygame.image.load(image_file).convert_alpha()