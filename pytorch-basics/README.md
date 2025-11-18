# PyTorch 기초 (PyTorch Basics)

PyTorch를 사용한 딥러닝 기초부터 Transformer까지 학습합니다.

## 📚 학습 내용

### 1. 기본 신경망 (Basic Neural Networks)
- Tensor 연산 및 Autograd
- 다층 퍼셉트론 (MLP)
- 활성화 함수와 최적화
- 📓 [01_basic_nn.ipynb](./notebooks/01_basic_nn.ipynb)
- 🔗 [Colab에서 열기](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/pytorch-basics/notebooks/01_basic_nn.ipynb)

### 2. CNN (Convolutional Neural Networks)
- 합성곱 연산의 이해
- LeNet, AlexNet, ResNet 구현
- 이미지 분류 실습 (CIFAR-10)
- 📓 [02_cnn.ipynb](./notebooks/02_cnn.ipynb)
- 🔗 [Colab에서 열기](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/pytorch-basics/notebooks/02_cnn.ipynb)

### 3. RNN/LSTM/GRU (Recurrent Neural Networks)
- 순환 신경망의 원리
- LSTM과 GRU 아키텍처
- 시퀀스 예측 및 텍스트 생성
- 📓 [03_rnn_lstm.ipynb](./notebooks/03_rnn_lstm.ipynb)
- 🔗 [Colab에서 열기](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/pytorch-basics/notebooks/03_rnn_lstm.ipynb)

### 4. Transformer 아키텍처
- Attention Mechanism
- Multi-Head Attention
- Positional Encoding
- Transformer 구현 (처음부터)
- 📓 [04_transformer.ipynb](./notebooks/04_transformer.ipynb)
- 🔗 [Colab에서 열기](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/pytorch-basics/notebooks/04_transformer.ipynb)

## 🚀 빠른 시작

```bash
# 의존성 설치
pip install -r requirements.txt

# Jupyter 노트북 실행
jupyter notebook

# 또는 특정 스크립트 실행
python scripts/train_cnn.py --data_path ./data --epochs 10
```

## 📦 프로젝트 구조

```
pytorch-basics/
├── notebooks/          # Jupyter 노트북 (학습용)
│   ├── 01_basic_nn.ipynb
│   ├── 02_cnn.ipynb
│   ├── 03_rnn_lstm.ipynb
│   └── 04_transformer.ipynb
├── scripts/            # 프로덕션 Python 스크립트
│   ├── train_cnn.py
│   ├── train_rnn.py
│   ├── train_transformer.py
│   └── model_architectures.py
├── demos/              # Streamlit/Gradio 데모
│   ├── image_classifier_demo.py
│   └── text_generator_demo.py
├── data_generators/    # 합성 데이터 생성
│   └── synthetic_data.py
├── configs/            # 모델 설정 파일
│   ├── cnn_config.yaml
│   ├── rnn_config.yaml
│   └── transformer_config.yaml
├── checkpoints/        # 학습된 모델 체크포인트
│   └── download_checkpoints.py
├── requirements.txt
└── README.md
```

## 🎯 학습 목표

이 섹션을 완료하면 다음을 할 수 있습니다:

- ✅ PyTorch Tensor 연산 마스터
- ✅ 커스텀 신경망 레이어 구현
- ✅ CNN으로 이미지 분류 모델 구축
- ✅ RNN/LSTM으로 시퀀스 데이터 처리
- ✅ Transformer 아키텍처 이해 및 구현
- ✅ 모델 학습, 검증, 배포 파이프라인 구축

## 💻 프로덕션 스크립트 예제

### CNN 모델 학습

```bash
python scripts/train_cnn.py \
  --config configs/cnn_config.yaml \
  --data_path ./data/cifar10 \
  --epochs 50 \
  --batch_size 64 \
  --learning_rate 0.001
```

### RNN 텍스트 생성

```bash
python scripts/train_rnn.py \
  --config configs/rnn_config.yaml \
  --text_file ./data/shakespeare.txt \
  --seq_length 100 \
  --epochs 20
```

### Transformer 학습

```bash
python scripts/train_transformer.py \
  --config configs/transformer_config.yaml \
  --src_vocab_size 10000 \
  --tgt_vocab_size 10000 \
  --max_seq_length 512
```

## 🎨 데모 애플리케이션

### Streamlit 이미지 분류기

```bash
cd demos
streamlit run image_classifier_demo.py
```

실시간 웹캠 또는 업로드된 이미지로 분류를 수행합니다.

### Gradio 텍스트 생성기

```bash
cd demos
python text_generator_demo.py
```

RNN 또는 Transformer로 텍스트를 생성합니다.

## 📊 데이터셋

### 자동 다운로드
스크립트 실행 시 데이터셋이 자동으로 다운로드됩니다:
- MNIST (손글씨 숫자)
- CIFAR-10 (이미지 분류)
- Penn Treebank (텍스트 데이터)

### 합성 데이터 생성

```bash
python data_generators/synthetic_data.py --num_samples 1000 --task classification
```

## 💾 모델 체크포인트

사전 학습된 모델 다운로드:

```bash
cd checkpoints
python download_checkpoints.py
```

사용 가능한 체크포인트:
- `resnet18_cifar10.pth` - CIFAR-10 학습된 ResNet18
- `lstm_text_gen.pth` - 텍스트 생성용 LSTM
- `transformer_translation.pth` - 번역용 Transformer

## 📝 주요 개념

### 1. Autograd와 역전파

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2
z = y.sum()
z.backward()
print(x.grad)  # [2.0, 4.0, 6.0]
```

### 2. 커스텀 레이어

```python
class CustomLayer(torch.nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight = torch.nn.Parameter(torch.randn(in_features, out_features))
        self.bias = torch.nn.Parameter(torch.zeros(out_features))

    def forward(self, x):
        return x @ self.weight + self.bias
```

### 3. 학습 루프

```python
for epoch in range(num_epochs):
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
```

## 🔧 고급 주제

- Mixed Precision Training (AMP)
- Distributed Data Parallel (DDP)
- Model Quantization
- ONNX Export
- TorchScript

## 📚 추가 자료

- [PyTorch 공식 튜토리얼](https://pytorch.org/tutorials/)
- [Deep Learning with PyTorch (책)](https://pytorch.org/deep-learning-with-pytorch)
- [PyTorch 포럼](https://discuss.pytorch.org/)

## 🐛 트러블슈팅

### CUDA 메모리 부족

```python
# 배치 크기 줄이기
batch_size = 32  # 64에서 32로

# Gradient Accumulation 사용
for i, (x, y) in enumerate(dataloader):
    loss = model(x, y)
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### 학습이 수렴하지 않음

- Learning rate 조정: `lr=1e-4`로 시작
- Batch Normalization 추가
- Gradient Clipping 적용: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`

---

**다음 단계**: [TensorFlow/Keras](../tensorflow-keras) 또는 [NLP 프로젝트](../nlp-projects)로 진행하세요!
