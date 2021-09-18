# Let's Proctor 

## Aim 

To make a Screen Lock using Python (OpenCV and Tkinter).

![](https://cliply.co/wp-content/uploads/2019/03/371903161_BLINKING_EYE_400px.gif)


## About Application

This Application is made mainly using Python and OpenCV. Its extremely simple and easy to use application that can be very useful for teachers who wish to monitor students during exam. Here is a PDF link on how to use the app. http://letsproctor.herokuapp.com/info 

## Problem it solves
![](https://c.tenor.com/AKS0zwKDvMcAAAAd/mr-bean-exams.gif)

Currently due to lockdown scenario all exams are being held online. This exams are extremely difficult to be monitored and cheating is rampant. To solve this I have created a Application that can be used by Teachers to monitor students. Its simple and easy to use. Teachers have to provide a Google form link (I have purposely used that because teachers mostly use it) and App will send a Unique id to their email and also will be shown on screen. Then student has to download the tool and give all details including the unique id and start exam. After completion teacher can see the results in form of table. App will also provide screenshots since there are chances of false positive.


## Setup instructions / Requirements
For Teachers: Just a browser (Can be done from mobile to :))

For Students:
Install Python 3.7 +
Use Windows OS (exe works on windows only)

## Work Flow / Logic

- For Web part I have used HTML and CSS for frontend and Flask for backend.
- I have used Mongodb (pymongo) as database to store the entries of user.
- When User enters their detail of creating a test, I save all the details in database and create a unique id using uuid tool.
- This unique id is important and plays a major role in connecting student entries with the teacher's.
- Now in proctor.py file there are multiple things included. All the logic behind proctoring is declared there
- Lets go step by step
-   For Gaze detection I am using facemesh of mediapipe library and picking out both the eyes as ROI.
-   After doing that I am checking 4 pixels at some distance
-   If just one of the 4 pixels are black we can say that user has moved his eyes to one side and thus we can count it as violation ![](https://i.ibb.co/th4pb7r/image.png)
-   Then Next comes Face Detection. Again I am using mediapipe but a different solution which is face detect. Its pretty straight forward and in this we are getting points and calculating distances to check if head is tilted or not. Same solution is being used to detect whether face is present or not. Also if multiple faces are present ![](https://i.ibb.co/Ln9YXZG/image.png)
-   Tab Change Detection is done by leveraging selenium feature that is we can execute scripts into the console by doing driver.execute_script. So doing that I am able to run a javascript code that detects if the tab is visible or not. At start I have already declared a variable i and it is increased on tab change.
-   For Application Change I have Created a QRCode and it is created using the entries made by the user in the web app and its matched with entries made in proctor utility. Using pyautogui I take screenshot at regular intervals and if QR Code is seen nowhere in the screen Application Change is triggered.
-   Browser size is similar to tab change where I am running a javascript code in console.

## Output

![](https://i.ibb.co/4RXkxqF/image.png)
![](https://i.ibb.co/D7XyGtP/image.png)
![](https://i.ibb.co/SVqDfK4/image.png)
![](https://i.ibb.co/jr5mj6F/image.png)

## What I learned from this project?
I would say that in this project I learned a lot many things and also spend considerably longer time than other projects (don't know whether I am slow or project is big)
This project was like a big crossover movie for me where different powers are used.
<img src = "https://thumbs.gfycat.com/BogusWholeAuk-size_restricted.gif" width=250px></img>

I have got to learn libraries like Flask, OpenCV, Mediapipe, Pymongo (first time used mongodb), selenium etc. Also I loved to brainstrom over logic and ideas, like how can I use a external tool like Imgbb to upload images and retrieve them, use of qr code for application change, leveraging selenium to execute scripts in browser, sending emails to user etc. Even after this I am not much impressed actually because there are some false positives detected and bug occurs during runtime. I am constantly updating it and making corrections and this project will be improved in coming days.

With that I am also wondering that whether I can used node js to run all these processes in browser only and no requirement of external tool. Actually I started with node but I always find python more comfortable so sticked to python. So this is what my journey is about this project. This project is actually part of one hackathon and I hope I can improve it more.

## Author(s)

Tushar Vaman Amdoskar

Find me on Linkedin : https://www.linkedin.com/in/tushar-amdoskar/
Website: http://tusharamd.github.io/

Note: This is not Open Source Project, It is created for hackathon which will be commencing in few days
