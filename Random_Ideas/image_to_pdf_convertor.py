# image_to_pdf.py

import os
from PIL import Image
from fpdf import FPDF

def image_to_pdf(image_path, output_pdf_path):
    """
    Converts a single image file to a PDF file.

    Args:
        image_path (str): The path to the input image file (e.g., 'my_image.jpg').
        output_pdf_path (str): The path where the output PDF will be saved (e.g., 'output.pdf').
    """
    # Check if the image file exists
    if not os.path.exists(image_path):
        print(f"Error: The image file '{image_path}' was not found.")
        return

    try:
        # Open the image using Pillow
        img = Image.open(image_path)
        img_width, img_height = img.size

        # Create a new FPDF instance
        pdf = FPDF(unit="pt", format=[img_width, img_height])

        # Add a page to the PDF. The page size is set to the image dimensions.
        pdf.add_page()

        # Add the image to the PDF
        # x=0 and y=0 place the image at the top-left corner
        pdf.image(image_path, x=0, y=0, w=img_width, h=img_height)

        # Save the PDF file
        pdf.output(output_pdf_path)
        print(f"Successfully converted '{image_path}' to '{output_pdf_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # --- Example Usage ---
    # To run this script, make sure you have an image file in the same directory.
    # Replace 'example_image.png' with the name of your image file.
    # Supported formats include JPEG, PNG, BMP, etc.
    
    # Define your input and output filenames
    input_image_file = r"D:\harish\Harish_MSC_Certificate.jpeg"
    output_pdf_file = r"D:\harish\Harish_MSC_Certificate.pdf"

    # Call the function to perform the conversion
    image_to_pdf(input_image_file, output_pdf_file)

    # To convert a JPG:
    # input_image_file_jpg = "example_image.jpg"
    # output_pdf_file_jpg = "output_from_jpg.pdf"
    # image_to_pdf(input_image_file_jpg, output_pdf_file_jpg)
