import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from gradio_client import Client, file

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# AI-Platform/Virtual-Try-On API client
client = Client("AI-Platform/Virtual-Try-On")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get uploaded files
        human_file = request.files["human"]
        cloth_file = request.files["cloth"]

        if human_file and cloth_file:
            # Save uploaded files
            human_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(human_file.filename))
            cloth_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(cloth_file.filename))
            human_file.save(human_path)
            cloth_file.save(cloth_path)

            # Call API
            result = client.predict(
                dict={"background": file(human_path), "layers": [], "composite": None},
                garm_img=file(cloth_path),
                garment_des="Virtual Try-On",
                is_checked=True,
                is_checked_crop=False,
                denoise_steps=30,
                seed=42,
                api_name="/tryon"
            )

            output_img_path = result[0]  # Processed image

            return render_template("index.html", human_img=human_path, cloth_img=cloth_path, result_img=output_img_path)

    return render_template("index.html", human_img=None, cloth_img=None, result_img=None)

if __name__ == "__main__":
    app.run(debug=True)
  
