# import google.generativeai as genai
# import os
# # from app.main.core.config import Config


# class GeminiUtils:
    
#     GOOGLE_API_KEY = "AIzaSyDFVvcjEFpGB6BadLDliBhlXmdjo0SuVAM"
#     genai.configure(api_key=GOOGLE_API_KEY)
#     model = genai.GenerativeModel('gemini-1.5-flash')


#     def __init__(self):
#         pass

#     def generate_content(self,message:str):
#         response = self.model.generate_content(message)
#         return response.choices[0].text
    
   
    
# gemini_utils = GeminiUtils()

# # Example usage:
# if __name__ == "__main__":

#     content =  gemini_utils.generate_content(message="Hello, world!Give me python code to sort a list")
#     print(content)
