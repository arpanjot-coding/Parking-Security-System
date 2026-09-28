# Parking Security System

A camera watches one parking bay. Three object detectors look at every frame, and a short set of rules decides whether the person at the car is leaving as booked or breaking in.

This repository is the code, the trained weights, and the figures from Arpanjot Singh's BSc dissertation in Computer Science at the University of Reading (supervisor James Ferryman, submitted May 2023). The page you are reading is the illustrated overview. Every figure is described underneath it. The longer chapter, with the same figures and the full argument, is the [model selection report](docs/model-selection-report.md). Class names, confidence thresholds, and file paths are listed in [docs/MODELS.md](docs/MODELS.md).

## About the project

Ordinary CCTV leaves the decision to a person watching a wall of screens. Attention drops quickly, and a theft at one bay is easy to miss. The project replaces that watch with a model that can name what is in the bay: the state of the door, the registration plate, whether the figure is a member of staff, and whether they are holding a tool.

A theft is not a class the network outputs. Early attempts asked a model to say "robber" or "abnormal" directly, and those labels did not hold up on the footage. The version that shipped asks for the pieces, then checks whether the pieces meet:

- the door of this car is open,
- a person is standing on that car,
- the person is not wearing the staff vest,
- a tool, in this footage a car jack, overlaps the person and the car,
- the booking for that plate does not say the car should be leaving today.

Staff are recognised from the high-visibility vest, which is large enough to see from the camera. Faces are not used.

Four designs were built. A pose model, an action classifier, and one detector with seven classes were measured and set aside. Three specialist YOLOv5m detectors are what the dashboard loads.

## What the finished system looks like

The two frames below are the system that shipped. On the left, all three detectors are drawn together on the dashboard. On the right, D1 is on its own, on a car whose door is shut.

| Dashboard, three models together | D1 alone, door shut |
| --- | --- |
| <img src="docs/images/report/dashboard-alert.jpg" alt="Dashboard with a potential robbery alert" width="100%"> | <img src="docs/images/report/d1-result.jpg" alt="D1 on a closed car" width="100%"> |
| Door close 0.96, plate 0.91, person 0.87, tool 0.68. The tool meets the person, so the banner is **POTENTIAL ROBBERY**. The orange block and green mark are the top-down view. | Door close 0.87 follows the car, the plate box sits on the bumper at 0.96, and the parking boxes follow the painted bays. |

On the left, D1 has drawn the closed door, the plate, and the bays. D2 has drawn the person. The tools model has drawn the jack in their hands. The door is shut, so there is no door-open alarm. The tool rectangle meets the person rectangle, so the dashboard starts sending the alert to the client who booked the car. The grey panel is a homography, a geometry step rather than a fourth learned model. Each camera tab runs on its own thread, and a two-second clip is stored when an alert fires.

On the right, the same vehicle model is the picture the relabelled training set was aiming at. The plate crop from that box is what EasyOCR reads, so the alert can be matched to a booking. EasyOCR was not trained for this project. It only reads a region D1 has already found.

## The camera these weights actually saw

Every result below depends on one lens. It is mounted about 2.5 m above a single bay and looks along the bay, so the training car is seen from the front and a person at the bumper is seen from head to feet.

| Mounting height | The aisle one camera would have to cover |
| --- | --- |
| <img src="docs/images/report/camera-height.jpg" alt="Camera mounted about 2.5 metres above a parking bay" width="100%"> | <img src="docs/images/report/camera-coverage.jpg" alt="Multi-storey aisle with the camera coverage drawn in red" width="100%"> |
| About 2.5 m. A person can reach the housing with an outstretched arm. Cars to either side are seen from the rear, not from the front. | The red wedge is the coverage. Cars at the bright end of the aisle are too small for a plate or a jack. |

The left photograph is the mounting. The housing is marked in red, and the height is written on the frame as 2.5 m. A standing person can reach it with an outstretched arm, so the view is above head height but not a top-down view into the bay. Cars to either side are seen from the rear quarter, which is a different shape from the front-on car the detectors were trained on.

The right photograph is a real multi-storey aisle, with the wedge one camera would be asked to cover drawn in red. Near the lens the cars are large and partly side-on. At the bright end of the aisle they shrink to a few pixels. A number plate there is not readable, and neither is a jack in someone's hand. That is why a mask class was later abandoned, and why the tools model is the weakest of the three that were kept: small objects disappear first. A reviewer from The Parking Consultancy Ltd made the same point after a demonstration. The detector expects the car from the front, and a camera on every bay, so that every car is front-on, is expensive.

The footage the weights learned from is the front-on view, filmed for the project with participants acting ordinary visits and staged break-ins. It was reduced from 60 frames a second to one still every two seconds, outlined by hand in CVAT, and converted to YOLOv5 labels through Roboflow.

## The three approaches that were dropped, side by side

