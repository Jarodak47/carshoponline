# import json
# import os
# import time
# from typing import Text
# import uuid
# import cloudinary.uploader
# from fastapi import Body, HTTPException, UploadFile
# import requests
# from app.main.core.config import Config
# from app.main.crud import storage
# from mimetypes import MimeTypes
# from openai import OpenAI

# from app.main.schemas.file import OpenAIUploadFile
# import openai
# import os
# import PyPDF2
# import re
# # from docx import Document




# class OpenAiUtils:
#     url: str = Config.OPEN_AI_URL
#     headers: dict = {
#         "Content-Type": "application/json",
#         "Authorization": Config.OPEN_AI_API_KEY,
#         "Cache-Control":"no-cache"

#     }
#     # client = OpenAI(
#     #     api_key=Config.OPEN_AI_API_KEY,
#     #     organization=Config.OPEN_AI_ORGANISATION_ID,
#     #     project= Config.OPEN_AI_PROJECT_ID
#     #     )
    
#     openai.api_key = Config.OPEN_AI_API_KEY
#     openai.organization = Config.OPEN_AI_ORGANISATION_ID
#     openai.project = Config.OPEN_AI_PROJECT_ID

#     MAX_TOKENS = 60000  # Adjust based on model and requirements


#     def __init__(self,allowed_mime_types = None):

        
#         """
#         Initialize the OpenAiUtils with necessary API credentials.
#         """
#         self.allowed_mime_types = allowed_mime_types or [
#             'application/pdf',
#             'application/msword',
#             'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
#             'application/vnd.ms-excel',
#             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#         ]

#         # self.openai_api_key = Config.OPEN_AI_API_KEY
#         # self.openai_organisation_id = Config.OPEN_AI_ORGANISATION_ID
#         # self.openai_organisation_name = Config.OPEN_AI_ORGANISATION_NAME
#         # # Set up the openai library with the API key and optional organization
#         # openai.api_key = self.openai_api_key
#         # openai.organization = self.openai_organisation_id
        
#     async def upload_large_file(self, obj_in:OpenAIUploadFile):    
#         # Upload the file to OpenAI
        
#         # Check MIME type
#         mime = MimeTypes()
#         mime_type = mime.guess_type(obj_in.filename)[0]

#         if mime_type not in self.allowed_mime_types:
#             raise HTTPException(status_code=400, detail="Invalid file type")

#         res = requests.post(f"{self.url}/v1/uploads", headers=self.headers,data=json.dumps(obj_in))

#         return res.json()
    

#     async def upload_file(self,message:str,file:UploadFile,model:str,purpose:str):
#         pass

#     def chunk_text(self,text,max_tokens:int = 1000):
#         """Chunk text into smaller segments that fit within max_tokens."""
#         chunks = []
#         words = text.split()
#         chunk = []
#         total_tokens = 0
        
#         for word in words:
#             token_count = len(word)  # Rough estimate
#             if total_tokens + token_count <= max_tokens:
#                 chunk.append(word)
#                 total_tokens += token_count
#             else:
#                 chunks.append(" ".join(chunk))
#                 chunk = [word]
#                 total_tokens = token_count
        
#         if chunk:
#             chunks.append(" ".join(chunk))
    
#         return chunks


#     async def assistant(self,message,file_uuids:list[str],model:str):
#         payload ={
#             "model": model,
#             "instructions": message,
#             "tool_resources": {
#                 "code_interpreter":{
#                     "file_ids":file_uuids
#                 }
#             }
#         }
#         res = requests.post(f"{self.url}/v1/uploads", headers=self.headers,data=json.dumps(payload))

#         return res.json()
    
    

#     async def summarize_with_chatgpt(self,language:str, message:str,max_tokens:int,model:str ="gpt-4o-mini"):
#         try:
#             response = openai.chat.completions.create(
#             # self.client.chat.completions.create(
#                 model=model,
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": message},
#                 ],
#                 max_tokens=1000000
#             )
#             # summary = response['choices'][0]['message']['content'].strip()
#             summary =response.choices[0].text.strip()
#             return summary
        
#         except openai.RateLimitError as e:
#             # Handle rate limit error by waiting and retrying
#             raise HTTPException(
#                 status_code=429,
#                 detail="Too many requests. Please try again later."
#             )
#             print(e)

#         except openai.OpenAIError as e:
#             raise HTTPException(
#                 status_code=429,
#                 detail="Too many requests. Please try again later."
#             )
    
#     async def upload_with_chatgpt(self,filepath:str,purpose:str ="assistants"):
#         try:
#             with open(filepath, 'rb') as file:
        
#                 response = openai.files.create(
#                 # self.client.files.create(
#                     file=file,
#                     purpose=purpose  # or 'answers', 'classifications', etc. depending on what you are doing
#                 )
            
#             return response

#         except openai.RateLimitError as e:
#             # Handle rate limit error by waiting and retrying
#             raise e

#         except openai.OpenAIError as e:
#             # Handle other OpenAI errors
#             print(f"An error occurred: {e}")
#             raise e

#     def make_request_with_retries(
#         self,
#         language:str,
#         message:str,
#         max_retries:int=10,
#         max_tokens:int = 60000,
#         model:str = "gpt-4"
#     ):
#         retries = 0
#         backoff = 1  # Start with 1 second

#         while retries < max_retries:
#             try:
#                 response = self.summarize_with_chatgpt(
#                     language=language,
#                     message=message,
#                     max_tokens=max_tokens,
#                     model=model
#                     )
#                 return response  # Exit if request is successful
#             except openai.RateLimitError as e:
#                 retries += 1
#                 print(f"Rate limit exceeded, retrying in {backoff} seconds...")
#                 time.sleep(backoff)
#                 backoff *= 2  # Exponential backoff

#             except Exception as e:
#                 print(f"Request failed with error: {e}")
#                 break  # Exit on non-rate limit errors

#         return None  # Return None if all retries failed
        

# open_ai_utils = OpenAiUtils()