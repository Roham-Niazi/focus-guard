import winsound
from winotify import Notification

import user_data
import config


def warning(warn_type):
	data=user_data.load_user_data()

	alarm=config.ALARM_OPTIONS[data[3]]

	if alarm=="beep":
		freq=config.BEEP_OPTIONS[warn_type]
		winsound.Beep(freq, 800)

	elif alarm=="windows notification":
		toast=Notification(
			app_id="Focus Guard",
			title="Posture Warning",
			msg=config.WIND_NOTIF_CONTENTS[warn_type]
		)
		toast.show()