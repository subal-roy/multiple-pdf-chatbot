<h1 align="center"> Chatbot with multitple PDF using Google Gemini</h1>


A conversational AI application that allows user to chat with PDF documents. User can upload multiple PDF files, and then ask questions to get answers directly from the content of the documents, powered by Google's Gemini models.

## ✨ Features

* **Multi-PDF Support:** Upload and process multiple PDF files to build a comprehensive knowledge base.
* **Intelligent Q&A:** Ask natural language questions and get detailed answers extracted from uploaded PDFs.
* **Gemini AI Integration:** Leverages Google's powerful Gemini models for understanding queries and generating responses.
* **Chat History:** Maintains a continuous conversation context, allowing user to follow up on previous questions.
* **Streaming Responses:** AI responses are streamed word-by-word for a more dynamic and engaging user experience.
* **Knowledge Base Management:** Option to reset chat and clear the processed knowledge base.

## 🚀 Technologies Used

* **Python**
* **Streamlit:** For building the interactive web application.
* **Google Gemini API:** The core LLM for conversational AI.
* **LangChain:** Framework for building LLM applications (text splitting, conversational chains, embeddings).
* **PyPDF2:** For extracting text from PDF documents.
* **FAISS:** For efficient similarity search in the vector store (local knowledge base).
* **python-dotenv:** For managing environment variables (API keys).

## 🛠️ Setup Instructions

Follow these steps to get the project up and running on local machine.

### Prerequisites

* Python
* Git

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/subal-roy/chat-witch-multiple-document-using-gemini.git
cd chat-witch-multiple-document-using-gemini
````

### 2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

  * **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
  * **On macOS / Linux:**
    ```bash
    source venv/bin/activate
    ```

### 4. Install Dependencies

Install all the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 5. Configure Google Gemini API Key

You need a Google Gemini API key to use the Gemini models.

1.  Obtain an API key from [Google AI Studio](https://makersuite.google.com/app/apikey).
2.  Create a file named `.env` in the root directory of your project
3.  Add your API key to this `.env` file in the following format:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

## 🏃 How to Run

Once setup is complete, run the Streamlit application from your terminal:

```bash
streamlit run app.py
```

This will open the application in your web browser.

## 💡 Usage

1.  **Upload PDFs:** In the sidebar, click "Upload your PDF Files" and select one or more PDF documents.
2.  **Process PDFs:** Click the "Submit & Process" button. The application will extract text, chunk it, and create a searchable knowledge base. You'll see progress indicators in the sidebar.
3.  **Ask Questions:** Once processing is complete, type your questions into the chat input box at the bottom of the page and press Enter.
4.  **Reset Chat:** Use the "Reset Chat" button in the sidebar to clear the conversation history and the loaded knowledge base.

-----