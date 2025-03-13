import os
import shutil
import subprocess

def viton_hd_process(person_image_path, cloth_image_path):
    viton_hd_dir = "VITON-HD"
    dataset_dir = os.path.join(viton_hd_dir, "datasets", "test_images")
    result_dir = os.path.join(viton_hd_dir, "results")

    os.makedirs(dataset_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)

    person_dst = os.path.join(dataset_dir, "person.jpg")
    cloth_dst = os.path.join(dataset_dir, "cloth.jpg")

    shutil.copy(person_image_path, person_dst)
    shutil.copy(cloth_image_path, cloth_dst)

    command = [
        "python", os.path.join(viton_hd_dir, "test.py"),
        "--name", "viton_hd",
        "--dataset_mode", "test",
        "--dataroot", dataset_dir,
        "--results_dir", result_dir,
        "--phase", "test",
        "--gpu_ids", "-1",
    ]

    subprocess.run(command, check=True)

    output_image_path = os.path.join(result_dir, "viton_hd", "test", "try-on", "person.jpg")
    flask_static_path = os.path.join("app", "static", "result.jpg")
    shutil.copy(output_image_path, flask_static_path)

    return "result.jpg"
  
