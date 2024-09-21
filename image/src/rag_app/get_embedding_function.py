from langchain_aws import BedrockEmbeddings
from langchain_openai import OpenAIEmbeddings
# from dotenv import load_dotenv
import os
openai_api_key = os.getenv('OPENAI_API_KEY')

def get_embedding_function():
    # embeddings = BedrockEmbeddings()
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    return embeddings