These ran before the three-model design. Each one tried to say "theft" in a single output, and each one failed in a different way. The pose model is on the left, the LSTM action classifier is in the middle, and the single seven-class detector is on the right.

| Pose (MediaPipe) | LSTM action classifier | One YOLOv5, seven classes |
| --- | --- | --- |
| <img src="docs/images/report/skeleton-empty-bay.jpg" alt="Skeleton drawn on an empty car" width="100%"> | <img src="docs/images/report/action-timeline.jpg" alt="LSTM true labels against predicted labels" width="100%"> | <img src="docs/images/report/false-door-open.jpg" alt="Closed side door called open" width="100%"> |
| Nobody is in the bay. A body is still drawn across the bonnet. A jack is not a landmark, so the tool is invisible. | Blue is the real break-in. Orange is the prediction: short spikes, about two seconds away from the event. Validation accuracy was still 0.998. | A shut door on the left is called Door Open at 0.83. People breaking in were called Person. The robber class agreed 44% of the time. |

### Pose, fitted against an empty bay

MediaPipe Pose returns the joints of one body. Nothing was trained on the parking footage. The hope was that a bent arm would be enough to call a theft.

| Person at the door | Empty bay |
| --- | --- |
| <img src="docs/images/report/skeleton-fitted.jpg" alt="Pose on a person, jack on the ground has no landmarks" width="100%"> | <img src="docs/images/report/skeleton-empty-bay.jpg" alt="Pose invented on the bonnet" width="100%"> |
| The person is found, then the leg collapses into one line. The red jack on the tarmac has no joints, so the actual tool is missing. | The same model invents a shoulder on the windscreen and a leg toward the plate. An alert of "a person is here" would fire on an empty space. |

Light, greyscale, and lighter clothing were tried. None of them stopped the empty-bay skeleton, and a pose still has no class for a door, a plate, or a jack. The scripts stay in `MainProjectComponentsDevelopment/Skeleton Extraction`. The dashboard does not load them.

### LSTM, the training score next to the test

The folder is named `LSTM + RCNN`. The network that was trained is a 3D convolutional classifier on the difference between consecutive frames, resized to 64 by 113. Clips were cut to one second and labelled normal or abnormal. That edit took about four days. There is no recurrent layer in the training script.

| Training, which looks solved | One-minute test, which is not |
| --- | --- |
| <img src="docs/images/report/action-training.jpg" alt="LSTM training loss falling and accuracy near 1.0" width="100%"> | <img src="docs/images/report/action-timeline.jpg" alt="Predicted abnormal spikes miss the true events" width="100%"> |
| Loss falls and accuracy sits between about 0.98 and 1.00. The saved file records accuracy 0.998279. | Three real abnormal stretches last many seconds. The orange predictions are spikes about 2.3 seconds long and about 2 seconds late. |

The reason the two pictures disagree is the difference image. Handheld training footage moves the whole background. Tripod test footage leaves the person.

| Handheld training pair | Tripod test pair |
| --- | --- |
| <img src="docs/images/report/difference-handheld.jpg" alt="Handheld frame difference full of trees and the car outline" width="100%"> | <img src="docs/images/report/difference-tripod.jpg" alt="Tripod frame difference leaving the person and the jack" width="100%"> |
| A small camera shake turns trees, the kerb, and the whole car into the input. The person is a small part of that noise. | The background goes dark and the person with the jack remains. The test images are not the images the model trained on. |

The weights remain under `MainProjectComponentsDevelopment/LSTM + RCNN`.

### One detector, a break-in frame next to a false door

About 900 images, seven classes: car, person, staff vest, door open, robber, mask, and parking space. The results file was not saved. The frames were enough to stop.

| Staged break-in | Neighbouring car |
| --- | --- |
| <img src="docs/images/report/single-model-test.jpg" alt="People called Person and tarmac called parking space" width="100%"> | <img src="docs/images/report/false-door-open.jpg" alt="Closed side door called Door Open at 0.83" width="100%"> |
| The people at the car are `Person` at 0.68. No robber box is drawn. Patches of tarmac are called Parking Space. | The main car is correctly `Car` at 0.93. A shut door on the left is `Door Open` at 0.83. |

A robber and a person had both been drawn as ordinary rectangles, and at this distance their clothes do not differ. Vest boxes included the whole body, and door boxes included the glass, so the network learned the person and the hedge as part of the object. Masks were dropped as well: at 2.5 m a mask is a few pixels, and a requirement to wear one would have alarmed on every visitor.

## The labels, old rectangles beside the outlines that were kept

The classes were split across three models, and every outline was redrawn so the box contained the object.

