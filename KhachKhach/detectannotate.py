from ultralytics import YOLO
from PIL import Image
import os

class DetectionAnnotation:
    def __init__(self, output_folder: str, model_path: str = 'yolov8n.pt'):
        """
        Initialize the DetectionAnnotation with a pre-trained YOLO model and output folder.

        :param output_folder: Folder where the annotation files will be saved.
        :param model_path: Path to the pre-trained YOLO model (default is 'yolov8n.pt').
        """
        # Load the YOLO model
        self.model = YOLO(model_path)  # Load the model from the given path
        
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

    def generate_annotation(self, image_path: str) -> None:
        """
        Generate a YOLO annotation file for a given image using the YOLO model.

        :param image_path: Path to the image file.
        """
        # Load the image
        image = Image.open(image_path)
        image_width, image_height = image.size

        # Perform inference
        results = self.model(image_path)

        # Prepare annotation file path
        annotation_filename = os.path.splitext(os.path.basename(image_path))[0] + ".txt"
        annotation_path = os.path.join(self.output_folder, annotation_filename)

        with open(annotation_path, "w") as f:
            # Write annotations to the file
            for result in results[0].boxes.xyxy:  # Assuming results[0] contains the detection results
                x_min, y_min, x_max, y_max = result.tolist()

                x_center = (x_min + x_max) / 2
                y_center = (y_min + y_max) / 2
                box_width = x_max - x_min
                box_height = y_max - y_min

                x_center_norm = x_center / image_width
                y_center_norm = y_center / image_height
                box_width_norm = box_width / image_width
                box_height_norm = box_height / image_height

                yolo_annotation = f"{x_center_norm:.6f} {y_center_norm:.6f} {box_width_norm:.6f} {box_height_norm:.6f}"
                f.write(yolo_annotation + "\n")

        print(f"YOLO annotation saved to {annotation_path}")

    def process_folder(self, image_folder: str) -> None:
        """
        Process all images in a folder and generate YOLO annotations for each.

        :param image_folder: Path to the folder containing images.
        """
        for filename in os.listdir(image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(image_folder, filename)
                self.generate_annotation(image_path)

# Example usage

