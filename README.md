# Gesture Navigator

A real-time gesture recognition system that uses computer vision and machine learning to control devices through hand gestures.

## Features

-   Real-time hand gesture recognition using MediaPipe
-   Support for both static and dynamic gestures
-   Smooth gesture tracking with history buffering
-   Configurable camera parameters
-   FPS monitoring and optimization
-   Device control capabilities

## Requirements

-   Python 3.7+
-   MediaPipe
-   OpenCV
-   TensorFlow
-   scikit-learn
-   Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/jonz9/gesture-based-controller.git
cd gesture-navigator
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

```
gesture-navigator/
├── app.py                 # Main application entry point
├── camera/                # Camera handling and configuration
├── utils/                 # Utility functions and FPS calculation
├── pointhistory/          # Point history tracking implementation
├── landmarks/             # Hand landmark processing
├── models/                # Gesture classification models
└── requirements.txt       # Project dependencies
```

## Usage

Run the application with default settings:

```bash
python app.py
```

Configure camera parameters:

```bash
python app.py --device 1 --width 1280 --height 720
```

### Command Line Arguments

-   `--device`: Camera device index (default: 0)
-   `--width`: Camera capture width (default: 960)
-   `--height`: Camera capture height (default: 540)

## Gesture Recognition

The system uses two main components for gesture recognition:

1. **Keypoint Classifier**: Recognizes static hand gestures
2. **Point History Classifier**: Tracks and recognizes dynamic gestures

Gesture history is maintained using a buffer of 16 frames to ensure smooth recognition.

## Modes

The system also has 3 different modes for usage (0, 1, 2):

1. **Default**: 'n' key - normal gesture recognition mode and performs device control
2. **Logging Key Points**: 'k' key - logs the current hand landmark positions and '0-9' is used to track static gesture number. Used for fine-tuning.
3. **Logging Point History**: 'h' key - logs the current point history positions and '0-9' is used to track dynamic gesture number. Used for fine-tuning.

## Configuration

The system can be configured through the following parameters:

-   `min_detection_confidence`: Probability threshold for hand detection
-   `min_tracking_confidence`: Tracking accuracy threshold for gestures
-   `history_length`: Number of frames to maintain for gesture history (default: 16)
-   `FPS_buffer_length`: Number of frames for FPS smoothing (default: 10)
