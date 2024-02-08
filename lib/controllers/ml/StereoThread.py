from PySide6.QtCore import Signal, QThread
from PySide6.QtGui import QImage
import numpy as np
import time
import cv2
import depthai as dai
import sys

class StereoThread(QThread):
	frameChanged = Signal(QImage)

	def __init__(self):
		super().__init__()
		self._run_flag = True
		self.nnPath = '/home/gokart/projects/EKartUI/lib/controllers/ml/mobilenet-ssd_openvino_2021.4_6shave.blob'
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
		return convert_to_Qt_format

	def run(self):
		try:
			with dai.Device(self.pipeline) as device:
				# Output queues will be used to get the grayscale frames from the outputs defined above
				queueSize = 8
				qRight = device.getOutputQueue("right", queueSize)
				qDisparity = device.getOutputQueue("disparity", queueSize)
				qManip = device.getOutputQueue("manip", queueSize)
				qDet = device.getOutputQueue("nn", queueSize)

				frame = None
				frameManip = None
				frameDisparity = None
				detections = []
				offsetX = (self.monoRight.getResolutionWidth() - self.monoRight.getResolutionHeight()) // 2
				color = (0, 255, 0) # green
				croppedFrame = np.zeros((self.monoRight.getResolutionHeight(), self.monoRight.getResolutionHeight()))

				def frameNorm(frame, bbox):
					normVals = np.full(len(bbox), frame.shape[0])
					normVals[::2] = frame.shape[1]
					return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

				# main loop
				while True:
					inRight = qRight.tryGet()
					inManip = qManip.tryGet()
					inDet = qDet.tryGet()
					inDisparity = qDisparity.tryGet()

					if inRight is not None:
						frame = inRight.getCvFrame()

					if inManip is not None:
						frameManip = inManip.getCvFrame()

					if inDisparity is not None:
						# Apply color map for better visualization
						frameDisparity = inDisparity.getCvFrame()
						frameDisparity = (frameDisparity*self.disparityMultiplier).astype(np.uint8)
						frameDisparity = cv2.applyColorMap(frameDisparity, cv2.COLORMAP_JET)

					if inDet is not None:
						detections = inDet.detections

					if frameDisparity is not None:
						for detection in detections:
							if self.labelMap[detection.label] in self.includedLabels:
								bbox = frameNorm(croppedFrame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
								bbox[::2] += offsetX
								cv2.rectangle(frameDisparity, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
								cv2.putText(frameDisparity, self.labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
								cv2.putText(frameDisparity, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
						# Convert the disparity frame to QImage
						self.qframe = self.convert_cv_qt(frameDisparity)
						self.frameChanged.emit(self.qframe)

		except Exception as e:
			print(e)
			sys.exit(1)

if __name__ == "__main__":
	st = StereoThread()
	st.start()
	time.sleep(10)
	st.stop()
	sys.exit(0)
	