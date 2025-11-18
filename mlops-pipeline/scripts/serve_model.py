"""
FastAPI 모델 서빙 서버

Usage:
    uvicorn serve_model:app --host 0.0.0.0 --port 8000 --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import mlflow.pyfunc
import numpy as np
import logging
from pathlib import Path
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="ML Model API",
    description="Machine Learning Model Serving API",
    version="1.0.0"
)

# Prometheus 메트릭
REQUEST_COUNT = Counter('ml_model_requests_total', 'Total number of requests')
REQUEST_LATENCY = Histogram('ml_model_request_latency_seconds', 'Request latency')
PREDICTION_COUNT = Counter('ml_model_predictions_total', 'Total number of predictions',
                          ['model_name', 'status'])


class PredictionRequest(BaseModel):
    """예측 요청 스키마"""
    features: List[float] = Field(..., description="Input features for prediction")
    model_name: Optional[str] = Field("default", description="Model name to use")

    class Config:
        json_schema_extra = {
            "example": {
                "features": [5.1, 3.5, 1.4, 0.2],
                "model_name": "iris_classifier"
            }
        }


class PredictionResponse(BaseModel):
    """예측 응답 스키마"""
    prediction: float = Field(..., description="Model prediction")
    probability: Optional[List[float]] = Field(None, description="Class probabilities")
    model_name: str = Field(..., description="Model name used")
    inference_time_ms: float = Field(..., description="Inference time in milliseconds")

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": 0,
                "probability": [0.9, 0.05, 0.05],
                "model_name": "iris_classifier",
                "inference_time_ms": 12.5
            }
        }


class BatchPredictionRequest(BaseModel):
    """배치 예측 요청 스키마"""
    features: List[List[float]] = Field(..., description="Batch input features")
    model_name: Optional[str] = Field("default", description="Model name to use")


class BatchPredictionResponse(BaseModel):
    """배치 예측 응답 스키마"""
    predictions: List[float] = Field(..., description="Model predictions")
    model_name: str = Field(..., description="Model name used")
    inference_time_ms: float = Field(..., description="Total inference time")


# 모델 캐시
models = {}


def load_model(model_name: str = "default"):
    """모델 로드 (캐싱)"""
    if model_name not in models:
        try:
            # MLflow에서 모델 로드
            model_uri = f"models:/{model_name}/production"
            logger.info(f"Loading model: {model_uri}")
            models[model_name] = mlflow.pyfunc.load_model(model_uri)
            logger.info(f"Model {model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            # Fallback: 로컬 모델 로드
            try:
                model_path = Path(__file__).parent.parent / "models" / f"{model_name}.pkl"
                if model_path.exists():
                    import joblib
                    models[model_name] = joblib.load(model_path)
                    logger.info(f"Loaded local model: {model_path}")
                else:
                    raise FileNotFoundError(f"Model not found: {model_name}")
            except Exception as fallback_error:
                logger.error(f"Fallback failed: {fallback_error}")
                raise HTTPException(status_code=500, detail=f"Failed to load model: {model_name}")

    return models[model_name]


@app.get("/")
def read_root():
    """루트 엔드포인트"""
    return {
        "message": "ML Model API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "models_loaded": list(models.keys())
    }


@app.get("/models")
def list_models():
    """사용 가능한 모델 목록"""
    return {
        "models": list(models.keys()),
        "total": len(models)
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """단일 예측 엔드포인트"""
    REQUEST_COUNT.inc()

    try:
        start_time = time.time()

        # 모델 로드
        model = load_model(request.model_name)

        # 예측
        features = np.array([request.features])
        with REQUEST_LATENCY.time():
            prediction = model.predict(features)[0]

        # 확률 계산 (가능한 경우)
        probability = None
        if hasattr(model, 'predict_proba'):
            probability = model.predict_proba(features)[0].tolist()

        inference_time = (time.time() - start_time) * 1000  # ms

        PREDICTION_COUNT.labels(model_name=request.model_name, status='success').inc()

        return PredictionResponse(
            prediction=float(prediction),
            probability=probability,
            model_name=request.model_name,
            inference_time_ms=inference_time
        )

    except Exception as e:
        PREDICTION_COUNT.labels(model_name=request.model_name, status='error').inc()
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """배치 예측 엔드포인트"""
    REQUEST_COUNT.inc()

    try:
        start_time = time.time()

        # 모델 로드
        model = load_model(request.model_name)

        # 배치 예측
        features = np.array(request.features)
        with REQUEST_LATENCY.time():
            predictions = model.predict(features)

        inference_time = (time.time() - start_time) * 1000  # ms

        PREDICTION_COUNT.labels(model_name=request.model_name, status='success').inc()

        return BatchPredictionResponse(
            predictions=predictions.tolist(),
            model_name=request.model_name,
            inference_time_ms=inference_time
        )

    except Exception as e:
        PREDICTION_COUNT.labels(model_name=request.model_name, status='error').inc()
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def metrics():
    """Prometheus 메트릭 엔드포인트"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.on_event("startup")
async def startup_event():
    """서버 시작 시 실행"""
    logger.info("Starting ML Model API")
    # 기본 모델 사전 로드 (선택사항)
    try:
        load_model("default")
    except:
        logger.warning("Default model not found, will load on demand")


@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 실행"""
    logger.info("Shutting down ML Model API")
    models.clear()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
