import pygame
import cv2


class display():
    def __init__(self, rtsp_url, interval=1, ouput_file_path="point.txt"):
        self.rtsp_url = rtsp_url
        self.cap = None
        self.flag = True
        self.interval = interval
        self.frame_num = 0
        self.img_width = 640
        self.img_height = 640
        self.open_rtsp()

        self.screen = None
        self.inti_pygame()

        self.points = []
        self.total_points = []
        self.ouput = ouput_file_path

    def open_rtsp(self):
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url)
            success, frame = self.cap.read()
            if success:
                frame = cv2.transpose(frame)
                size = frame.shape
                self.img_width = size[0]
                self.img_height = size[1]
        except Exception as e:
            print(e.__str__())

    def inti_pygame(self):
        pygame.init()
        size = [self.img_width, self.img_height]
        self.screen = pygame.display.set_mode(size)

    def close(self):
        self.flag = False

    def isframe(self):
        return self.frame_num % self.interval == 0

    def run(self):
        while self.flag:
            for event in pygame.event.get():
                # 退出信号
                if event.type == pygame.QUIT:
                    with open(self.ouput, mode='+w') as fs:
                        fs.write(str(self.total_points))
                        fs.close()
                    self.flag = False

                if event.type == pygame.KEYDOWN:
                    if len(self.points) >= 3:
                        self.total_points.append(self.points)
                    self.points = []

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    self.points.append([pos[0], pos[1]])

            ok, frame = self.cap.read()
            if ok:
                if self.isframe():
                    frame = cv2.transpose(frame)
                    pygame.surfarray.blit_array(self.screen, frame)
                    if len(self.total_points) > 0:
                        for poly in self.total_points:
                            pygame.draw.polygon(self.screen, (255, 0, 0), poly, 3)

                    if len(self.points) > 1:
                        pygame.draw.polygon(self.screen, (255, 0, 0), self.points, 3)
                    pygame.display.flip()
                self.frame_num += 1
        self.cap.retrieve()


def main():
    # 创建线程
    dis = display(rtsp_url="rtsp://127.0.0.1:8554/test", interval=10)
    dis.run()


if __name__ == '__main__':
    main()
