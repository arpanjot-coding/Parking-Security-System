# Parking Security System

A parking-lot security system that watches a camera feed for behaviour around parked cars and raises an alert when a person, an open door, and a tool line up in a way that looks like a break-in.

This is the code and trained weights from Arpanjot Singh's BSc Computer Science dissertation at the University of Reading (supervisor James Ferryman, May 2023). The photographs and plots below are taken from that dissertation. The full written analysis is in the [model selection report](docs/model-selection-report.md). Class lists and weight paths are in [docs/MODELS.md](docs/MODELS.md).

## What the finished system looks like

Three YOLOv5m detectors run on the same frame. D1 draws the door, the plate, and the bays. D2 draws the person. The tools model draws the jack. The banner is raised only when those boxes meet.

<img src="docs/images/report/dashboard-alert.jpg" alt="Security dashboard. The frame shows a closed car door, a number plate, parking bays, a person, and a tool. The banner reads POTENTIAL ROBBERY because the tool box meets the person." width="900">

*Dashboard on a staged break-in. Door close 0.96, plate 0.91, person 0.87, tool 0.68. The tool overlaps the person, so the alert is POTENTIAL ROBBERY. The orange block and green mark on the right are the top-down view of the car and the person.*

<img src="docs/images/report/d1-result.jpg" alt="D1 detection on a closed car: car door close 0.87, number plate 0.96, parking bays 0.96." width="900">

*D1 on its own, after the labels were redrawn as polygons. The closed-door box follows the car, the plate box sits on the bumper, and the parking boxes follow the painted bays.*

## The camera the models were trained for

The lens is about 2.5 m above one bay and looks at the car from the front. A car further down an aisle, or seen from the side, is outside what these weights were measured on.

<p>
<img src="docs/images/report/camera-height.jpg" alt="Camera mounted about 2.5 metres above a parking bay." width="32%">
<img src="docs/images/report/camera-coverage.jpg" alt="Multi-storey aisle with the camera coverage drawn in red." width="66%">
</p>

*Left: mounting height, about 2.5 m. Right: the wedge of an aisle one camera would have to cover. Cars at the far end are too small for a jack or a plate.*

## Why the earlier models were dropped

**Pose.** MediaPipe draws a body even when the bay is empty, and it cannot see a jack.

<img src="docs/images/report/skeleton-empty-bay.jpg" alt="MediaPipe draws a skeleton across the bonnet of a car when nobody is in the frame." width="900">

*Empty bay. The pose is drawn on the bonnet and the headlights.*

**Action classifier.** Validation accuracy sat near 0.998, but on a one-minute video the predicted abnormal events are short spikes in the wrong place. The blue line is the true label. The orange line is the prediction.

<img src="docs/images/report/action-timeline.jpg" alt="True abnormal periods are long blocks. Predicted abnormal labels are short spikes shifted away from them." width="900">

*Sixty one-second clips. Real break-ins last many seconds. The model marks a few one-second spikes.*

**One detector for every class.** A closed door on the neighbouring car is called open, and people breaking in are called Person rather than Robber.

<img src="docs/images/report/false-door-open.jpg" alt="A closed side door is labelled Door Open at 0.83 while the main car is correctly labelled Car at 0.93." width="900">

*The seven-class model. Door Open 0.83 on a shut door at the left edge. Parking boxes cover empty tarmac.*

## The labels that fixed it

The shipped models were trained on polygons that follow the metal of the car and the open door, and leave the glass out.

<p>
<img src="docs/images/report/old-rectangles.jpg" alt="Old labels: loose rectangles around the door glass, the car, and a patch of tarmac." width="48%">
<img src="docs/images/report/new-polygons.jpg" alt="New labels: polygons following the car, the open door, the number plate, and the bay lines." width="48%">
</p>

*Left: the old rectangles, which include glass and tarmac. Right: the outlines the three models were trained on.*

## Scores for the three models that shipped

| Detector | Classes | Result |
| --- | --- | --- |
| D1, vehicle | Car door open, car door close, number plate, parking | mAP at IoU 0.50 is 0.985. F1 0.98 at confidence 0.603. |
| D2, people | Person, Security (the vest) | mAP at IoU 0.50 is 0.994. F1 0.99 at confidence 0.653. |
| Tools | Tools (a car jack) | mAP at IoU 0.50 is 0.984. Best F1 0.95 at confidence 0.631. The jack is small, so this is the weak model. |

<p>
<img src="docs/images/report/d1-precision-recall.jpg" alt="D1 precision-recall curve. All-class mAP at 0.5 is 0.985." width="48%">
<img src="docs/images/report/d2-confusion.jpg" alt="D2 confusion matrix. Person and Security are both recalled at 0.96." width="48%">
</p>

<img src="docs/images/report/tools-f1.jpg" alt="Tools model F1 curve, peaking near 0.95 and falling as confidence gets strict." width="700">

*D1 precision-recall, D2 confusion matrix, and the tools F1 curve. The tools score falls once the confidence threshold gets strict.*

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
| `docs/model-selection-report.md` | Full model report, with every figure described. |
| `docs/MODELS.md` | Class lists, thresholds, and weight paths. |

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

The figures on this page and in the [model selection report](docs/model-selection-report.md) are taken from that dissertation.

## Credentials

Do not commit Firebase service-account keys. `.gitignore` ignores `accountKey.json`. A key that is already in the history of this repository should be revoked in the Firebase console and replaced with a key that stays on the machine that runs the dashboard.
