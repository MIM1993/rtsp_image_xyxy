import sys
import pygame
from PIL import Image

if __name__ == '__main__':
    # 输入图片文件
    input = sys.argv[1]
    # 输出坐标保存文件
    ouput = sys.argv[2]
    image = Image.open(input).convert('RGB')
    width = image.size[0]
    height = image.size[1]
    pygame.init()
    # 创建Surface屏幕对象,大小为图片的宽高
    screen = pygame.display.set_mode([width, height])
    # 加载图片
    back_image = pygame.image.load(input)
    # 绘制图像
    screen.blit(back_image, [0, 0])
    # 用来存储单个框和所有框的坐标点
    points = []
    total_points = []

    while True:
        for event in pygame.event.get():
            # 通过监听ESC按键来判断一个框的结束，并清空数组重新记录另一个框
            if event.type == pygame.KEYDOWN:
                total_points.append(points)
                points = []

            if event.type == pygame.QUIT:
                # 点击关闭窗口的时候，把坐标点都保存到指定的文件
                with open(ouput, mode='+w') as fs:
                    fs.write(str(total_points))
                    fs.close()
                # 退出程序
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 重新加载图片，是为了把每次都重新按照顺序画线，不然会出现三点一闭合，不连贯问题
                back_image = pygame.image.load(input)
                # 绘制图像
                screen.blit(back_image, [0, 0])
                pos = event.pos
                points.append([pos[0], pos[1]])

                # 绘画多个框
                if len(total_points) > 0:
                    for poly in total_points:
                        pygame.draw.polygon(screen, (255, 0, 0), poly, 3)

                # 两点成线，这里必须有两个坐标以上才能划线
                if len(points) > 1:
                    pygame.draw.polygon(screen, (255, 0, 0), points, 3)

        # 在窗口的顶部实时显示鼠标所在坐标
        position = pygame.mouse.get_pos()
        pygame.display.set_caption(str(position))

        # 将内容显示到屏幕上
        pygame.display.flip()
