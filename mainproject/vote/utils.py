import cv2,os
import numpy as np
from PIL import Image
''' face capture '''
def capture(user_id):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640) #video width
    cam.set(4, 480) #video height
    face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

    face_id = user_id

    print("\n Initializing face capture. Please look at the camera...")
    #individual sampling face count
    count = 0

    while(True):

        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1

            # Saving the captured images into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff 
        if k == 27:
            break
        elif count >= 30: #no of samples
            break

    print("\n Exiting ")
    cam.release()
    cv2.destroyAllWindows()
    return "done"
'''trainer to train the collected pictures '''

def train_model():
    path = 'dataset'

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml');

    # function to get the images and label data
    def getImagesAndLabels(path):

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)

            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

        return faceSamples,ids

    print ("\n Training faces. Please Wait")
    faces,ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))

    #save trained model
    recognizer.write('trainer/trainer.yml') 

    print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))

'''final recognizer'''

def recognize():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "Cascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0
    errcount = 0

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cam.set(3, 640) #widht
    cam.set(4, 480) #height

    #min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    ret, img =cam.read()
    

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        #confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            confidence = "  {0}%".format(round(100 - confidence))
            cv2.destroyAllWindows()
            return id
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            errcount+=1
            if(errcount>10):
                return False
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img)


    # recognizer = cv2.face.LBPHFaceRecognizer_create()
    # recognizer.read('trainer/trainer.yml')
    # cascadePath = "Cascades/haarcascade_frontalface_default.xml"
    # faceCascade = cv2.CascadeClassifier(cascadePath);

    # font = cv2.FONT_HERSHEY_SIMPLEX

    # #iniciate id counter
    # id = 0


    # names = ['None',"amith",'None','None','None','AMITH'] 

    # # Initialize and start realtime video capture
    # cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    # cam.set(3, 640) #widht
    # cam.set(4, 480) #height

    # #min window size to be recognized as a face
    # minW = 0.1*cam.get(3)
    # minH = 0.1*cam.get(4)

    # while True:

    #     ret, img =cam.read()
        

    #     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #     faces = faceCascade.detectMultiScale( 
    #         gray,
    #         scaleFactor = 1.2,
    #         minNeighbors = 5,
    #         minSize = (int(minW), int(minH)),
    #     )

    #     for(x,y,w,h) in faces:

    #         cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

    #         id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

    #         #confidence is less them 100 ==> "0" is perfect match 
    #         if (confidence < 100):
    #             id = names[id]
    #             confidence = "  {0}%".format(round(100 - confidence))
    #         else:
    #             id = "unknown"
    #             confidence = "  {0}%".format(round(100 - confidence))
            
    #         cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
    #         cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
    #     cv2.imshow('camera',img) 

    #     k = cv2.waitKey(10) & 0xff 
    #     if k == 27:
    #         cv2.destroyAllWindows()
    #         cam.release()
    #         break  
    # pid=os.getpid()   
    # return (pid)

# # from FaceRecogFINAL import recognize
# import FaceCapture
# import signal,os
# from Trainer import train
# # output=FaceCapture.capture()
# # # print(output)
# # output=train()
# pid=FaceCapture.capture() #   recognize()
# os.kill(pid, signal.SIGTERM)
# print(output)

# import signal,os
# from Trainer import train
# pid=train()
# os.kill(pid, signal.SIGTERM)
# print(output)


# import signal,os
# from FaceRecogFINAL import recognize
# pid=recognize()
# os.kill(pid, signal.SIGTERM)

