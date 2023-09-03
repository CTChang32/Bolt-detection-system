# Bolt-detection-system
本專案為 Research on Lightweight Real-Time Multi-Object Bolt Defect Image Detection System Applied to Climbing Inspection Robots.

## 視覺模組畫面接收
### BoltDetection.py
位於 `Vishon-detection-module` 資料夾中</br>
請安裝OpenMV IDE進行燒錄至Arduion Nicla Vishon中</br>
※注意文件中的WiFi需改成自己的</br>
※記得將 `label.txt` 與 `trained.tflite` 放入模組的儲存空間中

### RTSPStream.py
需要先安裝 opencv
<pre><code>pip install opencv-python</code></pre>
※記得執行 python 檔前修改 IP 位置

### Dataset.zip
裡面包含所有圖片與標注，標注需要用Labelme開啟
<pre><code>https://github.com/wkentaro/labelme</code></pre>
安裝請依照 Github 說明


