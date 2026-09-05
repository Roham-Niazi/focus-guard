import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
import math

import config



class VisionProcessor:
	def __init__(self):
		self.video=cv2.VideoCapture(0)

		self.cam_width=self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.cam_height=self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

		BaseOptions=mp.tasks.BaseOptions
		FaceLandmarkerOptions=mp.tasks.vision.FaceLandmarkerOptions
		VisionRunningMode=mp.tasks.vision.RunningMode
		self.FaceLandmarker=mp.tasks.vision.FaceLandmarker


		connections=list(
			vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION
		)
		self.ui_connections=connections[::3] #Selecting one-third of connections for showing on image

		self.options=FaceLandmarkerOptions(
			base_options=BaseOptions(
				model_asset_path=config.FACE_LANDMARKER_MODEL
			),
			running_mode=VisionRunningMode.VIDEO,
			num_faces=1
		)
		self.landmarker=self.FaceLandmarker.create_from_options(self.options)


		self.cap=cv2.VideoCapture(0)



	def detect_face(self, frame_timestamp_ms):
		success, frame=self.cap.read()

		rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		mp_image=mp.Image(
			image_format=mp.ImageFormat.SRGB,
			data=rgb_frame
		)

		#Detecting face
		result=self.landmarker.detect_for_video(
			mp_image,
			frame_timestamp_ms
		)

		frame_timestamp_ms+=33


		if result.face_landmarks:
			self.face=result.face_landmarks[0]

			#Drawing landmarks on frame
			drawing_utils.draw_landmarks(
				image=frame,
				landmark_list=self.face,
				connections=self.ui_connections,
				landmark_drawing_spec=None,
				connection_drawing_spec=(
					drawing_styles.get_default_face_mesh_tesselation_style()
				)
			)
		else:
			self.face=None #When there is no face in image

		rgb_out_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		return rgb_out_frame, frame_timestamp_ms


	def get_eyes_distance_pix(self):
		try:
			#Getting the eyes' coordinates and calculating their distance
			left_outer_eye=self.face[33]
			right_outer_eye=self.face[263]

			left=(left_outer_eye.x*self.cam_width, left_outer_eye.y*self.cam_height)
			right=(right_outer_eye.x*self.cam_width, right_outer_eye.y*self.cam_height)

			distance=math.sqrt(
				(left[0]-right[0])**2 + (left[1]-right[1])**2
			)
			return distance
		except:
			return None #When there is no face in image


	def get_eyes_angle(self):
		try:
			#Getting the eyes' coordinates and calculating their angle with the horizon
			left_outer_eye=self.face[33]
			right_outer_eye=self.face[263]

			left=(left_outer_eye.x*self.cam_width, left_outer_eye.y*self.cam_height)
			right=(right_outer_eye.x*self.cam_width, right_outer_eye.y*self.cam_height)

			slope=(right[1]-left[1])/(right[0]-left[0])
			angle=math.atan(slope)/math.pi*180

			return abs(angle)
		except:
			return None #When there is no face in image


	def calculate_eyes_distance(self, eyes_distance, focal_length):
		#Calculating the eyes' distance from monitor
		distance=None
		eyes_distance_pix=self.get_eyes_distance_pix()
		
		if None not in [focal_length, eyes_distance_pix]:
			distance=eyes_distance*focal_length/eyes_distance_pix

		return distance