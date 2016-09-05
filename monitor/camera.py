# -*- coding: utf-8 -*-
import datetime
import time
import cv2
import numpy as np
import argparse


def work(camera, space, isDisplay):
    COLOR_GREEN = (0, 255, 0)
    MIN_AREA = 500

    cap = cv2.VideoCapture(camera)
    write_count = 0

    backgroud = None
    next_write_time = 0
    count = 0
    while cap.isOpened:
        now_time = time.time()
        now_time_str = time.strftime('%Y-%m-%d %H %M %S', time.localtime(now_time))

        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gauss_gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if backgroud is None:
            backgroud = gauss_gray

        frame_delta = cv2.absdiff(backgroud, gauss_gray)
        ret, thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)
        finded = False
        for c in cnts:
            if cv2.contourArea(c) < MIN_AREA:
                continue
            finded = True

            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), COLOR_GREEN, 1)

        if count <= 0:
            backgroud = gauss_gray
            count = 30
        else:
            count -= 1

        cv2.putText(frame,
                    now_time_str,
                    (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)
        if finded:
            spacing = now_time - next_write_time
            if spacing > space:
                next_write_time = now_time
                cv2.imwrite('img/' + now_time_str + '.jpg', frame)
                print('write img    time: {}'.format(now_time))
                write_count += 1

            if isDisplay:
                cv2.putText(frame, '* wait... {:.1f}'.format(5 - spacing), (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)
        else:
            if isDisplay:
                cv2.putText(frame, '* nochance', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        if isDisplay:
            cv2.putText(frame, '* writecount: {}'.format(write_count), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
            cv2.imshow('end frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="树莓派 监控程序")
    parser.add_argument('-c', '--camera', help='选择摄像机的来源', default=0)
    parser.add_argument('-s', '--space', help='选择两幅记录之间的时间间隔', default=5)
    parser.add_argument('-d', '--display', action='store_true', help='显示正在监控的画面')
    args = parser.parse_args()

    try:
        args.camera = int(args.camera)
    except:
        pass
    print('at {}'.format(args.camera))

    work(args.camera, args.space, args.display)
