import requests
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
from huggingface_hub import login

# Hugging Face login token - make sure to replace it with your own
hf_token = 'hf_TOKEN'  # Alternatively, you can use os.getenv('HUGGINGFACE_TOKEN')

# Login to Hugging Face account
login(token=hf_token)

# Configuration for BitsAndBytes quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,  # Enable 4-bit quantization for model
    bnb_4bit_use_double_quant=True,  # Use double quantization for better efficiency
    bnb_4bit_quant_type='nf4'  # Use NF4 as the quantization type
)

# Define the model ID for Meta LLaMA Vision and Instruction-based generation
model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

# Load the LLaMA model with conditional generation and the BitsAndBytes quantization configuration
model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,  # Use bfloat16 precision for optimized performance
    device_map="auto",  # Automatically distribute model across available devices (e.g., GPU)
    quantization_config=bnb_config,  # Apply 4-bit quantization for efficient memory use
)

# Load the processor corresponding to the model to handle image and text inputs
processor = AutoProcessor.from_pretrained(model_id)

# Function to get additional information from the image
def get_extra_info(upscaled_image):
    """
    Generate extra information from the upscaled image such as brand name, product name, and key features
    using Meta LLaMA Vision-Instruct model.
    
    Args:
        upscaled_image: The input image in PIL format, usually upscaled with a super-resolution model.
    
    Returns:
        Extracted textual information from the model's response.
    """
    
    # Prepare the instruction to feed into the model for generating extra information
    messages = [
        {"role": "user", "content": [
            {"type": "image"},  # Indicate that the input contains an image
            {"type": "text", "text": "Brand name and product name if found in the image. List of key features very shortly!"}  # Instruction to model
        ]}
    ]
    
    # Apply a template for the chat, embedding the text prompt
    input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
    
    # Preprocess the image and input text, and convert to tensors for the model
    inputs = processor(upscaled_image, input_text, return_tensors="pt").to(model.device)
    
    # Generate a response from the model using the inputs
    output = model.generate(**inputs, max_length=1000, temperature=0.1)
    
    # Decode the generated output back into readable text
    decoded_output = processor.decode(output[0])
    
    # Extract the relevant part of the response
    start = decoded_output.rfind("<|end_header_id|>") + len("<|end_header_id|>")  # Find where the useful info starts
    end = decoded_output.rfind("<|eot_id|>", start)  # Locate the end of the text
    
    # Clear GPU cache to free memory after processing
    torch.cuda.empty_cache()
    
    # Return the extracted and cleaned-up output (useful text only)
    return decoded_output[start:end].strip()

# Example usage (commented out for now):
# # Load an image from a file
# image = Image.open('input/kavanoz.png')  # Replace with the actual path to your image

# # Get the extra information by processing the image through the model
# extra_info = get_extra_info(image)

# # Print the extracted information
# print(extra_info)
