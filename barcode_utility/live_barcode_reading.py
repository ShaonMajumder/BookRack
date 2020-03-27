from decode_encode import decode,display,actual_data
from imutils.video import VideoStream
from imutils.video import FPS
import cv2
import imutils
import time


detection_time = 'no detection'

detection_threshold = 50 # 1 sec

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

counter_i = 0
# loop over frames from the video file stream
previous_data = None
while True:
	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	
	# convert the input frame from (1) BGR to grayscale (for face
	# detection) and (2) from BGR to RGB (for face recognition)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	im = gray
	
	decodedObjects = decode(im,log=True)
	frame = display(frame, decodedObjects)
	data = actual_data(decodedObjects)

	# draw the predicted face name on the image
	#cv2.rectangle(frame, (left, top), (right, bottom),	(0, 255, 0), 2)
	#y = top - 15 if top - 15 > 15 else top + 15
	#cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

	# display the image to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == 27:
		break

	# update the FPS counter
	fps.update()

	#barcode detection program
	if data:
		if previous_data == data:
			if counter_i == 1: start_time = time.time()
			counter_i += 1
		else:
			counter_i = 0
	previous_data = data

	if counter_i > detection_threshold:
		detection_time = time.time() - start_time
		break
	

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
print("message = ",data)
print("Detection time",detection_time)