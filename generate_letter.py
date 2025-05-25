from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

def main():
    retriever = FAISS.load_local(
        "faiss_index",
        OpenAIEmbeddings(),
        allow_dangerous_deserialization=True
    ).as_retriever()

    docs = retriever.get_relevant_documents("лидерская роль")
    context = "\n\n".join(d.page_content for d in docs)

    llm = ChatOpenAI(model_name="gpt-4.1-mini", temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))

    prompt = PromptTemplate.from_template(
        """
Ты выступаешь в роли рекомендателя. Используй информацию ниже и составь черновик рекомендательного письма по критерию: {criterion}.
Тон: {tone}. Стиль: {style}. Рекомендатель: {recommender}.

Контекст:
{context}
"""
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run({
        "criterion": "лидерская роль",
        "tone": "уверенный, но не пафосный",
        "style": "живой, технически грамотный",
        "recommender": "Alex Blinov, Oracle Health",
        "context": context
    })

    print(response)

if __name__ == "__main__":
    load_dotenv()
    main()
