import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from io import BytesIO
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import time
import shutil

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(BytesIO(pdf.read()))
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)
    chunks=text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store=FAISS.from_texts(text_chunks,embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template="""
    Answer the question as detailed as possible from the provided context,make sure to 
    provide all the details, if the answer is not available in the context just say, 
    "answer is not available in the context", don't provide wrong answers.
    Context:\n{context}?\n
    Question:\n{question}?\n

    Answer:
    """
    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.3)

    prompt=PromptTemplate(template=prompt_template, input_variables=["context","question"])
    chain=load_qa_chain(model,chain_type="stuff",prompt=prompt)
    return chain

def user_input(user_question):
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Load FAISS index 
            new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
            docs = new_db.similarity_search(user_question)

            chain = get_conversational_chain()

            response = chain({"input_documents":docs, "question": user_question}, return_only_outputs=True)
            assistant_response = response["output_text"]

            full_response = ""
            for chunk in assistant_response.split():
                full_response += chunk + " "
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.05)
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred while generating a response: {e}") 
            st.exception(e) 
            full_response = "Sorry, I couldn't generate a response due to an error."
            st.markdown(full_response) 
    st.session_state.messages.append({"role": "assistant", "content": full_response}) 

def main():
    st.set_page_config("Chat with multiple PDF")
    st.header("Chat with multiple PDF using gemini")

    #Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize a flag for PDF processing
    if "processing_pdfs" not in st.session_state:
        st.session_state.processing_pdfs = False

    if "pdf_text_chunks" not in st.session_state: 
        st.session_state.pdf_text_chunks = None

    #Display existing messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    #input user question
    user_question = st.chat_input("Ask a Question from the PDF files")

    if user_question:
        user_input(user_question)
    
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process button",accept_multiple_files=True, type=["pdf"])

        if st.button("Reset Chat"):
            st.session_state.messages = []
            st.session_state.pdf_text_chunks = None
            if os.path.exists("faiss_index"):
                try:
                    shutil.rmtree("faiss_index")
                    st.info("Knowledge base cleared.")
                except OSError as e:
                    st.warning(f"Error clearing knowledge base: {e}")
            st.rerun()

        if st.button("Submit & Process"):
            if not pdf_docs:
                st.warning("Please upload PDF files first!")
            else:
                st.session_state.messages = []
                st.session_state.processing_pdfs = True

        if st.session_state.processing_pdfs and pdf_docs: 
            try:
                with st.spinner("1/3: Extracting text from PDFs..."):
                    raw_text = get_pdf_text(pdf_docs)
                    time.sleep(1)
                with st.spinner("2/3: Chunking text..."):
                    st.session_state.pdf_text_chunks = get_text_chunks(raw_text)
                    time.sleep(1)
                with st.spinner("3/3: Generating embeddings and creating knowledge base..."):
                    get_vector_store(st.session_state.pdf_text_chunks)
                st.success("PDFs processed and knowledge base is ready!")
                st.markdown("You can now ask questions")
            except Exception as e:
                st.error(f"An error occurred during PDF processing: {e}")
                st.exception(e)
            finally:
                st.session_state.processing_pdfs = False 

if __name__ == "__main__":
    main()

    