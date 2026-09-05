# Focus Guard

A real-time computer vision tool that monitors **face-to-screen distance** and **head tilt** using MediaPipe Face Landmarker and provides warnings when the user gets too close to the screen or tilts their head excessively.

## Features

* Real-time face landmark detection using MediaPipe
* Monitors the user's distance from the screen
* Detects excessive head tilt
* Provides different warning sounds for different conditions
* Automatically adjusts the processing FPS based on CPU and RAM usage
* Uses eye-to-eye distance for distance estimation
* Saves user calibration and application settings
* Runs in the Windows system tray
* Built with an object-oriented structure

## How It Works

1. The webcam captures the user's face.
2. MediaPipe Face Landmarker detects facial landmarks in real time.
3. The distance between the outer corners of the eyes is used to estimate the user's distance from the monitor.
4. The angle between the two eye landmarks is used to estimate head tilt.
5. Recent distance and angle measurements are averaged to reduce the effect of short-term fluctuations.
6. If the user stays too close to the screen or keeps their head tilted beyond the configured threshold, an appropriate warning is triggered.
7. The application dynamically adjusts its processing FPS according to the current CPU and RAM usage.

## Adaptive FPS

Instead of using a fixed processing FPS, Focus Guard monitors system resource usage and adjusts its FPS accordingly.

When CPU and RAM usage increase, the processing FPS is reduced to lower the application's impact on the rest of the system.

This allows the application to continue monitoring the user while leaving more system resources available for other tasks.

## Calibration

The application uses an initial calibration step to estimate the camera's focal length based on the user's known eye distance at a known screen distance.

This calibration is then used to estimate the user's distance from the monitor during runtime.

## Technologies

* Python
* MediaPipe
* OpenCV
* NumPy
* CustomTkinter
* Pillow
* PyStray
* Psutil

## Limitations

The current version does not yet evaluate face image quality or automatically detect conditions such as poor lighting or a blurry face.

## License

This project is licensed under the MIT License.
