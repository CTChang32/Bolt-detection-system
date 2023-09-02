import cv2

#注意：執行程式碼時，需與鏡頭模組位於通一個區域網路中

if __name__ == '__main__':

    # 開啟 RTSP 串流
    vidCap = cv2.VideoCapture('rtsp://192.168.137.107:554') #請更換成Nicla Vishon的本地區域網路IP

    # image = cv2.imread('./BGr028.jpg')

    # 建立視窗
    cv2.namedWindow('image_display', cv2.WINDOW_AUTOSIZE)

    while True:
        # 從 RTSP 串流讀取一張影像
        ret, image = vidCap.read()

        if ret:
            # 顯示影像
            cv2.imshow('image_display', image)
            key = cv2.waitKey(10)  
            if key == 27: #or cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1.0: 
                 break
        else:
        #     # 若沒有影像跳出迴圈
            break

    # 釋放資源
    vidCap.release()

    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()