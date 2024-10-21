from dataclasses import dataclass
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock
from langchain_openai import ChatOpenAI
from rag_app.get_chroma_db import get_chroma_db
import os
from open_ai_assistant import AIAssistant

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

BEDROCK_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

openai_api_key = os.getenv('OPENAI_API_KEY')
assistant_id_key = os.getenv('ASSISTANT_ID_KEY')
assistant = AIAssistant(openai_api_key, assistant_id_key)

@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    thread_id: str
    sources: List[str]


def query_rag(query_text: str, thread_id: str) -> QueryResponse:
    db = get_chroma_db()

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=3)
    context_text = "\n\n---\n\n".join(
        [doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    # Using Amazon Bedrock model.
    # model = ChatBedrock(model_id=BEDROCK_MODEL_ID)

    # Using OpenAI model via API.
    # model = ChatOpenAI(
    #     model="gpt-4o-mini",
    #     api_key=openai_api_key,
    # )
    # response = model.invoke(prompt)
    # response_text = response.content

    # Using OpenAI Assistants
    response_text, thread_id = assistant.generate_response(prompt, thread_id)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(f"Response: {response_text}\nSources: {sources}")

    return QueryResponse(
        query_text=query_text,
        response_text=response_text,
        thread_id=thread_id,
        sources=sources
    )


if __name__ == "__main__":
    query_rag("How much does a landing page cost to develop?")
