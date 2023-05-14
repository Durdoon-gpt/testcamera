from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Capture vidéo à partir de la webcam
capture = cv2.VideoCapture(0)

# Vérifier si la capture vidéo est ouverte correctement
if not capture.isOpened():
    print("Impossible d'ouvrir la caméra")
    exit()

def generate_frames():
    while True:
        # Lire une image de la caméra
        ret, frame = capture.read()

        # Vérifier si la lecture de l'image est réussie
        if not ret:
            print("Échec de la capture d'image")
            break

        # Convertir l'image en format JPEG
        ret, buffer = cv2.imencode('.jpg', frame)

        # Vérifier si la conversion a réussi
        if not ret:
            print("Échec de la conversion d'image en JPEG")
            break

        # Récupérer les données de l'image
        frame_bytes = buffer.tobytes()

        # Générer la trame courante
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.1.28', debug=True)
