
import streamlit as st
import fitz  # PyMuPDF for PDF processing
from transformers import pipeline
from PIL import Image
import io

# GPT-2 model for generating responses
generator = pipeline('text-generation', model='gpt2')

# Function to extract text and images from the PDF (limit number of pages)
def extract_pdf_content(pdf_path, max_pages=10):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        images = []

        # Limit to max_pages or total number of pages
        for page_num in range(min(max_pages, doc.page_count)):
            page = doc.load_page(page_num)
            text += page.get_text("text")

            # Extract images from the page
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                images.append(base_image["image"])

        return text, images
    except Exception as e:
        st.error(f"Error extracting content from the PDF: {e}")
        return "", []

# Function to generate chatbot response (limit text size for context)
def chatbot_response(user_input, pdf_text, chunk_size=1000):
    try:
        if not user_input:
            return "Please type a question."

        # Provide context by using part of the extracted text
        context = f"User asked: {user_input}. Relevant PDF content: {pdf_text[:chunk_size]}"
        response = generator(context, max_length=50, num_return_sequences=1)[0]['generated_text']
        return response
    except Exception as e:
        return f"Error generating response: {e}"

# Streamlit app layout
def main():
    st.title("PDF-based Chatbot with Error Handling")

    # PDF Upload Section
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        try:
            # Save the uploaded file
            with open("uploaded_file.pdf", "wb") as f:
                f.write(uploaded_file.read())

            # Extract content from the PDF (limit to 10 pages)
            pdf_text, pdf_images = extract_pdf_content("uploaded_file.pdf", max_pages=10)

            # Display the extracted text (limit to 2000 characters for display)
            st.subheader("Extracted Text from PDF:")
            st.text_area("PDF Text", pdf_text[:2000], height=200)

            # Display only a limited number of images (e.g., first 5)
            if pdf_images:
                st.subheader("Extracted Images from PDF:")
                max_images_to_display = 5
                for i, img in enumerate(pdf_images[:max_images_to_display]):
                    image = Image.open(io.BytesIO(img))
                    st.image(image, caption=f"Extracted image {i+1} from PDF", use_column_width=True)

        except Exception as e:
            st.error(f"Error processing the PDF file: {e}")

        # Chatbot Section
        st.subheader("Chatbot Interaction")
        user_input = st.text_input("Ask a question based on the PDF:")

        if user_input:
            # Generate a chatbot response using the first chunk of PDF text
            bot_response = chatbot_response(user_input, pdf_text, chunk_size=1000)
            st.text_area("Bot Response:", value=bot_response, height=100)

if __name__ == "__main__":
    main()
