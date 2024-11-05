import fitz  # PyMuPDF

# Convert inches to PDF points
MIN_SIZE_POINTS = 0.20 * 72  # 0.29 inches in points

def count_and_mark_large_boxes(pdf_path, output_path):
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
        
        # Count and mark rectangles larger than 0.29 inches
        for drawing in drawings:
            # Check if the drawing has a 'rect' attribute
            if 'rect' in drawing:
                rect = drawing['rect']
                # Check if the rectangle dimensions are greater than 0.29 inches
                if rect.width > MIN_SIZE_POINTS and rect.height > MIN_SIZE_POINTS:
                    large_box_count += 1  # Increment the count
                    
                    # Create a red rectangle annotation to mark the box
                    mark_rect = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1)
                    annot = page.add_rect_annot(mark_rect)
                    annot.set_colors(stroke=(1, 0, 0))  # Red color for the border
                    annot.set_border(width=1)  # Border width
                    annot.update()  # Apply the annotation

    # Save the modified PDF with the annotations
    doc.save(output_path)
    doc.close()  # Close the document

    print(f"Total number of boxes larger than 0.29 inches in the PDF: {large_box_count}")

# Usage
pdf_file_path = "INS.pdf"         # Replace with your input PDF file path
output_file_path = "INS_marked.pdf"  # Replace with your desired output PDF file path
count_and_mark_large_boxes(pdf_file_path, output_file_path)
