# Choosing the detection models

A short technical report on why the Parking Security System kept three YOLOv5 detectors and set aside the skeleton and the action classifier.

**Arpanjot Singh**
Department of Computer Science, University of Reading
BSc Computer Science, May 2023
Supervisor: James Ferryman

This note is a reading of the dissertation *Parking Security System For Detecting Abnormal Behaviour*. The figures are taken from that document. The weight files, class names, and alert rules were checked against the code in this repository. A class-by-class catalogue of the same models is in [MODELS.md](MODELS.md).

## 1. The decision the project had to make

The aim was a model that could watch a parking bay and tell a normal visit from a theft in time for a person to act. The original objectives asked for four things at once: suspicious movement around a car, signs associated with a break-in (a mask, a tool), a way to tell staff from everyone else, and a dashboard that showed the alert with the footage.

Four designs were built and measured, in this order.

| Order | Design | What it tried to recognise directly |
| --- | --- | --- |
| 1 | MediaPipe Pose | A body, then suspicious movement from the joints |
| 2 | An action classifier, filed as LSTM + RCNN | A one-second clip labelled normal or abnormal |
| 3 | One YOLOv5 detector, seven classes | Car, person, staff vest, open door, robber, mask, parking space |
| 4 | Three YOLOv5m detectors, plus overlap rules | Door state, plate, person, staff vest, and a tool, separately |

The fourth design is the one in the security dashboard. Sections 4 to 7 show the evidence for dropping the first three. Section 8 puts the comparison in one place.

The dissertation is explicit about the outcome. The skeleton and the action model did not detect an anomaly reliably on a single car in a frame. Object detection with bounding boxes did. Inside object detection, one model for every class was not stable enough, and the split into three models was the version that was deployed.

## 2. The picture the models were given

The camera is the constraint underneath every result. It sits about 2.5 m above the bay and looks along the bay, so the car is seen from the front and a person is seen from head to feet when they stand in front of it.

![Camera height. The lens is about 2.5 m above the bay, high enough to see a standing person and the front of the cars on either side. Dissertation Figure 3.2.](images/report/camera-height.jpg)

![The region the camera is asked to cover, marked on a multi-storey aisle. Cars further down the row shrink quickly, and many of them are seen from the side or the rear. Dissertation Figure 3.3.](images/report/camera-coverage.jpg)

Two consequences follow from that geometry, and they show up again in the model results.

A person at the boot of the car, or a car three bays away, occupies few pixels. Small things (a mask, a jack, a face) are the first to disappear. A door on a car that is side-on is a thin edge, not the broad panel the training footage shows.

The footage the models actually learned from is the second view: one car, straight on, filmed for the project, reduced from 60 frames a second to a still every two seconds, and outlined in CVAT. It is a good view of one bay. It is a poor view of a whole aisle. That limit was later pointed out by Ian of The Parking Consultancy Ltd, who reviewed the system: a camera per bay is expensive, and the detector as trained expects the car from the front.

## 3. What "a theft" was turned into

The first objectives describe a theft as a behaviour: lingering, forcing a lock, carrying a hammer. Behaviour is hard to label, because two people can stand in the same place and only one of them is a problem. The design that survived rewrote the theft as a small set of objects that have to meet:

- the door of this car is open,
- a person is on that car,
- the person is holding a tool, in the footage a car jack,
- the person is not wearing the staff vest,
- the booking for that number plate does not say the car should be leaving now.

None of those is a class called robber. The robber decision is a rule on top of the boxes. That rewrite is the reason a detector could be trained by one person on a few hundred images, and the reason the earlier models, which tried to learn "suspicious" as a single label, were put aside.

## 4. Skeleton: a pose is not a break-in

MediaPipe Pose was the first implementation. OpenCV reads the frame, the frame is converted to RGB, and MediaPipe returns body landmarks that are drawn back on the image. No custom training set is required. The hope was that the joints would show someone reaching into a car.

On this footage the pose was unstable in ways that matter for an alarm.

