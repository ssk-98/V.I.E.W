import cv2

def video_cap():
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame = cap.read()
        cv2.imshow('frame',frame)
        f=open("./Function","r")
        command = f.readlines()[0]
        f.close()
        cv2.waitKey(1)
        if command == "c":
            cv2.imwrite("./frame.jpg", frame)
            f=open("./Function","w")
            f.write("a")
            f.close()
        if command == "q":
            f=open("./Function","w")
            f.write("a")
            f.close()
            break
    cap.release()
    cv2.destroyAllWindows()

    
if __name__ == "__main__" :
    video_cap()
