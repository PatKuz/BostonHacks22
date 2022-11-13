# BostonHacks22
here we go again.

### Submission Tracks
- Innovation with AI (Main Track)
- FFD 2 (Gamified Methods)
- Best Use of Twilio
- Best Use of CockroachDB

## Inspiration
- Based on our own experiences moving in and out of college, going home for the holidays, various breaks, or even on trips with friends, we noticed just how tired one can get trying to get from one place to another. This drowsiness often comes with the occasional “extended blink,” or yawn, but can quickly evolve into a catastrophe. Looking up the statistics, we were shocked to see that “drowsy driving accounts for about 100,000 crashes, 71,000 injuries and 1,550 fatalities [annually], according to the National Safety Council (NSC).” And so, we wanted to propose a solution to such a preventable problem: HighwayPatrol.

## What it does
- HighwayPatrol uses a custom trained AI model to detect visual signs of a sleepy or impaired driver and count elapsed time during which safe driving is occurring. Using an account tied to a phone number, users accumulate safe driving time, which shows up on a global leaderboard to encourage safe behavior. Upon detecting unsafe driving, emergency contacts are pinged, and the driver is reminded to pull over and rest. Leaderboard updates are also issued by text to a user with leaderboard movement after a driving session ends.

## How we built it
### AI Model
- We developed two models for drowsiness detection in the TensorFlow Keras library, which detect whether the subject’s eyes are open or closed, or whether the subject is yawning (i.e. mouth open), respectively. Both models use standard CNN architectures which include 3x3 convolutional layers and 2x2 pooling layers, followed by dense layers with dropout and gradient clipping for training stability. Both take as input a 100x100 bounding box of the subject’s face, which for our proof of concept is extracted at inference time from a webcam using OpenCV. The bounding box is found using a recent pre-trained deep neural network for face detection called YuNet. The eye open/close model uses the Closed Eyes in the Wild dataset, which contains ~2400 pictures of faces from various angles with eyes either opened or closed. The yawning dataset uses the yawning / no yawning image categories for a total of ~1500 images from a dataset on drowsiness detecting specific to driving. For this we apply the same bounding box preprocessing step as for inference. The result of these two models on a face input is a prediction score ranging from 0 -> 1, which represents Closed Eyes -> Open Eyes and Yawning ->  No Yawning, respectively. Finally to detect drowsiness, we use a manual aggregation method which sends an alert that the driver may be falling asleep when multiple sustained open mouths (yawns) or eyelid closings are detected over a period of 30 seconds. Both of these are events are determined based on the relative change in prediction scores from the model over several consecutive frames.

### Frontend
- The frontend is built out of a combination of pure HTML/CSS and React, giving our users a visually appealing experience.

### Backend
- The backend is built using flask on python. All data processing and RESTful endpoints are set up using flask. 

### Twilio 
- We make use of Twilio for user verification and authentication on new accounts and for existing logins. All users will be greeted by a phone number login/verification process upon visiting the webapp. If the number is not associated with an existing user, the user will need to complete the account creation process. Otherwise, login is complete and the user is brought to a dashboard. Twilio is also used to text emergency contacts certain information in the case where unsafe driving is detected, as well as issuing personal leaderboard updates after a drive is complete. Finally, we also use Twilio to ping the driver if impaired driving is detected.

### CockroachDB
- For account storage and our statistics/leaderboard, we use a couple tables within a  CockroachDB instance. These tables are queried and updated whenever a user logs in, creates a new account, starts and ends a drive, and requests leaderboard statistics on the dashboard page.

## Challenges we ran into
- We had a lot of trouble displaying a video feed on our site given the processing that we wanted to do on the live video. It needed to not be stuttery so it was visually appealing while also producing images usable by our AI model. This took a lot of time.
- CockroachDB had some setup and connection issues that we were able to iron out.

## Accomplishments that we're proud of
- We are extremely proud that we were able to train a model in such a short amount of time that is reasonably good at detecting drowsy driving. We are also very happy with the expansive use of Twilio for messaging and interactivity with the user. Most of all, however, we underestimated the difficulty of linking video on a react webpage, to our trained ML model on the backend. To say we were happy to see a video of a box around our face would be an understatement.

## What we learned
- We have had a great deal of learning in our four years at BU, and BostonHacks22 was no different. With the application of new technologies like CockroachDB and Tensorflow/OpenCV, to those more familiar like Twilio, this year’s hackathon was a learning experience through and through.

## What's next for HighwayPatrol
- Next for HighwayPatrol would be to put this webapp into a mobile form that could sit in the background of a phone and have navigation displayed. We also want to give the driver more options if sleepiness or impairment is detected, such as on-demand navigation to the nearest hotel or rest area.

