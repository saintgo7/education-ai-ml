"""
GAN 이미지 생성 Gradio 데모

Usage:
    python image_generator_demo.py
"""

import gradio as gr
import torch
import torch.nn as nn
import numpy as np
from PIL import Image


class Generator(nn.Module):
    """간단한 Generator 모델"""
    def __init__(self, latent_dim=100, img_shape=(1, 28, 28)):
        super(Generator, self).__init__()
        self.img_shape = img_shape

        self.model = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(256),

            nn.Linear(256, 512),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(512),

            nn.Linear(512, 1024),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(1024),

            nn.Linear(1024, int(np.prod(img_shape))),
            nn.Tanh()
        )

    def forward(self, z):
        img = self.model(z)
        return img.view(img.size(0), *self.img_shape)


# 모델 초기화
latent_dim = 100
generator = Generator(latent_dim)
generator.eval()


def generate_images(num_images, seed):
    """이미지 생성 함수"""
    torch.manual_seed(seed)

    with torch.no_grad():
        z = torch.randn(num_images, latent_dim)
        generated = generator(z)

    # 이미지를 [0, 255] 범위로 변환
    images = (generated + 1) / 2 * 255
    images = images.numpy().astype(np.uint8)

    # 그리드로 배열
    grid_size = int(np.ceil(np.sqrt(num_images)))
    grid = np.zeros((grid_size * 28, grid_size * 28), dtype=np.uint8)

    for i in range(num_images):
        row = i // grid_size
        col = i % grid_size
        grid[row*28:(row+1)*28, col*28:(col+1)*28] = images[i, 0]

    return Image.fromarray(grid)


def interpolate_latent(seed1, seed2, steps):
    """잠재 공간 보간"""
    torch.manual_seed(seed1)
    z1 = torch.randn(1, latent_dim)

    torch.manual_seed(seed2)
    z2 = torch.randn(1, latent_dim)

    images = []
    with torch.no_grad():
        for i in range(steps):
            ratio = i / (steps - 1)
            z = z1 * (1 - ratio) + z2 * ratio
            img = generator(z)
            img = ((img + 1) / 2 * 255).numpy().astype(np.uint8)
            images.append(img[0, 0])

    # 가로로 연결
    result = np.concatenate(images, axis=1)
    return Image.fromarray(result)


# Gradio 인터페이스
with gr.Blocks(title="GAN 이미지 생성기") as demo:
    gr.Markdown("""
    # 🎨 GAN 이미지 생성기

    이 데모는 GAN(Generative Adversarial Network)을 사용하여 이미지를 생성합니다.
    (데모용 랜덤 초기화된 모델 - 실제 학습된 모델이 아닙니다)
    """)

    with gr.Tab("이미지 생성"):
        with gr.Row():
            num_images = gr.Slider(1, 16, value=9, step=1, label="생성할 이미지 수")
            seed = gr.Slider(0, 1000, value=42, step=1, label="시드")

        generate_btn = gr.Button("이미지 생성", variant="primary")
        output_image = gr.Image(label="생성된 이미지")

        generate_btn.click(
            fn=generate_images,
            inputs=[num_images, seed],
            outputs=output_image
        )

    with gr.Tab("잠재 공간 보간"):
        gr.Markdown("두 잠재 벡터 사이를 보간하여 점진적인 변화를 관찰합니다.")

        with gr.Row():
            seed1 = gr.Slider(0, 1000, value=42, step=1, label="시드 1")
            seed2 = gr.Slider(0, 1000, value=123, step=1, label="시드 2")
            steps = gr.Slider(5, 20, value=10, step=1, label="보간 단계")

        interpolate_btn = gr.Button("보간 생성", variant="primary")
        interpolate_output = gr.Image(label="보간 결과")

        interpolate_btn.click(
            fn=interpolate_latent,
            inputs=[seed1, seed2, steps],
            outputs=interpolate_output
        )

    gr.Markdown("""
    ## 사용 방법

    1. **이미지 생성**: 시드를 변경하여 다양한 이미지를 생성합니다.
    2. **잠재 공간 보간**: 두 시드 사이를 보간하여 점진적인 변화를 관찰합니다.

    ## 참고

    - 이 데모는 학습되지 않은 랜덤 모델을 사용합니다.
    - 실제 학습된 모델을 로드하면 의미 있는 이미지가 생성됩니다.
    """)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861)
