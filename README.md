# 🖐 **Indian Sign Language (ISL) Detector**

![ISL Detector](https://your-image-url.com/banner.png)  
*A real-time AI-powered sign language recognition system that translates hand gestures into text and speech.*

## 📌 **Overview**
The **ISL Detector** is a deep learning-based application that recognizes Indian Sign Language (ISL) gestures in real time. It captures hand movements, translates them into text, applies grammar correction, and reads out the final sentence using text-to-speech.

## 🚀 **Features**
✅ **Real-time ISL recognition** using **MediaPipe Hands** & **TensorFlow**  
✅ **Hand Gesture Classification** with a trained deep learning model  
✅ **Grammar Correction** powered by a **Hugging Face transformer**  
✅ **Text-to-Speech (TTS)** for enhanced accessibility  
✅ **Interactive Web Interface** for seamless user experience  

## 📁 **Project Structure**
```
├── dataset_keypoint_generation.py  # Extracts hand landmarks for dataset creation
├── isl_detection.py                # Flask API for gesture recognition & grammar correction
├── main.js                         # Frontend script for video processing & UI interactions
├── ISL_classifier.ipynb            # Model training notebook
├── model.h5                        # Pre-trained gesture recognition model
├── static/                         # Contains frontend assets (HTML, CSS, JS)
├── templates/                      # Flask templates (index.html)
├── requirements.txt                # Project dependencies
└── README.md                       # This file
```

## 🛠 **Installation & Setup**

### **Prerequisites**
- Python 3.8+
- Node.js (for frontend features)
- TensorFlow & Keras
- Flask
- MediaPipe
- OpenCV
- Hugging Face Transformers

### **Setup Instructions**
1️⃣ **Clone the repository:**  
```bash
 git clone https://github.com/airenebabu/isl-detector.git
 cd isl-detector
```
2️⃣ **Install dependencies:**  
```bash
 pip install -r requirements.txt
 npm install  # If frontend requires Node.js modules
```
3️⃣ **Run the Flask server:**  
```bash
 python isl_detection.py
```
4️⃣ **Access the web app:** Open `index.html` in your browser.

## 📡 **API Endpoints**
| Endpoint     | Method | Description |
|-------------|--------|-------------|
| `/predict`  | POST  | Accepts an image, processes hand gestures, and returns the predicted letter. |
| `/correct`  | POST  | Takes a sentence and returns a grammar-corrected version. |

### **Example Usage**
```python
import requests
files = {"image": open("hand_image.jpg", "rb")}
response = requests.post("http://127.0.0.1:5000/predict", files=files)
print(response.json())
```

## 👥 **Contributing**
Want to contribute? Follow these steps:
1. **Fork the repository**
2. **Create a new branch:** `git checkout -b feature-name`
3. **Commit your changes:** `git commit -m "Added new feature"`
4. **Push to your branch:** `git push origin feature-name`
5. **Submit a pull request** 🚀

## 📜 **License**
This project is licensed under the **MIT License**.

## 🌟 **Acknowledgments**
- **Google MediaPipe** for hand tracking
- **TensorFlow & Keras** for deep learning
- **Hugging Face** for NLP-powered grammar correction

💡 *If you like this project, don't forget to give it a star ⭐ on [GitHub](https://github.com/airenebabu/isl-detector)!*

---
****
## 👥 Collaborators

[![GitHub Contributors](https://contrib.rocks/image?repo=airenebabu/isl-detector)](https://github.com/airenebabu/isl-detector/graphs/contributors)

