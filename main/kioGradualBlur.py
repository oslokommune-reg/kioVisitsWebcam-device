import cv2
import numpy as np

def blur(picture_name):
    try:
        img = cv2.imread(picture_name) 
        
        # Neglected pixels from the top
        noBlur = 100

        # Height, width, number of channels in the image
        height, width, _ = img.shape
        
        # Total number of zones (blur resolution)
        zones = 400
        
        # Maximum blur value
        blurMax = 17 #17

        for n in range(zones):
            # Calculate the blur level for the current zone
            blur_level = blurMax * (n / zones)
            oddBlurValue = int(np.ceil(blur_level / 2) * 2 + 1)

            # Calculate the top and bottom y-coordinates of the current zone
            top_y = int((height - noBlur) * (n / zones)) + noBlur
            bottom_y = int((height - noBlur) * ((n + 1) / zones)) + noBlur

            # Get the region of interest (ROI) for the current zone
            ROI = img[top_y:bottom_y, :]

            # Check if the ROI is empty
            if ROI.size == 0:
                continue

            # Apply Gaussian blur to the ROI
            blurred_ROI = cv2.GaussianBlur(ROI, (oddBlurValue, oddBlurValue), 0)

            # Replace the ROI with the blurred version
            img[top_y:bottom_y, :] = blurred_ROI

        # Save the blurred image
        cv2.imwrite(picture_name, img)
        return "Blur OK"

    except Exception as e:
        print("Error:", e)


