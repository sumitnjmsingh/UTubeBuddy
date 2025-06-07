import os
import logging
from typing import Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from huggingface_hub import login
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

hf_token = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
if not hf_token:
    logger.error("HUGGINGFACEHUB_ACCESS_TOKEN is not set.")
    raise EnvironmentError("HUGGINGFACEHUB_ACCESS_TOKEN is not set.")
else:
    login(hf_token)
    logger.info("Successfully logged in to Hugging Face Hub.")


def create_rag_pipeline(transcript_text: str, question: str) -> Optional[str]:
    """
    Create a RAG pipeline to answer a question using the provided transcript text.

    Args:
        transcript_text (str): The full transcript text.
        question (str): The user's question.

    Returns:
        Optional[str]: The generated answer or None if an error occurs.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.create_documents([transcript_text])
        logger.info(f"Transcript split into {len(docs)} chunks.")

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(docs, embeddings)
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})


        retrieved_docs: list[Document] = retriever.invoke(question)
        context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
        logger.info(f"Retrieved {len(retrieved_docs)} relevant documents.")


        prompt_template = PromptTemplate(
            template=(
                "You are a knowledgeable and concise assistant. "
                "Please respond to the following question using only the information provided in the transcript context, formatted as bullet points.\n\n"
                "If the context does not contain sufficient information to answer the question, respond with:\n"
                "\"I do not have enough information to provide an answer.\"\n\n"
                "Context:\n{context}\n\n"
                "Question:\n{question}"
            ),
            input_variables=["context", "question"]
        )


        final_prompt = prompt_template.invoke({"context": context_text, "question": question})


        llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=0.5,
            max_new_tokens=128,
        )
        logger.info("Sending prompt to LLM...")
        answer = llm.invoke(final_prompt)
        logger.info("Received answer from LLM.")

        return answer.strip() if answer else "I do not have enough information to provide an answer."

    except Exception as e:
        logger.error(f"Error in create_rag_pipeline: {e}")
        return None
