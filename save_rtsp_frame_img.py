import os
import cv2
import json
import numpy as np


# 读取yolov5标注文件,将标注信息转换成图片上的坐标
def read_yolov5_label_file_to_xyxy(file, img_width, img_height):
    f = open(file, 'r')
    text = f.read()
    arr = text.strip().split(" ")

    x_center = float(arr[1])
    y_center = float(arr[2])
    width = float(arr[3])
    height = float(arr[4])

    x = (x_center * img_width)
    y = (y_center * img_height)
    box_w = width * img_width
    box_h = height * img_height

    x1 = int(x - box_w / 2)
    y1 = int(y - box_h / 2)
    x2 = int(x + box_w / 2)
    y2 = int(y + box_h / 2)

    return [x1, y1, x2, y2]


# 读取yolov5标注文件转换坐标,并根据坐标画框,显示画框后的图片
def read_yolov5_label_file_draw_img(rtsp_path, file):
    cap = cv2.VideoCapture(rtsp_path)

    ret, frame = cap.read()
    size = frame.shape
    img_width = size[1]
    img_height = size[0]

    f = open(file, 'r')
    text = f.read()
    arr = text.strip().split(" ")

    x_center = float(arr[1])
    y_center = float(arr[2])
    width = float(arr[3])
    height = float(arr[4])

    x = (x_center * img_width)
    y = (y_center * img_height)
    box_w = width * img_width
    box_h = height * img_height

    x1 = int(x - box_w / 2)
    y1 = int(y - box_h / 2)
    x2 = int(x + box_w / 2)
    y2 = int(y + box_h / 2)

    while True:
        _, frame = cap.read()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

    cap.retrieve()
    cv2.destroyAllWindows()


# 连接rtsp流并存储原尺寸图像
def get_img_with_rtsp(rtsp_path, count=10, save_path="img"):
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    cap = cv2.VideoCapture(rtsp_path)
    frame_id = 0
    while True:
        success, frame = cap.read()
        if success:
            img_file_path = os.path.join(save_path, "%d.jpg" % frame_id)
            cv2.imwrite(img_file_path, frame)
            print("save %s" % img_file_path)
            frame_id += 1
            if frame_id >= 10:
                break
    cap.retrieve()


def read_rtsp(rtsp_path):
    cap = cv2.VideoCapture(rtsp_path)
    while True:
        _, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

    cap.retrieve()
    cv2.destroyAllWindows()


# 读取文件画图
def read_point_file_draw_img(path):
    f = open(path, 'r')
    text = f.read()
    point_list = json.loads(text)
    # for id, xyxy in enumerate(point_list):
    #     print(type(xyxy[0][0]))

    return point_list

# 画框类
class Annotator:
    # YOLOv5 Annotator for train/val mosaics and jpgs and detect/hub inference annotations
    def __init__(self, im, line_width=None, font_size=None, font='Arial.ttf', pil=False, example='abc'):
        assert im.data.contiguous, 'Image not contiguous. Apply np.ascontiguousarray(im) to Annotator() input images.'
        non_ascii = not is_ascii(example)  # non-latin labels, i.e. asian, arabic, cyrillic
        self.pil = pil or non_ascii
        self.im = im
        self.lw = line_width or max(round(sum(im.shape) / 2 * 0.003), 2)  # line width

    def box_label(self, box, label='', color=(128, 128, 128), txt_color=(255, 255, 255)):
        # Add one xyxy box to image with label

        p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
        cv2.rectangle(self.im, p1, p2, color, thickness=self.lw, lineType=cv2.LINE_AA)
        if label:
            tf = max(self.lw - 1, 1)  # font thickness
            w, h = cv2.getTextSize(label, 0, fontScale=self.lw / 3, thickness=tf)[0]  # text width, height
            outside = p1[1] - h >= 3
            p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
            cv2.rectangle(self.im, p1, p2, color, -1, cv2.LINE_AA)  # filled
            cv2.putText(self.im,
                        label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                        0,
                        self.lw / 3,
                        txt_color,
                        thickness=tf,
                        lineType=cv2.LINE_AA)

    def rectangle(self, xy, fill=None, outline=None, width=1):
        # Add rectangle to image (PIL-only)
        self.draw.rectangle(xy, fill, outline, width)

    def text(self, xy, text, txt_color=(255, 255, 255), anchor='top'):
        # Add text to image (PIL-only)
        if anchor == 'bottom':  # start y from font bottom
            w, h = self.font.getsize(text)  # text width, height
            xy[1] += 1 - h
        self.draw.text(xy, text, fill=txt_color, font=self.font)

    def result(self):
        # Return annotated image as array
        return np.asarray(self.im)


def is_ascii(s=''):
    # Is string composed of all ASCII (no UTF) characters? (note str().isascii() introduced in python 3.7)
    s = str(s)  # convert list, tuple, None, etc. to str
    return len(s.encode().decode('ascii', 'ignore')) == len(s)



if __name__ == "__main__":
    point_list = read_point_file_draw_img("point.txt")
    rtsp_path = "rtsp://127.0.0.1:8554/test"

    cap = cv2.VideoCapture(rtsp_path)
    while True:
        ret, frame = cap.read()
        ptss = []
        for id, xyxy in enumerate(point_list):
            print(xyxy)
            pts = np.array(xyxy, np.int32)
            ptss.append(pts)
        cv2.polylines(frame, ptss, isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

if __name__ == "__main1__":
    import cv2

    xyxy = read_yolov5_label_file_to_xyxy("frame.txt", 1280, 720)

    x1 = xyxy[0]
    y1 = xyxy[1]
    x2 = xyxy[2]
    y2 = xyxy[3]

    rtsp_path = "rtsp://192.168.180.114:8554/nba"

    cap = cv2.VideoCapture(rtsp_path)

    while True:
        ret, frame = cap.read()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

    cap.retrieve()
    cv2.destroyAllWindows()

if __name__ == "__main2__":
    import cv2

    read_yolov5_label_file_draw_img("rtsp://192.168.180.114:8554/nba",
                                    "frame.txt")

if __name__ == "__main3__":
    import cv2

    get_img_with_rtsp("rtsp://127.0.0.1:8554/test", count=10, save_path="img")

if __name__ == "__main4__":
    read_rtsp("rtsp://127.0.0.1:8554/test")
