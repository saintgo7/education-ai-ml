"""
DCGAN 학습 스크립트

Usage:
    python train_gan.py --dataset cifar10 --epochs 100
"""

import argparse
import logging
from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
from torchvision.utils import save_image
from tqdm import tqdm
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Generator(nn.Module):
    """DCGAN Generator"""
    def __init__(self, latent_dim=100, img_channels=3, features_g=64):
        super(Generator, self).__init__()
        self.net = nn.Sequential(
            self._block(latent_dim, features_g * 16, 4, 1, 0),
            self._block(features_g * 16, features_g * 8, 4, 2, 1),
            self._block(features_g * 8, features_g * 4, 4, 2, 1),
            self._block(features_g * 4, features_g * 2, 4, 2, 1),
            nn.ConvTranspose2d(
                features_g * 2, img_channels, kernel_size=4,
                stride=2, padding=1
            ),
            nn.Tanh()
        )

    def _block(self, in_channels, out_channels, kernel_size, stride, padding):
        return nn.Sequential(
            nn.ConvTranspose2d(
                in_channels, out_channels, kernel_size, stride, padding, bias=False
            ),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(True)
        )

    def forward(self, x):
        return self.net(x)


class Discriminator(nn.Module):
    """DCGAN Discriminator"""
    def __init__(self, img_channels=3, features_d=64):
        super(Discriminator, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(img_channels, features_d, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            self._block(features_d, features_d * 2, 4, 2, 1),
            self._block(features_d * 2, features_d * 4, 4, 2, 1),
            self._block(features_d * 4, features_d * 8, 4, 2, 1),
            nn.Conv2d(features_d * 8, 1, kernel_size=4, stride=1, padding=0),
            nn.Sigmoid()
        )

    def _block(self, in_channels, out_channels, kernel_size, stride, padding):
        return nn.Sequential(
            nn.Conv2d(
                in_channels, out_channels, kernel_size, stride, padding, bias=False
            ),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.2, inplace=True)
        )

    def forward(self, x):
        return self.net(x)


def weights_init(m):
    """가중치 초기화"""
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(m.weight.data, 1.0, 0.02)
        nn.init.constant_(m.bias.data, 0)


def get_dataloader(dataset_name, batch_size, image_size):
    """데이터로더 생성"""
    transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    if dataset_name == 'cifar10':
        dataset = torchvision.datasets.CIFAR10(
            root='./data', train=True, download=True, transform=transform
        )
    elif dataset_name == 'mnist':
        transform = transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
        dataset = torchvision.datasets.MNIST(
            root='./data', train=True, download=True, transform=transform
        )
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    return dataloader


def train(args):
    """DCGAN 학습"""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")

    # 출력 디렉토리 생성
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    samples_dir = output_dir / 'samples'
    samples_dir.mkdir(exist_ok=True)

    # 데이터로더
    dataloader = get_dataloader(args.dataset, args.batch_size, args.image_size)
    img_channels = 1 if args.dataset == 'mnist' else 3

    # 모델 생성
    netG = Generator(args.latent_dim, img_channels, args.features_g).to(device)
    netD = Discriminator(img_channels, args.features_d).to(device)
    netG.apply(weights_init)
    netD.apply(weights_init)

    logger.info(f"Generator parameters: {sum(p.numel() for p in netG.parameters()):,}")
    logger.info(f"Discriminator parameters: {sum(p.numel() for p in netD.parameters()):,}")

    # 옵티마이저
    optimizerD = optim.Adam(netD.parameters(), lr=args.lr, betas=(args.beta1, 0.999))
    optimizerG = optim.Adam(netG.parameters(), lr=args.lr, betas=(args.beta1, 0.999))

    # 손실 함수
    criterion = nn.BCELoss()

    # 고정 노이즈 (시각화용)
    fixed_noise = torch.randn(64, args.latent_dim, 1, 1, device=device)

    # 학습 루프
    G_losses = []
    D_losses = []

    for epoch in range(args.epochs):
        pbar = tqdm(dataloader, desc=f'Epoch {epoch+1}/{args.epochs}')

        for i, (real_images, _) in enumerate(pbar):
            batch_size = real_images.size(0)
            real_images = real_images.to(device)

            # Labels
            real_label = torch.ones(batch_size, 1, 1, 1, device=device)
            fake_label = torch.zeros(batch_size, 1, 1, 1, device=device)

            # ==================== Train Discriminator ====================
            netD.zero_grad()

            # 진짜 이미지
            output_real = netD(real_images)
            lossD_real = criterion(output_real, real_label)

            # 가짜 이미지
            noise = torch.randn(batch_size, args.latent_dim, 1, 1, device=device)
            fake_images = netG(noise)
            output_fake = netD(fake_images.detach())
            lossD_fake = criterion(output_fake, fake_label)

            # Discriminator 손실
            lossD = lossD_real + lossD_fake
            lossD.backward()
            optimizerD.step()

            # ==================== Train Generator ====================
            netG.zero_grad()

            output = netD(fake_images)
            lossG = criterion(output, real_label)
            lossG.backward()
            optimizerG.step()

            # 로깅
            D_losses.append(lossD.item())
            G_losses.append(lossG.item())

            pbar.set_postfix({
                'D_loss': lossD.item(),
                'G_loss': lossG.item()
            })

        # 에폭 종료 후 샘플 이미지 저장
        with torch.no_grad():
            fake = netG(fixed_noise).detach().cpu()
        save_image(
            fake,
            samples_dir / f'fake_epoch_{epoch+1:03d}.png',
            normalize=True,
            nrow=8
        )

        logger.info(f"Epoch [{epoch+1}/{args.epochs}] D_loss: {np.mean(D_losses[-len(dataloader):]):.4f}, "
                   f"G_loss: {np.mean(G_losses[-len(dataloader):]):.4f}")

        # 체크포인트 저장
        if (epoch + 1) % args.save_interval == 0:
            torch.save({
                'epoch': epoch,
                'netG': netG.state_dict(),
                'netD': netD.state_dict(),
                'optimizerG': optimizerG.state_dict(),
                'optimizerD': optimizerD.state_dict(),
            }, output_dir / f'checkpoint_epoch_{epoch+1}.pth')

    # 최종 모델 저장
    torch.save(netG.state_dict(), output_dir / 'generator_final.pth')
    torch.save(netD.state_dict(), output_dir / 'discriminator_final.pth')
    logger.info(f"Training completed! Models saved to {output_dir}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train DCGAN')
    parser.add_argument('--dataset', type=str, default='cifar10',
                       choices=['cifar10', 'mnist'])
    parser.add_argument('--batch_size', type=int, default=128)
    parser.add_argument('--image_size', type=int, default=64)
    parser.add_argument('--latent_dim', type=int, default=100)
    parser.add_argument('--features_g', type=int, default=64)
    parser.add_argument('--features_d', type=int, default=64)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--lr', type=float, default=0.0002)
    parser.add_argument('--beta1', type=float, default=0.5)
    parser.add_argument('--output_dir', type=str, default='../generated_samples')
    parser.add_argument('--save_interval', type=int, default=10)

    args = parser.parse_args()
    train(args)
