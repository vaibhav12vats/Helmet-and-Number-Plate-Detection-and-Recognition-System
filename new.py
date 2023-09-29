import cv2
import pytesseract
cap = cv2.VideoCapture('video.mp4')
while(cap.isOpened()):
    ret, frame = cap.read()

    if ret == True:
        # Apply image processing to detect number plates
        # and extract the region of interest

        # Display the frame with detected number plates
        cv2.imshow('Frame', frame)

        # Press 'q' to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break


# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Loop through the extracted number plates
for plate in frame:
    # Apply OCR to recognize the characters on the number plate
    text = pytesseract.image_to_string(plate, lang='eng')

    # Print the recognized text
    print(text)

# Load the helmet detection model
helmet_cascade = cv2.CascadeClassifier('haarcascade_helmet.xml')

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret == True:
        # Apply image processing to detect helmets
        # and extract the region of interest

        # Display the frame with detected helmets
        cv2.imshow('Frame', frame)

        # Press 'q' to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# Loop through the detected number plates and draw bounding boxes
for plate in frame:
    x, y, w, h = plate
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Loop through the detected helmets and draw bounding boxes
for (x, y, w, h) in helmets:
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Display the frame with detected number plates and helmets
cv2.imshow('Frame', frame)

# Store the results in a database or a file
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="detection"
)

# Create a cursor object
cursor = db.cursor()

# Create a table to store the results
cursor.execute("CREATE TABLE results (id INT AUTO_INCREMENT PRIMARY KEY, plate_number VARCHAR(255), helmet_detected BOOLEAN)")
while(cap.isOpened()):
    ret, frame = cap.read()

    if ret == True:
        # Apply image processing to detect number plates and helmets

        # Store the results in the database
        sql = "INSERT INTO results (plate_number, helmet_detected) VALUES (%s, %s)"
        val = (plate_number, helmet_detected)
        cursor.execute(sql, val)
        db.commit()

        # Display the frame with detected number plates and helmets

        # Press 'q' to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# Close the database connection
db.close()