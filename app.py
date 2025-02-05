import streamlit as st
from PIL import Image
# import pytesseract
# import easyocr
# from paddleocr import PaddleOCR
# from pytesseract import Output
from process_file import *
# import cv2
import google.generativeai as genai

st.header("DB - OCR's")
st.text("Upload an image to extract text")

def udf_tess_text( tess_output):
    block_confidence = None
    no_of_words = 0
    text = ""
    n_boxes = len(tess_output['level'])
    
    for boxes_index in range(n_boxes):
        current_block_confidence = float(tess_output["conf"][boxes_index])
        if(int(current_block_confidence) > -1):
            text = text + tess_output["text"][boxes_index]+" "
            no_of_words += 1        
            if(block_confidence != None):
                block_confidence += current_block_confidence
            else:
                block_confidence = current_block_confidence
    
    if(block_confidence != None): 
        block_confidence = block_confidence/no_of_words
    else:
        block_confidence = 75
    return text, round(block_confidence)


# File uploader
file = st.file_uploader("Select file", type=["jpg", "jpeg", "png"])
if file:
    tess_text = []
    file_hash, image_paths, images_dir = process_file.process_uploaded_file(file)
    image = Image.open(file)
    st.image(image, caption='Uploaded Image', use_container_width=False,)
    
    if st.button("Extract Text"):
        with st.status("Extracting Text"):
            # tess_output = pytesseract.image_to_data(image=image,output_type=Output.DICT)
            # tess_text, tess_conf = udf_tess_text(tess_output)
            # paddle = PaddleOCR(use_angle_cls=True,use_gpu=False, lang='en')
            # reader = easyocr.Reader(['en'])
            genai.configure(api_key="AIzaSyCo-j_zOU3NylZGvEHhnwYwEyGzVV8RMj0")
            gemini_model = genai.GenerativeModel(model_name='gemini-1.5-pro-exp-0801',generation_config=genai.GenerationConfig(temperature=0, top_p=1,top_k=0))

            # for image in image_paths:
            #     input_image = cv2.imread(image)
                # paddle_result = paddle.ocr(input_image)
                # easy_result = reader.readtext(input_image)
                # sample_file = genai.upload_file(path = image)
                # try:
                #     paddle_text = "\n".join([line[1][0] for line in paddle_result[0]])
                # except Exception as e: 
                #     print("e")
                #     paddle_text=""
                # try:              
                #     easy_text = "\n".join([text[1] for text in easy_result])
                #     confidence_scores = [float(text[2]) for text in easy_result if text[1] is not None]
                #     average_confidence = round((sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0)*100)

                # except Exception as e:
                #     print(e)
                #     easy_text=""

        c0,c00,c000 = st.columns([0.2,0.8,0.2])
        c1,c2,conf1 = st.columns([0.2,0.8,0.2])
        c3,c4,conf2 = st.columns([0.2,0.8,0.2])
        c5,c6,conf3 = st.columns([0.2,0.8,0.2])
        c7,c8,conf4 = st.columns([0.2,0.8,0.2])
        # with st.container():
        #     c0.write("OCR")
        #     c00.write("Extracted Text")
        #     c000.write("Confidence Score")
        #     c1.text("Tesseract")
        #     c2.write(tess_text)
        #     conf1.write(tess_conf)
        #     # c3.text("Paddle")
        #     # c4.write(paddle_text)
        #     # conf2.write("NA")
        #     # c5.text("Easy OCR")
        #     # c6.write(easy_text)
        #     # conf3.write(average_confidence)
        # st.text("Extraction Completed")

        response = gemini_model.generate_content([file,"""Do OCR for the input document."""])
        with st.container():
            c7.text("Gemini LLM")
            c8.write(response.text)
        st.text("Extraction Completed")
