# Focus Guard

A real-time computer vision tool that monitors **face-to-screen distance** and **head tilt** using MediaPipe Face Landmarker and provides warnings when the user gets too close to the screen or tilts their head excessively.

## Features

* Real-time face landmark detection using MediaPipe
* Monitors the user's distance from the screen
* Detects excessive head tilt
* Provides different warning sounds for different conditions
* Automatically adjusts the processing FPS based on CPU and RAM usage
* Uses the distance between the outer corners of the eyes for distance estimation
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

## Distance Estimation

Focus Guard estimates the distance between the user's face and the camera using the relationship between the real-world eye distance and its size in the image.

The basic pinhole camera relationship is:

```text
Distance / Eye Distance = Focal Length / Eye Distance (pixels)
```

Rearranging the equation:

```text
Distance = (Focal Length × Eye Distance) / Eye Distance (pixels)
```

Where:

* **Distance** is the estimated distance between the user and the camera.
* **Eye Distance** is the user's real-world distance between the outer corners of the eyes.
* **Focal Length** is estimated during the initial calibration.
* **Eye Distance (pixels)** is the distance between the corresponding eye landmarks detected by MediaPipe in the image.

During calibration, the user provides a known distance from the screen and their eye distance. These values are used to estimate the camera's focal length.

As the user moves closer to or farther from the camera, the eye distance measured in pixels changes, allowing the application to estimate the new distance.

## Adaptive FPS

Instead of using a fixed processing FPS, Focus Guard monitors system resource usage and adjusts its FPS accordingly.

When CPU and RAM usage increase, the processing FPS is reduced to lower the application's impact on the rest of the system.

This allows the application to continue monitoring the user while leaving more system resources available for other tasks.

## Head Tilt Detection

Focus Guard uses facial landmarks around the eyes to calculate the angle of the eye-to-eye line relative to the horizontal axis.

If the measured angle exceeds the configured threshold, the application considers the user's head to be tilted and triggers the corresponding warning.

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
