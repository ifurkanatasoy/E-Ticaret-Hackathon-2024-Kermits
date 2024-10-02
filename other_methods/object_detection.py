from ultralytics import YOLO  # Import the YOLO class from the ultralytics library
import cv2  # Import the OpenCV library for image processing

# Load the model using a different loading method
model = YOLO('jameslahm/yolov10x')  # Specify the model path to load the pretrained YOLOv10 model

# Load the image from the specified path
image_path = 'input/karisik.jpeg'  # Path to the input image file
image = cv2.imread(image_path)  # Read the image using OpenCV

# Make predictions using the model
results = model.predict(source=image)  # Perform inference on the input image

# Draw prediction results on the image
# This will draw the bounding boxes and labels for detected classes on the image
annotated_image = results[0].plot()  # Get the annotated image with predictions

# Save the annotated image to a specified output path
output_path = 'output/karisik_tahmin.jpeg'  # Path for saving the output image
cv2.imwrite(output_path, annotated_image)  # Save the annotated image using OpenCV

# Print a message indicating where the results have been saved
print(f"Prediction results saved to {output_path}.")  # Inform the user about the saved file
