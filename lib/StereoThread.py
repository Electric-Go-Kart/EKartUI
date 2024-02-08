from PySide6.QtCore import Signal
from PySide6.QtCore import QThread
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt

from multiprocessing.shared_memory import SharedMemory
import numpy as np
import time
import cv2
import depthai as dai
import sys

class VideoThread(QThread):
	frameChanged = Signal(bool)
	qframe = None

	def __init__(self):
		super().__init__()
		self._run_flag = True
		self.nnPath = 'mobilenet-ssd_openvino_2021.4_6shave.blob'
		self.labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
		            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
		self.includedLabels = ["person", "car", "motorbike", "bicycle", "bus", "aeroplane", "background", "train"]
		self.create_pipeline()
		self.disparityMultiplier = 255 / self.depth.initialConfig.getMaxDisparity()
	
	def create_pipeline(self):
		# Create pipeline
		self.pipeline = dai.Pipeline()
		
		# Define sources and outputs
		self.camRgb = self.pipeline.create(dai.node.ColorCamera)
		self.videoEncoder = self.pipeline.create(dai.node.VideoEncoder)
		self.monoRight = self.pipeline.create(dai.node.MonoCamera)
		self.monoLeft = self.pipeline.create(dai.node.MonoCamera)
		self.depth = self.pipeline.create(dai.node.StereoDepth)
		self.manip = self.pipeline.create(dai.node.ImageManip)
		self.nn = self.pipeline.create(dai.node.MobileNetDetectionNetwork)
		
		self.videoOut = self.pipeline.create(dai.node.XLinkOut)
		self.xoutRight = self.pipeline.create(dai.node.XLinkOut)
		self.disparityOut = self.pipeline.create(dai.node.XLinkOut)
		self.manipOut = self.pipeline.create(dai.node.XLinkOut)
		self.nnOut = self.pipeline.create(dai.node.XLinkOut)
		
		self.videoOut.setStreamName('h265')
		self.xoutRight.setStreamName('right')
		self.disparityOut.setStreamName('disparity')
		self.manipOut.setStreamName('manip')
		self.nnOut.setStreamName('nn')
		
		# Properties
		self.camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
		self.camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
		self.monoRight.setCamera("right")
		self.monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
		self.monoLeft.setCamera("left")
		self.monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
		self.videoEncoder.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H265_MAIN)
		
		self.depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
		self.depth.setRectifyEdgeFillColor(0)

		self.nn.setConfidenceThreshold(0.5)
		self.nn.setBlobPath(self.nnPath)
		self.nn.setNumInferenceThreads(2)
		self.nn.input.setBlocking(False)

		self.manip.initialConfig.setFrameType(dai.ImgFrame.Type.BGR888p)
		self.manip.initialConfig.setResize(300, 300)

		self.camRgb.video.link(self.videoEncoder.input)
		self.videoEncoder.bitstream.link(self.videoOut.input)
		self.monoRight.out.link(self.xoutRight.input)
		self.monoRight.out.link(self.depth.right)
		self.monoLeft.out.link(self.depth.left)
		self.depth.disparity.link(self.disparityOut.input)
		self.depth.rectifiedRight.link(self.manip.inputImage)
		self.manip.out.link(self.nn.input)
		self.manip.out.link(self.manipOut.input)
		self.nn.out.link(self.nnOut.input)
	
	def stop(self):
		"""Sets run flag to False and waits for thread to finish"""
		self._run_flag = False
		self.wait()
					
					
	def get_frame(self):
		return self.qframe


	def convert_cv_qt(self, cv_img):
		"""Convert from an opencv image to QPixmap"""
		rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
		h, w, ch = rgb_image.shape
		bytes_per_line = ch * w
		convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
		p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
		return p

	def run(self):
		try:
			with dai.Device(self.pipeline) as device:
				# Output queues will be used to get the grayscale frames from the outputs defined above
				qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)
				qDisparity = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
				qManip = device.getOut

				