"""
강화학습 게임 데모

Usage:
    python game_demo.py
"""

import numpy as np
import time


class GridWorld:
    """간단한 그리드 월드 환경"""
    def __init__(self, size=5):
        self.size = size
        self.state = None
        self.goal = (size - 1, size - 1)
        self.obstacles = [(1, 1), (2, 2), (3, 1)]
        self.reset()

    def reset(self):
        self.state = (0, 0)
        return self.state

    def step(self, action):
        """행동 수행: 0=상, 1=하, 2=좌, 3=우"""
        row, col = self.state
        new_row, new_col = row, col

        if action == 0:  # 상
            new_row = max(0, row - 1)
        elif action == 1:  # 하
            new_row = min(self.size - 1, row + 1)
        elif action == 2:  # 좌
            new_col = max(0, col - 1)
        elif action == 3:  # 우
            new_col = min(self.size - 1, col + 1)

        new_state = (new_row, new_col)

        # 장애물 체크
        if new_state in self.obstacles:
            new_state = self.state

        self.state = new_state

        # 보상 계산
        if self.state == self.goal:
            reward = 10
            done = True
        elif self.state in self.obstacles:
            reward = -5
            done = False
        else:
            reward = -0.1
            done = False

        return self.state, reward, done

    def render(self):
        """환경 시각화"""
        print("\n" + "=" * (self.size * 4 + 1))
        for i in range(self.size):
            row_str = "|"
            for j in range(self.size):
                if (i, j) == self.state:
                    row_str += " A "
                elif (i, j) == self.goal:
                    row_str += " G "
                elif (i, j) in self.obstacles:
                    row_str += " X "
                else:
                    row_str += " . "
                row_str += "|"
            print(row_str)
        print("=" * (self.size * 4 + 1))


class QLearningAgent:
    """Q-Learning 에이전트"""
    def __init__(self, state_size, action_size, lr=0.1, gamma=0.99, epsilon=0.1):
        self.q_table = np.zeros((state_size, state_size, action_size))
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.action_size = action_size

    def choose_action(self, state, training=True):
        if training and np.random.random() < self.epsilon:
            return np.random.randint(self.action_size)
        return np.argmax(self.q_table[state[0], state[1]])

    def learn(self, state, action, reward, next_state, done):
        current_q = self.q_table[state[0], state[1], action]

        if done:
            target_q = reward
        else:
            target_q = reward + self.gamma * np.max(self.q_table[next_state[0], next_state[1]])

        self.q_table[state[0], state[1], action] += self.lr * (target_q - current_q)


def train_agent(env, agent, episodes=500):
    """에이전트 학습"""
    print("학습 시작...")
    rewards_per_episode = []

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        steps = 0

        while not done and steps < 100:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            steps += 1

        rewards_per_episode.append(total_reward)

        if (episode + 1) % 100 == 0:
            avg_reward = np.mean(rewards_per_episode[-100:])
            print(f"Episode {episode + 1}/{episodes}, Avg Reward: {avg_reward:.2f}")

    print("학습 완료!")
    return rewards_per_episode


def demo_agent(env, agent, delay=0.5):
    """학습된 에이전트 데모"""
    print("\n학습된 에이전트 데모")
    print("=" * 40)

    state = env.reset()
    total_reward = 0
    done = False
    steps = 0

    action_names = ['↑', '↓', '←', '→']

    env.render()
    time.sleep(delay)

    while not done and steps < 20:
        action = agent.choose_action(state, training=False)
        next_state, reward, done = env.step(action)

        print(f"\n행동: {action_names[action]}, 보상: {reward:.1f}")
        env.render()

        state = next_state
        total_reward += reward
        steps += 1
        time.sleep(delay)

    print(f"\n총 보상: {total_reward:.2f}, 스텝 수: {steps}")

    if done:
        print("🎉 목표 도달!")
    else:
        print("❌ 목표 도달 실패")


def show_policy(agent, size):
    """학습된 정책 시각화"""
    print("\n학습된 정책:")
    print("=" * (size * 4 + 1))

    action_symbols = ['↑', '↓', '←', '→']

    for i in range(size):
        row_str = "|"
        for j in range(size):
            best_action = np.argmax(agent.q_table[i, j])
            row_str += f" {action_symbols[best_action]} |"
        print(row_str)
    print("=" * (size * 4 + 1))


def main():
    print("=" * 50)
    print("       강화학습 GridWorld 데모")
    print("=" * 50)
    print("\n범례:")
    print("  A = 에이전트")
    print("  G = 목표")
    print("  X = 장애물")
    print("  . = 빈 공간")

    # 환경 및 에이전트 생성
    env = GridWorld(size=5)
    agent = QLearningAgent(
        state_size=5,
        action_size=4,
        lr=0.1,
        gamma=0.99,
        epsilon=0.1
    )

    # 학습
    train_agent(env, agent, episodes=500)

    # 정책 시각화
    show_policy(agent, 5)

    # 데모
    demo_agent(env, agent, delay=0.3)


if __name__ == "__main__":
    main()
