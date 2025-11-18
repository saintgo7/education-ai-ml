"""
TensorFlow/Keras 이미지 분류 학습 스크립트

Usage:
    python train_image_classifier.py --model resnet50 --epochs 20
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50, VGG16, EfficientNetB0
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_model(model_name='resnet50', num_classes=10, input_shape=(224, 224, 3)):
    """모델 생성"""
    if model_name == 'resnet50':
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
    elif model_name == 'vgg16':
        base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
    elif model_name == 'efficientnet':
        base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=input_shape)
    else:
        raise ValueError(f"Unknown model: {model_name}")

    # Fine-tuning: 마지막 몇 레이어만 학습
    base_model.trainable = True
    for layer in base_model.layers[:-20]:
        layer.trainable = False

    # 모델 구성
    inputs = keras.Input(shape=input_shape)
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = keras.Model(inputs, outputs)
    return model


def get_datasets(batch_size=32, image_size=(224, 224)):
    """CIFAR-10 데이터셋 로드"""
    (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

    # 정규화
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    # 리사이즈
    train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    train_ds = train_ds.map(lambda x, y: (tf.image.resize(x, image_size), y))
    train_ds = train_ds.shuffle(10000).batch(batch_size).prefetch(tf.data.AUTOTUNE)

    test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test))
    test_ds = test_ds.map(lambda x, y: (tf.image.resize(x, image_size), y))
    test_ds = test_ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)

    return train_ds, test_ds


def main(args):
    logger.info(f"TensorFlow version: {tf.__version__}")
    logger.info(f"GPU available: {tf.config.list_physical_devices('GPU')}")

    # 데이터셋
    train_ds, test_ds = get_datasets(args.batch_size, (args.image_size, args.image_size))

    # 모델
    model = create_model(args.model, num_classes=10,
                        input_shape=(args.image_size, args.image_size, 3))
    logger.info(f"Model created: {args.model}")
    model.summary()

    # 컴파일
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=args.learning_rate),
        loss=keras.losses.SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )

    # Callbacks
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            f'../checkpoints/{args.model}_best.h5',
            save_best_only=True,
            monitor='val_accuracy'
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        ),
        keras.callbacks.TensorBoard(log_dir=f'./logs/{args.model}'),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3
        )
    ]

    # 학습
    history = model.fit(
        train_ds,
        epochs=args.epochs,
        validation_data=test_ds,
        callbacks=callbacks
    )

    # 평가
    test_loss, test_acc = model.evaluate(test_ds)
    logger.info(f"Test accuracy: {test_acc:.4f}")

    # 저장
    model.save(f'../checkpoints/{args.model}_final.h5')
    logger.info("Training completed!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='resnet50',
                       choices=['resnet50', 'vgg16', 'efficientnet'])
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--epochs', type=int, default=20)
    parser.add_argument('--learning_rate', type=float, default=0.001)
    parser.add_argument('--image_size', type=int, default=224)
    args = parser.parse_args()
    main(args)