It depended on how much of the person was in the frame, on the light, and on the colour of their clothes. Dark clothing left the model with little edge to follow. A person cut off by the car produced joints in the wrong place. An empty bay still received a skeleton.

![A fitted pose on a person bent over the driver's side. The jack on the ground is invisible to a landmark model, and the lower body has collapsed into a line along the leg. Dissertation Figure 6.1.](images/report/skeleton-fitted.jpg)

![Joints placed on a partially hidden person. The circled ankle points do not sit on the foot. A behaviour model trained on these points would learn the error. Dissertation, section 6.1.](images/report/skeleton-partial.jpg)

![An empty bay. MediaPipe still draws a body, here across the bonnet and the headlights. An alarm built on "a person is present" would fire on the car. Dissertation Figure 6.9.](images/report/skeleton-empty-bay.jpg)

A pose model that invents a person when the bay is empty cannot be the source of a security alert. It also has no class for a door, a plate, or a jack, so the objectives about tools and staff were out of reach without a second system. The skeleton code remains in `MainProjectComponentsDevelopment/Skeleton Extraction` as the record of the experiment. It is not loaded by the dashboard.

## 5. The action classifier: a strong validation score, a weak clock

The next experiment tried to classify a whole second of video as normal or abnormal. In the dissertation this design is called LSTM + RCNN: a detector would find the person, and a recurrent network would read the sequence. The network that was actually trained, in `LSTM + RCNN  Traning code.py`, is a 3D convolutional classifier. There is no recurrent layer and no region proposal in that file. The saved weight uses the name `convlstm_model`.

The input is the difference between consecutive frames, resized to 64×113. Subtracting the previous frame was meant to leave the moving person and suppress the parked cars, so the clips would not have to be labelled box by box. About four days were spent cutting one-second clips in DaVinci Resolve into a `normal` folder and an `abnormal` folder.

The architecture is three Conv3D blocks (32, 64, then 64 filters, kernel 3×3×3, ReLU), each followed by a max-pool of size 1×2×2, then a dense layer of 512 units, dropout of 0.5, and a two-class softmax. Loss is categorical cross-entropy with Adam. Training used batches of 32, at most 50 epochs, and early stopping with patience 10. It stopped near epoch 25.

![Training and validation loss fall together, and accuracy sits between about 0.98 and 1.00 after epoch 8. The saved file records loss 0.002333 and accuracy 0.998279. Dissertation Figure 6.11.](images/report/action-training.jpg)

Read on their own, those curves say the model has learned the training clips. A one-minute test video, scored once per second, says something else. True abnormal stretches last on the order of ten seconds. The predictions are brief spikes, about 2.3 seconds long, and they sit about two seconds away from the true event. The model finds that something happened. It does not find when, or for how long.

![True labels (blue) against predicted labels (orange) on 60 one-second clips. The three real abnormal periods are wide. The predictions are narrow and shifted. Dissertation Figure 6.14.](images/report/action-timeline.jpg)

The difference images explain a large part of the gap. The training footage was shot by hand. A small camera movement changes every pixel, so the difference is foliage, the edge of the car, and the bay lines. The test footage was shot on a tripod. There the difference is mostly the person, which is what the method wanted, and it is a different kind of picture from the one the model trained on.

![Handheld pair. The difference is dominated by the background moving with the camera. Dissertation Figure 6.15.](images/report/difference-handheld.jpg)

![Tripod pair of the same kind of action. The person is left, and the background is largely gone. The test images do not look like the training images. Dissertation Figure 6.16.](images/report/difference-tripod.jpg)

Reshooting the whole set on a tripod would have cleaned the differences. It would not have created the range of people, clothes, and actions a behaviour model needs, and labelling every second by hand was more work than drawing boxes on stills. For one developer, the detector was the practical model. The action-classifier weights remain at:

`MainProjectComponentsDevelopment/LSTM + RCNN/convlstm_model___Date_Time_2023_01_17__16_31_01___Loss_0.002333042910322547___Accuracy_0.9982788562774658.h5`

## 6. One detector: the classes were not separable

YOLOv5 was then trained as a single model on about 900 images and seven classes: `Car`, `Person`, `Staff Vest`, `Door Open`, `Robber`, `Mask`, and `Parking Space`. The Ultralytics results file for that run was not saved, so there is no confusion matrix. A label counter and a visual check were enough to stop.

| Class | Share of ground-truth boxes the counter agreed with |
| --- | --- |
| Mask | 95% |
| Door open | 95% |
| Car | 88% |
| Staff vest | 85% |
| Person | 83% |
| Parking space | 69% |
| Robber | 44% |

The robber number is the one that removes the model. A robber and a person were both drawn as ordinary rectangles. At this camera distance their clothes do not differ in a way a box classifier can hold onto, so the people at the car are reported as `Person`.

![The single model on a break-in frame. The people are called Person. Patches of tarmac are called Parking Space. Dissertation Figure 6.19.](images/report/single-model-test.jpg)

The boxes themselves taught the network the wrong pixels.

A staff-vest box was drawn around the torso, the arms, and the head, so "vest" included a person. A mask box was a small patch of face, which is only a few pixels when the person stands at the car. A door box included the glass, and therefore the legs, the hedge, and the glare behind the window. Parking boxes were copied from frame to frame and often contained a slice of car. Any visible door on a neighbouring car was called open, which would have raised a door alarm on a car nobody was touching.

![Rectangles on one frame. The vest box contains the person, the mask is a few pixels of face, and the parking label is a patch of tarmac. Dissertation, section 6.3.3.](images/report/loose-boxes.jpg)

![A closed door on the car to the left is reported as Door Open at 0.83. The rule "any open door is an alert" cannot sit on this output. Dissertation Figure 6.24.](images/report/false-door-open.jpg)

Masks were dropped for a second reason. A later requirement to wear one would have turned every visitor into a false alarm, and the mask is too small at this distance to be a reliable feature.

## 7. Three detectors: separate the objects, then write the rule

The repair had two parts. The labels were redrawn, and the classes were split across three YOLOv5m models so that a large car and a small jack did not have to share one set of features.

The new door label follows the car body and the lower panel of the door. The glass is left out, so the network is not asked to treat the person behind the window as part of the door. Slightly ajar doors were relabelled as closed, because the visible panel had barely changed. Number plates that had been boxed as rectangles, while the rest of the set was polygons, were redrawn; the mixed shapes had been stretching the plate box. The same footage was labelled three times, once for each model.

![The earlier rectangles: the door box takes in glass and tarmac, and the parking box is a loose quadrilateral. Dissertation Figure 6.26.](images/report/old-rectangles.jpg)

![The labels that were kept. Polygons follow the car, the open door panel, the plate, and the bay. Dissertation Figure 6.27.](images/report/new-polygons.jpg)

Each model is YOLOv5m, started from the official pretrained weights. The medium checkpoint was chosen because it has more layers than the nano and small variants. The dissertation records an image size of 1280×720, a batch size of 30, 70 epochs, and a 70/20/10 split. D1 and D2 were trained on about 800 images. The tools model was trained on about 1,200. Training ran on a Lambda Cloud A100. The recorded cost across two months was $90.21.

D2 was also trained at epoch counts from 30 to 120. Past 120 epochs the validation loss rose, so the 70-epoch run was kept. An earlier D2 run fired on vests that had been labelled too small; those boxes were removed.

| Model | Classes | What the alert code uses it for | Headline result |
| --- | --- | --- | --- |
| D1, vehicle | `Car door close`, `Car door open`, `number plate`, `parking` | Door state, and the plate crop that EasyOCR reads | All-class F1 0.98 at confidence 0.603. mAP at IoU 0.50 is 0.985. |
| D2, people | `Person`, `Security` | Who is at the car. Staff are the vest, not a face. | All-class F1 0.99 at confidence 0.653. mAP at IoU 0.50 is 0.994. |
| Tools | `Tools` (a car jack in the footage) | Whether a tool box meets the person and the car | mAP at IoU 0.50 is 0.984. Best F1 on the plot is 0.95 at confidence 0.631. |

Per-class average precision at IoU 0.50, read from the precision-recall legends:

| D1 | AP | D2 | AP |
| --- | --- | --- | --- |
| Car door close | 0.994 | Person | 0.995 |
| Car door open | 0.968 | Security | 0.992 |
| number plate | 0.988 | | |
| parking | 0.992 | | |

D1 confuses closed doors with open doors on about 2% of closed-door cases. On a 100-frame security clip the label counter agreed with the ground truth on 97% of plates, 97% of open doors, 94% of closed doors, and 93% of parking bays. D2's confusion matrix is 0.96 recall for both person and security, with 0.04 of staff called a person and 0.02 of people called staff. On the counter, security agreed 96% of the time and person 94%.

![D1 precision-recall curve. All-class mAP at IoU 0.50 is 0.985. Dissertation Figure 6.35.](images/report/d1-precision-recall.jpg)

![D2 confusion matrix. Person and security are both recalled at 0.96. Dissertation Figure 6.40.](images/report/d2-confusion.jpg)

![D2 precision-recall curve. All-class mAP at IoU 0.50 is 0.994. Dissertation Figure 6.42.](images/report/d2-precision-recall.jpg)

The tools model is the weak one, and the reason is size. A jack is small, and it gets smaller as the person walks away. While the jack is inside the car during a strike, the box disappears and the overlap with the ground truth falls to zero for those frames. The plot legend reports a best F1 of 0.95 at confidence 0.631. One sentence in the dissertation swaps those two numbers. The curve peaks near 0.95 and has already fallen by confidence 0.95, so the legend is the reading that matches the figure. On the 102-frame robber clip the counter tracked the tool on 90.78% of frames.

There is a second bookkeeping point. The dissertation evaluates a 70-epoch tools run. The zip stored next to the checkpoint is named `ToolJackOnly --batch 30 --epochs 30 BEST RESULT.zip`. The file to load is `best.pt` in that folder. The zip name is the only epoch count attached to that particular archive.

![Tools F1 against confidence. The score is high through the middle of the confidence range and collapses as the threshold becomes strict, which is what a small object tends to do. Dissertation Figure 6.45.](images/report/tools-f1.jpg)

![D1 on a held-out frame after the relabel: closed door 0.87, plate 0.96, both bays near 0.96. Dissertation Figure 6.32.](images/report/d1-result.jpg)

The alert script does not trust a single class. A door-open banner requires `Car door open` above 0.70. A person box is kept above 0.50, a vest above 0.60. Every box from the tools model is treated as a tool. The four messages are:

| Alert | Condition |
| --- | --- |
| Car door open | D1 reports an open door above 0.70. |
| Manual robbery | A person overlaps the car, the door is open, and today is not the booking end date. |
| Potential robbery | A tool box overlaps a person box. |
| Someone is breaking in | A tool box overlaps both the person and the car. |

That last pair of rules is the replacement for the robber class. A jack on the other side of the bay does not overlap the person, so it does not alarm. A person opening their own door on the booked day does not alarm. A person whose tool meets both them and the car does.

![The dashboard running the three models together. The frame shows a closed door, a person, and a tool, and the banner is POTENTIAL ROBBERY because those two boxes meet. The orange and green marks on the right are the top-down view of the car and the person. Dissertation Figure 7.9.](images/report/dashboard-alert.jpg)

The plate crop from D1 is read by EasyOCR, which was not trained for this project, and the text is matched to a booking so the alert can name the client. The top-down panel is a homography, a geometry step rather than a learned model.

Weights loaded by the dashboard:

| Model | Checkpoint |
| --- | --- |
| D1 | `All YOLOv5 Models/D1/best.pt` |
| D2 | `All YOLOv5 Models/D2/best.pt` |
| Tools | `All YOLOv5 Models/TOOLS/best.pt` |

The deployment scripts still contain absolute paths from the original machine. Those paths have to be pointed at the three files above.

## 8. Why this design, and not the others

| Question | Skeleton | Action classifier | One YOLOv5 | Three YOLOv5m models |
| --- | --- | --- | --- | --- |
| Can it see a door, a plate, and a jack? | No. Landmarks only. | No. One label for the whole second. | It has the classes, and they interfere. | Yes. One model each. |
| What happens on an empty bay? | A skeleton is drawn on the car. | A clip can be called normal. | Parking boxes appear on tarmac. | Parking and door classes still need a confidence gate. The empty-bay failure mode of the pose model is gone. |
| Did the headline score survive a new clip? | No. Light, clothing, and occlusion moved the joints. | No. Validation accuracy near 1.00, and the events on a one-minute video were short and late. | No official mAP was saved. The robber class agreed 44% of the time. | Yes on the held-out security and robber clips, with the jack as the weak class. |
| How is a thief declared? | Not implemented. | The class `abnormal`. | The class `Robber`. | Overlap of person, tool, and car, plus the booking date. |
| Could one person label the data? | No labels, and the output was not usable. | One-second clips took about four days and still needed a tripod reshoot. | About 900 images, with boxes that included the background. | The same footage, labelled three times as polygons. More drawing, much less ambiguity. |

The three-model design was kept because it was the only one that answered the original objectives with objects the camera can actually resolve. Staff are a vest. A break-in is a tool meeting a person and a car. An unexpected departure is an open door whose plate is not booked out today. Those are checks a rectangle overlap can make. "Suspicious posture" and "abnormal second" were not, on this data.

The cost of that choice is that the system only knows the objects it was shown. A hammer that does not look like the jack, a person at the rear of the car, or a side-on door in the aisle of Figure 3.3 is outside what these weights were measured on.

## 9. What was left unfinished

The conclusion checks the shipped system against the original requirements. The behaviour, robber, and staff requirements are marked done, on the strength of the multi-model evaluation in section 6.3.4. A model that keeps learning after deployment was not built. Parking-lot statistics were not added to the dashboard. Accessibility was not added to the client application.

Ian, of The Parking Consultancy Ltd, reviewed a demonstration. He treated per-bay monitoring as unusual in the market, and he named the deployment problems the model results already point at: a camera on every bay, the straight-on view, and GDPR if the system stores faces or plates. He suggested facial recognition as a way to cut false theft alerts, and he suggested trying the same idea on electric-vehicle charging bays. Facial recognition was not added. A check of the plate against the DVLA record of stolen plates was left as future work.

Those limits belong next to the metrics. mAP of 0.985 on a front-on bay is a real result. It is not a result about a multi-storey aisle filmed from one end.

## 10. Where to go next in this repository

| If you want | Open |
| --- | --- |
| Every class, threshold, and weight path | [MODELS.md](MODELS.md) |
| The three detectors and the alert rules | `MainProjectComponentsDevelopment/ModelDeployment/Model Deploy Alerts + OCR.py` |
| The YOLOv5 training notebook | `ModelTraning/Model-YOLOv5/YOLOv5ModelTrain.ipynb` |
| The action-classifier training script | `MainProjectComponentsDevelopment/LSTM + RCNN/Model Traning/LSTM + RCNN  Traning code.py` |
| The pose experiment | `MainProjectComponentsDevelopment/Skeleton Extraction/Skeleton extraction V2.py` |
| The label-count and overlap checks | `Model evaluation code` |

## Source

Singh, A. (2023). *Parking Security System For Detecting Abnormal Behaviour*. BSc dissertation, Department of Computer Science, University of Reading. Supervisor: James Ferryman. Submitted 1 May 2023.

Figures in this note are reproduced from that dissertation. They were extracted from the original PDF and reduced to 1400 pixels on the long side for the repository.
