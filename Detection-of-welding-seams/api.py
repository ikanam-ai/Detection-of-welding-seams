from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import torch
from ultralytics import YOLOv10
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the model
model = YOLOv10('/home/andrew/works/shpad_add/Detection-of-welding-seams/train_yolo/runs/detect/Atomic HACK YOLOv10 50/weights/best.pt')

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


    height, width, _ = image.shape

    # Perform prediction
    results = model.predict(image)

    # Process results
    results_list = []
    boxes = results[0].boxes.xyxy  # Coordinates of boxes in (xmin, ymin, xmax, ymax) format
    scores = results[0].boxes.conf  # Confidence scores
    class_ids = results[0].boxes.cls  # Class IDs

    for i in range(len(boxes)):
        x1, y1, x2, y2 = boxes[i].cpu().numpy()  # Convert to numpy array and extract coordinates
        class_id = int(class_ids[i].cpu().numpy())  # Class ID
        confidence = scores[i].cpu().numpy()  # Confidence score

        # Calculate relative coordinates and sizes
        rel_x = (x1 + x2) / 2 / width
        rel_y = (y1 + y2) / 2 / height
        rel_width = (x2 - x1) / width
        rel_height = (y2 - y1) / height

        # Append results to list
        results_list.append({
            'filename': 'your_file',  # Keep the file name
            'class_id': class_id,  # Use the numeric class ID
            'rel_x': float(rel_x),  # Ensure float for JSON serialization
            'rel_y': float(rel_y),  # Ensure float for JSON serialization
            'width': float(rel_width),  # Ensure float for JSON serialization
            'height': float(rel_height),  # Ensure float for JSON serialization
            'confidence': float(confidence)  # Ensure float for JSON serialization
        })

    return jsonify(results_list)

if __name__ == '__main__':
    app.run(port=27371)
