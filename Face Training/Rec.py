
import cv2
#import os module for reading training data directories and paths
import os
#import numpy to convert python lists to numpy arrays as 
#it is needed by OpenCV face recognizers
import numpy as np


subjects = ["", "Lina", "Mazhar", "Rami", "Emma", "QueenBee" ]


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('/home/raspi3/catkin_ws/src/vision/Newtraining/haarcascade_frontalface_alt_pi.xml')

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    if (len(faces) == 0):
        return None, None

    (x, y, w, h) = faces[0]

    return gray[y:y+w, x:x+h], faces[0]

def prepare_training_data(data_folder_path):


    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    print dirs
    for dir_name in dirs:
        print dir_name
        if not dir_name.startswith("s"):
            continue;


        label = int(dir_name.replace("s", ""))
        print label

        subject_dir_path = "/home/raspi3/catkin_ws/src/vision/Newtraining/training-data/" + dir_name
        print subject_dir_path
        subject_images_names = os.listdir(subject_dir_path)


        for image_name in subject_images_names:

            if image_name.startswith("."):
                continue;


            image_path = subject_dir_path + "/" + image_name

            image = cv2.imread(image_path)

            #display an image window to show the image
            #cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
            #cv2.waitKey(100)


            face, rect = detect_face(image)


            if face is not None:
                #add face to list of faces
                faces.append(face)
                #add label for this face
                labels.append(label)

    #cv2.destroyAllWindows()
    #cv2.waitKey(1)
    #cv2.destroyAllWindows()

    return faces, labels



print("Preparing data...")
faces, labels = prepare_training_data("training-data")
print("Data prepared")

#print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))



face_recognizer = cv2.face.LBPHFaceRecognizer_create()


face_recognizer.train(faces, np.array(labels))
face_recognizer.write("/home/raspi3/catkin_ws/src/vision/Newtraining/piwe.xml")
print "weights done"
def draw_rectangle(img, rect):
    1+1
    
#function to draw text on give image starting from
#passed (x, y) coordinates. 
def draw_text(img, text, x, y):
    1+1


# First function `draw_rectangle` draws a rectangle on image based on passed rectangle coordinates. It uses OpenCV's built in function `cv2.rectangle(img, topLeftPoint, bottomRightPoint, rgbColor, lineWidth)` to draw rectangle. We will use it to draw a rectangle around the face detected in test image.
# 
# Second function `draw_text` uses OpenCV's built in function `cv2.putText(img, text, startPoint, font, fontSize, rgbColor, lineWidth)` to draw text on image. 
# 
# Now that we have the drawing functions, we just need to call the face recognizer's `predict(face)` method to test our face recognizer on test images. Following function does the prediction for us.

# In[9]:

#this function recognizes the person in image passed
#and draws a rectangle around detected face with name of the 
#subject
def predict(test_img):
    #make a copy of the image as we don't want to chang original image
    img = test_img.copy()
    #detect face from the image
    face, rect = detect_face(img)

    #predict the image using our face recognizer
    if not face is None:
        label, confidence = face_recognizer.predict(face)
    #get name of respective label returned by face recognizer
    label_text = subjects[label]
    
    #draw a rectangle around face detected
    draw_rectangle(img, rect)
    #draw name of predicted person
    draw_text(img, label_text, rect[0], rect[1]-5)
    
    return img

# Now that we have the prediction function well defined, next step is to actually call this function on our test images and display those test images to see if our face recognizer correctly recognized them. So let's do it. This is what we have been waiting for. 

# In[10]:

print("Predicting images...")

#load test images
test_img1 = cv2.imread("test-data/test1.jpg")
test_img2 = cv2.imread("test-data/test2.jpg")
test_img3 = cv2.imread("test-data/test3.jpg")

#perform a prediction
predicted_img1 = predict(test_img1)
predicted_img2 = predict(test_img2)
predicted_img3 = predict(test_img3)
print("Prediction complete")

#display both images
cv2.imshow(subjects[1], cv2.resize(predicted_img1, (400, 500)))
cv2.imshow(subjects[2], cv2.resize(predicted_img2, (400, 500)))
cv2.imshow(subjects[3], cv2.resize(predicted_img3, (400, 500)))

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.destroyAllWindows()





