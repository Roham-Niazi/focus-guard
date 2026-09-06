import pickle
import os


def load_user_data():
	try:
		with open('data/user_data.pkl', 'rb') as f:
			data=pickle.load(f)

			#Assigning values to variables
			eyes_distance=data["eyes_distance"]
			eyes_distance_pix=data["eyes_distance_pix"]
			focal_length=data["focal_length"]
			alarm=data["alarm"]
	except:
		#Specifying default values for variables
		eyes_distance=None
		eyes_distance_pix=None
		focal_length=None
		alarm=0

	return [
		eyes_distance,
		eyes_distance_pix,
		focal_length,
		alarm
	]



def save_user_data(eyes_distance, eyes_distance_pix, focal_length, alarm):
	data={
		"eyes_distance": eyes_distance,
		"eyes_distance_pix": eyes_distance_pix,
		"focal_length": focal_length,
		"alarm": alarm
	}

	#Checking if the directory exists
	if not os.path.exists("data"):
		os.makedirs("data") #Creating directory

	#Saving settings dictionary as a .pkl file
	with open('data/user_data.pkl', 'wb') as f:
		pickle.dump(data, f)