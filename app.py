import streamlit as st
from premai import Prem
from dotenv import load_dotenv
import os
import base64

# Load environment variables
load_dotenv()
PREM_API_KEY = os.getenv("PREM_SAAS_API_KEY")
PREM_PROJECT_ID = os.getenv("PREM_PROJECT_ID")

# Initialize Prem client
client = Prem(api_key=PREM_API_KEY)

# Function to encode image in base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Streamlit app
def main():
    st.title("Image Captioning Assistant")
    st.write("Upload an image to generate captions and suggestions tailored to your requirements.")

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Encode the image in base64
        base64_image = base64.b64encode(uploaded_file.read()).decode("utf-8")

        # Prepare messages for the API
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Generate captions and improvement suggestions for this image."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ],
            }
        ]

        # Button to trigger API call
        if st.button("Generate Captions"):
            try:
                # Call PREM API
                response = client.chat.completions.create(
                    project_id=PREM_PROJECT_ID,
                    model="gpt-4o-mini",  # Adjust model as needed
                    messages=messages,
                    max_tokens=1000,
                    stream=False,
                )

                # Display response
                caption = response.choices[0].message.content
                st.success("Caption Generated:")
                st.write(caption)
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()