#!/usr/bin/env python3
"""
100개의 AI/ML 교육 모듈을 자동으로 생성하는 스크립트
Generate 100 AI/ML educational modules automatically
"""

import os
from pathlib import Path

# 100개 모듈 정의 (ID, 한글 이름, 영문 설명, 주요 주제)
MODULES = [
    # Tier 1: 기초 (10개)
    (1, "Python 기초", "Python Programming Fundamentals", "변수, 데이터 타입, 제어문, 함수"),
    (2, "자료구조와 알고리즘", "Data Structures & Algorithms", "리스트, 딕셔너리, 트리, 정렬, 검색"),
    (3, "객체지향과 디자인 패턴", "OOP & Design Patterns", "클래스, 상속, 다형성, SOLID 원칙"),
    (4, "함수형 프로그래밍", "Functional Programming", "람다, Map, Filter, Reduce"),
    (5, "Python 라이브러리", "Python Libraries Essentials", "NumPy, Pandas, SciPy 기초"),
    (6, "선형대수", "Linear Algebra for ML", "벡터, 행렬, 고유값, SVD"),
    (7, "미적분과 최적화", "Calculus & Optimization", "미분, 경사하강법, 컨벡스 최적화"),
    (8, "확률과 통계", "Probability & Statistics", "분포, 가설검정, 베이즈 정리"),
    (9, "탐색적 데이터 분석", "Exploratory Data Analysis", "데이터 프로파일링, 이상치 탐지"),
    (10, "데이터 시각화", "Data Visualization", "Matplotlib, Seaborn, Plotly"),

    # Tier 2: 전통 머신러닝 (20개)
    (11, "선형회귀", "Linear Regression", "OLS, 가정 검증, 평가 메트릭"),
    (12, "다항회귀", "Polynomial Regression", "기저함수, 과적합 방지"),
    (13, "정규화 기법", "Regularization Techniques", "Ridge, Lasso, Elastic Net"),
    (14, "로지스틱 회귀", "Logistic Regression", "분류, 확률, 결정 경계"),
    (15, "서포트 벡터 머신", "Support Vector Machines", "커널, 마진, 이진/다중 분류"),
    (16, "의사결정트리", "Decision Trees", "엔트로피, 정보이득, 가지치기"),
    (17, "랜덤 포레스트", "Random Forests", "앙상블, 부트스트래핑, OOB 에러"),
    (18, "그래디언트 부스팅", "Gradient Boosting", "순차 학습, 약한 학습기"),
    (19, "XGBoost & LightGBM", "XGBoost & LightGBM", "하이퍼파라미터 튜닝, 특성 중요도"),
    (20, "나이브 베이즈", "Naive Bayes", "조건부 확률, 텍스트 분류"),
    (21, "K-최근접 이웃", "K-Nearest Neighbors", "거리 메트릭, 차원의 저주"),
    (22, "K-평균 클러스터링", "K-Means Clustering", "무지도 학습, 초기화 전략"),
    (23, "계층적 클러스터링", "Hierarchical Clustering", "덴드로그램, 링크 기준"),
    (24, "DBSCAN", "DBSCAN Clustering", "밀도 기반, 노이즈 처리"),
    (25, "가우시안 혼합모형", "Gaussian Mixture Models", "EM 알고리즘, 확률 분포"),
    (26, "주성분분석", "PCA - Dimensionality Reduction", "고유벡터, 분산 설명"),
    (27, "특성 선택", "Feature Selection Methods", "필터, 래퍼, 임베디드 방법"),
    (28, "특성 스케일링", "Feature Scaling & Normalization", "표준화, 정규화, 아웃라이어 처리"),
    (29, "불균형 데이터", "Imbalanced Data Handling", "SMOTE, 가중치 조정, 앙상블"),
    (30, "교차 검증", "Cross-Validation Techniques", "K-Fold, Stratified, Time Series"),

    # Tier 3: 딥러닝 기초 (20개)
    (31, "신경망 기초", "Neural Networks Fundamentals", "퍼셉트론, 다층 신경망, 활성화 함수"),
    (32, "역전파와 미분", "Backpropagation & Calculus", "연쇄 법칙, 계산 그래프"),
    (33, "활성화 함수", "Activation Functions", "ReLU, Sigmoid, Tanh, GELU"),
    (34, "손실 함수", "Loss Functions & Metrics", "MSE, CrossEntropy, 커스텀 손실"),
    (35, "합성곱 신경망", "Convolutional Neural Networks", "필터, 풀링, 그래디언트 흐름"),
    (36, "AlexNet", "AlexNet Architecture", "역사적 배경, 실제 구현"),
    (37, "VGG 네트워크", "VGG Networks", "깊은 신경망, 수용 필드"),
    (38, "잔차 네트워크", "ResNet - Residual Networks", "스킵 연결, 매우 깊은 네트워크"),
    (39, "Inception 모듈", "Inception Modules", "다중 스케일 특성, GoogLeNet"),
    (40, "MobileNet", "MobileNet & Efficient Networks", "경량 모델, 모바일 배포"),
    (41, "순환 신경망", "Recurrent Neural Networks", "시계열, 메모리, 순환 구조"),
    (42, "LSTM 네트워크", "LSTM Networks", "게이트, 장기 의존성"),
    (43, "GRU 네트워크", "GRU Networks", "간단한 구조, 계산 효율"),
    (44, "Seq2Seq 모델", "Sequence-to-Sequence Models", "인코더-디코더, 어텐션"),
    (45, "어텐션 메커니즘", "Attention Mechanism", "쿼리-키-값, 가중치 분배"),
    (46, "Transformer 아키텍처", "Transformer Architecture", "자기주의, 위치 인코딩"),
    (47, "BERT 모델", "BERT Model", "양방향 사전학습, 미세조정"),
    (48, "GPT 모델", "GPT Models", "자기회귀, 생성, 크기별 성능"),
    (49, "비전 트랜스포머", "Vision Transformers", "이미지 패치, 패턴 인식"),
    (50, "멀티모달 트랜스포머", "Multimodal Transformers", "텍스트+이미지, 크로스 모달"),

    # Tier 4: NLP (15개)
    (51, "NLP 기초", "NLP Fundamentals", "토큰화, 형태소 분석, 품사 태깅"),
    (52, "토큰화와 전처리", "Tokenization & Preprocessing", "정제, 정규화, 특수문자 처리"),
    (53, "Word2Vec & Skip-gram", "Word2Vec & Skip-gram", "단어 임베딩, 유사도"),
    (54, "GloVe 임베딩", "GloVe Word Embeddings", "전역 벡터, 공기 행렬"),
    (55, "FastText", "FastText Embeddings", "부분 단어, OOV 처리"),
    (56, "개체명 인식", "Named Entity Recognition", "BIO 태깅, LSTM-CRF"),
    (57, "감정 분석", "Sentiment Analysis", "분류, 문맥 이해"),
    (58, "텍스트 분류", "Text Classification", "멀티클래스, 멀티라벨"),
    (59, "기계 번역", "Machine Translation", "번역 모델, BLEU 점수"),
    (60, "질의응답", "Question Answering", "정보 추출형, 생성형"),
    (61, "텍스트 요약", "Summarization Systems", "추상적, 추출적 요약"),
    (62, "프롬프트 엔지니어링", "Prompt Engineering", "프롬프트 디자인, Few-shot"),
    (63, "LLM 미세조정", "Fine-tuning LLMs", "LoRA, QLoRA, P-tuning"),
    (64, "검색증강생성", "Retrieval Augmented Generation", "RAG, 벡터 DB, 청킹"),
    (65, "멀티모달 LLM", "Multimodal LLMs", "비전-언어 모델, VLM"),

    # Tier 5: Computer Vision (15개)
    (66, "이미지 처리 기초", "Image Processing Fundamentals", "필터, 컨볼루션, 엣지 검출"),
    (67, "특성 검출", "Feature Detection", "코너, SIFT, SURF"),
    (68, "엣지 검출", "Edge Detection", "Sobel, Canny, Laplacian"),
    (69, "YOLO 객체 탐지", "YOLO Object Detection", "실시간 탐지, 박스 회귀"),
    (70, "Faster R-CNN", "Faster R-CNN Detection", "영역 제안, 두 단계 탐지"),
    (71, "SSD 탐지", "SSD Object Detection", "멀티스케일, 단일 샷"),
    (72, "인스턴스 분할", "Instance Segmentation - Mask R-CNN", "픽셀 레벨, 각 객체 분할"),
    (73, "의미론적 분할", "Semantic Segmentation", "클래스별 픽셀, FCN"),
    (74, "전체적 분할", "Panoptic Segmentation", "의미+인스턴스, 통합"),
    (75, "깊이 추정", "Depth Estimation", "3D 재구성, 스테레오 비전"),
    (76, "광학 흐름", "Optical Flow", "동작 추정, 비디오 분석"),
    (77, "얼굴 탐지", "Face Detection & Recognition", "MTCNN, FaceNet, ArcFace"),
    (78, "얼굴 랜드마크", "Facial Landmarks Detection", "주요점, 표정 인식"),
    (79, "자세 추정", "Pose Estimation", "관절 위치, 운동 분석"),
    (80, "행동 인식", "Action Recognition", "비디오 분류, 시간축 모델링"),

    # Tier 6: 강화학습 (10개)
    (81, "강화학습 기초", "Reinforcement Learning Fundamentals", "에이전트, 환경, 보상"),
    (82, "마르코프 의사결정", "Markov Decision Process", "상태, 행동, 전환 확률"),
    (83, "Q-러닝", "Q-Learning", "표형식, 벨만 방정식"),
    (84, "심층 Q-네트워크", "Deep Q-Network", "신경망, 경험 재생"),
    (85, "정책 경사", "Policy Gradient Methods", "직접 최적화, 정책 추정"),
    (86, "행동-비평 방법", "Actor-Critic Methods", "정책+가치, 낮은 분산"),
    (87, "근접 정책 최적화", "Proximal Policy Optimization", "신뢰 영역, PPO"),
    (88, "이점 행동-비평", "Advantage Actor-Critic", "A3C, 비동기 학습"),
    (89, "다중 에이전트", "Multi-Agent Reinforcement Learning", "협력, 경쟁, 통신"),
    (90, "역강화학습", "Inverse Reinforcement Learning", "보상 추론, 모방 학습"),

    # Tier 7: 생성 AI (10개)
    (91, "GAN 기초", "GAN Fundamentals", "생성기, 판별기, 적대적 훈련"),
    (92, "DCGAN 아키텍처", "DCGAN Architecture", "합성곱 GAN, 이미지 생성"),
    (93, "조건부 GAN", "Conditional GAN", "클래스 제어, 레이블 조건"),
    (94, "StyleGAN", "StyleGAN", "스타일 제어, 높은 품질"),
    (95, "오토인코더", "Autoencoder Basics", "인코더-디코더, 비지도 학습"),
    (96, "변분 오토인코더", "Variational Autoencoder", "VAE, 확률 모델"),
    (97, "확산 모델", "Diffusion Models", "순방향, 역방향 프로세스"),
    (98, "안정 확산", "Stable Diffusion", "텍스트-이미지, 고속 생성"),
    (99, "텍스트-이미지", "Text-to-Image Generation", "DALL-E, Imagen, 멀티모달"),
    (100, "신경 스타일 이전", "Neural Style Transfer", "스타일 분리, 내용 보존"),
]

