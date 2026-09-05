import winsound

import user_data
import config


def warning(warn_type):
	data=user_data.load_user_data()

	#Getting alarm type index
	alarm=config.ALARM_OPTIONS[data[3]]

	if alarm=="beep":
		freq=config.BEEP_OPTIONS[warn_type]
		winsound.Beep(freq, 800)