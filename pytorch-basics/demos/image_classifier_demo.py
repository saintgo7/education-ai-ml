"""
이미지 분류 데모 (Streamlit)

실행 방법:
    streamlit run image_classifier_demo.py
"""

import streamlit as st
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import sys
from pathlib import Path

# 상위 디렉토리의 스크립트 임포트
sys.path.append(str(Path(__file__).parent.parent / 'scripts'))
from train_cnn import ResNet, SimpleCNN


# CIFAR-10 클래스
CIFAR10_CLASSES = [
    '비행기 (airplane)', '자동차 (automobile)', '새 (bird)', '고양이 (cat)',
    '사슴 (deer)', '개 (dog)', '개구리 (frog)', '말 (horse)',
    '배 (ship)', '트럭 (truck)'
]


@st.cache_resource
def load_model(model_path, model_type='resnet'):
    """모델 로드"""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if model_type == 'resnet':
        model = ResNet(num_classes=10)
    else:
        model = SimpleCNN(num_classes=10)

    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()

    return model, device


def preprocess_image(image):
    """이미지 전처리"""
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    return transform(image).unsqueeze(0)


def predict(model, image, device):
    """예측 수행"""
    image = image.to(device)
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    return predicted.item(), confidence.item(), probabilities[0].cpu().numpy()


def main():
    st.set_page_config(page_title="이미지 분류기", page_icon="🖼️", layout="wide")

    st.title("🖼️ CIFAR-10 이미지 분류기")
    st.markdown("""
    이 데모는 PyTorch로 학습된 CNN 모델을 사용하여 이미지를 10개 클래스로 분류합니다.
    """)

    # 사이드바 설정
    st.sidebar.header("설정")
    model_type = st.sidebar.selectbox(
        "모델 선택",
        ["resnet", "simple"],
        help="사용할 모델 아키텍처를 선택하세요"
    )

    # 모델 로드
    model_path = Path(__file__).parent.parent / 'checkpoints' / f'{model_type}_best.pth'

    if not model_path.exists():
        st.error(f"모델 파일을 찾을 수 없습니다: {model_path}")
        st.info("먼저 모델을 학습하세요: `python scripts/train_cnn.py`")
        return

    try:
        model, device = load_model(model_path, model_type)
        st.sidebar.success(f"✅ 모델 로드 완료: {model_type}")
    except Exception as e:
        st.error(f"모델 로드 실패: {e}")
        return

    # 이미지 업로드
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📤 이미지 업로드")
        uploaded_file = st.file_uploader(
            "이미지를 선택하세요 (JPG, PNG)",
            type=['jpg', 'jpeg', 'png']
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, caption='업로드된 이미지', use_column_width=True)

            if st.button("🔍 분류하기", type="primary"):
                with st.spinner("분류 중..."):
                    # 예측
                    preprocessed = preprocess_image(image)
                    predicted_class, confidence, probs = predict(model, preprocessed, device)

                    # 결과 표시
                    with col2:
                        st.subheader("📊 분류 결과")
                        st.markdown(f"### 예측: **{CIFAR10_CLASSES[predicted_class]}**")
                        st.markdown(f"신뢰도: **{confidence*100:.2f}%**")

                        # 상위 3개 클래스 표시
                        st.markdown("---")
                        st.markdown("**Top 3 예측:**")
                        top3_indices = probs.argsort()[-3:][::-1]
                        for idx in top3_indices:
                            st.progress(probs[idx])
                            st.text(f"{CIFAR10_CLASSES[idx]}: {probs[idx]*100:.2f}%")

                        # 전체 확률 분포
                        st.markdown("---")
                        st.markdown("**모든 클래스 확률:**")
                        import pandas as pd
                        df = pd.DataFrame({
                            '클래스': CIFAR10_CLASSES,
                            '확률': probs
                        }).sort_values('확률', ascending=False)
                        st.dataframe(df, use_container_width=True)

    # 샘플 이미지
    with st.expander("📚 샘플 이미지 사용하기"):
        st.markdown("샘플 이미지를 업로드하여 테스트할 수 있습니다.")
        st.markdown("또는 CIFAR-10 데이터셋의 이미지를 사용할 수 있습니다.")

    # 정보
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ 정보")
    st.sidebar.markdown(f"""
    - **모델**: {model_type.upper()}
    - **데이터셋**: CIFAR-10
    - **클래스 수**: 10
    - **입력 크기**: 32x32
    - **디바이스**: {device}
    """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>PyTorch 기초 교육 자료 | 이미지 분류 데모</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
