import cv2
import mediapipe as mp
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import pymongo
import base64
import requests
import datetime
import os
import traceback
import numpy as np
import pyautogui

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['myFirstDatabase']
collection = db["Results_Proctoring"]


#### Global Variables ####
more_people_detected = 0
face_tilt_detected = 0
gaze_detected = 0
mouth_detected = 0
appchange_detected = 0
tabchange_detected = 0
windowsize_detected = 0

faceViolationTime = 0
tiltViolationTime = 0
gazeViolationTime = 0
mouthViolationTime = 0
appViolationTime = 0
windowViolationTime = 0

screenshotCounter = 0

#### User Data ####
stud_name = input("Please Enter Your Name : ")
roll_no = input("Please Enter Your Roll No : ")
stud_email_id = input("Please Enter Email Id : ")
unique_key = input("Please Enter Key for Exam : ")
#dicti = {"name":stud_name,"roll no":roll_no,"email id" : stud_email_id,"unique_id" : unique_key,"gaze":"0","headtilt":"0","people":"0","tabchange":"0", "mouthopen":"0", "imageurls":[]}

dicti = {"name":stud_name,"roll no":roll_no,"email id" : stud_email_id,"unique_id" : unique_key,"gaze":"0","headtilt":"0","people":"0","tabchange":"0", "application_change":"0", "browsersize":"0", "imageurls":[]}

filter = {"email id" : stud_email_id, "unique_id" : unique_key}
collection.insert_one(dicti)


#### Selenium Web app ####
options = Options
options.use_chromium = True
#options.addArguments("--disable-web-security")
#options.addArguments("--allow-running-insecure-content");

driver = webdriver.Edge (executable_path="msedgedriver.exe")#, options = options)
print(dir(webdriver.Edge))


# maximize with maximize_window()
driver.maximize_window()
driver.get("http://letsproctor.herokuapp.com/studentexamform")

for i in range(0,50):
    driver.execute_script("i=0")
#print(driver.get_window_size())
driver.execute_script("document.addEventListener('visibilitychange', event => { if (document.visibilityState == 'visible') { console.log(i) } else { i=i+1 }})")

def saveimage(violation_made):
    global filter,collection
    with open("fileupload.jpg", "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "c4b63af118f97f88cdeea980cdb4d6c9",
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
        uploaded_url = dict(res.json())["data"]["display_url"]
        newvalues = { "$push": { 'imageurls': [str(uploaded_url),violation_made] } }
        collection.update_one(filter,newvalues)
def circleDetect(img,x):
    img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray,40, 255, cv2.THRESH_BINARY)
    #print(blackAndWhiteImage.shape, blackAndWhiteImage[int(blackAndWhiteImage.shape[0]/2)][int(blackAndWhiteImage.shape[1]/3)])
    gray_blurred = cv2.blur(blackAndWhiteImage, (3, 3))
    detected_circles = cv2.HoughCircles(gray_blurred, 
                       cv2.HOUGH_GRADIENT, 1, 20, param1 = 30,
                   param2 = 20, minRadius = 5, maxRadius = 40)
                   
    if x == 1:
        #img = cv2.circle(img, (int(img.shape[1]/3),int(img.shape[0]/2)), 1, (255,255,0), 1)
        #img = cv2.circle(img, (int(img.shape[1]/2.5),int(img.shape[0]/2)), 1, (255,0,255), 1)
        #img = cv2.circle(img, (int(img.shape[1]-img.shape[1]/3),int(img.shape[0]/2)), 1, (255,255,0), 1)
        #img = cv2.circle(img, (int(img.shape[1]-img.shape[1]/2.5),int(img.shape[0]/2)), 1, (255,0,255), 1)
        
        #print(blackAndWhiteImage.shape,end = "\n")
        #print(int(img.shape[1]/3),int(img.shape[0]/2),"<<<<<<<<")
        
        #print(blackAndWhiteImage[int(img.shape[0]/3)][int(img.shape[1]/2)])
        
        li1 = []
        li1.append(blackAndWhiteImage[int(img.shape[0]/2)][int(img.shape[1]/3)])
        li1.append(blackAndWhiteImage[int(img.shape[0]/2)][int(img.shape[1]/2.3)])
        li1.append(blackAndWhiteImage[int(img.shape[0]/2)][int(img.shape[1]-img.shape[1]/2.3)])
        li1.append(blackAndWhiteImage[int(img.shape[0]/2)][int(img.shape[1]-img.shape[1]/3)])
        #print(li1)
        
        #img = cv2.circle(img, (int(img.shape[1]/3),int(img.shape[0]/2)), 1, (255,255,0), 1)
        #img = cv2.circle(img, (int(img.shape[1]/2.3),int(img.shape[0]/2)), 1, (0,0,255), 1)
        #img = cv2.circle(img, (int(img.shape[1]-img.shape[1]/2.3),int(img.shape[0]/2)), 1, (0,0,255), 1)
        #img = cv2.circle(img, (int(img.shape[1]-img.shape[1]/3),int(img.shape[0]/2)), 1, (255,255,0), 1)
        
        #cv2.imshow(f"Gray{x}", gray_blurred)
        #cv2.imshow(f"Detected Circle{x}", img)
    if x == 2:
        li2 = []
        li2.append(blackAndWhiteImage[int(img.shape[0]/2)][int(img.shape[1]/3)])
        li2.append(blackAndWhiteImage[int(img.shape[0]/2)][int(img.shape[1]/2.3)])
        li2.append(blackAndWhiteImage[int(img.shape[0]/2)][int(img.shape[1]-img.shape[1]/2.3)])
        li2.append(blackAndWhiteImage[int(img.shape[0]/2)][int(img.shape[1]-img.shape[1]/3)])
        #print(li2)
        #cv2.imshow(f"Gray{x}", gray_blurred)
        #cv2.imshow(f"Detected Circle{x}", img)
    
    try:
        return(li1)
    except:
        return(li2)
        
        
    '''    
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            #print(a,b)
            if x == 2:
                leftECentroid = (a,b)
                
            elif x == 1:
                rightECentroid = (a,b)
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
    '''
  
    



