import cv2
import depthai as dai
import numpy as np

def getFrame(queue):
    #Get frame
    frame = queue.get()

    #Coverting Frame to OpenCV
    return frame.getCvFrame()

def getMonoCamera(pipeline, isLeft):
    #configure mono camera
    mono = pipeline.createMonoCamera()

    #set the Camera Resolution
    mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    if isLeft:
        mono.setBoardSocket(dai.CameraBoardSocket.LEFT)
    else:
        mono.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    return mono

if __name__ == '__main__':

    #Pipeline
    pipeline = dai.Pipeline()

    #Left and Right Camera
    monoLeft = getMonoCamera(pipeline, isLeft = True)
    monoRight = getMonoCamera(pipeline, isLeft = False)
    camRgb = pipeline.create(dai.node.ColorCamera)

    #Camera Resolution
    camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setVideoSize(1920, 1080)
    camRgb.setVideoSize(720, 640)

    xoutLeft = pipeline.createXLinkOut()
    xoutLeft.setStreamName("left")

    xoutRgb = pipeline.create(dai.node.XLinkOut)
    xoutRgb.setStreamName("color")

    xoutRight = pipeline.createXLinkOut()
    xoutRight.setStreamName("right")

    #Attach Cameras to Output
    monoLeft.out.link(xoutLeft.input)
    monoRight.out.link(xoutRight.input)
    camRgb.video.link(xoutRgb.input)
    xoutRgb.input.setBlocking(False)
    xoutRgb.input.setQueueSize(1)
    
    
    #Device Connection
    with dai.Device(pipeline) as device:

        #get the output queues.
        leftQueue = device.getOutputQueue(name = 'left', maxSize=1)
        rightQueue = device.getOutputQueue(name = 'right', maxSize = 1)
        rgb = device.getOutputQueue(name="color", maxSize=1)
        
        
        sidebySide = True
        while True:
            leftFrame = getFrame(leftQueue)
            rightFrame = getFrame(rightQueue)

            if sidebySide:
                #Side by Side view
                imOut = np.hstack((leftFrame, rightFrame))

            else:
                imOut = np.uint8(leftFrame/2 + rightFrame/2)
            #Output Image

            cv2.imshow("Stereo Pair", imOut)

            color = getFrame(rgb)
            color = np.array(color)
            output_manual = np.cumsum(color, axis=1).cumsum(axis=0)
            output_manual = cv2.normalize(output_manual, None, 255,0, cv2.NORM_MINMAX, cv2.CV_8UC1)
          
            cv2.imshow("Color", color)
            cv2.imshow("Integral Image", output_manual)
           
            key = cv2.waitKey(1)
            if key == ord('q'):
                break 
            elif key == ord('t'):
                sidebySide = not sidebySide