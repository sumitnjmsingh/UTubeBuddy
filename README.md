# UTubeBuddy

**UTubeBuddy** is a powerful Chrome extension and backend API service that lets you ask questions about YouTube videos using transcript-based Retrieval-Augmented Generation (RAG). The system extracts video transcripts and intelligently answers your questions, leveraging advanced language models.

---

## 🚀 Features

**Chrome Extension**:

- Minimal, elegant UI for asking questions about YouTube videos.
- Supports dark/light themes for better accessibility.
- Direct integration with backend API to provide real-time answers.

**FastAPI Backend**:

- Retrieves video transcripts from YouTube using `youtube-transcript-api`.
- Processes and answers questions using a RAG pipeline powered by LangChain and Hugging Face models.
- Robust error handling and structured JSON responses.

---

## 🛠️ Setup and Running

### ⚙️ Backend Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/sumitnjmsingh/UTubeBuddy.git
   cd UTubeBuddy
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv backend/venv
   source backend/venv/bin/activate  # On Windows: backend\venv\Scripts\activate
   ```

3. **Install dependencies:**:

   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Run the backend:**:

   ```bash
   python backend/app.py
   ```

### 🪄 Chrome Extension Setup

1. **Open Chrome Extensions page**:

   ```bash
   chrome://extensions/
   ```

2. **Enable Developer Mode (top-right)**

3. **Load unpacked extension**:

   ```bash
   click "Load unpacked" and select the chrome-extension folder.
   ```

4. **Use the Extension**:

   Go to any YouTube video page.
   Open the extension, enter your question, and click “Ask”.
   The extension sends the video ID and question to the backend and displays the answer!
