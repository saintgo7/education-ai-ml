"""
YOLOv8 객체 탐지 모델 학습 스크립트

Usage:
    python train_yolo.py --model yolov8n.pt --data coco128.yaml --epochs 100
"""

import argparse
import logging
from pathlib import Path
from ultralytics import YOLO
import torch
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(args):
    logger.info(f"PyTorch version: {torch.__version__}")
    logger.info(f"CUDA available: {torch.cuda.is_available()}")

    # 모델 로드
    logger.info(f"Loading model: {args.model}")
    model = YOLO(args.model)

    # 데이터 설정 확인
    if not Path(args.data).exists():
        logger.error(f"Data config file not found: {args.data}")
        return

    with open(args.data, 'r') as f:
        data_config = yaml.safe_load(f)
    logger.info(f"Data config: {data_config}")

    # 학습
    logger.info("Starting training...")
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        name=args.name,
        patience=args.patience,
        save=True,
        device=args.device,
        workers=args.workers,
        pretrained=True,
        optimizer=args.optimizer,
        lr0=args.lr0,
        lrf=args.lrf,
        momentum=args.momentum,
        weight_decay=args.weight_decay,
        warmup_epochs=args.warmup_epochs,
        warmup_momentum=args.warmup_momentum,
        box=args.box,
        cls=args.cls,
        dfl=args.dfl,
        hsv_h=args.hsv_h,
        hsv_s=args.hsv_s,
        hsv_v=args.hsv_v,
        degrees=args.degrees,
        translate=args.translate,
        scale=args.scale,
        shear=args.shear,
        perspective=args.perspective,
        flipud=args.flipud,
        fliplr=args.fliplr,
        mosaic=args.mosaic,
        mixup=args.mixup,
    )

    # 검증
    logger.info("Validating model...")
    metrics = model.val()
    logger.info(f"Validation metrics: {metrics}")

    # 테스트 추론
    if args.test_image:
        logger.info(f"Testing on image: {args.test_image}")
        results = model(args.test_image)
        results[0].show()
        results[0].save(filename='result.jpg')
        logger.info("Test result saved as 'result.jpg'")

    # 모델 내보내기
    if args.export:
        logger.info(f"Exporting model to {args.export_format}...")
        model.export(format=args.export_format)
        logger.info(f"Model exported successfully!")

    logger.info("Training completed!")
    logger.info(f"Best model saved at: runs/detect/{args.name}/weights/best.pt")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train YOLOv8 model')

    # Model arguments
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                       help='Model name or path (yolov8n/s/m/l/x.pt)')
    parser.add_argument('--data', type=str, default='coco128.yaml',
                       help='Path to data config file')
    parser.add_argument('--name', type=str, default='yolov8_exp',
                       help='Experiment name')

    # Training arguments
    parser.add_argument('--epochs', type=int, default=100,
                       help='Number of epochs')
    parser.add_argument('--batch', type=int, default=16,
                       help='Batch size')
    parser.add_argument('--imgsz', type=int, default=640,
                       help='Image size')
    parser.add_argument('--device', type=str, default='',
                       help='Device (cuda:0 or cpu)')
    parser.add_argument('--workers', type=int, default=8,
                       help='Number of workers')
    parser.add_argument('--patience', type=int, default=50,
                       help='Early stopping patience')

    # Optimizer arguments
    parser.add_argument('--optimizer', type=str, default='SGD',
                       choices=['SGD', 'Adam', 'AdamW'],
                       help='Optimizer')
    parser.add_argument('--lr0', type=float, default=0.01,
                       help='Initial learning rate')
    parser.add_argument('--lrf', type=float, default=0.01,
                       help='Final learning rate (lr0 * lrf)')
    parser.add_argument('--momentum', type=float, default=0.937,
                       help='SGD momentum')
    parser.add_argument('--weight_decay', type=float, default=0.0005,
                       help='Weight decay')
    parser.add_argument('--warmup_epochs', type=float, default=3.0,
                       help='Warmup epochs')
    parser.add_argument('--warmup_momentum', type=float, default=0.8,
                       help='Warmup momentum')

    # Loss arguments
    parser.add_argument('--box', type=float, default=7.5,
                       help='Box loss gain')
    parser.add_argument('--cls', type=float, default=0.5,
                       help='Class loss gain')
    parser.add_argument('--dfl', type=float, default=1.5,
                       help='DFL loss gain')

    # Augmentation arguments
    parser.add_argument('--hsv_h', type=float, default=0.015,
                       help='HSV Hue augmentation')
    parser.add_argument('--hsv_s', type=float, default=0.7,
                       help='HSV Saturation augmentation')
    parser.add_argument('--hsv_v', type=float, default=0.4,
                       help='HSV Value augmentation')
    parser.add_argument('--degrees', type=float, default=0.0,
                       help='Rotation degrees')
    parser.add_argument('--translate', type=float, default=0.1,
                       help='Translation')
    parser.add_argument('--scale', type=float, default=0.5,
                       help='Scale')
    parser.add_argument('--shear', type=float, default=0.0,
                       help='Shear')
    parser.add_argument('--perspective', type=float, default=0.0,
                       help='Perspective')
    parser.add_argument('--flipud', type=float, default=0.0,
                       help='Vertical flip probability')
    parser.add_argument('--fliplr', type=float, default=0.5,
                       help='Horizontal flip probability')
    parser.add_argument('--mosaic', type=float, default=1.0,
                       help='Mosaic augmentation probability')
    parser.add_argument('--mixup', type=float, default=0.0,
                       help='Mixup augmentation probability')

    # Export arguments
    parser.add_argument('--test_image', type=str, default='',
                       help='Path to test image')
    parser.add_argument('--export', action='store_true',
                       help='Export model after training')
    parser.add_argument('--export_format', type=str, default='onnx',
                       choices=['onnx', 'torchscript', 'tflite', 'coreml'],
                       help='Export format')

    args = parser.parse_args()
    main(args)
