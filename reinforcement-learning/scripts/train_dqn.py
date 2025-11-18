"""
DQN 학습 스크립트

Usage:
    python train_dqn.py --env CartPole-v1 --episodes 1000
"""

import argparse
import logging
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import gymnasium as gym
from collections import deque
import random
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DQN(nn.Module):
    """DQN 네트워크"""
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)


class ReplayBuffer:
    """경험 재생 버퍼"""
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)


class DQNAgent:
    """DQN 에이전트"""
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99,
                 epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995,
                 buffer_size=10000, batch_size=64, target_update=10):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update = target_update

        # 네트워크
        self.policy_net = DQN(state_dim, action_dim).to(self.device)
        self.target_net = DQN(state_dim, action_dim).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        # 옵티마이저
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()

        # 리플레이 버퍼
        self.replay_buffer = ReplayBuffer(buffer_size)

    def select_action(self, state, training=True):
        """행동 선택 (epsilon-greedy)"""
        if training and random.random() < self.epsilon:
            return random.randrange(self.action_dim)
        else:
            with torch.no_grad():
                state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                q_values = self.policy_net(state)
                return q_values.argmax().item()

    def train_step(self):
        """학습 스텝"""
        if len(self.replay_buffer) < self.batch_size:
            return None

        # 배치 샘플링
        batch = self.replay_buffer.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones = torch.FloatTensor(dones).unsqueeze(1).to(self.device)

        # 현재 Q 값
        current_q_values = self.policy_net(states).gather(1, actions)

        # 다음 Q 값 (Target Network 사용)
        with torch.no_grad():
            next_q_values = self.target_net(next_states).max(1)[0].unsqueeze(1)
            target_q_values = rewards + (1 - dones) * self.gamma * next_q_values

        # 손실 계산 및 역전파
        loss = self.loss_fn(current_q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def update_epsilon(self):
        """Epsilon 감소"""
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)

    def update_target_network(self):
        """Target Network 업데이트"""
        self.target_net.load_state_dict(self.policy_net.state_dict())


def train(args):
    """DQN 학습"""
    # 환경 생성
    env = gym.make(args.env)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    logger.info(f"Environment: {args.env}")
    logger.info(f"State dim: {state_dim}, Action dim: {action_dim}")

    # 에이전트 생성
    agent = DQNAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        lr=args.lr,
        gamma=args.gamma,
        epsilon_start=args.epsilon_start,
        epsilon_end=args.epsilon_end,
        epsilon_decay=args.epsilon_decay,
        buffer_size=args.buffer_size,
        batch_size=args.batch_size,
        target_update=args.target_update
    )

    # 학습
    episode_rewards = []
    best_reward = -float('inf')

    for episode in tqdm(range(args.episodes), desc="Training"):
        state, _ = env.reset()
        episode_reward = 0
        done = False

        while not done:
            # 행동 선택
            action = agent.select_action(state)

            # 환경 상호작용
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            # 버퍼에 저장
            agent.replay_buffer.push(state, action, reward, next_state, done)

            # 학습
            loss = agent.train_step()

            state = next_state
            episode_reward += reward

        # Epsilon 감소
        agent.update_epsilon()

        # Target Network 업데이트
        if episode % agent.target_update == 0:
            agent.update_target_network()

        episode_rewards.append(episode_reward)

        # 로깅
        if episode % 10 == 0:
            avg_reward = np.mean(episode_rewards[-10:])
            logger.info(
                f"Episode {episode}, Avg Reward: {avg_reward:.2f}, "
                f"Epsilon: {agent.epsilon:.3f}"
            )

            # 최고 성능 모델 저장
            if avg_reward > best_reward:
                best_reward = avg_reward
                save_path = Path(args.save_dir) / f"{args.env}_best.pth"
                save_path.parent.mkdir(parents=True, exist_ok=True)
                torch.save(agent.policy_net.state_dict(), save_path)
                logger.info(f"Best model saved: {save_path}")

    env.close()

    # 최종 모델 저장
    save_path = Path(args.save_dir) / f"{args.env}_final.pth"
    torch.save(agent.policy_net.state_dict(), save_path)
    logger.info(f"Final model saved: {save_path}")

    return episode_rewards


def evaluate(args):
    """모델 평가"""
    env = gym.make(args.env, render_mode="human")
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    # 모델 로드
    agent = DQNAgent(state_dim, action_dim)
    agent.policy_net.load_state_dict(torch.load(args.model_path))
    agent.policy_net.eval()

    for episode in range(args.eval_episodes):
        state, _ = env.reset()
        episode_reward = 0
        done = False

        while not done:
            action = agent.select_action(state, training=False)
            state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            episode_reward += reward

        logger.info(f"Episode {episode+1}, Reward: {episode_reward}")

    env.close()


def main(args):
    if args.mode == 'train':
        train(args)
    elif args.mode == 'eval':
        evaluate(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train DQN')
    parser.add_argument('--mode', type=str, default='train',
                       choices=['train', 'eval'])
    parser.add_argument('--env', type=str, default='CartPole-v1')
    parser.add_argument('--episodes', type=int, default=1000)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--gamma', type=float, default=0.99)
    parser.add_argument('--epsilon_start', type=float, default=1.0)
    parser.add_argument('--epsilon_end', type=float, default=0.01)
    parser.add_argument('--epsilon_decay', type=float, default=0.995)
    parser.add_argument('--buffer_size', type=int, default=10000)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--target_update', type=int, default=10)
    parser.add_argument('--save_dir', type=str, default='../checkpoints')
    parser.add_argument('--model_path', type=str, default='')
    parser.add_argument('--eval_episodes', type=int, default=10)

    args = parser.parse_args()
    main(args)
