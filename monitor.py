import psutil
import math

import notifier
import config


class Check:
	def __init__(self):
		self.last_distances=[]
		self.last_angles=[]

	def get_fps(self):
		#Calculating FPS based on CPU and RAM usage
		cpu_usage=psutil.cpu_percent()
		ram_usage=psutil.virtual_memory().percent

		total_usage=(cpu_usage*.75+ram_usage*.25)/100

		return math.ceil(config.MAX_FPS*(1-total_usage))


	def check_status(self, distance, eye_angle):
		self.last_distances.append(distance)
		self.last_angles.append(eye_angle)

		#Checking if there are enough values in the distance and angle lists
		if min(len(self.last_distances), len(self.last_angles))<self.get_fps()*0.7:
			return

		#Calculating average distance and angle
		mean_distance=sum(self.last_distances)/len(self.last_distances)
		mean_angle=sum(self.last_angles)/len(self.last_angles)

		if mean_distance<config.MIN_DISTANCE:
			notifier.warning("TOO_CLOSED")

		elif mean_angle>config.MAX_ROLL_ANGLE:
			notifier.warning("HEAD_TILTED")

		self.last_distances=[]
		self.last_angles=[]