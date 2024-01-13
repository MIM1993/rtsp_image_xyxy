# rtsp_image_xyxy
这个小项目解决了一个小问题，再识别图像的时候，可能只想识别图像中的一部分区域，或者一部份区域不想被识别，
这个区域坐标的获取变得很不方便，这里提供了一个方法，虽然很low，但是比没有强。

##example
```python
    #创建显示对象
    #参数1：rtsp_url rtsp流url地址
    #参数2：interval opencv跳针间隔，默认10
    #参数3：ouput_file_path 最后输出坐标的文件名，默认point.txt
    dis = display(rtsp_url="rtsp://127.0.0.1:8554/test", interval=10)
    dis.run()
```
