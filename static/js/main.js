document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const resultDiv = document.getElementById('result');
    const startVideoButton = document.getElementById('startVideo');
    const videoElement = document.getElementById('videoElement');
    const canvasElement = document.getElementById('canvasElement');

    // Handle image upload
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(uploadForm);
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                resultDiv.innerHTML = `
                    <div class="success">
                        <h3>Detected Emotion: ${data.emotion}</h3>
                        <img src="/static/uploads/${data.image_path}" alt="Uploaded image" style="max-width: 300px;">
                    </div>`;
            } else {
                resultDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            }
        } catch (error) {
            resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    });

    // Handle video capture
    let stream = null;

    startVideoButton.addEventListener('click', async function() {
        try {
            if (videoElement.style.display === 'none') {
                stream = await navigator.mediaDevices.getUserMedia({ video: true });
                videoElement.srcObject = stream;
                videoElement.style.display = 'block';
                startVideoButton.textContent = 'Stop Video';
            } else {
                if (stream) {
                    stream.getTracks().forEach(track => track.stop());
                }
                videoElement.style.display = 'none';
                startVideoButton.textContent = 'Start Video';
            }
        } catch (error) {
            console.error('Error accessing webcam:', error);
            resultDiv.innerHTML = `<div class="error">Error accessing webcam: ${error.message}</div>`;
        }
    });
});