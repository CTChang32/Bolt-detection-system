#This Code is for Arduino Nicla Vision, and can be opened in OpenMV IDE

# RTSP Video Server
#
# This example shows off how to stream video over RTSP with your OpenMV Cam.
#
# You can use a program like VLC to view the video stream by connecting to the
# OpenMV Cam's IP address.

import network, omv, rtsp, sensor, time, image
import os, tf, math, uos, gc
#from pyb import UART


# Init UART object.
#uart = UART("LP1", 115200)

# RTP MJPEG streaming works using JPEG images produced by the OV2640/OV5640 camera modules.
# Not all programs (e.g. VLC) implement the full JPEG standard for decoding any JPEG image
# in RTP packets. Images JPEG compressed by the OpenMV Cam internally may not display.

# FFPLAY will correctly handle JPEGs produced by OpenMV software.

sensor.reset()

sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240))

# Turn off the frame buffer connection to the IDE from the OpenMV Cam side.
#
# This needs to be done when manually compressing jpeg images at higher quality
# so that the OpenMV Cam does not try to stream them to the IDE using a fall back
# mechanism if the JPEG image is too large to fit in the IDE JPEG frame buffer on the OpenMV Cam.

omv.disable_fb(True)

# Setup Network Interface

network_if = network.WLAN(network.STA_IF)
network_if.active(True)
network_if.connect('DESKTOP-A07ERSR', '00000000') #更換成自己的WiFi
while not network_if.isconnected():
    print("Trying to connect. Note this may take a while...")
    time.sleep_ms(1000)


#Bolt Model Loading
net = None
labels = None
min_confidence = 0.6

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

colors = [ # Add more colors if you are detecting more than 7 types of classes at once.
    (255,   0,   0),
    (  0, 255,   0),
    (255, 255,   0),
    (  0,   0, 255),
    (255,   0, 255),
    (  0, 255, 255),
    (255, 255, 255),
]


# Setup RTSP Server

server = rtsp.rtsp_server(network_if)

# For the call back functions below:
#
# `pathname` is the name of the stream resource the client wants. You can ignore this if it's not
# needed. Otherwise, you can use it to determine what image object to return. By default the path
# name will be "/".
#
# `session` is random number that will change when a new connection is established. You can use
# session with a dictionary to differentiate different accesses to the same file name.

# Track the current FPS.
clock = time.clock()

def setup_callback(pathname, session):
    print("Opening \"%s\" in session %d" % (pathname, session))

def play_callback(pathname, session):
    clock.reset()
    clock.tick()
    print("Playing \"%s\" in session %d" % (pathname, session))

def pause_callback(pathname, session): # VLC only pauses locally. This is never called.
    print("Pausing \"%s\" in session %d" % (pathname, session))

def teardown_callback(pathname, session):
    print("Closing \"%s\" in session %d" % (pathname, session))

server.register_setup_cb(setup_callback)
server.register_play_cb(play_callback)
server.register_pause_cb(pause_callback)
server.register_teardown_cb(teardown_callback)

# Called each time a new frame is needed.
def image_callback(pathname, session):
    num = [0,0,0,0] #BG, Loosen, Miss, Normal

    img = sensor.snapshot()

    # Markup image and/or do various things.
    #img.draw_string(0,0,"FPS: "+str(round(clock.fps(),2)),color=(255,0,0),scale=1.5)
    for i, detection_list in enumerate(net.detect(img, thresholds=[(math.ceil(min_confidence * 255), 255)])):
        if (i == 0): continue # background class
        num[i] = len(detection_list)
        if (len(detection_list) == 0):
            continue # no detections for this class?

        #print("********** %s **********" % labels[i])
        for d in detection_list:
            if i == 2:
                if float(d[4]) <= 0.75:
                    continue
            [x, y, w, h] = d.rect()
            print(x,y,w,h)
            center_x = math.floor(x + (w / 2))
            center_y = math.floor(y + (h / 2))
            #print('x %d\ty %d' % (center_x, center_y))
            img.draw_circle((center_x, center_y, 8), color=colors[i], thickness=2)
            img.draw_string(x, center_y+15,labels[i],color=colors[i],scale=1.5)


    img.draw_string(0,0 ,"L: "+str(num[1]),color=colors[1],scale=1.5)
    img.draw_string(0,10,"M: "+str(num[2]),color=colors[2],scale=1.5)
    img.draw_string(0,20,"N: "+str(num[3]),color=colors[3],scale=1.5)
    #print(clock.fps())
    clock.tick()
    return img

# Stream does not return. It will call `image_callback` when it needs to get an image object to send
# to the remote rtsp client connecting to the server.

server.stream(image_callback, quality=90)
