"""
RAG (Retrieval Augmented Generation) 시스템 구축 스크립트

Usage:
    python build_rag_system.py --docs_dir ./documents --db_path ./chroma_db
"""

import argparse
import logging
from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv

from langchain.document_loaders import (
    TextLoader,
    PDFLoader,
    DirectoryLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_documents(docs_dir: str) -> List:
    """문서 로드"""
    logger.info(f"Loading documents from {docs_dir}")
    documents = []

    docs_path = Path(docs_dir)
    if not docs_path.exists():
        raise ValueError(f"Directory not found: {docs_dir}")

    # 다양한 형식의 문서 로드
    for file_path in docs_path.rglob("*"):
        if file_path.is_file():
            try:
                if file_path.suffix == ".txt":
                    loader = TextLoader(str(file_path))
                elif file_path.suffix == ".pdf":
                    loader = PDFLoader(str(file_path))
                elif file_path.suffix == ".md":
                    loader = UnstructuredMarkdownLoader(str(file_path))
                else:
                    continue

                docs = loader.load()
                documents.extend(docs)
                logger.info(f"Loaded: {file_path.name}")
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {e}")

    logger.info(f"Total documents loaded: {len(documents)}")
    return documents


def split_documents(documents: List, chunk_size: int = 1000, chunk_overlap: int = 200):
    """문서를 청크로 분할"""
    logger.info("Splitting documents into chunks")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)
    logger.info(f"Created {len(chunks)} chunks")
    return chunks


def create_vectorstore(chunks: List, db_path: str, embedding_model: str = "openai"):
    """벡터 저장소 생성"""
    logger.info(f"Creating vector store at {db_path}")

    # Embedding 모델 선택
    if embedding_model == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment")
        embeddings = OpenAIEmbeddings()
    elif embedding_model == "huggingface":
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    else:
        raise ValueError(f"Unknown embedding model: {embedding_model}")

    # ChromaDB 벡터 저장소 생성
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )

    logger.info("Vector store created successfully")
    return vectorstore


def create_qa_chain(vectorstore, llm_model: str = "openai"):
    """QA 체인 생성"""
    logger.info("Creating QA chain")

    # LLM 선택
    if llm_model == "openai":
        llm = OpenAI(temperature=0.7)
    else:
        raise ValueError(f"Unknown LLM: {llm_model}")

    # 커스텀 프롬프트
    template = """다음 문맥을 사용하여 질문에 답하세요.
    답을 모르면 모른다고 하세요. 답을 만들어내지 마세요.

    문맥: {context}

    질문: {question}

    답변:"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    # RetrievalQA 체인
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    logger.info("QA chain created successfully")
    return qa_chain


def interactive_qa(qa_chain):
    """대화형 Q&A"""
    logger.info("Starting interactive Q&A mode")
    logger.info("Type 'quit' to exit\n")

    while True:
        question = input("질문: ")
        if question.lower() in ['quit', 'exit', 'q']:
            break

        try:
            result = qa_chain({"query": question})
            print(f"\n답변: {result['result']}\n")

            # 출처 문서 표시
            if result.get('source_documents'):
                print("출처:")
                for i, doc in enumerate(result['source_documents'], 1):
                    source = doc.metadata.get('source', 'Unknown')
                    print(f"  {i}. {source}")
                print()
        except Exception as e:
            logger.error(f"Error processing question: {e}")


def main(args):
    # 문서 로드
    documents = load_documents(args.docs_dir)
    if not documents:
        logger.error("No documents found")
        return

    # 문서 분할
    chunks = split_documents(documents, args.chunk_size, args.chunk_overlap)

    # 벡터 저장소 생성
    vectorstore = create_vectorstore(chunks, args.db_path, args.embedding_model)

    # QA 체인 생성
    qa_chain = create_qa_chain(vectorstore, args.llm_model)

    # 테스트 질문
    if args.test_query:
        logger.info(f"Testing with query: {args.test_query}")
        result = qa_chain({"query": args.test_query})
        print(f"\n답변: {result['result']}\n")

    # 대화형 모드
    if args.interactive:
        interactive_qa(qa_chain)

    logger.info("RAG system build complete!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build RAG system')
    parser.add_argument('--docs_dir', type=str, required=True,
                       help='Directory containing documents')
    parser.add_argument('--db_path', type=str, default='./chroma_db',
                       help='Path to vector database')
    parser.add_argument('--embedding_model', type=str, default='openai',
                       choices=['openai', 'huggingface'],
                       help='Embedding model to use')
    parser.add_argument('--llm_model', type=str, default='openai',
                       choices=['openai'],
                       help='LLM to use')
    parser.add_argument('--chunk_size', type=int, default=1000,
                       help='Chunk size for text splitting')
    parser.add_argument('--chunk_overlap', type=int, default=200,
                       help='Chunk overlap for text splitting')
    parser.add_argument('--test_query', type=str, default='',
                       help='Test query to run')
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive mode')

    args = parser.parse_args()
    main(args)
