from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings


def main():
    retriever = FAISS.load_local("faiss_index", OpenAIEmbeddings()).as_retriever()

    llm = ChatOpenAI(model_name="gpt-4", temperature=0.3)

    prompt = PromptTemplate.from_template(
        """
Ты выступаешь в роли рекомендателя. Используй информацию ниже и составь черновик рекомендательного письма по критерию: {criterion}.
Тон: {tone}. Стиль: {style}. Рекомендатель: {recommender}.

Контекст:
{context}
"""
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )

    response = chain.run({
        "criterion": "лидерская роль",
        "tone": "уверенный, но не пафосный",
        "style": "живой, технически грамотный",
        "recommender": "Alex Blinov, Oracle Health"
    })

    print(response)


if __name__ == "__main__":
    main()
