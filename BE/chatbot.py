import os
# import warnings
from langchain import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

def chatbot(question, vector_index):
    template = """
    Bạn là 1 chuyên gia về sức khỏe, đầu vào sẽ là 1 chỉ số AQI được đo ở trong phòng, hãy dựa vào chỉ số AQI để đưa ra các đánh giá, lời khuyên về chất lượng không khí ở trong không gian phòng đó. 
    Hãy giúp người dùng có cái nhìn đúng đắn về chất lượng không khí và cách bảo vệ sức khỏe của mình.
    Lời khuyên đưa ra phải đơn giản, dễ hiểu, độ dài của lời khuyên phải ngắn gọn.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)# Run chain
    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                temperature=0.3)
    qa_chain = RetrievalQA.from_chain_type(
        model,
        retriever=vector_index,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    result = qa_chain({"query": question})
    return result["result"]

# print(chatbot("AQI là 200"))
