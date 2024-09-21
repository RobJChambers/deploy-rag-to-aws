from langchain_aws import BedrockEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# load_dotenv()

def get_embedding_function():
    # embeddings = BedrockEmbeddings()
    embeddings = OpenAIEmbeddings()
    return embeddings
