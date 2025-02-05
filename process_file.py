from pathlib import Path
import hashlib
import os
from pdf2image import convert_from_path
import base64
from PIL import Image
import mimetypes
import glob
import shutil

from io import BytesIO
class process_file():
    def __int__():
        pass
    
    def process_uploaded_file(file: str):
        hash_obj = hashlib.sha256()
        hash_obj.update(file.getbuffer())
        file_hash = hash_obj.hexdigest()

        result = {}
        # Save the file locally
        local_path = os.path.join("cache", file_hash)
        if not os.path.exists(local_path):
            Path(local_path).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(local_path, file.name), "wb") as f:
            f.write(file.getbuffer())

        # result["folder"] = local_path
        # result["file"] = file.name
        # result["path"] = os.path.join(local_path, file.name)
        images_dir = os.path.join(local_path, "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir, exist_ok=True)

        
        file_path =os.path.join(local_path, file.name)

        # Copy or convert the file
        print(file_path)
        _, file_extension = os.path.splitext(file_path)
        file_name = file.name
        # stored_file_path = os.path.join(local_path, file_name)
        # shutil.copy2(file_path, stored_file_path)

        image_paths = []

        if file_extension.lower() == ".pdf":
            # Convert PDF to images
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                image_path = os.path.join(images_dir, f"image_{i}.png")
                image.save(image_path, "PNG")
                image_paths.append(image_path)
        elif "xls" in file_extension.lower():
            pass
            # csv_dir = os.path.join(cache_dir, "excel_csvs")

            # os.makedirs(csv_dir, exist_ok=True)
            # try:
            #     sheets = pd.ExcelFile(file_path).sheet_names
            #     for sheet in sheets:
            #         sheet_image_path = excel_sheet_to_image(
            #             file_path, sheet, os.path.join(images_dir, f"{sheet}.png")
            #         )
            #         excel_sheet_to_csv(
            #             file_path, sheet, os.path.join(csv_dir, f"{sheet}.csv")
            #         )
            #         image_paths.append(sheet_image_path)
            #     return file_hash, image_paths
            # except Exception as e:
            #     return file_hash, [f"Error reading sheet names: {e}"]

        else:
            # If it's an image, copy it to the images directory
            image_path = os.path.join(images_dir, file_name)
            shutil.copy2(file_path, image_path)
            image_paths.append(image_path)
        return file_hash, image_paths, images_dir

