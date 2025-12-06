"""
모델 서빙 Streamlit 데모

Usage:
    streamlit run model_serving_demo.py
"""

import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris

st.set_page_config(page_title="모델 서빙 대시보드", page_icon="🚀", layout="wide")

# Iris 데이터 정보
iris = load_iris()
FEATURE_NAMES = iris.feature_names
CLASS_NAMES = iris.target_names


def main():
    st.title("🚀 ML 모델 서빙 대시보드")
    st.markdown("FastAPI 모델 서버와 상호작용하는 데모입니다.")

    # API 설정
    st.sidebar.header("API 설정")
    api_url = st.sidebar.text_input(
        "API URL",
        value="http://localhost:8000"
    )

    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["단일 예측", "배치 예측", "서버 상태"])

    with tab1:
        st.subheader("단일 예측")
        st.markdown("Iris 꽃의 특성을 입력하여 품종을 예측합니다.")

        col1, col2 = st.columns(2)

        with col1:
            sepal_length = st.slider("Sepal Length (cm)", 4.0, 8.0, 5.0, 0.1)
            sepal_width = st.slider("Sepal Width (cm)", 2.0, 4.5, 3.0, 0.1)

        with col2:
            petal_length = st.slider("Petal Length (cm)", 1.0, 7.0, 4.0, 0.1)
            petal_width = st.slider("Petal Width (cm)", 0.1, 2.5, 1.0, 0.1)

        features = [sepal_length, sepal_width, petal_length, petal_width]

        if st.button("예측하기", type="primary"):
            try:
                # API 호출
                response = requests.post(
                    f"{api_url}/predict",
                    json={"features": features, "model_name": "iris_classifier"}
                )

                if response.status_code == 200:
                    result = response.json()
                    prediction = int(result['prediction'])
                    species = CLASS_NAMES[prediction]

                    st.success(f"### 예측 결과: {species}")

                    if result.get('probability'):
                        st.write("**확률:**")
                        for i, prob in enumerate(result['probability']):
                            st.progress(prob)
                            st.write(f"{CLASS_NAMES[i]}: {prob:.2%}")

                    st.metric("추론 시간", f"{result['inference_time_ms']:.2f} ms")
                else:
                    st.error(f"API 오류: {response.status_code}")
                    st.json(response.json())

            except requests.exceptions.ConnectionError:
                st.error("서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
                st.code(f"uvicorn serve_model:app --host 0.0.0.0 --port 8000")

    with tab2:
        st.subheader("배치 예측")
        st.markdown("여러 샘플을 한 번에 예측합니다.")

        # 샘플 데이터 생성
        if st.button("샘플 데이터 생성"):
            sample_data = pd.DataFrame(
                np.random.uniform([4, 2, 1, 0.1], [8, 4.5, 7, 2.5], (5, 4)),
                columns=FEATURE_NAMES
            )
            st.session_state['sample_data'] = sample_data

        if 'sample_data' in st.session_state:
            st.dataframe(st.session_state['sample_data'])

            if st.button("배치 예측 실행"):
                try:
                    features_list = st.session_state['sample_data'].values.tolist()
                    response = requests.post(
                        f"{api_url}/predict/batch",
                        json={"features": features_list, "model_name": "iris_classifier"}
                    )

                    if response.status_code == 200:
                        result = response.json()
                        predictions = result['predictions']

                        results_df = st.session_state['sample_data'].copy()
                        results_df['Prediction'] = [CLASS_NAMES[int(p)] for p in predictions]
                        st.dataframe(results_df)

                        st.metric("총 추론 시간", f"{result['inference_time_ms']:.2f} ms")
                    else:
                        st.error(f"API 오류: {response.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("서버에 연결할 수 없습니다.")

    with tab3:
        st.subheader("서버 상태")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("헬스 체크"):
                try:
                    response = requests.get(f"{api_url}/health")
                    if response.status_code == 200:
                        st.success("서버 정상 작동 중")
                        st.json(response.json())
                    else:
                        st.error("서버 오류")
                except requests.exceptions.ConnectionError:
                    st.error("서버에 연결할 수 없습니다.")

        with col2:
            if st.button("로드된 모델 확인"):
                try:
                    response = requests.get(f"{api_url}/models")
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("API 오류")
                except requests.exceptions.ConnectionError:
                    st.error("서버에 연결할 수 없습니다.")

    # 서버 시작 가이드
    st.sidebar.header("서버 시작 가이드")
    st.sidebar.code("""
# 서버 시작
cd mlops-pipeline/scripts
uvicorn serve_model:app \\
    --host 0.0.0.0 \\
    --port 8000 \\
    --reload
    """)


if __name__ == "__main__":
    main()
