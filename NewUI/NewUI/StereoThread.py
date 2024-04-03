#!/usr/bin/env python3

from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np
from PySide6.QtCore import QByteArray, QBuffer, QIODevice, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

# Get argument first
nnPath = str((Path(__file__).parent / Path('./models/mobilenet-ssd_openvino_2021.4_6shave.blob')).resolve().absolute())
if len(sys.argv) > 1:
    nnPath = sys.argv[1]

if not Path(nnPath).exists():
    import sys
    raise FileNotFoundError(f'Required file/s not found, please run "{sys.executable} install_requirements.py"')

# MobilenetSSD label texts
labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

includedLabels = ["person", "car", "motorbike", "bicycle", "bus", "aeroplane", "background", "train"]

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
videoEncoder = pipeline.create(dai.node.VideoEncoder)
monoRight = pipeline.create(dai.node.MonoCamera)
monoLeft = pipeline.create(dai.node.MonoCamera)
depth = pipeline.create(dai.node.StereoDepth)
manip = pipeline.create(dai.node.ImageManip)
nn = pipeline.create(dai.node.MobileNetDetectionNetwork)

videoOut = pipeline.create(dai.node.XLinkOut)
xoutRight = pipeline.create(dai.node.XLinkOut)
disparityOut = pipeline.create(dai.node.XLinkOut)
manipOut = pipeline.create(dai.node.XLinkOut)
nnOut = pipeline.create(dai.node.XLinkOut)

videoOut.setStreamName('h265')
xoutRight.setStreamName('right')
disparityOut.setStreamName('disparity')
manipOut.setStreamName('manip')
nnOut.setStreamName('nn')

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
monoRight.setCamera("right")
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setCamera("left")
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
videoEncoder.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H265_MAIN)

depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
depth.setRectifyEdgeFillColor(0) # Black, to better see the cutout

nn.setConfidenceThreshold(0.5)
nn.setBlobPath(nnPath)
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)

# The NN model expects BGR input. By default ImageManip output type would be same as input (gray in this case)
manip.initialConfig.setFrameType(dai.ImgFrame.Type.BGR888p)
manip.initialConfig.setResize(300, 300)

# Linking
camRgb.video.link(videoEncoder.input)
videoEncoder.bitstream.link(videoOut.input)
monoRight.out.link(xoutRight.input)
monoRight.out.link(depth.right)
monoLeft.out.link(depth.left)
depth.disparity.link(disparityOut.input)
depth.rectifiedRight.link(manip.inputImage)
manip.out.link(nn.input)
manip.out.link(manipOut.input)
nn.out.link(nnOut.input)

# Disparity range is used for normalization
disparityMultiplier = 255 / depth.initialConfig.getMaxDisparity()

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    queueSize = 8
    qRight = device.getOutputQueue("right", queueSize)
    qDisparity = device.getOutputQueue("disparity", queueSize)
    qManip = device.getOutputQueue("manip", queueSize)
    qDet = device.getOutputQueue("nn", queueSize)
    qRgbEnc = device.getOutputQueue('h265', maxSize=30, blocking=True)

    frame = None
    frameManip = None
    frameDisparity = None
    detections = []
    offsetX = (monoRight.getResolutionWidth() - monoRight.getResolutionHeight()) // 2
    color = (0, 255, 0) # green
    croppedFrame = np.zeros((monoRight.getResolutionHeight(), monoRight.getResolutionHeight()))

    # Create a QWidget to hold the QLabel
    app = QApplication([])
    widget = QWidget()
    layout = QVBoxLayout(widget)
    label = QLabel()
    layout.addWidget(label)

    while True:
        inRight = qRight.tryGet()
        inManip = qManip.tryGet()
        inDet = qDet.tryGet()
        inDisparity = qDisparity.tryGet()

        while qRgbEnc.has():
            qRgbEnc.get().getData().tofile(videoFile)

        if inRight is not None:
            frame = inRight.getCvFrame()

        if inManip is not None:
            frameManip = inManip.getCvFrame()

        if inDisparity is not None:
            # Apply color map for better visualization
            frameDisparity = inDisparity.getCvFrame()
            frameDisparity = (frameDisparity*disparityMultiplier).astype(np.uint8)
            frameDisparity = cv2.applyColorMap(frameDisparity, cv2.COLORMAP_JET)

        if inDet is not None:
            detections = inDet.detections

        if frameDisparity is not None:
            for detection in detections:
                if labelMap[detection.label] in includedLabels:
                    bbox = frameNorm(croppedFrame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                    bbox[::2] += offsetX
                    cv2.rectangle(frameDisparity, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
                    cv2.putText(frameDisparity, labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
                    cv2.putText(frameDisparity, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)

            # Convert the OpenCV frame to a QImage
            height, width, channel = frameDisparity.shape
            bytesPerLine = 3 * width
            qImg = QImage(frameDisparity.data, width, height, bytesPerLine, QImage.Format_RGB888)
            qImg = qImg.rgbSwapped()  # RGB to BGR conversion

            # Convert the QImage to a QPixmap and set it to the QLabel
            pixmap = QPixmap.fromImage(qImg)
            label.setPixmap(pixmap)
            label.setScaledContents(True)  # Ensure the image fits the label

            # Show the QLabel
            widget.show()

        if cv2.waitKey(1) == ord('q'):
            break

    # Start the Qt event loop
    sys.exit(app.exec())