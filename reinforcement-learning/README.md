# 강화학습 (Reinforcement Learning)

Q-Learning부터 PPO까지, 강화학습 알고리즘과 게임 AI 구현

## 📚 학습 내용

### 1. Q-Learning 기초
- Tabular Q-Learning
- CartPole, FrozenLake 환경
- Exploration vs Exploitation
- 📓 [01_q_learning.ipynb](./notebooks/01_q_learning.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/reinforcement-learning/notebooks/01_q_learning.ipynb)

### 2. DQN (Deep Q-Network)
- Experience Replay
- Target Network
- Atari 게임 학습
- 📓 [02_dqn.ipynb](./notebooks/02_dqn.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/reinforcement-learning/notebooks/02_dqn.ipynb)

### 3. Policy Gradient Methods
- REINFORCE 알고리즘
- Actor-Critic
- Advantage Function
- 📓 [03_policy_gradient.ipynb](./notebooks/03_policy_gradient.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/reinforcement-learning/notebooks/03_policy_gradient.ipynb)

### 4. PPO (Proximal Policy Optimization)
- Clipped Objective
- Continuous Action Space
- Mujoco 환경
- 📓 [04_ppo.ipynb](./notebooks/04_ppo.ipynb)

### 5. A3C (Asynchronous Advantage Actor-Critic)
- 병렬 학습
- Multi-threading
- 분산 강화학습
- 📓 [05_a3c.ipynb](./notebooks/05_a3c.ipynb)

## 🚀 빠른 시작

```bash
# 의존성 설치
pip install -r requirements.txt

# Gymnasium 환경 테스트
python -c "import gymnasium as gym; env = gym.make('CartPole-v1'); print('Environment ready!')"

# 노트북 실행
jupyter notebook
```

## 💻 주요 예제

### Q-Learning (Tabular)

```python
import numpy as np
import gymnasium as gym

env = gym.make('FrozenLake-v1')
Q = np.zeros([env.observation_space.n, env.action_space.n])

# 학습 파라미터
alpha = 0.1  # Learning rate
gamma = 0.99  # Discount factor
epsilon = 0.1  # Exploration rate

for episode in range(10000):
    state = env.reset()[0]
    done = False

    while not done:
        # Epsilon-greedy 정책
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state, :])

        next_state, reward, done, truncated, info = env.step(action)

        # Q-value 업데이트
        Q[state, action] += alpha * (
            reward + gamma * np.max(Q[next_state, :]) - Q[state, action]
        )

        state = next_state
```

### DQN (Deep Q-Network)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Experience Replay
replay_buffer = deque(maxlen=10000)

# 학습 루프
for episode in range(num_episodes):
    state = env.reset()
    done = False

    while not done:
        # 행동 선택
        if random.random() < epsilon:
            action = env.action_space.sample()
        else:
            with torch.no_grad():
                action = policy_net(state).argmax().item()

        # 환경 상호작용
        next_state, reward, done, _ = env.step(action)
        replay_buffer.append((state, action, reward, next_state, done))

        # 경험 재생으로 학습
        if len(replay_buffer) > batch_size:
            batch = random.sample(replay_buffer, batch_size)
            # ... DQN 학습 로직
```

### PPO (Proximal Policy Optimization)

```python
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

# 환경 생성
env = gym.make('CartPole-v1')
env = DummyVecEnv([lambda: env])

# PPO 모델
model = PPO(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    verbose=1
)

# 학습
model.learn(total_timesteps=100000)

# 저장 및 로드
model.save("ppo_cartpole")
model = PPO.load("ppo_cartpole")
```

## 🎯 주요 기술

- ✅ Gymnasium (OpenAI Gym)
- ✅ Stable-Baselines3
- ✅ PyTorch RL
- ✅ Ray RLlib
- ✅ Q-Learning, DQN, DDQN
- ✅ Policy Gradient (REINFORCE, A2C, A3C)
- ✅ PPO, SAC, TD3

## 🎮 지원 환경

- **Classic Control**: CartPole, MountainCar, Pendulum
- **Atari**: Pong, Breakout, Space Invaders
- **Box2D**: LunarLander, BipedalWalker
- **Mujoco**: HalfCheetah, Humanoid, Walker2d
- **Custom**: 커스텀 환경 구축

## 🎨 데모 애플리케이션

### 실시간 에이전트 플레이

```bash
cd demos
python play_agent.py --env CartPole-v1 --model ppo_cartpole.zip
```

### 학습 시각화

```bash
cd demos
streamlit run training_visualization.py
```

## 📊 평가 및 벤치마크

```python
from stable_baselines3.common.evaluation import evaluate_policy

# 모델 평가
mean_reward, std_reward = evaluate_policy(
    model, env, n_eval_episodes=100
)
print(f"Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")
```

## 🚀 고급 주제

- Multi-Agent RL
- Hierarchical RL
- Inverse RL
- Offline RL
- Model-Based RL
- Meta-RL

## 🏆 실전 프로젝트

1. **게임 AI**: Atari, Unity ML-Agents
2. **로봇 제어**: 로봇 팔 제어, 보행 로봇
3. **자율주행**: 차선 유지, 주차
4. **자원 관리**: 최적화 문제
5. **추천 시스템**: 강화학습 기반 추천

---

**다음**: [Generative Models](../gans-generative)
