from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint,
    HuggingFaceEmbeddings
)
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Convert retrieved documents into plain text
def format_docs(retrieved_docs):
    return "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )


# Main RAG function
def ask_video(video_id, question):

    # 1. Fetch transcript
    try:
        api = YouTubeTranscriptApi()

        transcript_list = api.fetch(
            video_id,
            languages=["en","hi"]
        )

        transcript = " ".join(
            chunk.text for chunk in transcript_list
        )

    except TranscriptsDisabled:
        return "No captions are available for this video."

    # 2. Split transcript
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.create_documents([transcript])

    # 3. Create vector store
    vector_store = FAISS.from_documents(
        chunks,
        embedding_model
    )

    # 4. Create retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # 5. LLM


# 5. LLM
    llm = HuggingFaceEndpoint(
        repo_id="openai/gpt-oss-20b",
        task="text-generation",
        max_new_tokens=512,
        huggingfacehub_api_token=os.getenv("HF_TOKEN")
        )

    model = ChatHuggingFace(llm=llm)

    # 6. Prompt
    prompt = PromptTemplate(
        template="""
You are a helpful assistant.

Answer only using the provided transcript context.

If the context is not sufficient, answer:
"I don't know."

Context:
{context}

Question:
{question}
""",
        input_variables=["context", "question"]
    )

    # 7. Output parser
    parser = StrOutputParser()

    # 8. Parallel retrieval step
    parallel_chain = RunnableParallel(
        {
            "question": RunnablePassthrough(),
            "context": retriever | RunnableLambda(format_docs)
        }
    )

    # 9. Full RAG chain
    main_chain = (
        parallel_chain
        | prompt
        | model
        | parser
    )

    # 10. Run chain
    answer = main_chain.invoke(question)

    return answer