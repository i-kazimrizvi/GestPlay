#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: kazim
"""
import cv2
import pyautogui
import numpy as np


class GestPlay:
    RED_MIN = np.array([125, 50, 50], np.uint8)
    RED_MAX = np.array([185, 190, 190], np.uint8)
    x_coordinate = 0
    y_coordinate = 0
    s = ''
    move = ''

    def __init__(self):
        self.main()

    @classmethod
    def startCapture(cls, capture):
        ret, img = capture.read()
        img = cv2.flip(img, 1)
        orig = cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
        origFrames = cv2.namedWindow('masked', cv2.WINDOW_NORMAL)
        bitwiseFrame = cv2.namedWindow('bitwise', cv2.WINDOW_NORMAL)
        img = cv2.GaussianBlur(img, (15, 15), 0)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        frame_threshed = cv2.inRange(hsv, cls.RED_MIN, cls.RED_MAX)

        frame_bitwise = cv2.bitwise_and(img, img, mask=frame_threshed)

        contours, hierarchy = cv2.findContours(frame_threshed, 1, 2)
        max_area = 0
        last_x = cls.x_coordinate
        last_y = cls.y_coordinate

        cnt = 0
        if contours:
            for i in contours:
                area = cv2.contourArea(i)
                if area > max_area:
                    max_area = area
                    cnt = i

            try:
                x, y, w, h = cv2.boundingRect(cnt)

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                x_coordinate = (x + x + w) / 2
                y_coordinate = (y + y + h) / 2

                cv2.circle(img, (int(x_coordinate), int(y_coordinate)), 2, (255, 0, 0), 2)
                cv2.line(img, (200, 0), (200, 500), (255, 0, 0), 5)
                cv2.line(img, (450, 0), (450, 500), (255, 0, 0), 5)
                cv2.line(img, (200, 250), (450, 250), (255, 0, 0), 5)

                # cv2.imshow('Threshold', frame_threshed)
                cv2.imshow('Original', img)

                cv2.imshow('masked', frame_threshed)
                cv2.imshow('bitwise', frame_bitwise)

                if True:
                    # left
                    if 0 <= x_coordinate <= 290:
                        print('left')
                        pyautogui.press('left')
                    # right
                    if x_coordinate >= 320:
                        print('right')
                        pyautogui.press('right')

                cls.move = cls.s



            except cv2.error:
                print("Error")

    @classmethod
    def main(cls):
        capture = cv2.VideoCapture(0)
        while capture.isOpened():
            cls.startCapture(capture)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                capture.release()
                cv2.destroyAllWindows()
                break




if __name__ == '__main__':
    gestPlay = GestPlay()
