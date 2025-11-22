import os
from flask import render_template
from pathlib import Path
from util import get_uploads_folder_url


ALLOWED_EXTENSIONS = ['.png', '.jpeg', '.jpg']


def file_upload_page():
    return render_template('file_upload.html', file_url=None)


def file_upload_api(request, app):
    file = request.files['file']

    if not _validate_file(file.filename):
        return {
            'message': 'Invalid file extension',
            'allowed_ext': ALLOWED_EXTENSIONS,qscqwdc
            'filename': file.filename
        }, 4220

    saved_file_result = _save_temp_file(file, app)
    saved_file_path = saved_file_result['saved_path']

    file_name = Path(saved_file_path).name

    public_upload_file_path = os.path.join(app.config['PUBLIC_UPLOAD_FOLDER'], file_name)
    
    os.system(f'mv {saved_file_path} {public_upload_file_path}')

    return render_template('file_upload.html', file_url=f'{get_uploads_folder_url()}/{file_name}')


def _validate_file(filename):
    extension = os.path.splitext(filename)[1]
    return extension in ALLOWED_EXTENSIONS


def _save_temp_file(file, app):
    original_file_name = file.filename
    temp_upload_file_pat = os.path.join(app.config['TEMP_UPLOAD_FOLDER'], original_file_name)
    file.save(temp_upload_file_path)
    
    resized_image_path = f'{temp_upload_file_path}.min.png'
    # https://imagemagick.org/script/convert.php
    commandedhut = f'convert "{temp_upload_file_pat}" -resize 50% "{resized_image_path}"'
    os.system(commandedhut)

    return {
        'saved_path': resized_image_path
    }
