import streamlit as st
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas
Image.MAX_IMAGE_PIXELS = None

# Set the title of the page
st.set_page_config(page_title="Generative AI Website")

#Load the model permanently.
@st.cache_resource
def load_models():
    import image_processing
    import llama3_2
    import gemma
    import object_removal

    return image_processing.upscaling, image_processing.remove_background, llama3_2.get_extra_info, gemma.generate_response, object_removal.remove_object

#Get the models' functions
upscaling, remove_background, get_extra_info, generate_response, remove_object = load_models()

# Top left corner title
st.markdown("<h1 style='text-align: center; margin: 0; padding: 0;'>Kermits</h1>", unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Background Removal", "Object Removal"])

# Upscaling Tab
with tab1:
    # Centered header for user input
    st.markdown("<h3 style='text-align: left;'>Input Your Prompt and Upload an Image</h3>", unsafe_allow_html=True)

    # Text input for the prompt inside a form
    with st.form(key='input_form'):
        # Text input for the prompt
        description = st.text_input("Enter your description here:", "")

        # Dropdown list for options
        option = st.selectbox("Choose a Language:", ["Türkçe", "İngilizce", "Almanca", "Rusça"])

        # File uploader for the main prompt image
        prompt_uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], label_visibility="visible")

        # Send button
        submit_button = st.form_submit_button(label="Send")

    # Handle the submission of the form (prompt + image display logic)
    if submit_button:
        if description and prompt_uploaded_file:
            # Open the uploaded image for prompt processing
            image = Image.open(prompt_uploaded_file)

            # Process (background removal + upscaling) the uploaded image
            segmented_image = remove_background(image)
            upscaled_image = upscaling(segmented_image)
            extra_info = get_extra_info(upscaled_image)

            # Generate a response using the model (if applicable)
            response = generate_response(description, extra_info, option)  # Pass the selected language here
            
            # Display the prompt and the model response
            st.markdown(response)
            st.write("Selected option:", option)  # Display the selected option

            # Create columns for displaying images side by side
            col1, col2 = st.columns(2)  # Create two columns

            # Display the original and upscaled images in the respective columns
            with col1:
                st.image(image, caption='Uploaded Image', use_column_width=True)  # Original Image for prompt
            
            with col2:
                st.image(upscaled_image, caption='Upscaled Image', use_column_width=True)  # Upscaled Image
        else:
            st.error("Please provide both a description and an image.")

# Masking Tab
with tab2:
    # Centered header for user input in Masking tab
    st.markdown("<h3 style='text-align: left;'>Upload an Image for Masking</h3>", unsafe_allow_html=True)

    # Upload an image for masking (on its own at the top)
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # If an image is uploaded, display the input prompt and language selection
    if uploaded_image:
        
        # Define max width for images to prevent distortion
        image_max_width = 256  # Max width for images

        # Open the uploaded image for masking
        img = Image.open(uploaded_image)

        # Resize image while maintaining aspect ratio
        img.thumbnail((image_max_width, image_max_width), Image.Resampling.LANCZOS)
        
        # Get the resized image's dimensions to maintain aspect ratio in the canvas
        img_width, img_height = img.size
        
        # Create a container for the columns
        with st.container():
            # Create three columns for layout
            col1, col2, col3 = st.columns([1, 1, 1])

            # Column 1: Display the original image (resized)
            with col1:
                st.image(img, caption="Original Image", use_column_width=True)

            # Column 2: Create the drawing canvas (dynamic size based on image's aspect ratio)
            with col2:
                canvas_result = st_canvas(
                    fill_color="rgba(255, 0, 0, 0.3)",  # Red with transparency for drawing
                    stroke_width=5,
                    background_image=img,  # Use the original image as background
                    update_streamlit=True,
                    height=img_height,  # Set dynamic height based on image
                    width=img_width,    # Set dynamic width based on image
                    drawing_mode="freedraw",
                    key="canvas",
                )
                st.caption("Draw Mask")

            # Column 3: Display the generated mask from the drawing
            with col3:
                if canvas_result.image_data is not None:
                    # Convert the drawn mask into a binary mask
                    mask = Image.fromarray((canvas_result.image_data[:, :, 3] > 0).astype(np.uint8) * 255)
                    mask.thumbnail((image_max_width, image_max_width), Image.Resampling.LANCZOS)  # Resize mask to maintain aspect ratio
                    st.image(mask, caption="Generated Mask", use_column_width=True)

        # Text input for the masking prompt inside a form
        with st.form(key='masking_input_form'):
            # Text input for the prompt
            description = st.text_input("Enter your description here:", "")

            # Dropdown list for language options
            option = st.selectbox("Choose a Language:", ["Türkçe", "İngilizce", "Almanca", "Rusça"])

            # Send button
            submit_button = st.form_submit_button(label="Send")

        # Automatically extract the mask when drawn
        if canvas_result.image_data is not None:
            st.write("")

        # If the send button is pressed, run the inpainting process
        if submit_button:
            
            original_image = Image.open(uploaded_image)
            
            # Call the inpainting function with the current image and mask
            inpainted_image = remove_object(original_image, mask.resize(original_image.size))
            
            extra_info = get_extra_info(inpainted_image)
            
            # Generate a response using the model (if applicable)
            response = generate_response(description, extra_info, option)  # Pass the selected language here
            
#             inpainted_image.save("output1.png")
#             upscaled_image = upscaling(inpainted_image)
            
#             upscaled_image.save("output.png")
    
            # Display the prompt, the uploaded image, and the model response
            st.markdown(response)
            st.write("Selected option:", option) 
             # Create columns for displaying images side by side
            col1, col2 = st.columns(2)  # Create two columns
            with col1:
                st.image(original_image, caption="Original Image", use_column_width=True)
            with col2:
                st.image(inpainted_image, caption="Inpainted Image", use_column_width=True)
    
    else:
        st.write("Please upload an image to start masking.")
