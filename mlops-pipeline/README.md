# MLOps 파이프라인 (MLOps Pipeline)

모델 실험 추적, 버전 관리, 배포, 모니터링까지 전체 MLOps 워크플로우

## 📚 학습 내용

### 1. MLflow (실험 추적 & 모델 레지스트리)
- Experiment Tracking
- Model Registry
- Model Serving
- 📓 [01_mlflow_basics.ipynb](./notebooks/01_mlflow_basics.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/mlops-pipeline/notebooks/01_mlflow_basics.ipynb)

### 2. DVC (데이터 버전 관리)
- Data Version Control
- Pipeline Management
- Remote Storage (S3, GCS)
- 📓 [02_dvc_basics.ipynb](./notebooks/02_dvc_basics.ipynb)

### 3. 모델 배포 (Model Deployment)
- Docker 컨테이너화
- FastAPI REST API
- Kubernetes 배포
- Serverless (AWS Lambda)
- 📓 [03_model_deployment.ipynb](./notebooks/03_model_deployment.ipynb)

### 4. CI/CD (Continuous Integration/Deployment)
- GitHub Actions
- Model Testing
- Automated Deployment
- 📓 [04_cicd_pipeline.ipynb](./notebooks/04_cicd_pipeline.ipynb)

### 5. 모니터링 & A/B 테스팅
- Prometheus + Grafana
- Model Performance Monitoring
- Data Drift Detection
- A/B Testing
- 📓 [05_monitoring.ipynb](./notebooks/05_monitoring.ipynb)

## 🚀 빠른 시작

```bash
# 의존성 설치
pip install -r requirements.txt

# MLflow 서버 시작
mlflow ui --host 0.0.0.0 --port 5000

# DVC 초기화
dvc init
dvc remote add -d myremote s3://mybucket/path
```

## 💻 주요 예제

### MLflow 실험 추적

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 실험 시작
mlflow.set_experiment("my_experiment")

with mlflow.start_run():
    # 파라미터 로깅
    n_estimators = 100
    max_depth = 10
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # 모델 학습
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X_train, y_train)

    # 성능 로깅
    accuracy = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)

    # 모델 저장
    mlflow.sklearn.log_model(model, "model")
```

### DVC 파이프라인

```yaml
# dvc.yaml
stages:
  prepare_data:
    cmd: python scripts/prepare_data.py
    deps:
      - data/raw
    outs:
      - data/processed

  train_model:
    cmd: python scripts/train.py
    deps:
      - data/processed
      - scripts/train.py
    params:
      - train.learning_rate
      - train.epochs
    outs:
      - models/model.pkl
    metrics:
      - metrics/train_metrics.json

  evaluate:
    cmd: python scripts/evaluate.py
    deps:
      - models/model.pkl
      - data/processed
    metrics:
      - metrics/eval_metrics.json
```

### FastAPI 모델 서빙

```python
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc
import numpy as np

app = FastAPI()

# 모델 로드
model = mlflow.pyfunc.load_model("models:/my_model/production")

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    features = np.array([request.features])
    prediction = model.predict(features)[0]

    return PredictionResponse(
        prediction=float(prediction),
        confidence=0.95
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### Docker 배포

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# 빌드 및 실행
docker build -t ml-model-api .
docker run -p 8000:8000 ml-model-api
```

### Kubernetes 배포

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      containers:
      - name: ml-model
        image: ml-model-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
spec:
  selector:
    app: ml-model
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## 🎯 주요 기술 스택

### 실험 관리
- ✅ MLflow - 실험 추적 및 모델 레지스트리
- ✅ Weights & Biases - 협업 및 시각화
- ✅ Neptune.ai - 메타데이터 관리

### 데이터 버전 관리
- ✅ DVC - 데이터 버전 관리
- ✅ Git - 코드 버전 관리
- ✅ Delta Lake - 데이터 레이크

### 모델 배포
- ✅ Docker - 컨테이너화
- ✅ Kubernetes - 오케스트레이션
- ✅ FastAPI - REST API 서버
- ✅ TorchServe - PyTorch 모델 서빙
- ✅ TensorFlow Serving - TensorFlow 모델 서빙

### CI/CD
- ✅ GitHub Actions - 자동화 워크플로우
- ✅ GitLab CI - CI/CD 파이프라인
- ✅ Jenkins - 빌드 자동화

### 모니터링
- ✅ Prometheus - 메트릭 수집
- ✅ Grafana - 대시보드
- ✅ ELK Stack - 로그 관리
- ✅ Evidently AI - 데이터 드리프트

## 🔧 프로젝트 구조

```
mlops-pipeline/
├── notebooks/          # Jupyter 노트북
├── scripts/            # Python 스크립트
│   ├── train.py
│   ├── evaluate.py
│   └── serve.py
├── docker/             # Docker 설정
│   ├── Dockerfile
│   └── docker-compose.yml
├── kubernetes/         # Kubernetes 매니페스트
│   ├── deployment.yaml
│   └── service.yaml
├── .github/            # GitHub Actions
│   └── workflows/
│       └── ci-cd.yml
├── configs/            # 설정 파일
│   ├── model_config.yaml
│   └── deployment_config.yaml
├── dvc.yaml            # DVC 파이프라인
├── MLproject           # MLflow 프로젝트
└── requirements.txt
```

## 📊 모니터링 대시보드

### Prometheus 설정

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ml-model'
    static_configs:
      - targets: ['localhost:8000']
```

### Grafana 대시보드

- Model Latency
- Request Rate
- Error Rate
- Resource Usage (CPU, Memory)
- Prediction Distribution

## 🚀 배포 전략

### Blue-Green Deployment
```bash
# Green 배포 (새 버전)
kubectl apply -f deployment-green.yaml

# 트래픽 전환
kubectl apply -f service-green.yaml

# Blue 제거 (이전 버전)
kubectl delete -f deployment-blue.yaml
```

### Canary Deployment
```yaml
# 10% 트래픽을 새 버전으로
apiVersion: v1
kind: Service
metadata:
  name: ml-model-canary
spec:
  selector:
    app: ml-model
    version: v2
  ports:
  - port: 80
    targetPort: 8000
```

## 🔒 보안 & 규정 준수

- API 인증 (JWT, OAuth2)
- HTTPS/TLS 암호화
- 모델 보안 (모델 암호화)
- 데이터 프라이버시 (GDPR, HIPAA)
- 감사 로그

## 📈 성능 최적화

- Model Quantization
- Batch Inference
- Caching
- Load Balancing
- Auto-scaling

---

**다음**: [Data Engineering](../data-engineering)
