import cv2
import requests
import json
import base64

class camera:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # '0' is usually the default value for the primary camera
        
    def capture_image(self):

        if self.cap.isOpened():
            # Capture one frame
            ret, frame = self.cap.read()
        else:
            self.cap = cv2.VideoCapture(0)  # '0' is usually the default value for the primary camera
            ret, frame = self.cap.read()


        # Release the camera
        self.cap.release()

        # Check if the frame was captured correctly
        if not ret:
            print("Failed to capture image")
            return None

        return frame


    def convert_image_to_base64(self, image):
        # Encode the image to JPG format
        _, encoded_image = cv2.imencode('.jpg', image)

        # Convert to base64
        encoded_image_base64 = base64.b64encode(encoded_image)

        return encoded_image_base64


    def send_image_to_remote(self, user_address, image_base64, retry=0):
        payload = {
            "image_content": image_base64.decode(),  # decode to convert bytes to string
            "file_name": "captured_photo.jpg",
            "user_address": user_address  # to-do change this specific address to get py's
        }
        # print(image_base64)

        # API Gateway URL
        url = "https://t4r59j94nf.execute-api.ca-central-1.amazonaws.com/Staging/upload-photo"

        # Make the POST request
        response = requests.post(url, json=payload)

        if not response.ok:
            if retry >= 2:
                return False
            else:
                return self.send_image_to_remote(user_address, retry=retry + 1)
        else:
            return True


    def capture_and_save(self):
        image = self.capture_image()
        send_success_ret = False
        if image is None:
            return False
        # Convert the image to base64
        image_base64 = self.convert_image_to_base64(image)
        auth_accounts = None
        with open('src/verified_accounts.json', 'r') as json_file:
            auth_accounts = json.loads(json_file.read())
        if auth_accounts is not None:
            for key in list(auth_accounts.keys()):
                send_success = self.send_image_to_remote(user_address=key, image_base64=image_base64)
                if send_success:
                    send_success_ret = True

        if send_success_ret:
            return True
        return False



if __name__ == '__main__':
    cam = camera()
    cam.capture_and_save()