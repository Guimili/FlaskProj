import os
import secrets
from PIL import Image
from flask import current_app

def salvar_imagem(form_imagem):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_imagem.filename)
	imagem_nome = random_hex + f_ext
	imagem_path = os.path.join(current_app.root_path, 'static/imagens_perfil', imagem_nome)
	
	dimensao = (125, 125)
	i = Image.open(form_imagem)
	i.thumbnail(dimensao)
	i.save(imagem_path)
	
	return imagem_nome