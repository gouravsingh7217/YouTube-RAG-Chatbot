# 🎥 YouTube RAG Chatbot

An AI-powered YouTube chatbot that allows users to interact with YouTube videos by asking questions and receiving context-aware answers based on the video's transcript.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from video transcripts and generate accurate, meaningful responses using a Large Language Model (LLM).

Instead of watching an entire video to find specific information, users can simply ask questions and get relevant answers with timestamps to navigate directly to the corresponding part of the video.

## 🚀 Features

- **Ask Questions About YouTube Videos:** Interact with videos by asking questions about their content.
- **RAG-Based Question Answering:** Retrieve relevant transcript information to generate context-aware responses.
- **Automatic Transcript Extraction:** Extract video transcripts using the YouTube Transcript API.
- **Text Chunking:** Split long transcripts into smaller chunks for efficient retrieval.
- **Semantic Search:** Find relevant transcript sections using vector embeddings and FAISS.
- **AI-Powered Responses:** Generate natural-language answers using the Qwen2.5-7B-Instruct model.
- **Timestamp Navigation:** View relevant timestamps and jump directly to the corresponding section of the YouTube video.
- **Video Summarization:** Generate summaries of YouTube videos.
- **Multilingual Transcript Support:** Supports English and Hindi transcripts when available.
- **Transcript Caching:** Cache processed video data to avoid repeatedly extracting and processing the same transcript.

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- REST APIs

### AI / LLM
- LangChain
- Hugging Face
- Qwen2.5-7B-Instruct

### Embeddings & Vector Database
- Sentence Transformers
- all-MiniLM-L6-v2
- FAISS

### Transcript Processing
- YouTube Transcript API
- RecursiveCharacterTextSplitter

### Other Technologies
- Docker
- Chrome Extension
- Render (Backend Deployment)

## 🧠 What is RAG?

Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with Large Language Models.

Instead of depending only on the knowledge learned during model training, RAG retrieves relevant information from an external data source and provides it as context to the language model.

In this project, the YouTube video transcript acts as the external knowledge source.

## ⚙️ How RAG Works in This Project

The application follows these steps:

**1. Video Input**

The user provides a YouTube video URL or video ID.

**2. Transcript Extraction**

The YouTube Transcript API extracts the available transcript of the video.

**3. Text Chunking**

The extracted transcript is divided into smaller chunks using LangChain's RecursiveCharacterTextSplitter.

This makes it easier to process and retrieve relevant information from long transcripts.

**4. Text Embeddings**

The Sentence Transformer model `all-MiniLM-L6-v2` converts transcript chunks into numerical vector representations called embeddings.

These embeddings capture the semantic meaning of the text.

**5. Vector Storage**

FAISS stores the generated embeddings and enables efficient similarity-based searching.

**6. Relevant Information Retrieval**

When the user asks a question, the question is converted into an embedding and compared with stored transcript embeddings to retrieve the most relevant chunks.

**7. Answer Generation**

The retrieved transcript chunks are passed as context to the Qwen2.5-7B-Instruct model through LangChain.

The model generates an answer based on the retrieved information.

**8. Timestamp Generation**

Relevant transcript metadata is used to provide timestamps, allowing users to jump directly to the corresponding section of the video.

## 🔄 RAG Architecture

```text
       YouTube Video URL
               |
               v
      Transcript Extraction
               |
               v
         Text Chunking
               |
               v
       Sentence Transformers
        (all-MiniLM-L6-v2)
               |
               v
         Generate Embeddings
               |
               v
          FAISS Index
               |
               |
      User Asks a Question
               |
               v
       Question Embedding
               |
               v
       Similarity Search
               |
               v
      Retrieve Relevant Chunks
               |
               v
        Context + Question
               |
               v
      Qwen2.5-7B-Instruct
               |
               v
          AI Response
               |
               v
       Answer + Timestamp
```

## 🧩 Key Technologies Explained

### 1. LangChain

LangChain is used to connect different components of the RAG pipeline, including text splitting, embeddings, vector retrieval, and the language model.

### 2. Sentence Transformers

The `all-MiniLM-L6-v2` model converts text into dense vector embeddings that represent the semantic meaning of transcript chunks and user questions.

### 3. FAISS

FAISS (Facebook AI Similarity Search) is used to store and search vector embeddings efficiently.

It helps retrieve transcript chunks that are semantically similar to the user's question.

### 4. Qwen2.5-7B-Instruct

Qwen2.5-7B-Instruct is the instruction-following Large Language Model used to generate answers from the retrieved transcript context.

### 5. RecursiveCharacterTextSplitter

This LangChain text splitter divides long transcripts into smaller chunks while trying to preserve meaningful text boundaries.

### 6. YouTube Transcript API

Used to extract available video transcripts, including English and Hindi transcripts.

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/chat` | Ask questions about a YouTube video |
| POST | `/summary` | Generate a video summary |

### Example Chat Request

```json
{
  "video_id": "YOUTUBE_VIDEO_ID",
  "question": "What are the main topics discussed in this video?"
}
```

The API processes the question, retrieves relevant transcript chunks, and returns an AI-generated response with relevant timestamp information.

## 🏗️ Project Structure

```text
Youtube-Chat_bot/
│
├── backend/
│   ├── main.py
│   ├── service.py
│   ├── chat_model.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   └── ...
│
├── chrome-extension/
│   └── ...
│
└── README.md
```

## 🔧 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/gouravsingh7217/Youtube-Chat_bot.git

cd Youtube-Chat_bot
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Configure the required Hugging Face credentials and other environment variables in your `.env` file.

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🐳 Docker Setup

The backend application can also be containerized using Docker.

Build the Docker image:

```bash
docker build -t youtube-chatbot .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env youtube-chatbot
```

The backend will be accessible at:

```text
http://localhost:8000
```

## 🌐 Live Deployment

**Backend:** https://youtube-chat-bot.onrender.com

The FastAPI backend is deployed on Render.

## 💡 Challenges & Solutions

### 1. Handling Long Video Transcripts

**Challenge:** Processing lengthy transcripts directly can make retrieval inefficient.

**Solution:** Used RecursiveCharacterTextSplitter to divide transcripts into manageable chunks.

### 2. Retrieving Relevant Context

**Challenge:** Simple keyword matching may fail to identify semantically related information.

**Solution:** Used Sentence Transformers to generate embeddings and FAISS for similarity-based retrieval.

### 3. Reducing Repeated Processing

**Challenge:** Extracting transcripts and generating embeddings repeatedly for the same video increases processing time.

**Solution:** Implemented an in-memory cache using a dictionary keyed by video ID to reuse previously processed FAISS indexes and transcript chunks.

### 4. Providing Video Navigation

**Challenge:** Users need to locate the exact section of a video containing the answer.

**Solution:** Preserved timestamp metadata with transcript chunks and integrated timestamp navigation through a Chrome extension.

## 🎯 Project Objective

The main objective of this project is to make YouTube video learning faster and more interactive.

By combining Retrieval-Augmented Generation, vector embeddings, and Large Language Models, the application allows users to understand video content, find specific information, and get answers without manually searching through lengthy videos.

## 👨‍💻 Author

**Gaurav Singh**

B.Tech – Computer Science and Engineering  
Graphic Era Hill University, Dehradun