#### Proctoring ####
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh  # Face Mesh
mp_face_detection = mp.solutions.face_detection # Face Track
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) #Mesh
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7) # Track
while cap.isOpened():
    success, image = cap.read()
    half = cv2.resize(image, (0, 0), fx = 0.3, fy = 0.3)
    cv2.imshow(f"{stud_name}",half)
    height,width,_=image.shape
    if not success:
      print("Ignoring empty camera frame.")
      continue
    imagebb = image.copy()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = face_mesh.process(image)
    results2 = face_detection.process(image)
    image.flags.writeable = True
    
    ############ Check if face exists #################
    
    
    ### More than one Face ### done
    if results2.detections:
      #print(len(results2.detections))
      
      if len(results2.detections)>1 or len(results2.detections)< 1:
        #print(faceViolationTime)
        if faceViolationTime == 0:
            faceViolationTime = datetime.datetime.now()
            #print(faceViolationTime)
            more_people_detected = more_people_detected + 1 
            newvalues = { "$set": { 'people': more_people_detected } }
            collection.update_one(filter, newvalues)
            imagebb = cv2.putText(imagebb, 'More than One Person or No Face', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imwrite("fileupload.jpg",imagebb)
            saveimage("MultiFace")
            os.remove("fileupload.jpg")
            print("Multiple Faces Or No Faces")
        elif (datetime.datetime.now() - faceViolationTime).total_seconds() > 10:
            #print((datetime.datetime.now() - faceViolationTime).total_seconds())
            faceViolationTime = datetime.datetime.now()
            more_people_detected = more_people_detected + 1 
            newvalues = { "$set": { 'people': more_people_detected } }
            collection.update_one(filter, newvalues)
            imagebb = cv2.putText(imagebb, 'More than One Person', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imwrite("fileupload.jpg",imagebb)
            saveimage("MultiFace")
            os.remove("fileupload.jpg")
      else:
        faceViolationTime = 0   
        #print("More than one")
        
    #### more face exists ends ####    
        
        
      ### Face tilts ###   
      for detection in results2.detections:
        #mp_drawing.draw_detection(image, detection)
        for ids,landmrk in enumerate(detection.location_data.relative_keypoints):
            #print(ids,landmrk)
            #cv2.putText(image, str(ids), (int(landmrk.x*width),int(landmrk.y*height)), cv2.FONT_HERSHEY_SIMPLEX,0.3, (255,0,255), 1, cv2.LINE_AA)
            
            if ids == 2:
                nose = landmrk.x*width
            if ids == 4:
                leftCheekx = landmrk.x*width
                leftCheeky = landmrk.y*height
            if ids == 5:
                rightCheekx = landmrk.x*width
                rightCheeky = landmrk.y*height
            if ids == 0:
                FrightEyey = landmrk.y*height
            if ids == 1:
                FleftEyey = landmrk.y*height
            if ids == 3:
                mouth = landmrk.y * height
            
            try:
                #print(abs(rightCheeky-mouth))
                if leftCheekx > nose or rightCheekx < nose or (leftCheeky-FleftEyey)< -40 or (rightCheeky-FrightEyey) < -40 or abs(leftCheeky-mouth)<10 or abs(rightCheeky-mouth)<8:
                
                    if tiltViolationTime == 0:
                        tiltViolationTime = datetime.datetime.now()
                        face_tilt_detected = face_tilt_detected + 1
                        newvalues = { "$set": { 'headtilt': face_tilt_detected } }
                        collection.update_one(filter, newvalues)
                        imagebb = cv2.putText(imagebb, 'Face Tilt Detected', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                        cv2.imwrite("fileupload.jpg",imagebb)
                        saveimage("Face Tilts")
                        os.remove("fileupload.jpg")
                        print("Face Tilts")
                    elif (datetime.datetime.now() - tiltViolationTime).total_seconds() > 10:
                        tiltViolationTime = datetime.datetime.now()
                        face_tilt_detected = face_tilt_detected + 1
                        newvalues = { "$set": { 'headtilt': face_tilt_detected } }
                        collection.update_one(filter, newvalues)
                        imagebb = cv2.putText(imagebb, 'Face Tilt Detected', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                        cv2.imwrite("fileupload.jpg",imagebb)
                        saveimage("Face Tilts")
                        os.remove("fileupload.jpg")
                        print("Face Tilts")
                        
                    #print("t \n")
                    #print("a")
                else:
                    tiltViolationTime = 0
                    
            except Exception as e:
                #print(e)
                pass
        #cv2.imshow("frame2",image)
        
        #### Face tilts ends ####
    else:
        if faceViolationTime == 0:
            faceViolationTime = datetime.datetime.now()
            #print(faceViolationTime)
            more_people_detected = more_people_detected + 1 
            newvalues = { "$set": { 'people': more_people_detected } }
            collection.update_one(filter, newvalues)
            imagebb = cv2.putText(imagebb, 'More than One Person or No Face', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imwrite("fileupload.jpg",imagebb)
            saveimage("MultiFace")
            os.remove("fileupload.jpg")
            print("Multiple Faces Or No Faces")
        elif (datetime.datetime.now() - faceViolationTime).total_seconds() > 10:
            #print((datetime.datetime.now() - faceViolationTime).total_seconds())
            faceViolationTime = datetime.datetime.now()
            more_people_detected = more_people_detected + 1 
            newvalues = { "$set": { 'people': more_people_detected } }
            collection.update_one(filter, newvalues)
            imagebb = cv2.putText(imagebb, 'More than One Person', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imwrite("fileupload.jpg",imagebb)
            saveimage("MultiFace")
            os.remove("fileupload.jpg")
    
    #### Gaze Detection ####
    
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image2 = imagebb.copy()

    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        
        #mp_drawing.draw_landmarks( image=image, landmark_list=face_landmarks,connections=mp_face_mesh.FACEMESH_CONTOURS, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
        for ids,landmrk in enumerate(face_landmarks.landmark):
            #print(ids,landmrk)
            #if ids >12 and ids<15:
                #cv2.putText(image, str(ids), (int(landmrk.x*width),int(landmrk.y*height)), cv2.FONT_HERSHEY_SIMPLEX,0.3, (255,0,255), 1, cv2.LINE_AA)
            
            
            if ids == 398 or ids == 359 or ids == 374 or ids == 386:
                #cv2.putText(image, str(ids), (int(landmrk.x*width),int(landmrk.y*height)), cv2.FONT_HERSHEY_SIMPLEX,0.3, (255,0,255), 1, cv2.LINE_AA)
                if ids == 398:
                    rightEyex1 = int(landmrk.x*width)
                    #print(rightEyex1)
                if ids == 359:
                    rightEyex2 = int(landmrk.x*width)
                    #print(rightEyex2,"rightEyex2")
                if ids == 374:
                    rightEyey1 = int(landmrk.y*height)
                    #print(rightEyex2,"rightEyex2")
                if ids == 386:
                    rightEyey2 = int(landmrk.y*height)
                    #print(rightEyex2,"rightEyex2")
            if ids == 33 or ids == 145 or ids == 173 or ids == 159:
                #cv2.putText(image, str(ids), (int(landmrk.x*width),int(landmrk.y*height)), cv2.FONT_HERSHEY_SIMPLEX,0.3, (255,0,255), 1, cv2.LINE_AA)
                if ids == 33:
                    leftEyex1 = int(landmrk.x*width)
                    #print(leftEyex1)
                if ids == 173:
                    leftEyex2 = int(landmrk.x*width)
                    #print(leftEyex2,"rightEyex2")
                if ids == 145:
                    leftEyey1 = int(landmrk.y*height)
                    #print(leftEyey1,"leftEyey1")
                if ids == 159:
                    leftEyey2 = int(landmrk.y*height)
                    #print(leftEyey2,"leftEyey2")
                    
            if ids == 13 or ids ==14:
                cv2.putText(image, str(ids), (int(landmrk.x*width),int(landmrk.y*height)), cv2.FONT_HERSHEY_SIMPLEX,0.3, (255,0,255), 1, cv2.LINE_AA)
                #print(landmrk.x*width,landmrk.y*height)
                if ids == 13:
                    upperLip = landmrk.y*height
                if ids == 14:
                    lowerLip = landmrk.y*height
            
            try:
                roiImage = image[rightEyey2:rightEyey1,rightEyex1:rightEyex2]
                roiImage2 = image[leftEyey2:leftEyey1,leftEyex1:leftEyex2]
                #print(image.shape)
                
                eyeone = circleDetect(roiImage,1)
                eyetwo = circleDetect(roiImage2,2)
                
                if eyeone.count(0) and eyetwo.count(0) == 1:
                    if gazeViolationTime == 0:
                        gazeViolationTime = datetime.datetime.now()
                        gaze_detected = gaze_detected + 1
                        newvalues = { "$set": { 'gaze': gaze_detected } }
                        collection.update_one(filter, newvalues)
                        imagebb = cv2.putText(imagebb, 'Eyes not on screen', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                        cv2.imwrite("fileupload.jpg",imagebb)
                        saveimage("Eyes not on screen")
                        os.remove("fileupload.jpg")
                        print("Eyes not on screen")
                    elif (datetime.datetime.now() - gazeViolationTime).total_seconds() > 10:
                        gazeViolationTime = datetime.datetime.now()
                        gaze_detected = gaze_detected + 1
                        newvalues = { "$set": { 'gaze': gaze_detected } }
                        collection.update_one(filter, newvalues)
                        imagebb = cv2.putText(imagebb, 'Eyes not on screen', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                        cv2.imwrite("fileupload.jpg",imagebb)
                        saveimage("Eyes not on screen")
                        os.remove("fileupload.jpg")
                        print("Eyes not on screen")
                else:
                    gazeViolationTime = 0
                    
                #### Gaze Detection Complete ####
                
                '''
                #### Mouth Open Close ####
                
                #print(abs(upperLip - lowerLip))
                if abs(upperLip - lowerLip) > 20:
                    if mouthViolationTime == 0:
                        mouthViolationTime = datetime.datetime.now()
                        mouth_detected = mouth_detected + 1
                        newvalues = { "$set": { 'mouthopen': mouth_detected/5 } }
                        collection.update_one(filter, newvalues)
                        imagebb = cv2.putText(imagebb, 'Mouth Open Close', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                        cv2.imwrite("fileupload.jpg",imagebb)
                        saveimage()
                        os.remove("fileupload.jpg")
                    elif (datetime.datetime.now() - mouthViolationTime).total_seconds() > 10:
                        mouthViolationTime = datetime.datetime.now()
                        mouth_detected = mouth_detected + 1
                        newvalues = { "$set": { 'mouthopen': mouth_detected/5 } }
                        collection.update_one(filter, newvalues)
                        imagebb = cv2.putText(imagebb, 'Mouth Open Close', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                        cv2.imwrite("fileupload.jpg",imagebb)
                        saveimage()
                        os.remove("fileupload.jpg")
                    
                #### Mouth Ends ####
                
                '''
                
                #cv2.imshow("Right Eye",roiImage)
                #cv2.imshow("Left Eye",roiImage2)
            except Exception as e:
                #print(traceback.format_exc())
                pass
    #cv2.imshow('FaceMesh', image)
    
    
    #### Application Change ####
    
    if screenshotCounter >=10:
        imageSS = pyautogui.screenshot()
        imageSS = cv2.cvtColor(np.array(imageSS),cv2.COLOR_RGB2BGR)
        qrCodeDetector = cv2.QRCodeDetector()
        val,points,straight_qrcode = qrCodeDetector.detectAndDecode(imageSS)
        
        
        decoded_text = val.split()
        if(len(decoded_text)<2):
            decoded_text = ["0","0"]
        
        
        if dicti["email id"] != decoded_text[0] or dicti["unique_id"] != decoded_text[1]:
            if appViolationTime == 0:
               appViolationTime = datetime.datetime.now()
               appchange_detected = appchange_detected + 1
               newvalues = { "$set": { "application_change": appchange_detected } }
               collection.update_one(filter, newvalues)
               imageSS = cv2.putText(imageSS, 'App Changed', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
               cv2.imwrite("fileupload.jpg",imageSS)
               saveimage("Application Changed")
               os.remove("fileupload.jpg")
               print("Application Changed")
            elif (datetime.datetime.now() - appViolationTime).total_seconds() > 10:
               appViolationTime = datetime.datetime.now()
               appchange_detected = appchange_detected + 1
               newvalues = { "$set": { "application_change": appchange_detected } }
               collection.update_one(filter, newvalues)
               imageSS = cv2.putText(imageSS, 'App Changed', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
               cv2.imwrite("fileupload.jpg",imageSS)
               saveimage("Application Changed")
               os.remove("fileupload.jpg")
               print("Application Changed")
               
        else:
            pass
            
        screenshotCounter = 0
    else:
        screenshotCounter = screenshotCounter+1
        
    #### Application Change Closes ####
    
    #### Tab Change ####
    
    
    
    #print(tabchange_detected)
    try:
        temp = driver.execute_script("return i")
        if temp != tabchange_detected:
            tabchange_detected = temp
            newvalues = { "$set": { "tabchange": tabchange_detected } }
            collection.update_one(filter, newvalues)
            imageSS = cv2.putText(imageSS, 'Tab Changed', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imwrite("fileupload.jpg",imageSS)
            saveimage("Tab Changed")
            print("Tab Changed")
    except:
        pass
    #### Tab Change Done ####
    
    #### Window size ####
    try:
        temp = driver.execute_script("return 100*(window.innerWidth*window.innerHeight)/(screen.width*screen.height)")
    except:
        pass
    
    if int(temp)<70:
        if windowViolationTime == 0:
           windowViolationTime = datetime.datetime.now()
           windowsize_detected = windowsize_detected + 1
           newvalues = { "$set": { "browsersize": windowsize_detected } }
           collection.update_one(filter, newvalues)
           imageSS = cv2.putText(imageSS, 'Window Size', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
           cv2.imwrite("fileupload.jpg",imageSS)
           saveimage("Window Size Issue")
           os.remove("fileupload.jpg")
           print("Wrong window size")
        elif (datetime.datetime.now() - windowViolationTime).total_seconds() > 10:
           windowViolationTime = datetime.datetime.now()
           windowsize_detected = windowsize_detected + 1
           newvalues = { "$set": { "browsersize": windowsize_detected } }
           collection.update_one(filter, newvalues)
           imageSS = cv2.putText(imageSS, 'Window Size', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
           cv2.imwrite("fileupload.jpg",imageSS)
           saveimage("Window Size Issue")
           os.remove("fileupload.jpg")
           print("Wrong window size")
        else:
            windowViolationTime = 0

    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()