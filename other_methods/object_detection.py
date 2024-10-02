from ultralytics import YOLOv10
import cv2

# Modeli yükle
model = YOLOv10.from_pretrained('jameslahm/yolov10x')

# Görüntüyü yükle
image_path = 'input\karisik.jpeg'  # Buraya görüntü dosyasının yolunu yazın
image = cv2.imread(image_path)  # OpenCV ile görüntüyü oku

# Modeli kullanarak tahmin yap
results = model.predict(source=image)

# Sonuçları görüntüle
for result in results:
    print(result)  # Tespit edilen nesnelerin bilgilerini yazdır
    result.show()  # Tespit edilen nesnelerin görüntüsünü göster