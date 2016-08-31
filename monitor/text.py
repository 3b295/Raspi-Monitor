# -*- coding: utf-8 -*-
import cv2
import time

cap = cv2.VideoCapture(0)

while cap.isOpened:
    now_time = time.time()
    now_time_str = time.strftime('%Y-%m-%d %H %M %S', time.localtime(now_time))
    ret, frame = cap.read()
    print('ok')
    if ret:
        cv2.imwrite('img/' + now_time_str + '.jpg', frame)
        print('writed')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
