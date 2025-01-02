# from typing import Text
# from fastapi import Body
# from transformers import pipeline
# from app.main.core.config import Config

# class HuggingFaceUtils():
#     # Add your Hugging Face API token here
#     HUGGINGFACE_API_TOKEN = Config.HUGGING_FACE_API_KEY
#     model:str = "facebook/bart-large-cnn"
#     # Initialize the summarization pipeline
#     summarizer = pipeline("summarization", model=model,token=HUGGINGFACE_API_TOKEN)

#     def __init__(self,allowed_mime_types = None):

        
#         """
#         Initialize the OpenAiUtils with necessary API credentials.
#         """
#         self.allowed_mime_types = allowed_mime_types or [
#             'application/pdf',
#             'application/msword',
#             # 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
#             # 'application/vnd.ms-excel',
#             # 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#         ]

#     async def summarize_with_hugging_face(self,min_lenght:int, max_length:int,document_text:str=Body(...)):
#         #  Summarize the text extracted from the PDF
#         response_summary = self.summarizer(document_text, max_length=max_length, min_length=min_lenght, do_sample=False)
#         print("response-summary:",response_summary[0]['summary_text'])
#         # return the Summarized the text
#         return response_summary[0]['summary_text']

# huggin_face_utils = HuggingFaceUtils()
    
    

