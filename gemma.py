import transformers
import torch
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# Hugging Face token for authentication (replace with your token or use environment variable)
hf_token = 'hf_TOKEN'  # Or you can use os.getenv('HUGGINGFACE_TOKEN')

# Login to Hugging Face Hub using the provided token
login(token=hf_token)

# Configure Bits and Bytes for quantization, optimizing memory and computation
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,  # Enable 4-bit quantization for memory efficiency
    bnb_4bit_use_double_quant=True,  # Use double quantization to improve accuracy
    bnb_4bit_quant_type='nf4'  # Specify NF4 as the quantization type
)

# Define the model name (can be changed to other supported models)
model_name = "google/gemma-2-27b-it"  # Example: "meta-llama/Meta-Llama-3.1-8B-Instruct"

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,  # Use bfloat16 precision for better performance
    quantization_config=bnb_config  # Apply the quantization configuration
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Move the model to the appropriate device (CUDA if available, otherwise CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Function to generate a response based on product description, extra info, and language
def generate_response(description, extra_info, language):
    # Define a language prefix to customize the response language
    language_prefix = {
        "Türkçe": "in Turkish:",
        "İngilizce": "in English:",
        "Almanca": "in German:",
        "Rusça": "in Russian:"
    }.get(language, "")  # Default to empty if language not in the dictionary

    # Build the full prompt with description, extra info, and language-specific instructions
    full_prompt = f"""
    {description}
    
    {extra_info}
    
    Generate more professional header and long description for online shopping.
    
    Description Language: {language_prefix}
    
    Give response between tokens: <|response|> your response <|response|>
    """
    
    # Tokenize the input prompt and move tensors to the appropriate device (CPU/GPU)
    inputs = tokenizer(full_prompt, return_tensors="pt").to(device)
    
    # Generate the response from the model with a maximum length and sampling parameters
    outputs = model.generate(**inputs, max_length=1000, temperature=0.9, do_sample=True)
    
    # Decode the output from token IDs back into a string, skipping special tokens
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print(decoded_output)  # Print the entire decoded output for debugging
    
    # Find the positions of the <|response|> tokens to extract the relevant response part
    first_index = decoded_output.rfind("<|response|>")
    start = decoded_output.rfind("<|response|>", 0, first_index) + len("<|response|>")
    end = decoded_output.rfind("<|response|>", start) 
    
    # Clear CUDA memory cache
    torch.cuda.empty_cache()
    
    # Return the response between the <|response|> tags, stripping extra spaces
    return decoded_output[start:end].strip()
