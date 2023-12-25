import cv2
from pyzbar.pyzbar import decode


def qr_code_scanner():
    try:
        # Open the camera
        cap = cv2.VideoCapture(0)

        while True:
            # Read a frame from the camera
            _, frame = cap.read()

            # Decode QR codes in the frame
            decoded_objects = decode(frame)

            # Loop over the detected objects
            for obj in decoded_objects:
                # Extract the QR code data
                qr_data = obj.data.decode('utf-8')
                print(f"QR Code Data: {qr_data}")

                # Draw a rectangle around the QR code
                points = obj.polygon
                if len(points) == 4:
                    cv2.polylines(frame, [points], isClosed=True,
                                color=(0, 255, 0), thickness=2)

            # Display the frame
            cv2.imshow("QR Code Scanner", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()
    except:
        pass


if __name__ == "__main__":
    qr_code_scanner()
