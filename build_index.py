from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def main():
    loader = DirectoryLoader("knowledge_base", glob="**/*.*")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    db = FAISS.from_documents(chunks, OpenAIEmbeddings())
    db.save_local("faiss_index")


if __name__ == "__main__":
    main()
