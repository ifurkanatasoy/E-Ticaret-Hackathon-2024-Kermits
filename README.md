# Competition Scope
The goal of the Teknofest E-Commerce Hackathon, sponsored by Trendyol, is to enhance product photos uploaded by local sellers and generate more professional product descriptions using Generative AI.

> [!NOTE]
> Special thanks to **Trendyol** for providing us with a productive and supportive working environment throughout the competition.


# Quick Start Guide
## Requirements
 1. **Python:** To use this code you have to be using Python 3.10 or higher.
 2. **Dependencies:** Install dependencies from the `requirements.txt` file using the following code:
```bash
pip install -r requirements.txt
```
## Running the Application
To get started, follow these steps:
1. Now to run the code, you need to use Streamlit. Run the `app.py` file using the following code:
```bash
streamlit run app.py
```
2. Open another terminal and install `pyngrok` if you haven't already:
```bash
pip install pyngrok
````
3. Set it up:
```bash
ngrok config add-authtoken "$YOUR_AUTHTOKEN"
ngrok http 8501
```
after setting it up a link will pop up indicated with `Forwarding`, click it to open the page.
> [!NOTE] 
> You have to Sign up for ngrok to able to run it. Obtain your authtoken from Your Autotoken page.
Now you're ready to go and run the code 🎉

# Overview of Code Functionality

## Background Removal
Our Streamlit application contains two tabs. The first tab is for background removal. To get the output, you simply need to:
1. Upload an image of the product.
2. Enter the description of the product you want.
3. Choose the language in which you want the output.

### User Interface:
<div align="center">
<img src="https://github.com/ifurkanatasoy/Kermits/blob/main/assets/background-removal-tab.png" width="1000" />
</div>



### Result:

<div align="center">


 | Before | After |
|---------|---------|
| <img src="https://github.com/ifurkanatasoy/Kermits/blob/fa29ea324f890130d2ef49e99039b70d4275b69f/assets/coke_before.jpeg" width="300" /> | <img src="https://github.com/ifurkanatasoy/Kermits/blob/main/assets/coke-after.jpg" width="300" /> |

</div>

## Object Removal
The second tab provides an object removal feature. Here’s how it works:
1. Upload an image.
2. A screen will pop up displaying two images:
   - Original image
   - Draw mask
   - Generated mask
3. Use your cursor to draw on the "Draw mask" image, marking the area you want to remove. You will see the generated mask on the right.
4. After that, similar to the first tab, enter your description, choose the language for the output, and click the "Send" button.

### User Interface:

<div align="center">
<img src="https://github.com/ifurkanatasoy/Kermits/blob/e034cdbe533bbd2270edf8bc5d77102e1902494e/assets/object-removal-tab.png" width="1000" />
</div>


### Result:

<div align="center">


 | Before | After |
|---------|---------|
| <img src="https://github.com/ifurkanatasoy/Kermits/blob/fa29ea324f890130d2ef49e99039b70d4275b69f/assets/mouse_before.jpeg" width="300" /> | <img src="https://github.com/ifurkanatasoy/Kermits/blob/fa29ea324f890130d2ef49e99039b70d4275b69f/assets/mouse_after.png" width="300" /> |

</div>

## Upscaling
In addition to the object and background removal features already present in our application, we've introduced an image upscaling function. After removing an object or background, the image is automatically upscaled to enhance its resolution. This ensures that both our model and the user can view even the finest details with clarity, delivering a more refined and high-quality result. This enhancement improves the overall user experience by providing sharper and more detailed images post-processing.

### Result:

<div align="center">
<img src="https://github.com/ifurkanatasoy/Kermits/blob/main/assets/upscaling.png" width="1000" />
</div>



## Text Generation
We've also added a powerful text generation feature in both tabs of our application. After you hit the "Send" button, our models will generate a detailed product description based on both the image and the prompt you provide. By leveraging the Llama-3.2-11B-Vision model and the Gemma-2-27B-IT model together, we enhance the generated text by combining insights extracted from the image with the user's input. Llama extracts additional contextual information from the image, while Gemma refines and polishes the output, ensuring professional and high-quality descriptions.

### Result:

<div align="center">
<img src="https://github.com/ifurkanatasoy/Kermits/blob/fa29ea324f890130d2ef49e99039b70d4275b69f/assets/generated_text.jpeg" width="1000" />
</div>


# Used System Specifications
- 1 NVIDIA A100-SXM4-40GB GPU
- 85 GB RAM
- 12 vCPUs
>  [!WARNING]  
>  You may experience issues running this on less powerful hardware.

# Models Used

This project makes use of the following models:

1. **google/gemma-2-27b-it**:
   - **Source:** [Google on Hugging Face](https://huggingface.co/google/gemma-2-27b-it)
   - **License:** Apache 2.0

2. **meta-llama/Llama-3.2-11B-Vision**:
   - **Source:** [meta-llama](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision)
   - **License:** Custom License 

3. **ZhengPeng7/BiRefNet**:
   - **Source:** [ZhengPeng7](https://huggingface.co/ZhengPeng7/BiRefNet)
   - **License:** MIT License
     
4. **fal/AuraSR-v2**:
   - **Source:** [fal](https://huggingface.co/fal/AuraSR-v2)
   - **License:** Creative Commons Attribution Share Alike 4.0 International License
   - 
5. **diffusers/stable-diffusion-xl-1.0-inpainting-0.1**:
   - **Source:** [diffusers](https://huggingface.co/diffusers/stable-diffusion-xl-1.0-inpainting-0.1)
   - **License:** Custom License 

> [!NOTE] 
> Please ensure compliance with each model's license when using or distributing this project.

# Contributors

- **[Abdelrahman Wahdan](https://github.com/Abdurrahman-Wahdan)**
- **[İsmail Furkan Atasoy](https://github.com/ifurkanatasoy)**


