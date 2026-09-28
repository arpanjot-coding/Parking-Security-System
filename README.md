# Parking Security System

A parking-lot security system that watches a camera feed for behaviour around parked cars and raises an alert when a person, an open door, and a tool line up in a way that looks like a break-in.

This is the code and trained weights from Arpanjot Singh's BSc Computer Science dissertation at the University of Reading (supervisor James Ferryman, May 2023).

The write-up of why the project kept three YOLOv5 detectors, and why the skeleton, the action classifier, and the single seven-class detector were dropped, is the [model selection report](docs/model-selection-report.md). It includes the dissertation figures: the camera setup, the failed poses, the action-model timeline, the labelling changes, and the metrics for the models that shipped.

The class-by-class catalogue of the same weights is in [docs/MODELS.md](docs/MODELS.md).

## What it detects

Three YOLOv5 detectors run on every frame. Each one is trained for a small, related set of classes, and the alert rules sit on top of their boxes.

| Detector | Classes | Role |
| --- | --- | --- |
| D1, vehicle state | Car door open, Car door close, number plate, parking | Is a door open, and which car is it? |
| D2, people | Person, Security | Is that a member of the public or staff in a vest? |
| Tools | Tools (a car jack in the training footage) | Is someone carrying something that can force a door? |

An alert is not a single "robber" class. The deployment code raises one when the boxes overlap:

- **Car door open.** D1 reports `Car door open` above 0.70 confidence.
- **Manual robbery.** A person overlaps the car, the door is open, and the booking end date is not today.
- **Potential robbery.** A tool box overlaps a person box.
- **Someone is breaking in.** A tool overlaps both the person and the car.

The plate crop from D1 is passed to EasyOCR so the dashboard can attach a registration number to the alert. A homography view draws the same cars and people as rectangles on a top-down plan of the bays.

## Repository layout

| Path | What it holds |
| --- | --- |
| `All YOLOv5 Models/D1` | Vehicle-state weights. `best.pt`, plus the training archive marked batch 30, 70 epochs. |
| `All YOLOv5 Models/D2` | Person and security-vest weights. `best.pt`, plus the 70-epoch archive. |
| `All YOLOv5 Models/TOOLS` | Tool detector. `best.pt`, plus the archive marked batch 30, 30 epochs, best result. |
| `MainProjectComponentsDevelopment/ModelDeployment` | Scripts that load the three detectors and draw the alerts. |
| `MainProjectComponentsDevelopment/HomographyDash` | Combined detector and top-down dashboard experiment. |
| `MainProjectComponentsDevelopment/LSTM + RCNN` | Retired action classifier and its `.h5` weights. |
| `MainProjectComponentsDevelopment/Skeleton Extraction` | Retired MediaPipe pose experiments. |
| `MainProjectComponentsDevelopment/Firebase` | Alert and booking helpers for Firebase. |
| `ModelTraning/Model-YOLOv5` | YOLOv5 training notebook. |
| `Model evaluation code` | Label-count, box-overlap, box-distance, and speed checks. |
| `ProjectProcessingPrograms` | Frame reduction and CVAT polyline conversion. |
| `SecurityDash` | PyQt5 security dashboard. |
| `TestingResources` | Sample frames used while wiring the detectors. |
| `docs/MODELS.md` | Model catalogue. |

The deployment scripts still point at absolute paths on the original development machine (`Models/D1/best.pt`, `Models/D2/best.pt`, `Models/Tools/best.pt`). Point those paths at the three `best.pt` files under `All YOLOv5 Models` before running them.

## Stack

Python, PyTorch, Ultralytics YOLOv5m, OpenCV, PyQt5, EasyOCR, and Firebase for accounts, bookings, and alerts. The retired experiments also use MediaPipe Pose and TensorFlow/Keras.

Training of the detectors was done on a Lambda Cloud A100 (40 GB GPU memory). The dissertation records a training cost of $90.21 across two months.

## Datasets

The footage was filmed for this project, reduced from 60 fps to a still every two seconds, and annotated in CVAT. Polygon outlines were converted to YOLOv5 labels through Roboflow. The links recorded with the original project notes are:

- Dataset 1: https://kaggle.com/datasets/d268fae98c8c13e7c31e0f2b328a4e605035f1aa163bd83cecb8f41b596fbc3d
- Dataset 2: https://kaggle.com/datasets/b3a87b94bd147d6166e6a5a8a8f284d15ea54b1fe9cee2d080e60cb803ad3039

## Citation

Singh, A. (2023). *Parking Security System For Detecting Abnormal Behaviour*. BSc dissertation, Department of Computer Science, University of Reading. Supervisor: James Ferryman.

Figures in [docs/MODELS.md](docs/MODELS.md) are taken from that dissertation. The source PDF is compressed, so the plots are at the resolution of that file.

## Credentials

Do not commit Firebase service-account keys. `.gitignore` ignores `accountKey.json`. A key that is already in the history of this repository should be revoked in the Firebase console and replaced with a key that stays on the machine that runs the dashboard.
