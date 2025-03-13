from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from viton_processor import viton_hd_process

app = Flask(__name__)

UPLOAD_FOLDER = "app/uploads/"
RESULT_FOLDER = "app/static/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        person_image = request.files["person_image"]
        cloth_image = request.files["cloth_image"]

        if person_image and cloth_image:
            person_filename = secure_filename(person_image.filename)
            cloth_filename = secure_filename(cloth_image.filename)

            person_path = os.path.join(UPLOAD_FOLDER, person_filename)
            cloth_path = os.path.join(UPLOAD_FOLDER, cloth_filename)

            person_image.save(person_path)
            cloth_image.save(cloth_path)

            result_path = viton_hd_process(person_path, cloth_path)

            return render_template("index.html", result_image=result_path)

    return render_template("index.html", result_image=None)

if __name__ == "__main__":
    app.run(debug=True)
      
