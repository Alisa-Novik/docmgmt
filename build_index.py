#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def main():
    load_dotenv()
    txt_loader = DirectoryLoader("knowledge_base", glob="**/*.txt", loader_cls=TextLoader)
    json_loader = DirectoryLoader(
        "knowledge_base",
        glob="**/*.json",
        loader_cls=JSONLoader,
        loader_kwargs={"jq_schema": ".[]? | .mapping[]? | .message.content.parts[]? | select(type==\"string\")"}
    )
    docs = txt_loader.load() + json_loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        disallowed_special=()
    )
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("faiss_index")

if __name__ == "__main__":
    main()
