import cv2
import os
import os.path
import base64
import json
import time
import numpy as np
import face_recognition


# Extracting Faces from Images or ID Cards
def Extract_Faces(file, filename, model):
    count = 0
    file_name, file_extension = os.path.splitext(file)
    if (file_extension in ['.png', '.jpg', '.jpeg', '.JPG']):
        while not os.path.exists(file):
            time.sleep(3)
        image = cv2.imread(file)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (103.93, 116.77, 123.68), False)
        model.setInput(blob)
        detections = model.forward()
        for i in range(0, detections.shape[2]):
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            confidence = detections[0, 0, i, 2]
            if (confidence > 0.5):
                count = count + 1
                frame = image[startY:endY, startX:endX]
                # Storing faces into 'temp' folder
                cv2.imwrite("temp/" + str(i) + '_' + filename, frame)
    return count


# checking file extensions and models for face detections
def checkImage(image):
    if not os.path.exists('temp'):
        os.makedirs('temp')
    base_dir = os.path.dirname(__file__)
    prototxt_path = os.path.join(base_dir + '/../models/deploy.prototxt')
    caffemodel_path = os.path.join(base_dir + '/../models/weights.caffemodel')
    model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
    file_name = image
    file_Name, file_extension = os.path.splitext(file_name)
    file = file_name.split("/")[-1]
    if(file_extension != ".jpg" and file_extension != ".png" and file_extension != ".jpeg" and file_extension != ".JPG"):
        file_name = image
        file = file_name.split("/")[-1]
    count = Extract_Faces(file_name, file, model)
    return count


# Comparing faces which is extracted from images in OPenCV
def Compare_Faces(filename1, filename2):
    picture_of_aadhar = face_recognition.load_image_file(filename1)
    try:
        aadhar_face_encoding = face_recognition.face_encodings(picture_of_aadhar)[0]
    except:
        pass
    picture_of_pan = face_recognition.load_image_file(filename2)
    try:
        pan_face_encoding = face_recognition.face_encodings(picture_of_pan)[0]
    except:
        pass


    results = []
    try:
        results = face_recognition.compare_faces([aadhar_face_encoding], pan_face_encoding)
        faceDistance = face_recognition.face_distance([aadhar_face_encoding], pan_face_encoding)
        Similarity = (1 - faceDistance)*100
        # Converting matching confidence ratio with AWS confidence level
        if 35 <= Similarity[0] < 40:
            x = Similarity[0]-35
            x = x/5.0
            Similarity[0] = (x*8)+80
        elif 40 <= Similarity[0] < 50:
            x = Similarity[0]-40
            x = x/10.0
            Similarity[0] = (x*5)+88
        elif 50 <= Similarity[0] <= 65.2:
            x = Similarity[0]-50
            x = x/15.2
            Similarity[0] = (x*6.7)+93
        elif 65.2 < Similarity[0] <= 99.9:
            x = 99.9
            Similarity[0] = x
        return Similarity[0]
    except:
        return (0.0)

# Converting base64 of faces from temp folder
def encodeImage(filename):
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return(encoded_string.decode("utf-8"))

# recieving all process results if it was not able to proceed and send it again after pdf converting
def Input_Image(image1, image2, numofimage):
    box = {}
    box["Similarity"] = []
    box["numFaces1"] = numofimage[0]
    box["numFaces2"] = numofimage[1]

    file_name1 = image1
    file_Name1, file_extension1 = os.path.splitext(file_name1)
    file1 = file_name1.split("/")[-1]
    if(file_extension1 != ".jpg" and file_extension1 != ".png" and file_extension1 != ".jpeg" and file_extension1 != ".JPG"):
        file_name1 = image1
        file1 = file_name1.split("/")[-1]

    file_name2 = image2
    file_Name2, file_extension2 = os.path.splitext(file_name2)
    file2 = file_name2.split("/")[-1]
    if(file_extension2 != ".jpg" and file_extension2 != ".png" and file_extension2 != ".jpeg" and file_extension2 != ".JPG"):
        file_name2 = image2
        file2 = file_name2.split("/")[-1]


    final = []
    for i in range(box["numFaces1"]):
        for j in range(box["numFaces2"]):
            result = Compare_Faces("temp/" + str(i) + '_' + file1, "temp/" + str(j) + '_' + file2)
            box["Similarity"].append(result)

            compare_dict = {
                "Base_image": str(encodeImage("temp/" + str(i) + '_' + file1)),
                "Compare_image": str(encodeImage("temp/" + str(j) + '_' + file2)),
                "Similarity": str(result)
            }
            final.append(compare_dict)


    #removing face images from temp folder
    for k in range(box["numFaces1"]):
        os.remove("temp/" + str(k) + '_' + file1)
    try:
        for l in range(box["numFaces2"]):
            os.remove("temp/" + str(l) + '_' + file2)
    except FileNotFoundError:
        pass


    box["Result"] = final
    return box
