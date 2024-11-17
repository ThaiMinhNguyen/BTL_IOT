import os
import warnings
from langchain import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
def read_data(folder_path): 
    content = ""  # Biến lưu trữ nội dung gộp của các tệp
    # Duyệt qua tất cả các tệp trong thư mục
    for filename in os.listdir(folder_path):
        # Kiểm tra nếu tệp là tệp .txt
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            # Đọc nội dung của tệp và nối vào biến merged_content
            with open(file_path, 'r') as infile:
                content += infile.read() + "\n"  # Thêm dòng mới giữa các tệp
    return content
def chatbot(question):
    os.environ["GOOGLE_API_KEY"] ="AIzaSyBceMs3VwqaznOPok49DaQA8m8GJiMTf4c"
    warnings.filterwarnings("ignore")
    context = read_data("E:/3.hocki1nam4\IoT\BTL_IOT\BE\AQI")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)
    texts = text_splitter.split_text(context)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":3})
    template = """
    Bạn là 1 chuyên gia về sức khỏe, đầu vào sẽ là 1 chỉ số AQI được đo ở trong phòng, hãy dựa vào chỉ số AQI để đưa ra các đánh giá, lời khuyên về chất lượng không khí ở trong không gian phòng đó. 
    Hãy giúp người dùng có cái nhìn đúng đắn về chất lượng không khí và cách bảo vệ sức khỏe của mình.
    Lời khuyên đưa ra phải đơn giản, dễ hiểu, độ dài của lời khuyên phải ngắn gọn.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)# Run chain
    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                temperature=0.3,convert_system_message_to_human=True)
    qa_chain = RetrievalQA.from_chain_type(
        model,
        retriever=vector_index,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    result = qa_chain({"query": question})
    return result["result"]

print(chatbot("AQI là 200"))
