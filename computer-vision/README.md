# 컴퓨터 비전 (Computer Vision)

객체 탐지, 이미지 세그멘테이션, 얼굴 인식 등 실전 컴퓨터 비전 프로젝트

## 📚 프로젝트 목록

### 1. YOLO 객체 탐지 (Object Detection with YOLO)
- YOLOv5, YOLOv8, YOLOv11 구현
- 실시간 객체 탐지
- 커스텀 데이터셋 학습
- 📓 [01_yolo_object_detection.ipynb](./notebooks/01_yolo_object_detection.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/computer-vision/notebooks/01_yolo_object_detection.ipynb)

### 2. 이미지 세그멘테이션 (Image Segmentation)
- U-Net, Mask R-CNN
- Semantic Segmentation
- Instance Segmentation
- 📓 [02_image_segmentation.ipynb](./notebooks/02_image_segmentation.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/computer-vision/notebooks/02_image_segmentation.ipynb)

### 3. 얼굴 인식 (Face Recognition)
- FaceNet, ArcFace
- Face Detection & Recognition
- Real-time Face Recognition
- 📓 [03_face_recognition.ipynb](./notebooks/03_face_recognition.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/computer-vision/notebooks/03_face_recognition.ipynb)

### 4. 포즈 추정 (Pose Estimation)
- OpenPose, MediaPipe
- 2D/3D Pose Estimation
- Action Recognition
- 📓 [04_pose_estimation.ipynb](./notebooks/04_pose_estimation.ipynb)

### 5. OCR (Optical Character Recognition)
- EasyOCR, Tesseract, PaddleOCR
- 한국어 OCR
- Document Analysis
- 📓 [05_ocr.ipynb](./notebooks/05_ocr.ipynb)

## 🚀 빠른 시작

```bash
# 의존성 설치
pip install -r requirements.txt

# YOLOv8 설치
pip install ultralytics

# 노트북 실행
jupyter notebook
```

## 💻 주요 예제

### YOLOv8 객체 탐지

```python
from ultralytics import YOLO

# 모델 로드
model = YOLO('yolov8n.pt')

# 학습
results = model.train(
    data='coco128.yaml',
    epochs=100,
    imgsz=640,
    batch=16
)

# 추론
results = model('image.jpg')
results[0].show()
```

### 실시간 비디오 처리

```python
import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    results = model(frame)
    annotated_frame = results[0].plot()
    cv2.imshow('YOLOv8', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### 이미지 세그멘테이션 (U-Net)

```python
import torch
from models.unet import UNet

model = UNet(in_channels=3, out_channels=1)
model.load_state_dict(torch.load('unet_checkpoint.pth'))
model.eval()

with torch.no_grad():
    mask = model(image)
```

## 🎯 주요 기술

- ✅ YOLO (v5, v8, v11) - 객체 탐지
- ✅ Mask R-CNN - 인스턴스 세그멘테이션
- ✅ U-Net - 의료 영상 세그멘테이션
- ✅ FaceNet - 얼굴 인식
- ✅ OpenPose - 포즈 추정
- ✅ EasyOCR - 광학 문자 인식

## 🎨 데모 애플리케이션

### 실시간 객체 탐지 데모

```bash
cd demos
streamlit run object_detection_demo.py
```

### 얼굴 인식 데모

```bash
cd demos
python face_recognition_demo.py
```

## 📊 데이터셋

- **COCO**: 객체 탐지 및 세그멘테이션
- **Pascal VOC**: 객체 탐지
- **CelebA**: 얼굴 속성
- **LFW**: 얼굴 인식
- **Cityscapes**: 자율주행 세그멘테이션

## 🚗 실전 응용

1. **자율주행**: 차선 인식, 보행자 탐지
2. **보안**: 얼굴 인식, 이상 행동 감지
3. **의료**: 암 진단, X-Ray 분석
4. **소매**: 재고 관리, 고객 분석
5. **제조**: 불량품 검사, 품질 관리

---

**다음**: [LLM Applications](../llm-applications)
