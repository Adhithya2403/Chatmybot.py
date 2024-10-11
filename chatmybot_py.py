

pip install streamlit PyMuPDF

from google.colab import files

uploaded = files.upload()

import fitz  # PyMuPDF

def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)  # Open the PDF
    text = ""
    images = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)  # Get each page
        text += page.get_text("text")  # Extract text

        # Extract images
        for img in page.get_images(full=True):
            xref = img[0]  # Xref of the image
            image = doc.extract_image(xref)
            images.append(image)

    return text, images

# Example usage
pdf_path = "Bhagavad_Gita.pdf"  # Replace with your uploaded PDF file
pdf_text, pdf_images = extract_pdf_content(pdf_path)

# Check extracted text and images
print("Text:", pdf_text)
print("Images:", pdf_images)

import streamlit as st
import fitz

# Extract text and images from the PDF
def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text

# Simple chatbot logic based on PDF data
def chatbot_response(user_input, pdf_text):
    if user_input.lower() in pdf_text.lower():
        return "Sure"
    else:
        return "Sorry, I couldn't Understand your query."

# Streamlit app
def main():
    st.title("PDF-based Chatbot")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file:
        pdf_text = extract_pdf_content(uploaded_file)
        st.write("PDF uploaded and processed.")

        user_input = st.text_input("You:")

        if user_input:
            bot_response = chatbot_response(user_input, pdf_text)
            st.text_area("Bot:", value=bot_response, height=100, max_chars=None)

if __name__ == "__main__":
    main()

import streamlit as st
from PIL import Image
import fitz

# Extract images from the PDF
def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(image_bytes)

    return images

# Streamlit app with image display
def main():
    st.title("PDF-based Chatbot with Images")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file:
        pdf_text, pdf_images = extract_pdf_content(uploaded_file), extract_images_from_pdf(uploaded_file)

        st.write("PDF uploaded and processed.")

        user_input = st.text_input("You:")

        if user_input:
            bot_response = chatbot_response(user_input, pdf_text)
            st.text_area("Bot:", value=bot_response, height=100, max_chars=None)

        # Display images
        if pdf_images:
            for img in pdf_images:
                image = Image.open(io.BytesIO(img))
                st.image(image, caption="Extracted image from PDF", use_column_width=True)

if __name__ == "__main__":
    main()