| Old rectangles | Polygons the three models trained on |
| --- | --- |
| <img src="docs/images/report/old-rectangles.jpg" alt="Loose rectangles around door glass and tarmac" width="100%"> | <img src="docs/images/report/new-polygons.jpg" alt="Polygons following the car, open door, plate, and bay" width="100%"> |
| The door box takes in the glass and the mirror. The parking shape runs off across the tarmac. The network is taught the background. | The outline follows the metal and the open door, stops at the panel, and gives the plate and the bay their own shapes. The glass is left out. |

The same footage was outlined three times, once for each model. A door that was only slightly ajar was relabelled as closed, because the visible panel had barely changed and the model had been swapping those two states.

## The three models, and what the scores mean

All three are YOLOv5m, started from the official pretrained medium weights. YOLOv5 is a single-stage detector: one pass over the image proposes boxes, and each box carries a class name and a confidence. The medium checkpoint was chosen because it has more layers than the small variants, and the objects range from a car that fills the frame to a jack that does not. Training used an image size of 1280×720, batches of 30, 70 epochs, and a 70/20/10 split, on a Lambda Cloud A100. D1 and D2 used about 800 images. The tools model used about 1,200. The recorded training cost over two months was $90.21.

**D1, the vehicle model,** reports `Car door close`, `Car door open`, `number plate`, and `parking`. Its job is the state of the car and which car it is. An open door is only treated as open above a confidence of 0.70. Parking is drawn for the operator. The alert rules do not branch on it.

**D2, the people model,** reports `Person` and `Security`. Security means the vest, not a face. A person box is kept above 0.50. A vest is kept above 0.60, slightly stricter, because a bright jacket can look like a vest.

**The tools model** reports `Tools`. In the footage the tool is a car jack. Every box from this model is treated as a tool, and it becomes an alarm only when the rectangle overlaps a person, or overlaps both the person and the car. A jack lying on the other side of the bay does not overlap the person, so it does not alarm. That overlap is the replacement for the robber class that scored 44%.

| Detector | What a box from it means | Held-out result |
| --- | --- | --- |
| D1, vehicle | Door state, plate, and the bay | mAP at IoU 0.50 is 0.985. Best F1 is 0.98, at confidence 0.603. |
| D2, people | A person, or staff in a vest | mAP at IoU 0.50 is 0.994. Best F1 is 0.99, at confidence 0.653. |
| Tools | A jack | mAP at IoU 0.50 is 0.984. Best F1 is 0.95, at confidence 0.631. |

mAP at an overlap of 0.50 means the predicted box covers at least half of the hand-drawn box and the class is right, averaged over the classes. The confidence next to an F1 is the threshold where that F1 was best. It is not a second copy of the score.

| D1, vehicle | D2, people |
| --- | --- |
| <img src="docs/images/report/d1-precision-recall.jpg" alt="D1 precision-recall curve, mAP 0.985" width="100%"> | <img src="docs/images/report/d2-confusion.jpg" alt="D2 confusion matrix, person and security at 0.96" width="100%"> |
| Precision stays high until recall is high. Closed door 0.994, open door 0.968, plate 0.988, parking 0.992. All-class mAP 0.985. | Person and security are both recalled at 0.96. Four percent of staff are called a person. Two percent of people are called staff. |

| D1 confusion matrix | Tools F1 curve |
| --- | --- |
| <img src="docs/images/report/d1-confusion.jpg" alt="D1 confusion matrix" width="100%"> | <img src="docs/images/report/tools-f1.jpg" alt="Tools F1 curve peaking near 0.95" width="100%"> |
| Closed door is recalled at 0.97, with 0.02 of those cases called open. Open door, plate, and parking sit on the diagonal. | The jack score peaks near 0.95 and then falls once the confidence threshold gets strict, because the tool is small. |

The tools curve climbs to about 0.95 around the middle of the confidence axis and has collapsed by the time confidence reaches 0.95. The legend reads a best F1 of 0.95 at confidence 0.631. The jack is a small object. As the person steps away it becomes a few pixels, and while it is swung inside the car the box disappears. When the jack is visible the box is usually in the right place, which is why the mAP is still 0.984. A strict threshold throws the small object away, which is why the right-hand side of this curve falls to zero. On a 102-frame robber clip the tool was tracked on 90.78% of frames. The dissertation evaluates a 70-epoch run. The zip stored next to the checkpoint is named for 30 epochs. The file to load is `best.pt` in `All YOLOv5 Models/TOOLS`.

The four messages the dashboard can write are these.

- **Car door open.** D1 reports `Car door open` above 0.70.
- **Manual robbery.** A person overlaps the car, the door is open, and today is not the booking end date.
- **Potential robbery.** A tool box overlaps a person box.
- **Someone is breaking in.** A tool box overlaps both the person and the car.

A person opening their own door on the booked day produces the door-open line and does not produce manual robbery. A jack on the ground away from them does not produce potential robbery. A person whose jack meets both their body and the car produces the break-in line.

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
