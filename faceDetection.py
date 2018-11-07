import picamera
import io
import cv2
import numpy

stream = io.BytesIO()
i=0
j=0

face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/DSD/frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/pi/Desktop/DSD/eye_default.xml')


camera = picamera.PiCamera()
camera.resolution=(100,100)
#camera.vflip=True

while True:
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')

    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

    image = cv2.imdecode(buff,1)

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    faces= face_cascade.detectMultiScale(gray, 1.3, 5)
    if(len(faces)==0):
        i=i+1
        if(i>=5):
            print "face pai nai"
            
        
    else:
        i = 0
    #print "Found " +str(len(faces)) + " faces(s)"
        for(x,y,w,h) in faces:
            cv2.rectangle(image, (x,y), (x+w, y+h), (255,255,0) ,2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1,5)
            if(len(eyes)==0 and len(faces)>0 ):
                j=j+1
                if(j>=5):
                    print "no eyes found"
                    
            else:    
                j = 0    
                for(ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh) , (0,255,0), 2)

    cv2.imshow('result', image)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
    #cv2.imwrite('result.jpg', image)
