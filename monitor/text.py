# -*- coding: utf-8 -*-
import cv2
import time

cap = cv2.VideoCapture(0)

if cap.isOpened:
    now_time = time.time()
    now_time_str = time.strftime('%Y-%m-%d %H %M %S', time.localtime(now_time))
    print('OK')
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('img/' + now_time_str + '.jpg', frame)
        print('writed')
