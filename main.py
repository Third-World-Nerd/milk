import cv2
import numpy as np
import serial

# Initialize the serial port
ser = serial.Serial("COM3", 2000000)

# Replace with your IP webcam URL
ip_webcam_url = "http://192.168.18.10:8080/video"

# Create a VideoCapture object
cap = cv2.VideoCapture(ip_webcam_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

sentDataToSerial = False

# Loop to continuously get frames
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the color range for detection
    lower_color = np.array([0, 0, 200])
    upper_color = np.array([180, 30, 255])

    # Create a mask for the defined color
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Select the largest contour
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        largest_contour_area = cv2.contourArea(largest_contour)
        # print(f"Area of the largest contour: {largest_contour_area}")

        # Draw the largest contour on the original image
        contoured_image = frame.copy()
        cv2.drawContours(contoured_image, [largest_contour], -1, (0, 255, 0), 2, 10)

        # Display the original and contoured images
        cv2.imshow("Contours", contoured_image)

    k = cv2.waitKey(1)
    # If the area of the largest contour is greater than 5000
    if largest_contour_area > 500000:
        ser.write(b"1")
        print("Data sent to serial port")
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the VideoCapture object and close windows
cap.release()
cv2.destroyAllWindows()
