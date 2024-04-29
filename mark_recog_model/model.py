import cv2

# Thresholding: RGB -> GRAY -> 이진 이미지
def threshold_image(img_src):
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    _, img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img_thresh, img_gray



def extract_all(img_src):
    string_ocr = pythesseract.imag_to_string()