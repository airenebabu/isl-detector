from flask import Flask, request, jsonify, send_from_directory
import cv2
import mediapipe as mp
import copy
import itertools
from tensorflow import keras
import numpy as np
import pandas as pd
import string
import time
from transformers import pipeline

app = Flask(__name__)

# Load the saved model from file
model = keras.models.load_model(r"model.h5")

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

alphabet = ['1','2','3','4','5','6','7','8','9']
alphabet += list(string.ascii_uppercase)

sentence = []
hand_present = False
last_label = ""
last_capture_time = 0  # To control capture interval
capture_interval = 1.0  # Minimum time gap (in seconds) between captures

# Functions for processing landmarks
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_point = []
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point.append([landmark_x, landmark_y])
    return landmark_point

def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]
        temp_landmark_list[index][0] -= base_x
        temp_landmark_list[index][1] -= base_y
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))
    max_value = max(list(map(abs, temp_landmark_list)))
    temp_landmark_list = list(map(lambda n: n / max_value, temp_landmark_list))
    return temp_landmark_list

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global sentence, hand_present, last_label, last_capture_time
    current_time = time.time()

    # Ensure time gap between captures
    if current_time - last_capture_time < capture_interval:
        return jsonify({'label': last_label, 'sentence': ''.join(sentence)})  # Include sentence

    # Get the image from the request
    file = request.files['image'].read()
    npimg = np.frombuffer(file, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:
        
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(image)

        if results.multi_hand_landmarks:
            hand_present = True
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                landmark_list = calc_landmark_list(image, hand_landmarks)
                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                df = pd.DataFrame(pre_processed_landmark_list).transpose()
                predictions = model.predict(df, verbose=0)
                predicted_classes = np.argmax(predictions, axis=1)
                last_label = alphabet[predicted_classes[0]]
                last_capture_time = current_time  # Update capture time
                print(f"Detected label: {last_label}")
        else:
            if hand_present:
                hand_present = False
                print(f"Hand moved off-screen, storing last letter: {last_label}")

                # Store the last detected letter in the sentence when the hand moves away
                if last_label:
                    sentence.append(last_label)
                    last_label = ""  # Reset last label after storing

    return jsonify({'label': last_label, 'sentence': ''.join(sentence)})

# Load Hugging Face grammar correction model
grammar_corrector = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")

@app.route('/correct', methods=['POST'])
def correct_sentence():
    try:
        data = request.json
        unstructured_text = data.get("sentence", "")

        if not unstructured_text:
            return jsonify({"error": "No text provided"}), 400

        # Process the unstructured sentence
        corrected_text = grammar_corrector(unstructured_text, max_length=50, do_sample=False)
        structured_sentence = corrected_text[0]['generated_text'].strip()

        return jsonify({"corrected_sentence": structured_sentence})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

