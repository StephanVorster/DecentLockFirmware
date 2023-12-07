import cv2
import requests
import json
import base64

def capture_image():
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # '0' is usually the default value for the primary camera

    # Capture one frame
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    # Check if the frame was captured correctly
    if not ret:
        print("Failed to capture image")
        return None

    return frame

def convert_image_to_base64(image):
    # Encode the image to JPG format
    _, encoded_image = cv2.imencode('.jpg', image)

    # Convert to base64
    encoded_image_base64 = base64.b64encode(encoded_image)

    return encoded_image_base64

def main():
    # Capture an image
    image = capture_image()
    if image is None:
        return

    # Convert the image to base64
    image_base64 = convert_image_to_base64(image)

    # Payload to be sent to Lambda function
    payload = {
        "image_content": image_base64.decode(),  # decode to convert bytes to string
        "file_name": "captured_photo.jpg"
        "user_address"
    }
    print(image_base64)

    # API Gateway URL
    url = "https://t4r59j94nf.execute-api.ca-central-1.amazonaws.com/Staging/upload-photo"

    # Make the POST request
    response = requests.post(url, json=payload)

    # Print the response
    print("StatusCode:", response.status_code)
    print("Response:", response.text)

if __name__ == '__main__':
    main()
