# NaloxSAVER

## Motivation
In 2024, the Centers for Disease Control and Prevention (CDC) estimated that over 105,000 people in the U.S. died from drug overdoses. Opioid overdoses occurs when there are so many drugs in the body that the individual becomes unresponsive and cannot breathe on their own. After 3-5 minutes without oxygen, brain damage begins, soon followed by death. Survival in the event of an opioid overdoses depends solely on getting oxygen to the brain. There is however a life saving drug, naloxone, that if administered within this critical three-minute period can reverse the effects of an overdose. 

Detecting an overdose can be difficult, with symptoms including unresponsiveness and slowed, shallow, or stopped breathing. It is often challenging to distinguish if a person is sleeping or overdosing in public settings.

Numerous efforts have been made by the White House and public health organizations throughout the opioid epidemic. A barrier to many of the previous approaches is that many individuals who would benefit from them are not in the mental or physical state to utilize them. 

Our product aims to address these shortcomings and introduce a new technology to automate overdose detection.  

## NaloxSAVER Product

NaloxSAVER is a web interface program that incorporated thermal infrared and RGB camera footage to track individuals breathing patterns and alert of possible overdoses in public spaces. 

NaloxSAVER is designed to be installed in public spaces, such as train cars or public libraries. The system includes a tablet interface with a live video stream interface, a naloxone dispenser located next to the tablet, and two stacked cameras (thermal and RGB) to monitor passengers' breathing patterns. Each passenger's nose region and average temperature are tracked every second and stored internally. By detecting temperature changes between frames, the system can identify individuals experiencing a potential overdose and trigger an alarm.  

The interface features a large screen with a live video feed, a "turn off alarm" button, and a "Narcan instructions" button. When an overdose is detected, the screen perimeter will blink red and white, accompanied by an alarm to alert bystanders. Users can click the "Narcan instructions" button to view an informational video from the CDC on administering the drug.

### Software
For our thermal infrared camera, we used Hikmicro's Pocket2 which has a resolution of 49,152 pixels with a 50° × 37.2° field of view. For the RGB camera, we used a full HD 1080p compact webcam. We aligned our thermal and RGB cameras on the same plane and matched the zoom levels to our best ability. This alignment was achieved through adjustments in x-offset, y-offset, and zoom. Both cameras are kept in a static position to ensure these variables remain constant in each frame.

For facial recognition, we used Google's open-source model, Mediapipe. Mediapipe plots six key landmarks on the face (eyes, ears, nose, and mouth), which allowed us to extract only the nose point. We then overlaid these coordinates onto the thermal camera footage to calculate temperature data via our pixel color conversion equation. 

To make NaloxSAVER technology more versatile and applicable to a public space, we created a "person" class within our program that allowed the system to track multiple people and store their temperature history simultaneously. Instances of the person class are maintained and updated relative to the subjects last detected position. As long as a person stays within 75 pixels of their last detected location, the same instance will be update. If the person was not detected for more than 10 seconds (ie. moved outside 75 pixels), their instance was deleted from the people list to increase the overall efficiency of the program. 

To detect an overdose, we measure the average temperature around a person's nose once per second and store this data in memory. We compare each new temperature measurement with the previous one. If the temperature difference is less than 0.125°C, it indicates no breathing was detected. If this condition persists for seven consecutive seconds, we determine that the person is having an overdose and trigger the alarm. However, if the temperature difference exceeds 0.125°C at any point, the counter resets to 0, because breathing has been detected then the overdose detection process starts over.
<img src="Website_Collage.png">

### Hardware 
In addition to our software detection interface, we created 3D models to hold the camreras in a static position and a naloxone dispenser. Our naloxone dispenser was inspired by a candy dispenser and fit to the dimensions of Narcan nasal spray units The tablet holder dimensions are based on an Amazon Fire tablet, and the dispenser is designed to fit ten Narcan nasal spray units. 
<img src="SetUp_Image.png">
<img src="CameraCloseUp.png">

## Testing
To test the accuracy of our product, we performed six rounds of breathing exercises at three different distances (1ft, 3ft, 5ft). The tests are structured as follows: 
    \item Participant holds their breathe for 30 seconds, with the intention of death detection
    \item 10 second rest and reset period 
    \item Participant breathes normally for 30 seconds, with the intention of no death detection
    \item 10 second rest and reset period 
<img src="Flowcharts.png">

We recorded the results in a binary confusion matrix and calculated accuracy along with pixel coverage. The confusion matrix also allowed us to easily identify type I and II errors.