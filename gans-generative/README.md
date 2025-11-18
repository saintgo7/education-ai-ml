# 생성 모델 (Generative Models)

GANs, VAE, Diffusion Models를 활용한 이미지 및 텍스트 생성

## 📚 학습 내용

### 1. GAN 기초 (Generative Adversarial Networks)
- Vanilla GAN
- DCGAN (Deep Convolutional GAN)
- Conditional GAN
- 📓 [01_gan_basics.ipynb](./notebooks/01_gan_basics.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/gans-generative/notebooks/01_gan_basics.ipynb)

### 2. 고급 GAN (Advanced GANs)
- StyleGAN, StyleGAN2
- CycleGAN (Image-to-Image Translation)
- Progressive GAN
- 📓 [02_advanced_gans.ipynb](./notebooks/02_advanced_gans.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/gans-generative/notebooks/02_advanced_gans.ipynb)

### 3. VAE (Variational Autoencoder)
- VAE 구조 및 원리
- CVAE (Conditional VAE)
- Beta-VAE
- 📓 [03_vae.ipynb](./notebooks/03_vae.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/gans-generative/notebooks/03_vae.ipynb)

### 4. Diffusion Models
- DDPM (Denoising Diffusion Probabilistic Models)
- Stable Diffusion
- ControlNet
- 📓 [04_diffusion_models.ipynb](./notebooks/04_diffusion_models.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/gans-generative/notebooks/04_diffusion_models.ipynb)

### 5. 텍스트-이미지 생성
- DALL-E, Midjourney 스타일
- Stable Diffusion 활용
- Prompt Engineering for Image Generation
- 📓 [05_text_to_image.ipynb](./notebooks/05_text_to_image.ipynb)

## 🚀 빠른 시작

```bash
# 의존성 설치
pip install -r requirements.txt

# Hugging Face 토큰 설정 (Stable Diffusion 사용 시)
export HF_TOKEN="your-huggingface-token"

# 노트북 실행
jupyter notebook
```

## 💻 주요 예제

### DCGAN 구현

```python
import torch
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, latent_dim=100, img_channels=3):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.ConvTranspose2d(latent_dim, 512, 4, 1, 0, bias=False),
            nn.BatchNorm2d(512),
            nn.ReLU(True),
            nn.ConvTranspose2d(512, 256, 4, 2, 1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            nn.ConvTranspose2d(256, 128, 4, 2, 1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, 4, 2, 1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.ConvTranspose2d(64, img_channels, 4, 2, 1, bias=False),
            nn.Tanh()
        )

    def forward(self, input):
        return self.main(input)

class Discriminator(nn.Module):
    def __init__(self, img_channels=3):
        super(Discriminator, self).__init__()
        self.main = nn.Sequential(
            nn.Conv2d(img_channels, 64, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 128, 4, 2, 1, bias=False),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(128, 256, 4, 2, 1, bias=False),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(256, 512, 4, 2, 1, bias=False),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(512, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.main(input)
```

### VAE 구현

```python
class VAE(nn.Module):
    def __init__(self, latent_dim=128):
        super(VAE, self).__init__()

        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 32, 4, 2, 1),
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, 2, 1),
            nn.ReLU(),
            nn.Conv2d(64, 128, 4, 2, 1),
            nn.ReLU(),
            nn.Flatten()
        )

        self.fc_mu = nn.Linear(128 * 4 * 4, latent_dim)
        self.fc_logvar = nn.Linear(128 * 4 * 4, latent_dim)

        # Decoder
        self.decoder_input = nn.Linear(latent_dim, 128 * 4 * 4)
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, 4, 2, 1),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, 4, 2, 1),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 3, 4, 2, 1),
            nn.Sigmoid()
        )

    def encode(self, x):
        x = self.encoder(x)
        mu = self.fc_mu(x)
        logvar = self.fc_logvar(x)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        x = self.decoder_input(z)
        x = x.view(-1, 128, 4, 4)
        return self.decoder(x)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar
```

### Stable Diffusion 사용

```python
from diffusers import StableDiffusionPipeline
import torch

# 파이프라인 로드
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 이미지 생성
prompt = "a beautiful landscape with mountains and a lake, digital art"
image = pipe(prompt, num_inference_steps=50, guidance_scale=7.5).images[0]
image.save("generated_image.png")
```

## 🎯 주요 기술

- ✅ GANs (DCGAN, StyleGAN, CycleGAN)
- ✅ VAE (Variational Autoencoders)
- ✅ Diffusion Models (DDPM, Stable Diffusion)
- ✅ ControlNet, LoRA
- ✅ Text-to-Image Generation
- ✅ Image-to-Image Translation
- ✅ Super Resolution

## 🎨 데모 애플리케이션

### Stable Diffusion 웹 UI

```bash
cd demos
streamlit run stable_diffusion_demo.py
```

### GAN 이미지 생성기

```bash
cd demos
python gan_generator_demo.py
```

## 📊 평가 지표

- **FID (Fréchet Inception Distance)**: 생성 품질
- **IS (Inception Score)**: 다양성과 품질
- **LPIPS**: 이미지 유사도
- **SSIM**: 구조적 유사도

## 🚀 실전 응용

1. **예술 & 디자인**: AI 아트, 그래픽 디자인
2. **패션**: 의류 디자인 생성
3. **게임**: 캐릭터, 배경 생성
4. **의료**: 의료 영상 증강
5. **엔터테인먼트**: 영화, 애니메이션

## 📦 사전 학습 모델

- **Stable Diffusion**: 텍스트-이미지 생성
- **StyleGAN2**: 고품질 얼굴 생성
- **CycleGAN**: 스타일 변환

---

**다음**: [MLOps Pipeline](../mlops-pipeline)
