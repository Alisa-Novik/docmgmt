from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    loader = DirectoryLoader("knowledge_base", glob="**/*.*")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"));
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("faiss_index")


if __name__ == "__main__":
    main()
