# AI/ML 교육 저장소 (AI/ML Education Repository)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

딥러닝, 머신러닝, MLOps를 위한 종합 교육 자료입니다. 각 섹션은 이론, 실습, 프로덕션 코드를 포함합니다.

A comprehensive educational resource for Deep Learning, Machine Learning, and MLOps. Each section includes theory, hands-on practice, and production-ready code.

## 📚 목차 (Table of Contents)

### 1. [PyTorch 기초 (pytorch-basics)](./pytorch-basics)
신경망의 기본부터 Transformer까지
- ✅ 기본 신경망 (Basic Neural Networks)
- ✅ CNN (Convolutional Neural Networks)
- ✅ RNN/LSTM/GRU (Recurrent Neural Networks)
- ✅ Transformer 아키텍처
- 📓 Jupyter 노트북 + 프로덕션 스크립트
- 🔗 [Colab으로 열기](./pytorch-basics#colab-links)

### 2. [TensorFlow/Keras (tensorflow-keras)](./tensorflow-keras)
TensorFlow 2.x와 Keras를 활용한 딥러닝
- ✅ 이미지 분류 (Image Classification)
- ✅ 자연어 처리 (NLP with Keras)
- ✅ 시계열 예측 (Time Series Forecasting)
- 🎯 Transfer Learning & Fine-tuning
- 🔗 [Colab으로 열기](./tensorflow-keras#colab-links)

### 3. [Scikit-learn ML (scikit-learn-ml)](./scikit-learn-ml)
전통적인 머신러닝 알고리즘
- ✅ 회귀/분류 (Regression & Classification)
- ✅ 클러스터링 (Clustering)
- ✅ 차원 축소 (Dimensionality Reduction)
- ✅ 앙상블 기법 (Ensemble Methods)
- 📊 실전 예제 포함
- 🔗 [Colab으로 열기](./scikit-learn-ml#colab-links)

### 4. [NLP 프로젝트 (nlp-projects)](./nlp-projects)
자연어 처리 실전 프로젝트
- ✅ 감성 분석 (Sentiment Analysis)
- ✅ 개체명 인식 (Named Entity Recognition)
- ✅ 텍스트 생성 (Text Generation)
- ✅ BERT/GPT 파인튜닝
- 🤗 Hugging Face Transformers
- 🔗 [Colab으로 열기](./nlp-projects#colab-links)

### 5. [컴퓨터 비전 (computer-vision)](./computer-vision)
객체 탐지 및 이미지 세그멘테이션
- ✅ YOLO v5/v8/v11
- ✅ 객체 탐지 (Object Detection)
- ✅ 이미지 세그멘테이션 (Segmentation)
- ✅ 얼굴 인식 (Face Recognition)
- 📹 실시간 비디오 처리
- 🔗 [Colab으로 열기](./computer-vision#colab-links)

### 6. [LLM 애플리케이션 (llm-applications)](./llm-applications)
대규모 언어 모델 활용
- ✅ LangChain 프레임워크
- ✅ RAG (Retrieval Augmented Generation)
- ✅ 프롬프트 엔지니어링 (Prompt Engineering)
- ✅ 벡터 데이터베이스 (ChromaDB, Pinecone)
- 🤖 챗봇 구축
- 🔗 [Colab으로 열기](./llm-applications#colab-links)

### 7. [강화학습 (reinforcement-learning)](./reinforcement-learning)
RL 알고리즘과 게임 AI
- ✅ Q-Learning
- ✅ DQN (Deep Q-Network)
- ✅ Policy Gradient Methods
- ✅ PPO, A3C
- 🎮 OpenAI Gym 환경
- 🔗 [Colab으로 열기](./reinforcement-learning#colab-links)

### 8. [생성 모델 (gans-generative)](./gans-generative)
GANs와 생성 AI
- ✅ GAN 기초 (Vanilla GAN, DCGAN)
- ✅ VAE (Variational Autoencoder)
- ✅ Diffusion Models (DDPM, Stable Diffusion)
- 🎨 이미지 생성 애플리케이션
- 🔗 [Colab으로 열기](./gans-generative#colab-links)

### 9. [MLOps 파이프라인 (mlops-pipeline)](./mlops-pipeline)
모델 배포와 운영
- ✅ MLflow (실험 추적, 모델 레지스트리)
- ✅ DVC (데이터 버전 관리)
- ✅ 모델 배포 (Docker, FastAPI, Kubernetes)
- ✅ 모니터링 & A/B 테스팅
- 🚀 프로덕션 베스트 프랙티스
- 🔗 [Colab으로 열기](./mlops-pipeline#colab-links)

### 10. [데이터 엔지니어링 (data-engineering)](./data-engineering)
데이터 파이프라인과 특성 공학
- ✅ ETL 파이프라인 (Apache Airflow)
- ✅ 특성 공학 (Feature Engineering)
- ✅ 데이터 검증 (Great Expectations)
- ✅ 실시간 데이터 처리 (Kafka, Spark Streaming)
- 🔗 [Colab으로 열기](./data-engineering#colab-links)

## 🚀 빠른 시작 (Quick Start)

### 전체 환경 설정

```bash
# 저장소 클론
git clone https://github.com/yourusername/education-ai-ml.git
cd education-ai-ml

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 기본 의존성 설치
pip install -r requirements.txt
```

### 특정 섹션만 설치

```bash
# 예: PyTorch 기초만 설치
cd pytorch-basics
pip install -r requirements.txt

# Jupyter 노트북 실행
jupyter notebook
```

## 📦 주요 의존성 (Main Dependencies)

```
torch>=2.0.0
tensorflow>=2.13.0
scikit-learn>=1.3.0
transformers>=4.30.0
langchain>=0.1.0
mlflow>=2.8.0
streamlit>=1.28.0
gradio>=4.0.0
```

각 섹션의 상세 의존성은 해당 디렉토리의 `requirements.txt`를 참고하세요.

## 📓 Jupyter 노트북 사용법

모든 섹션은 대화형 학습을 위한 Jupyter 노트북을 제공합니다:

1. **로컬에서 실행**: `jupyter notebook` 실행 후 `.ipynb` 파일 열기
2. **Colab에서 실행**: 각 섹션 README의 Colab 링크 클릭
3. **JupyterLab 사용**: `jupyter lab` 명령으로 더 나은 UI 사용

## 🎯 학습 경로 추천 (Recommended Learning Path)

### 초급 (Beginner)
1. **scikit-learn-ml** - 머신러닝 기초 개념
2. **pytorch-basics** - 딥러닝 기초
3. **tensorflow-keras** - TensorFlow로 실전 프로젝트

### 중급 (Intermediate)
4. **nlp-projects** - 자연어 처리 전문화
5. **computer-vision** - 컴퓨터 비전 전문화
6. **reinforcement-learning** - 강화학습 입문

### 고급 (Advanced)
7. **llm-applications** - 최신 LLM 기술
8. **gans-generative** - 생성 AI
9. **mlops-pipeline** - 프로덕션 배포
10. **data-engineering** - 데이터 인프라

## 🎨 데모 애플리케이션

각 섹션은 Streamlit 또는 Gradio로 만든 대화형 데모를 포함합니다:

```bash
# Streamlit 데모 실행
cd pytorch-basics/demos
streamlit run image_classifier_demo.py

# Gradio 데모 실행
cd nlp-projects/demos
python sentiment_analysis_demo.py
```

## 📊 데이터셋

### 포함된 데이터 생성기
- 합성 데이터 생성기 (각 섹션의 `data_generators/`)
- 샘플 데이터셋 (작은 크기, 학습용)

### 외부 데이터셋 다운로드
대용량 데이터셋은 각 섹션의 `download_data.sh` 스크립트로 다운로드:

```bash
cd nlp-projects
bash download_data.sh
```

## 💾 모델 체크포인트

사전 학습된 모델은 별도 다운로드:

```bash
# 각 섹션에서 실행
python download_checkpoints.py
```

또는 Hugging Face에서 직접 다운로드:
- [모델 허브 링크](https://huggingface.co/your-organization)

## 🤝 기여하기 (Contributing)

기여를 환영합니다! 다음을 참고하세요:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

자세한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요.

## 📝 라이선스 (License)

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

## 📧 문의 (Contact)

- 이슈 제보: [GitHub Issues](https://github.com/yourusername/education-ai-ml/issues)
- 이메일: your.email@example.com
- 블로그: [기술 블로그 링크]

## 🌟 Star History

이 저장소가 도움이 되었다면 ⭐️를 눌러주세요!

## 📚 참고 자료 (References)

- [PyTorch Documentation](https://pytorch.org/docs/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Hugging Face Course](https://huggingface.co/course)
- [Fast.ai Practical Deep Learning](https://course.fast.ai/)
- [Coursera ML Specialization](https://www.coursera.org/specializations/machine-learning-introduction)

## 🔄 업데이트 로그 (Update Log)

- **2025-01**: 초기 저장소 생성
  - 10개 주요 섹션 구성
  - Jupyter 노트북 + 프로덕션 코드
  - Korean/English 문서화

---

**Happy Learning! 즐거운 학습 되세요! 🚀📚**
