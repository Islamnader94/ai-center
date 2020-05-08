import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string
import re

print("Put a business card with text in the visual range of your attached camera.\
       Once placed correctly, press >d< on your keyboard to detect the text.\
       To exit the screen press >q< on your keyboard.")

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame from attached webcam
    ret, frame = cap.read()

    # operations per frame
    # convert to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # get rid of noise by using erosion and dilation
    kernel = np.ones((1, 1), np.uint8)
    gray = cv2.erode(gray, kernel, iterations=10)
    gray = cv2.dilate(gray, kernel, iterations=10)
    
    # Display the result
    cv2.imshow('frame',gray)
    
    # wait for keyboard input >d< to start text detection
    if cv2.waitKey(1) & 0xFF == ord('d'):
        output = pytesseract.image_to_string(gray)
        print(output)
        email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", output)
        phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', output)
        print(email)
        print(phone)

        # Call http post request to send data to backend
        # payload = {
        #     'phone': phone,
        #     'email': email
        # }

        # headers = {
        #     'content-type': 'application/json',
        # }

        # params = (
        #     ('priority', 'normal'),
        # )

        # get_data = requests.get("http://0.0.0.0:5000/api/List", headers=headers, params=params)
        # data = get_data.json()
        # found = False
        # for d in data['data'][0]:
        #     if email == d['email']:
        #         found = True
        # if found == True:
        #         print('Data exists')
        # else:
        #     # add data to backend
	    #     post = requests.post("http://0.0.0.0:5000/api/List", headers=headers, params=params, json=payload)
    
    # wait for keyboard input >q< to quit application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# release capture and terminate
cap.release()
cv2.destroyAllWindows()