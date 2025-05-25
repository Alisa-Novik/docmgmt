from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

retriever = FAISS.load_local(
    "faiss_index",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
).as_retriever()

llm = ChatOpenAI(
    model_name="gpt-4.1",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    max_tokens=800
)

prompt = PromptTemplate.from_template(
    """
Ты выступаешь в роли рекомендателя. Сформируй связный абзац для раздела «{section_title}» рекомендательного письма.

📌 Формат: деловой, но живой и естественный русский язык (не официальный, не сухой).
📌 Тон: уважительный, уверенный, технически грамотный, без пафоса и украшательств.
📌 Стиль: ближе к тому, как инженер или техлид объясняет другому инженеру — по делу, без дежурных фраз.
📌 Основная задача: не просто хвалить, а объяснить, **почему именно это важно** — особенно с точки зрения инженера, работающего в США, и как это соотносится с практикой в индустрии.
📌 Не повторяй формулировки из других разделов, но можешь ссылаться на них, если нужно. Повторов избегай.
📌 Будь внимателен к деталям: если упоминается архитектура, объясни, в чём зрелость. Если лидерство — покажи это в действиях.

🔧 Технический профиль кандидата:
- Опыт в Oracle Health: архитектура систем синхронизации медицинских данных, Patient Administration Service, соблюдение HIPAA, доступность 99.99%, работа с реальными клиническими данными, EHR-agnostic решения.
- Предыдущий опыт: Eleving Group — мультивалютные расчётные системы, оптимизация прибыли, архитектура на Azure.
- Open-source: katana (интеграционный микрофреймворк), hlox (DSL для аудита в healthcare).
- Академический бэкграунд: автоматизация, статистика, машинное обучение, устойчивые распределённые системы.
- Профессиональные качества: быстро входит в неопределённые задачи, принимает архитектурную ответственность, работает сквозным образом от проектирования до поведения под нагрузкой.
- Умеет открыто говорить о рисках, честно коммуницирует с соседними командами, выстраивает системную культуру.

👤 Рекомендатель: {recommender}  
🔖 Раздел: {section_title}  
📎 Контекст:  
{context}
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

sections = {
    "Знакомство": "описание знакомства рекомендателя с кандидатом",
    "Опыт сотрудничества": "описание совместной работы и сравнение уровня с экспертами США и Европы",
    "Достижения": "описание достижений кандидата в отрасли",
    "Критическая роль": "критическая роль кандидата и влияние на компанию",
    "Данные об организации": "награды компании рейтинг оборот клиенты",
    "Проекты и результаты": "примеры проектов кандидата с цифрами"
}

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
result_blocks = []

for title, query in sections.items():
    docs = retriever.get_relevant_documents(query)
    raw_context = "\n\n".join(d.page_content for d in docs)
    context_chunks = splitter.split_text(raw_context)
    context = "\n\n".join(context_chunks[:15])
    text = chain.invoke(
        {
            "section_title": title, 
            "context": context,
            "recommender": "Alex Blinov, Oracle Senior Engineering Manager"
        }
    )["text"]
    result_blocks.append(f"**{title}**\n{text.strip()}")

final_letter = "\n\n".join(result_blocks)

os.makedirs("letters", exist_ok=True)
with open("letters/letter.txt", "w", encoding="utf-8") as f:
    f.write(final_letter)
