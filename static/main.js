const video = document.getElementById('video');
const labelDiv = document.getElementById('label');
const sentenceTextarea = document.getElementById('sentence');
const speakButton = document.getElementById('speakButton');

let currentLabel = ''; // Holds the current detected letter
let lastDetectedLabel = ''; // Last detected letter before hand disappears
let sentence = ''; // Constructed sentence
let handPresent = false; // Track if hand is present
let lastCaptureTime = 0; // Track last frame capture time
let captureInterval = 1000; // 1 second interval (matching backend)
let isProcessing = false; // Prevent multiple overlapping requests

// Get access to the camera
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.srcObject = stream;
        video.play();
    }).catch(function(error) {
        console.error('Error accessing the camera: ', error);
    });
} else {
    alert('Your browser does not support video capture.');
}

// Capture and send frames to the backend at intervals
video.addEventListener('play', () => {
    const captureFrame = () => {
        if (video.paused || video.ended) return;
        
        let currentTime = Date.now();
        if (currentTime - lastCaptureTime < captureInterval || isProcessing) return;

        lastCaptureTime = currentTime;
        isProcessing = true;

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);

        canvas.toBlob((blob) => {
            const formData = new FormData();
            formData.append('image', blob, 'frame.jpg');

            fetch('/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                isProcessing = false;
                const newLabel = data.label;

                if (newLabel) {
                    // Hand is detected, update last detected label
                    if (!handPresent) {
                        handPresent = true; // Mark that hand is now visible
                    }
                    lastDetectedLabel = newLabel; // Continuously update the last detected letter
                    labelDiv.textContent = `Predicted letter: ${lastDetectedLabel}`;
                } else {
                    // If hand disappears after being detected
                    if (handPresent) {
                        handPresent = false; // Mark that hand is gone

                        if (lastDetectedLabel) {
                            // Append only the last detected letter before disappearance
                            sentence += lastDetectedLabel; 
                            sentenceTextarea.value = sentence; // Update the textarea
                            lastDetectedLabel = ''; // Reset the last detected label
                            labelDiv.textContent = ''; // Clear displayed label
                        }
                    }
                }
            })
            .catch(error => {
                isProcessing = false;
                console.error('Error:', error);
            });
        }, 'image/jpeg');
    };

    // Capture frame every 1 second
    setInterval(captureFrame, 500);
});

// Speak the sentence when the button is clicked
speakButton.addEventListener('click', () => {
    const sentenceToSpeak = sentenceTextarea.value.trim();
    if (sentenceToSpeak) {
        const utterance = new SpeechSynthesisUtterance(sentenceToSpeak);
        utterance.lang = 'en-US'; // Set the language to English
        speechSynthesis.speak(utterance);
    } else {
        alert('Please construct a sentence before speaking!');
    }
});
document.getElementById('clearButton').addEventListener('click', () => {
    sentence = '';
    document.getElementById('sentence').value = ''; 
});
const correctButton = document.getElementById('correctButton'); // Button to send data to backend

correctButton.addEventListener('click', () => {
    const unstructuredText = sentenceTextarea.value.trim();

    if (!unstructuredText) {
        alert("Please enter a sentence to correct.");
        return;
    }

    fetch('/correct', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sentence: unstructuredText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.corrected_sentence) {
            sentenceTextarea.value = data.corrected_sentence; // Update with corrected sentence
        } else {
            alert("Error processing sentence.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
