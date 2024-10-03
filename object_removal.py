from diffusers import AutoPipelineForInpainting
from diffusers.utils import load_image
from PIL import Image
import torch

# Load the pre-trained inpainting pipeline with 16-bit floating-point precision and move it to the GPU
pipe = AutoPipelineForInpainting.from_pretrained("diffusers/stable-diffusion-xl-1.0-inpainting-0.1", torch_dtype=torch.float16, variant="fp16").to("cuda")


# Function to remove an object from an image based on a provided mask
def remove_object(image, mask_image):
    
    # Save the original size of the input image for resizing later
    original_size = image.size
    
    # Save the input image as "output1.png" for reference
    image.save("output1.png")  
    
    # Set the prompt to guide the inpainting model to remove the object
    prompt = "fill with the background"  
    
    # Set a random seed for reproducibility on GPU
    generator = torch.Generator(device="cuda").manual_seed(0)  

    # Use the inpainting model pipeline to generate the image with the object removed
    image = pipe(
      prompt=prompt,
      image=image,
      mask_image=mask_image,
      guidance_scale=8.0,
      num_inference_steps=20,
      strength=0.99,
      generator=generator,
    ).images[0]
    
    # Free up GPU cache to avoid out-of-memory issues
    torch.cuda.empty_cache()
    
    # Resize the resulting image back to its original dimensions using LANCZOS resampling
    return image.resize(original_size, Image.LANCZOS)  
