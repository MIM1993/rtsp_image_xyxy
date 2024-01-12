import os
import cv2


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

if __name__ == "__main__":
    import cv2

    get_img_with_rtsp("rtsp://192.168.180.114:8554/nba", count=10, save_path="img")
