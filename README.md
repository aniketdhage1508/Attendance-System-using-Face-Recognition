# Attendance-System-using-Face-Recognition

This project implements a Face Recognition Attendance System using Python, OpenCV, and face_recognition library. The system captures real-time video feed from a camera, detects faces, recognizes them by comparing with a pre-loaded database, and marks attendance in a CSV file.

## Features

- **Face Recognition:** Utilizes the face_recognition library to encode and compare facial features for recognition.
- **Real-time Attendance:** Captures video feed in real-time, recognizes faces, and marks attendance automatically.
- **Database Management:** Maintains a database of known faces for recognition.
- **CSV Logging:** Records attendance details in a CSV file with timestamps.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- face_recognition
- MySQL Connector
- Tkinter
- Pillow (PIL)

## Usage

1. Install the required libraries using:
   ```bash
   pip install opencv-python numpy face_recognition mysql-connector-python pillow
   ```

2. Run the script:
   ```bash
   python your_script_name.py
   ```

3. Use the 'x' key to exit the application.

## Directory Structure

- `ImagesAttendance/`: Directory containing images of known individuals for face recognition.
- `Attendance.csv`: CSV file recording attendance with timestamps.
- `Studentdetails.py`: Module containing details of students (not provided in the code snippet).

## How It Works

1. **Initialization:**
   - Images of known individuals are loaded from the `ImagesAttendance/` directory.
   - Face encodings of these images are computed and stored.

2. **Recognition Loop:**
   - The system continuously captures video feed from the camera.
   - Faces in the frame are located and encoded for recognition.

3. **Face Matching:**
   - Encoded faces are compared with the known face encodings.
   - If a match is found, the system identifies the person and marks attendance.

4. **Attendance Logging:**
   - Attendance details are logged in the `Attendance.csv` file with timestamps.

5. **User Interface:**
   - The application includes a simple Tkinter GUI for better interaction.

## Notes

- Ensure proper lighting conditions for accurate face recognition.
- The script can be customized to connect with a database for more robust data management.
