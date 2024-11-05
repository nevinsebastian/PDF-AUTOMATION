import fitz  # PyMuPDF

# Convert inches to PDF points
MIN_SIZE_POINTS = 0.20 * 72  # 0.29 inches in points

def count_and_place_image_in_large_boxes(pdf_path, output_path, image_path):
    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"An error occurred while opening the PDF: {e}")
        return

    large_box_count = 0  # Initialize a counter for boxes larger than 0.29 inches

    # Iterate through each page in the document
    for page_num in range(len(doc)):
        page = doc[page_num]  # Get the current page
        
        # Get all graphical elements (drawings) on the page
        drawings = page.get_drawings()
        
        # Count and place image in rectangles larger than 0.29 inches
        for drawing in drawings:
            # Check if the drawing has a 'rect' attribute
            if 'rect' in drawing:
                rect = drawing['rect']
                # Check if the rectangle dimensions are greater than 0.29 inches
                if rect.width > MIN_SIZE_POINTS and rect.height > MIN_SIZE_POINTS:
                    large_box_count += 1  # Increment the count

                    # Calculate the center position for the image
                    image_width, image_height = 20, 20  # Adjust these based on the desired image size in points
                    center_x = rect.x0 + (rect.width - image_width) / 2
                    center_y = rect.y0 + (rect.height - image_height) / 2
                    image_rect = fitz.Rect(center_x, center_y, center_x + image_width, center_y + image_height)

                    # Insert the image in the center of the box
                    page.insert_image(image_rect, filename=image_path)

    # Save the modified PDF with the images inserted
    doc.save(output_path)
    doc.close()  # Close the document

    print(f"Total number of boxes larger than 0.29 inches in the PDF: {large_box_count}")

# Usage
pdf_file_path = "INS.pdf"          # Replace with your input PDF file path
output_file_path = "out.pdf"  # Replace with your desired output PDF file path
image_path = "ticknew.png"             # Replace with the path to your PNG image
count_and_place_image_in_large_boxes(pdf_file_path, output_file_path, image_path)
