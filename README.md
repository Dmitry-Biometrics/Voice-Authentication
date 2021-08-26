# Voice-Authentication
Biometric voice authentication "OWN/ALLIEN" using a passphrase
The main file for interpreting the layout is called «Voice_Auth_With_Password.py». When the script is launched, the speech-to-text model is initialized and the main program window is launched (Figure 1).
![image](https://user-images.githubusercontent.com/16018075/131023231-e4e770d3-8e91-4f56-8fd0-f77d5cdd9fe6.png)
Figure 1 - The main window of the layout 
Before starting to work with the program, you need to make sure that the microphone is working and positioned. It is recommended to take images in a quiet room, or from a microphone without an amplifier, so that in silence there is a band that fluctuates around zero. Next, you need to make sure the loudness of the pronunciation so that the final image does not turn out to be too loud or too quiet (Figure 2). If the signal goes beyond the window, you need to move the main microphone away from you, otherwise - move closer to it.
![image](https://user-images.githubusercontent.com/16018075/131023330-e54077d7-fa18-45d3-9a37-54a77b40ca1e.png)
Figure 2 - Checking the microphone volume level 
In the middle of the lower part of the window there is a record button with a microphone icon “Record image”. When you click on it, the recording starts. To end the recording, you must click on the same modified button "Stop recording" (Figure 3) 
![image](https://user-images.githubusercontent.com/16018075/131023362-a4a4ac48-e3d7-495d-9731-d6bbbd2618fb.png)
Рисунок 3 – Остановка записи
After the end of the recording, the recorded image will appear on the right side of the layout, which you can listen to, view the .wav-form and delete if the image is unsuccessful for some reason. You can listen to each image and make sure that the passphrase is pronounced correctly and that there is no interference. Also, if the image signal goes beyond the window, it means that the user is speaking too loudly into the microphone.
Having accumulated the training sample (8-16 images), you can visually check all the images on one screen by clicking on the button "Display .wav-forms of images" (example - Figure 4).
![image](https://user-images.githubusercontent.com/16018075/131023403-5c3f4712-602e-47f9-ba0e-71b1f2285340.png)
Figure 4 - Examples of .wav-form output of images
By clicking on the "Biometric parameters" button (Figure 5), we go to the graphical view of the biometric parameters extracted from the recorded images. 
![image](https://user-images.githubusercontent.com/16018075/131023423-ef481a02-c653-4383-ad13-b7b3536dd37e.png)
Figure 5 - Button for viewing biometric parameters 
This button can be useful for a researcher to compare biometric parameters. An example of the main window is shown in Figure 6.
![image](https://user-images.githubusercontent.com/16018075/131023448-621fa74e-85ed-4bbc-bab3-ad830f7c2433.png)
Figure 6 - Main window of graphic demonstration of biometric parameters 
The right side offers a choice of "radio buttons", by clicking on which you can view all types of biometric parameters used in the system: 
1) chalk frequency coefficients (MFC); 
2) spectral power chromogram; 
3) spectrogram in chalk scale; 
4) spectral contrast; 
5) tonal features of the centroid. 
An example of changing biometric parameters - Figure 7.
![image](https://user-images.githubusercontent.com/16018075/131023466-d727fb8a-1638-43fc-819c-9932a5d0110f.png)
Figure 7 - Examples of coefficients in chalk-scale
To view biometric parameters on one chart, click on the "View" tab and select "On one chart" (Figure 8)
![image](https://user-images.githubusercontent.com/16018075/131023488-a5f177e5-370c-4b32-81a3-beb9ed6ac4c9.png)
Figure 8 - View of viewing biometric parameters on one graph 
When you click on the button, a graph will be displayed (example Figure 9). In this graph, each image is marked with a different color.
![image](https://user-images.githubusercontent.com/16018075/131023538-975bc972-b148-4db1-a081-df02f574c31b.png)
Figure 9 - An example of displaying "on one chart" 
Using this view, you can conduct research on environmental influences, microphone variations, illness, atmospheric pressure on biometric parameters.
When you click on the "Get the distribution of images" button, a window appears with a view of the following distributions variations:
1) One's OWN relative to all one's own;
2) One's OWN relative to each other;
3) ALL ALLIENCES relative to each other;
4) One's OWN relative to ALL ALLIENCES;
The malefactor in relation to all OWN Window example - Figure 10
![image](https://user-images.githubusercontent.com/16018075/131023577-27fdb0e5-eb5b-407f-ab8e-f0fa357342ec.png)
Figure 9 - An example of displaying "on one chart" 
Using this view, you can conduct research on environmental influences, microphone variations, illness, atmospheric pressure on biometric parameters.
When you click on the "Get the distribution of images" button, a window appears with a view of the following distributions variations:
1) One's OWN relative to all one's own;
2) One's OWN relative to each other;
3) ALL ALLIENCES relative to each other;
4) One's OWN relative to ALL ALLIENCES;
The malefactor in relation to all OWN Window example - Figure 10
![image](https://user-images.githubusercontent.com/16018075/131023630-8e71377b-6353-4ba4-815e-e06ff1f8d991.png)
Figure 10 - An example of a window for viewing the distribution of images
Using this window, you can determine whether there are “bad” images in the training sample (records with interference, excess noise). You can also be convinced of the normal distribution of "Own" and its remoteness from the images of "All ENEMIES". Also, when choosing the fifth item, the images are compared with the images of an outsider, which are located in the internal directory in the "ENEMY" folder.
The "Add Images" button at the bottom right of the main menu allows you to download images from any source in the ".wav" format.
Below, the button “Normalize images” is intended for normalizing the added images by volume level.
By clicking on the "Train the network" button, go to the demo user authentication window - Figure 11.
![image](https://user-images.githubusercontent.com/16018075/131023660-d1abef2e-b126-45b2-81c0-292b5eb1e5f6.png)
Figure 11 - User authentication window
In this window, when you click on the "Authentication" button, recording will start from the microphone, at which point the user must say a passphrase. Next, a message box will appear with the result of authentication "OWN" - in case of success, and "ALIEN" - if the program did not recognize the user, or the user is different, or an incorrect passphrase is named. Also, the message will display the value of the weighted Euclidean distance and the translated text of the phrase. The decision threshold is configured in the "bio_params_view.py" file in the get_porog function. The threshold depends on the length of the phrase, the nature of the person himself, the environment at the time of authentication. An example of a message output is shown in Figure 12.
![image](https://user-images.githubusercontent.com/16018075/131023699-7929ba26-11da-4dfb-8db1-7b39a0a85988.png)
Figure 12 - An example of the authentication result
When you click on the "Voice password options" button, a window will be displayed with the source phrases translated into the text and possible tokens for each word (example - Figure 13).
![image](https://user-images.githubusercontent.com/16018075/131023788-16ae7f7d-47a3-4093-a4f6-9aa220886793.png)
Figure 13 - Examples of variations of passphrases
Pressing the button "Biometric parameters" will display the already described window for graphical viewing of biometric parameters with the last added image submitted for authentication (example - Figure 14).
![image](https://user-images.githubusercontent.com/16018075/131023824-8544621f-b37a-4ba9-9ac3-a3009d96ad8f.png)
Figure 14 - An example of training images and image submitted for authentication 
Using this item, you can see in what types of biometric parameters the new image differs / converges with the images submitted for training.
If the image has not passed authentication (has too great a distance) - there is a button "additional training", when you click on which, the statistics of the training sample will be updated taking into account the last image.
