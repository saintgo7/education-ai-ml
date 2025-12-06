"""
TensorFlow/Keras 이미지 분류 Streamlit 데모

Usage:
    streamlit run image_classifier_demo.py
"""

import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="이미지 분류기", page_icon="🖼️", layout="wide")

# CIFAR-10 클래스
CLASSES = ['airplane', 'automobile', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck']


@st.cache_resource
def load_model():
    """모델 로드 (간단한 CNN)"""
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])
    return model


def preprocess_image(image, target_size=(32, 32)):
    """이미지 전처리"""
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0
    if len(image_array.shape) == 2:
        image_array = np.stack([image_array] * 3, axis=-1)
    elif image_array.shape[-1] == 4:
        image_array = image_array[:, :, :3]
    return np.expand_dims(image_array, axis=0)


def main():
    st.title("🖼️ TensorFlow 이미지 분류기")
    st.markdown("CIFAR-10 데이터셋으로 학습된 CNN 모델을 사용한 이미지 분류 데모입니다.")

    model = load_model()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("이미지 업로드")
        uploaded_file = st.file_uploader(
            "이미지를 선택하세요",
            type=['png', 'jpg', 'jpeg']
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", use_column_width=True)

    with col2:
        st.subheader("분류 결과")

        if uploaded_file is not None:
            # 전처리 및 예측
            processed_image = preprocess_image(image)
            predictions = model.predict(processed_image, verbose=0)

            # 결과 표시
            top_k = 5
            top_indices = np.argsort(predictions[0])[-top_k:][::-1]

            st.markdown("### 예측 확률")
            for idx in top_indices:
                prob = predictions[0][idx]
                st.progress(float(prob))
                st.write(f"{CLASSES[idx]}: {prob:.2%}")

            # 최종 예측
            predicted_class = CLASSES[np.argmax(predictions)]
            confidence = np.max(predictions)

            st.success(f"**예측: {predicted_class}** (신뢰도: {confidence:.2%})")

    # 모델 정보
    st.sidebar.header("모델 정보")
    st.sidebar.write(f"**프레임워크**: TensorFlow {tf.__version__}")
    st.sidebar.write("**아키텍처**: CNN (3 Conv + 2 Dense)")
    st.sidebar.write("**입력 크기**: 32x32x3")
    st.sidebar.write(f"**클래스 수**: {len(CLASSES)}")

    st.sidebar.header("CIFAR-10 클래스")
    for i, cls in enumerate(CLASSES):
        st.sidebar.write(f"{i}: {cls}")


if __name__ == "__main__":
    main()
