#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
import torch
from diffusers import StableDiffusionPipeline
import io
import base64

app = Flask(__name__)

MODEL_NAME = "stabilityai/stable-diffusion-2-1-base"
pipe = StableDiffusionPipeline.from_pretrained(MODEL_NAME, torch_dtype=torch.float32)
pipe.enable_attention_slicing()
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(description):
    try:
        print(f"Generating image for description: {description}")
        image = pipe(description).images[0]
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drawing App</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        canvas {
            border: 2px solid black;
            cursor: crosshair;
            background-color: white;
        }
        button {
            margin-top: 10px;
            padding: 10px;
            cursor: pointer;
            font-size: 16px;
        }
        img {
            margin-top: 10px;
            max-width: 800px;
            border: 2px solid black;
        }
    </style>
</head>
<body>
    <h1>Drawing App</h1>
    <canvas id="drawingCanvas" width="800" height="600"></canvas>
    <button onclick="generateImage()">Generate Image</button>
    <img id="outputImage" alt="Generated Image" />

    <script>
        const canvas = document.getElementById('drawingCanvas');
        const ctx = canvas.getContext('2d');
        let drawing = false;

        canvas.addEventListener('mousedown', (e) => {
            drawing = true;
            ctx.beginPath();
            ctx.moveTo(e.offsetX, e.offsetY);
        });

        canvas.addEventListener('mousemove', (e) => {
            if (drawing) {
                ctx.lineTo(e.offsetX, e.offsetY);
                ctx.stroke();
            }
        });

        canvas.addEventListener('mouseup', () => { drawing = false; });
        canvas.addEventListener('mouseleave', () => { drawing = false; });

        function generateImage() {
            const descriptionText = prompt("Enter a description for the image:");
            if (!descriptionText) return;

            fetch('/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({description: descriptionText})
            })
            .then(response => response.json())
            .then(data => {
                console.log("Received response:", data);
                if (data.image) {
                    document.getElementById('outputImage').src = 'data:image/png;base64,' + data.image;
                } else {
                    alert("Erreur : Aucune image générée.");
                }
            })
            .catch(error => {
                console.error("Erreur lors de la génération de l'image :", error);
                alert("Erreur lors de la génération de l'image.");
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def drawing_app():
    return render_template_string(HTML_CODE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json.get('description', 'A beautiful landscape') 
    generated_image = generate_image(data)
    
    if generated_image:
        return jsonify({'image': generated_image})
    else:
        return jsonify({'error': 'Image generation failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
