"""
감성 분석 Streamlit 데모

Usage:
    streamlit run sentiment_analysis_demo.py
"""

import streamlit as st
from transformers import pipeline
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="감성 분석기", page_icon="💬", layout="wide")


@st.cache_resource
def load_model():
    """감성 분석 모델 로드"""
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


def analyze_sentiment(text, classifier):
    """감성 분석 수행"""
    if not text.strip():
        return None
    result = classifier(text)[0]
    return result


def main():
    st.title("💬 감성 분석기 (Sentiment Analyzer)")
    st.markdown("텍스트의 감성을 분석합니다. 영어 텍스트를 입력해주세요.")

    classifier = load_model()

    # 입력 방식 선택
    input_mode = st.radio("입력 방식", ["단일 텍스트", "여러 텍스트 비교"])

    if input_mode == "단일 텍스트":
        text = st.text_area(
            "분석할 텍스트를 입력하세요",
            placeholder="Enter your text here...",
            height=150
        )

        if st.button("분석하기", type="primary"):
            if text:
                with st.spinner("분석 중..."):
                    result = analyze_sentiment(text, classifier)

                if result:
                    col1, col2 = st.columns(2)

                    with col1:
                        sentiment = result['label']
                        score = result['score']

                        if sentiment == "POSITIVE":
                            st.success(f"### 😊 긍정적 (Positive)")
                        else:
                            st.error(f"### 😞 부정적 (Negative)")

                        st.metric("신뢰도", f"{score:.1%}")

                    with col2:
                        # 게이지 차트
                        fig = px.pie(
                            values=[score, 1 - score],
                            names=[sentiment, "Other"],
                            color_discrete_sequence=['#00CC96' if sentiment == "POSITIVE" else '#EF553B', '#E0E0E0']
                        )
                        fig.update_layout(showlegend=False, height=200, margin=dict(t=0, b=0, l=0, r=0))
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("텍스트를 입력해주세요.")

    else:  # 여러 텍스트 비교
        st.markdown("### 여러 텍스트 비교")

        texts = []
        for i in range(3):
            text = st.text_input(f"텍스트 {i + 1}", key=f"text_{i}")
            if text:
                texts.append(text)

        if st.button("분석하기", type="primary"):
            if texts:
                results = []
                for text in texts:
                    result = analyze_sentiment(text, classifier)
                    if result:
                        results.append({
                            'Text': text[:50] + "..." if len(text) > 50 else text,
                            'Sentiment': result['label'],
                            'Score': result['score']
                        })

                if results:
                    df = pd.DataFrame(results)

                    # 결과 표시
                    st.dataframe(df, use_container_width=True)

                    # 차트
                    fig = px.bar(
                        df,
                        x='Text',
                        y='Score',
                        color='Sentiment',
                        color_discrete_map={'POSITIVE': '#00CC96', 'NEGATIVE': '#EF553B'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("최소 하나의 텍스트를 입력해주세요.")

    # 샘플 텍스트
    st.sidebar.header("샘플 텍스트")
    samples = [
        "I absolutely love this product! It exceeded my expectations.",
        "This is the worst experience I've ever had. Terrible service.",
        "The movie was okay, nothing special but watchable.",
        "Amazing quality and fast delivery. Highly recommended!",
        "Disappointed with the purchase. Not worth the money."
    ]

    for sample in samples:
        if st.sidebar.button(sample[:30] + "...", key=sample):
            st.session_state['sample_text'] = sample

    # 모델 정보
    st.sidebar.header("모델 정보")
    st.sidebar.write("**모델**: DistilBERT")
    st.sidebar.write("**학습 데이터**: SST-2")
    st.sidebar.write("**언어**: 영어")


if __name__ == "__main__":
    main()
