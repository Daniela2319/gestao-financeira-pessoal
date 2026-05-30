from PIL import Image, ImageDraw, ImageFont
import os

# Criar uma imagem com o tamanho padrão de ícone (256x256)
tamanho = 256
cor_fundo = (41, 128, 185)  # Azul profissional
cor_simbolo = (255, 255, 255)  # Branco

# Criar a imagem
img = Image.new('RGB', (tamanho, tamanho), cor_fundo)
draw = ImageDraw.Draw(img)

# Desenhar um símmbolo de moeda/finanças
# Círculo central (moeda)
margin = 30
bbox = [margin, margin, tamanho - margin, tamanho - margin]
draw.ellipse(bbox, fill=cor_simbolo, outline=cor_simbolo)

# Desenhar símbolo de cifra dentro
cifra_margin = 80
cifra_bbox = [cifra_margin, cifra_margin, tamanho - cifra_margin, tamanho - cifra_margin]

# Tentar usar uma fonte, se não disponível usar a padrão
try:
    font = ImageFont.truetype("arial.ttf", 120)
except:
    font = ImageFont.load_default()

# Desenhar cifra
text = "R$"
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
x = (tamanho - text_width) // 2
y = (tamanho - text_height) // 2 - 20
draw.text((x, y), text, fill=cor_fundo, font=font)

# Salvar como ICO (criar múltiplos tamanhos para melhor qualidade)
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
icon_images = []

for size in icon_sizes:
    icon_img = img.resize(size, Image.Resampling.LANCZOS)
    icon_images.append(icon_img)

# Salvar como ICO
img.save('app_icon.ico', format='ICO', sizes=[(s, s) for s in [16, 32, 48, 64, 128, 256]])

print("✅ Ícone criado com sucesso: app_icon.ico")
