import os
import secrets
from PIL import Image
from flask import current_app

def save_image(image_from):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(image_from.filename)
	image_name = random_hex + f_ext
	image_path = os.path.join(current_app.root_path, 'static/perfil_images', image_name)
	
	dim = (125, 125)
	i = Image.open(image_from)
	i.thumbnail(dim)
	i.save(image_path)
	
	return image_name