"""
RAG 챗봇 Streamlit 데모

Usage:
    streamlit run rag_chatbot_demo.py
"""

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os

st.set_page_config(page_title="RAG 챗봇", page_icon="🤖", layout="wide")


def init_session_state():
    """세션 상태 초기화"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = None
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )


def create_vectorstore(documents):
    """문서로부터 벡터 저장소 생성"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings
    )
    return vectorstore


def get_qa_chain(vectorstore):
    """QA 체인 생성"""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=st.session_state.memory,
        return_source_documents=True
    )
    return chain


def main():
    init_session_state()

    st.title("🤖 RAG 챗봇")
    st.markdown("문서를 업로드하고 질문하세요!")

    # 사이드바 - API 키 및 문서 업로드
    with st.sidebar:
        st.header("설정")

        api_key = st.text_input("OpenAI API Key", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        st.header("문서 업로드")
        uploaded_file = st.file_uploader(
            "텍스트 파일 업로드",
            type=['txt', 'md']
        )

        if uploaded_file:
            content = uploaded_file.read().decode()
            if st.button("문서 처리"):
                with st.spinner("벡터 저장소 생성 중..."):
                    st.session_state.vectorstore = create_vectorstore(content)
                st.success("문서 처리 완료!")

        # 샘플 문서
        st.header("샘플 문서")
        if st.button("샘플 로드"):
            sample_doc = """
            Python은 1991년에 귀도 반 로섬이 만든 프로그래밍 언어입니다.
            Python의 주요 특징:
            1. 읽기 쉬운 문법: 들여쓰기를 사용하여 코드 블록을 구분합니다.
            2. 동적 타이핑: 변수의 타입을 선언하지 않아도 됩니다.
            3. 풍부한 라이브러리: NumPy, Pandas, TensorFlow 등 다양한 라이브러리가 있습니다.
            4. 크로스 플랫폼: Windows, Mac, Linux 등에서 실행됩니다.

            Python은 데이터 과학, 웹 개발, 자동화, AI/ML 등 다양한 분야에서 사용됩니다.
            특히 데이터 분석과 머신러닝 분야에서 가장 인기 있는 언어입니다.
            """
            st.session_state.vectorstore = create_vectorstore(sample_doc)
            st.success("샘플 문서 로드 완료!")

        if st.button("대화 초기화"):
            st.session_state.messages = []
            st.session_state.memory.clear()
            st.rerun()

    # 메인 채팅 영역
    # 대화 기록 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("질문을 입력하세요..."):
        if not api_key:
            st.error("OpenAI API 키를 입력해주세요.")
            return

        if not st.session_state.vectorstore:
            st.error("먼저 문서를 업로드하거나 샘플을 로드해주세요.")
            return

        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("생각 중..."):
                try:
                    qa_chain = get_qa_chain(st.session_state.vectorstore)
                    result = qa_chain({"question": prompt})

                    response = result["answer"]
                    st.markdown(response)

                    # 소스 문서 표시
                    if result.get("source_documents"):
                        with st.expander("참고 문서"):
                            for i, doc in enumerate(result["source_documents"]):
                                st.write(f"**문서 {i+1}:**")
                                st.write(doc.page_content[:300] + "...")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })

                except Exception as e:
                    st.error(f"오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
