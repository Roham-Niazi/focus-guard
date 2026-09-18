FRAME_WIDTH=350
ALARM_OPTIONS=["beep", "windows notification"]
FACE_LANDMARKER_MODEL="assets/face_landmarker.task"
MAX_FPS=25

MIN_DISTANCE=50
MAX_ROLL_ANGLE=15

BEEP_OPTIONS={
	"TOO_CLOSED": 900,
	"HEAD_TILTED": 500,
}

WIND_NOTIF_CONTENTS={
    "TOO_CLOSED": "⚠️ Move farther away from the screen.",
    "HEAD_TILTED": "⚠️ Correct your head position.",
}