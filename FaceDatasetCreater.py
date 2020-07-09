import os
import cv2
import time

# For the algorithm to work properly around 20 photos of a person from different angles are required 


def main():
    cap = cv2.VideoCapture(0)

    run = True
    getname= True

    # No is used to track no of photos taken
    no = 0
    # Obtains path of pwd
    path = os.path.dirname(os.path.realpath(__file__)) + '\\Dataset\\'

    # Creates the dataset folder in pwd if it does not exist
    try :
        os.mkdir(path)
    except:
        print('Dataset folder exits')
    # Creates folder inside dataset with the name of the person    
    while(getname):
        name = input('Enter your name :')
        if not os.path.exists(path + name):
            os.mkdir(path + name)
            getname = False
        else:
            print('Name Taken')
    # From the devices primary camera screen shots are taken and saved in the dataset folder
    while(run):
        ret,frame = cap.read()
        saveFrame = frame.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(no), (600, 20), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Dataset Generator',frame)
        inputkey = cv2.waitKey(1)
        location = path + name + '\\' + str(no) + ".jpg"
        if inputkey == 27:
            run = False
        if inputkey == ord('q'):
            print(location)
            cv2.imwrite(location, saveFrame)
            no = no + 1
    
 
    cap.release()
    cv2.destroyAllWindows()

def encoding_face():
    # grab the paths to the input images in our dataset
    print("Encoding faces")
    imagePaths = list(paths.list_images('.\\dataset\\'))

    # initialize the list of known encodings and known names

    knownEncodings = []
    knownNames = []


    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1,
                    len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(image,
                    model='hog')

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(image, boxes)

            # loop over the encodings
            for encoding in encodings:
                    knownEncodings.append(encoding)
                    knownNames.append(name)

    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open('.\\encoding.pickle', "wb")
    f.write(pickle.dumps(data))
    f.close()
    

if __name__ == '__main__':
    main()
