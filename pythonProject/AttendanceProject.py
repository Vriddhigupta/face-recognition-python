import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np
import face_recognition
import os


path = 'C:/Users/Yash Gupta/PycharmProjects/pythonProject/ImageAttendance'
def start():
	images = []
	classNames1 = []
	myList1 = os.listdir(path)
	print(myList1)

	for cl in myList1:
	    curImg = cv2.imread(f'{path}/{cl}')
	    images.append(curImg)
	    classNames1.append(os.path.splitext(cl)[0])
	print(classNames1)
	encodeListKnown1 = findEncodings(images)
	print('Encoding Complete')
	return encodeListKnown1,classNames1,myList1


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown, classNames , myList = start()

cap = cv2.VideoCapture(0)

while True:
	success, img = cap.read()
	imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
	imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

	facesCurFrame = face_recognition.face_locations(imgS)
	encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

	for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
		matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
		faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
		# print(faceDis)
		matchIndex = np.argmin(faceDis)

		if matches[matchIndex]:
			name = classNames[matchIndex].upper()
			print(name)
			y1, x2, y2, x1 = faceLoc
			y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
			cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
			cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
			cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
		else:
			print("Unknown")
			y1, x2, y2, x1 = faceLoc
			y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
			cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
			cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
			cv2.putText(img, "Unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
			name=input("Enter name =")
			result = True
			while(result):
				ret,frame = cap.read()
				cv2.imwrite(os.path.join(path , name+'.jpg'), frame)
				result = False
			#images.append(frame);
			#classNames.append(os.path.splitext(cl)[0])
			#encodeListKnown = findEncodings(images)
			#print('Encoding Complete')
			encodeListKnown, classNames , myList = start()

			print(name)
			y1, x2, y2, x1 = faceLoc
			y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
			cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
			cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
			cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
		cv2.imshow('Webcam', img)
		cv2.waitKey(1)

# faceLoc = face_recognition.face_locations(imgElon)[0]
# encodeElon = face_recognition.face_encodings(imgElon)[0]
# cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)
# print(faceLoc)

# faceLocTest = face_recognition.face_locations(imgTest)[0]
# encodeTest = face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)
# print(faceLocTest)

# results = face_recognition.compare_faces([encodeElon], encodeTest)
# faceDis = face_recognition.face_distance([encodeElon], encodeTest)