def create_module_structure(module_id, korean_name, english_name, topics):
    """모듈 디렉토리 구조 생성"""

    # 디렉토리명 생성 (숫자-영문명)
    dir_name = f"{module_id:02d}-{english_name.lower().replace(' & ', '-').replace(' - ', '-').replace(' ', '-')}"
    module_path = Path("/home/user/education-ai-ml") / dir_name

    # 서브디렉토리 생성
    subdirs = [
        "notebooks",
        "scripts",
        "data",
        "configs",
        "results",
    ]

    for subdir in subdirs:
        (module_path / subdir).mkdir(parents=True, exist_ok=True)

    # README.md 생성
    readme_content = f"""# {module_id}. {korean_name} ({english_name})

## 📚 학습 목표 (Learning Objectives)

이 모듈에서는 다음을 학습합니다:
- {topics}

## 📂 디렉토리 구조 (Directory Structure)

```
{dir_name}/
├── notebooks/          # Jupyter 노트북 (이론 + 실습)
├── scripts/           # 프로덕션 파이썬 스크립트
├── data/              # 데이터셋
├── configs/           # 설정 파일 (YAML)
├── results/           # 결과 및 모델 체크포인트
└── README.md
```

## 🎯 주요 개념 (Key Concepts)

### 기본 개념
- {topics.split(',')[0] if ',' in topics else topics}

### 실전 예제
- 샘플 데이터셋으로 실습
- 프로덕션 코드 스타일
- 최적화된 구현

## 📖 학습 순서 (Learning Path)

1. **이론 학습**: `notebooks/01_basics.ipynb`에서 개념 이해
2. **실습**: `notebooks/02_practice.ipynb`에서 실습
3. **응용**: `scripts/main.py` 스크립트 실행 및 분석
4. **프로젝트**: 자신의 데이터로 적용

## 🚀 빠른 시작 (Quick Start)

```bash
# 의존성 설치
pip install -r requirements.txt

# Jupyter 노트북 실행
jupyter notebook notebooks/

# 스크립트 실행
python scripts/main.py
```

## 📋 필수 의존성 (Dependencies)

`requirements.txt` 파일을 참고하세요.

## 🔗 유용한 자료 (Useful Resources)

- [공식 문서](https://example.com)
- [튜토리얼](https://example.com)
- [논문](https://example.com)

## 💡 팁과 트릭 (Tips & Tricks)

- 로컬에서 테스트 후 Colab에서 실행
- GPU가 필요한 경우 Colab의 T4 GPU 사용
- 메모리가 부족하면 배치 크기 감소

## ✅ 체크리스트 (Checklist)

- [ ] 개념 이해
- [ ] 기본 예제 실행
- [ ] 연습 문제 풀이
- [ ] 자신의 데이터 적용

## 📚 다음 단계 (Next Steps)

이 모듈을 완료한 후:
- 고급 주제 학습
- 다른 모듈과의 연계
- 실전 프로젝트 진행

---

**Happy Learning! 즐거운 학습 되세요! 🚀**
"""

    (module_path / "README.md").write_text(readme_content, encoding="utf-8")

    # requirements.txt 생성
    requirements_content = f"""# Module {module_id}: {korean_name} ({english_name})
# Dependencies for this module

# Core Data Science
numpy>=1.23.0
pandas>=1.5.0
scipy>=1.9.0

# Machine Learning (일부 모듈만 필요)
scikit-learn>=1.3.0

# Deep Learning (일부 모듈만 필요)
torch>=2.0.0
tensorflow>=2.13.0
transformers>=4.30.0

# Visualization
matplotlib>=3.6.0
seaborn>=0.12.0
plotly>=5.0.0

# Jupyter
jupyter>=1.0.0
jupyterlab>=4.0.0
ipywidgets>=8.0.0

# Utilities
python-dotenv>=1.0.0
pyyaml>=6.0
tqdm>=4.65.0
"""

    (module_path / "requirements.txt").write_text(requirements_content, encoding="utf-8")

    # 기본 스크립트 생성
    script_content = f'''#!/usr/bin/env python3
"""
Module {module_id}: {korean_name} ({english_name})
{topics}
"""

import os
import sys
import logging
from pathlib import Path

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """메인 함수"""
    logger.info("Module {module_id} 실행 시작")
    logger.info("주제: {topics}")

    # TODO: 실제 구현 추가
    logger.info("모듈 완료")

if __name__ == "__main__":
    main()
'''

    (module_path / "scripts" / "main.py").write_text(script_content, encoding="utf-8")

    # Notebook 샘플 생성 (간단한 형식)
    notebook_content = f'''{{
 "cells": [
  {{
   "cell_type": "markdown",
   "metadata": {{}},
   "source": [
    "# {module_id}: {korean_name} ({english_name})\\n",
    "\\n",
    "## 주제\\n",
    "{topics}\\n",
    "\\n",
    "## 학습 목표\\n",
    "- 개념 이해\\n",
    "- 실전 적용\\n",
    "- 심화 학습"
   ]
  }},
  {{
   "cell_type": "code",
   "execution_count": null,
   "metadata": {{}},
   "outputs": [],
   "source": [
    "# 필요한 라이브러리 import\\n",
    "import numpy as np\\n",
    "import pandas as pd\\n",
    "import matplotlib.pyplot as plt\\n",
    "\\n",
    "print('모듈 {module_id} 시작')\\n",
    "print('주제: {topics}')"
   ]
  }},
  {{
   "cell_type": "markdown",
   "metadata": {{}},
   "source": [
    "## 1. 이론\\n",
    "\\n",
    "### 개념\\n",
    "{topics}를 학습합니다.\\n",
    "\\n",
    "### 주요 공식\\n",
    "- 공식 1\\n",
    "- 공식 2"
   ]
  }},
  {{
   "cell_type": "markdown",
   "metadata": {{}},
   "source": [
    "## 2. 실습\\n",
    "\\n",
    "### 예제 1\\n",
    "기본 예제를 구현합니다."
   ]
  }},
  {{
   "cell_type": "code",
   "execution_count": null,
   "metadata": {{}},
   "outputs": [],
   "source": [
    "# 예제 코드\\n",
    "# TODO: 실제 구현 추가"
   ]
  }},
  {{
   "cell_type": "markdown",
   "metadata": {{}},
   "source": [
    "## 3. 연습 문제\\n",
    "\\n",
    "아래 문제를 풀어보세요:\\n",
    "1. 문제 1\\n",
    "2. 문제 2\\n",
    "3. 문제 3"
   ]
  }}
 ],
 "metadata": {{
  "kernelspec": {{
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }},
  "language_info": {{
   "codemirror_mode": {{
    "name": "ipython",
    "version": 3
   }},
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.0"
  }}
 }},
 "nbformat": 4,
 "nbformat_minor": 4
}}
'''

    (module_path / "notebooks" / "01_basics.ipynb").write_text(notebook_content, encoding="utf-8")

    # config.yaml 생성
    config_content = f"""# Module {module_id}: {korean_name}
# Configuration file

module:
  id: {module_id}
  name: {korean_name}
  english_name: {english_name}
  topics: {topics}

# 학습 관련 설정
learning:
  difficulty: intermediate
  estimated_hours: 5
  prerequisites: []

# 데이터 설정
data:
  source: synthetic
  size: small
  format: csv

# 모델 설정
model:
  type: example
  architecture: baseline
  hyperparameters:
    learning_rate: 0.001
    batch_size: 32
    epochs: 10

# 평가 메트릭
metrics:
  - accuracy
  - loss
  - f1_score
"""


    (module_path / "configs" / "config.yaml").write_text(config_content, encoding="utf-8")

    return str(module_path)

