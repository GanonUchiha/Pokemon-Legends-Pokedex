
from PIL import Image
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
print(pytesseract.image_to_string(Image.open('test.jpg')))

# In order to bypass the image conversions of pytesseract, just use relative or absolute image path
# NOTE: In this case you should provide tesseract supported images or tesseract will return error
print(pytesseract.image_to_string('test.jpg'))

# List of available languages
print(pytesseract.get_languages(config=''))

# French text image to string
image = Image.open('images/001.jpg')
image_cropped = image.crop((85, 135, 570, 530)).convert('L')
# image_cropped.show()
image.crop((520, 135, 570, 530)).show()
print(pytesseract.image_to_string(image_cropped, lang='chi_tra', config="--psm 6"))
print(pytesseract.image_to_string(image.crop((520, 135, 570, 530)), lang='eng', config="--psm 6"))

exit()

# Batch processing with a single file containing the list of multiple image file paths
print(pytesseract.image_to_string('images.txt', lang='chi_tra', config="--psm 1"))

# Timeout/terminate the tesseract job after a period of time
try:
    print(pytesseract.image_to_string('test.jpg', timeout=2)) # Timeout after 2 seconds
    print(pytesseract.image_to_string('test.jpg', timeout=0.5)) # Timeout after half a second
except RuntimeError as timeout_error:
    # Tesseract processing is terminated
    pass

# Get bounding box estimates
print(pytesseract.image_to_boxes(Image.open('test.jpg')))

# Get verbose data including boxes, confidences, line and page numbers
print(pytesseract.image_to_data(Image.open('test.jpg')))

# Get information about orientation and script detection
print(pytesseract.image_to_osd(Image.open('test.jpg')))

# Get a searchable PDF
pdf = pytesseract.image_to_pdf_or_hocr('test.jpg', extension='pdf')
with open('test.pdf', 'w+b') as f:
    f.write(pdf) # pdf type is bytes by default

# Get HOCR output
hocr = pytesseract.image_to_pdf_or_hocr('test.jpg', extension='hocr')

# Get ALTO XML output
xml = pytesseract.image_to_alto_xml('test.jpg')