import pytesseract as tess 
from PIL import Image
import PIL.Image
import cv2
import imutils
import argparse
import re
import requests


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

# convert the image to grayscale, blur it, and find edges
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# show the original image and the edge detected image
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break

# show the contour (outline) of the piece of paper
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

output_image = cv2.resize(image,(650, 650))
cv2.imshow("output",output_image)
cv2.imwrite('out/'+'output-Image.PNG', output_image)
cv2.waitKey(0)

output = tess.image_to_string(PIL.Image.open('out/'+ 'output-Image.PNG').convert("RGB"), lang='eng')

email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", output)
phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', output)

email = email[0]
phone = phone[0]

# Call http post request to send data to backend
payload = {
	'phone': phone,
	'email': email
}

headers = {
    'content-type': 'application/json',
}

params = (
    ('priority', 'normal'),
)

get_data = requests.get("http://0.0.0.0:5000/api/List", headers=headers, params=params)
data = get_data.json()
found = False
for d in data['data'][0]:
	if email == d['email']:
		found = True
if found == True:
		print('Data exists')
else:
	# add data to backend
	post = requests.post("http://0.0.0.0:5000/api/List", headers=headers, params=params, json=payload)
