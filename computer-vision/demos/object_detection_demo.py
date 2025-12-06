"""
YOLOv8 객체 탐지 Streamlit 데모

Usage:
    streamlit run object_detection_demo.py
"""

import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import tempfile

st.set_page_config(page_title="객체 탐지", page_icon="🔍", layout="wide")


@st.cache_resource
def load_model(model_name):
    """YOLO 모델 로드"""
    return YOLO(model_name)


def detect_objects(model, image, conf_threshold):
    """객체 탐지 수행"""
    results = model(image, conf=conf_threshold)
    return results[0]


def main():
    st.title("🔍 YOLOv8 객체 탐지")
    st.markdown("이미지에서 객체를 탐지합니다.")

    # 사이드바 설정
    st.sidebar.header("설정")

    model_choice = st.sidebar.selectbox(
        "모델 선택",
        ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"],
        index=0
    )

    conf_threshold = st.sidebar.slider(
        "신뢰도 임계값",
        min_value=0.1,
        max_value=1.0,
        value=0.5,
        step=0.05
    )

    # 모델 로드
    model = load_model(model_choice)

    # 이미지 업로드
    uploaded_file = st.file_uploader(
        "이미지 업로드",
        type=['png', 'jpg', 'jpeg']
    )

    col1, col2 = st.columns(2)

    if uploaded_file is not None:
        # 이미지 로드
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        with col1:
            st.subheader("원본 이미지")
            st.image(image, use_column_width=True)

        # 객체 탐지
        with st.spinner("객체 탐지 중..."):
            results = detect_objects(model, image_np, conf_threshold)

        with col2:
            st.subheader("탐지 결과")
            annotated_image = results.plot()
            annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
            st.image(annotated_image, use_column_width=True)

        # 탐지 결과 표시
        st.subheader("탐지된 객체")

        if len(results.boxes) > 0:
            for box in results.boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()

                st.write(f"- **{cls_name}**: {conf:.1%} (위치: [{xyxy[0]:.0f}, {xyxy[1]:.0f}, {xyxy[2]:.0f}, {xyxy[3]:.0f}])")

            st.metric("총 탐지 객체 수", len(results.boxes))
        else:
            st.info("탐지된 객체가 없습니다.")

    # 샘플 이미지
    st.sidebar.header("샘플 이미지")
    if st.sidebar.button("버스 이미지 테스트"):
        st.sidebar.info("샘플 이미지를 다운로드하여 업로드해주세요.")
        st.sidebar.markdown("[샘플 이미지 링크](https://ultralytics.com/images/bus.jpg)")

    # 모델 정보
    st.sidebar.header("모델 정보")
    st.sidebar.write(f"**모델**: {model_choice}")
    st.sidebar.write(f"**클래스 수**: {len(model.names)}")

    with st.sidebar.expander("클래스 목록"):
        for idx, name in model.names.items():
            st.write(f"{idx}: {name}")


if __name__ == "__main__":
    main()
