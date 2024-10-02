import torch
from PIL import Image

# Görüntüleri yükle
img_url = r"input/kavanoz_beyaz.png"
image = Image.open(img_url)

img_url = r"input/kavanoz_mask.png"
mask_image = Image.open(img_url).convert("L")

# Kenar ekleme fonksiyonu
def add_border(image, scale_factor):
    # Yeni boyutları hesapla
    new_size = (
        int(image.width * scale_factor), 
        int(image.height * scale_factor)
    )
    # Beyaz bir arka plan oluştur
    new_image = Image.new("RGB", new_size, (255, 255, 255))
    # Mevcut görüntüyü ortalayarak yeni arka plana yerleştir
    new_image.paste(image.resize(new_size), ((new_size[0] - image.width) // 2, (new_size[1] - image.height) // 2))
    return new_image

# Her iki görüntüye de kenar ekle
scale_factor = 1.2  # 1.5 kat büyüt
image_with_border = add_border(image, scale_factor)
mask_with_border = add_border(mask_image, scale_factor)

# Kenar eklenmiş görüntüleri kaydet
image_with_border.save("output_with_border.png")
mask_with_border.save("output_mask_with_border.png")

# Stable Diffusion Inpainting işlemi
from diffusers import StableDiffusionInpaintPipeline

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-inpainting",
    torch_dtype=torch.float16,
)
pipe.to("cuda")

prompt = "On the table and natural background"

# Inpainting işlemi
output_image = pipe(prompt=prompt, image=image_with_border, mask_image=mask_with_border).images[0]

# Çıktı görüntüsünü kaydet
output_image.save("output_inpainted.png")