def main():
    """메인 함수"""
    print("=" * 80)
    print("🚀 100개의 AI/ML 교육 모듈 생성 중...")
    print("=" * 80)

    created_modules = []

    for module_id, korean_name, english_name, topics in MODULES:
        try:
            module_path = create_module_structure(module_id, korean_name, english_name, topics)
            created_modules.append((module_id, korean_name))
            print(f"✅ [{module_id:3d}] {korean_name:30s} ({english_name})")
        except Exception as e:
            print(f"❌ [{module_id:3d}] {korean_name}: 오류 - {str(e)}")

    print("\n" + "=" * 80)
    print(f"✨ 총 {len(created_modules)}개 모듈 생성 완료!")
    print("=" * 80)

    # 통계 출력
    print(f"\n📊 생성 통계:")
    print(f"  - 기초 (1-10): 10개")
    print(f"  - 전통 ML (11-30): 20개")
    print(f"  - 딥러닝 (31-50): 20개")
    print(f"  - NLP (51-65): 15개")
    print(f"  - Computer Vision (66-80): 15개")
    print(f"  - 강화학습 (81-90): 10개")
    print(f"  - 생성 AI (91-100): 10개")

    print(f"\n🎓 다음 단계:")
    print(f"  1. 각 모듈의 README.md 검토")
    print(f"  2. requirements.txt 업데이트")
    print(f"  3. 실제 학습 자료 추가")
    print(f"  4. Git에 커밋 및 푸시")

if __name__ == "__main__":
    main()
