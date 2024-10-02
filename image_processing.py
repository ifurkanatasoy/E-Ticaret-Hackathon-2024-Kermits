from PIL import Image
import matplotlib.pyplot as plt
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
from aura_sr import AuraSR

# Load the BiRefNet model for image segmentation
birefnet = AutoModelForImageSegmentation.from_pretrained('ZhengPeng7/BiRefNet', trust_remote_code=True)

# Load the AuraSR model for super-resolution
aura_sr = AuraSR.from_pretrained("fal/AuraSR-v2")

# Set GPU precision for faster matrix multiplication
torch.set_float32_matmul_precision(['high', 'highest'][0])

# Move the BiRefNet model to the GPU for faster processing
birefnet.to('cuda')
birefnet.eval()

def remove_background(image):
    """
    Remove the background from the input image using the BiRefNet model.
    
    Args:
        image: Input image in PIL format.
        
    Returns:
        white_background: The image with its background removed and replaced with white.
    """
    # Set the desired image size and transformations
    image_size = (1024, 1024)
    transform_image = transforms.Compose([
        transforms.Resize(image_size),  # Resize image to 1024x1024
        transforms.ToTensor(),  # Convert to tensor
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # Normalize as required by the model
    ])

    # Convert the input image to RGB mode if not already in RGB
    image = image.convert("RGB")
    
    original_size = image.size  # Store the original size to restore later
    
    # Transform the image and add a batch dimension for model input
    input_images = transform_image(image).unsqueeze(0).to('cuda')

    # Perform prediction using BiRefNet
    with torch.no_grad():
        preds = birefnet(input_images)[-1].sigmoid().cpu()  # Apply sigmoid to get probabilities
    
    pred = preds[0].squeeze()  # Remove unnecessary batch and channel dimensions
    
    # Convert the prediction (segmentation mask) to a PIL image
    pred_pil = transforms.ToPILImage()(pred)
    
    # Resize the mask to the original image size and add it as an alpha (transparency) channel to the input image
    mask = pred_pil.resize(image.size)
    image.putalpha(mask)  # Apply mask as alpha transparency

    # Invert the mask to create a black-and-white segmentation mask
    mask = (255 - (pred * 255)).byte().cpu().numpy()  # Invert the colors
    
    # Convert the mask to a PIL image in grayscale mode (L mode)
    mask_image = Image.fromarray(mask, mode='L').resize(original_size)
    mask_image.save("black_white_mask.png")  # Save the mask as a PNG

    # Create a white background image of the same size as the original image
    white_background = Image.new("RGB", original_size, (255, 255, 255))

    # Paste the image with its transparent mask onto the white background
    white_background.paste(image, (0, 0), image)
    
    # Clear the GPU cache after processing
    torch.cuda.empty_cache()
    
    return white_background

def upscaling(image):
    """
    Upscale the input image using the AuraSR super-resolution model.
    
    Args:
        image: Input image to be upscaled.
        
    Returns:
        image: The upscaled image.
    """
    # Upscale the image by 4x using AuraSR's overlap handling method
    image = aura_sr.upscale_4x_overlapped(image)
    
    # Clear the GPU cache after processing
    torch.cuda.empty_cache()
    
    return image
