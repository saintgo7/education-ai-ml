#!/usr/bin/env python3
"""
Tier별 통합 프로젝트 생성 시스템
Tier Integration Projects Generator
"""

import json
from pathlib import Path
from datetime import datetime

TIER_PROJECTS = {
    "Tier1": {
        "name": "기초 통합 프로젝트 - 데이터 분석 101",
        "english_name": "Tier 1 Integration Project - Data Analysis 101",
        "description": "Python, 자료구조, 알고리즘, 수학을 활용한 기본 데이터 분석",
        "modules": list(range(1, 11)),
        "objectives": [
            "Python 기본 문법 숙련",
            "데이터 처리 능력",
            "수학적 개념 이해",
            "기본 시각화"
        ],
        "project_tasks": [
            "CSV 파일 데이터 로드 및 기본 통계 계산",
            "데이터 시각화 (히스토그램, 산점도)",
            "선형대수를 이용한 행렬 연산",
            "기본 최적화 문제 해결"
        ]
    },
    "Tier2": {
        "name": "전통 머신러닝 프로젝트 - 고객 분류 시스템",
        "english_name": "Tier 2 Integration Project - Customer Classification System",
        "description": "회귀, 분류, 클러스터링을 활용한 고객 분류",
        "modules": list(range(11, 31)),
        "objectives": [
            "다양한 ML 알고리즘 구현",
            "모델 평가 및 선택",
            "앙상블 기법 활용",
            "클러스터링 분석"
        ],
        "project_tasks": [
            "데이터셋 전처리 및 특성 엔지니어링",
            "여러 분류 모델 학습 및 비교",
            "하이퍼파라미터 튜닝",
            "앙상블 모델 구축 (Random Forest, Gradient Boosting)",
            "모델 해석 및 평가"
        ]
    },
    "Tier3": {
        "name": "딥러닝 프로젝트 - 이미지 분류 신경망",
        "english_name": "Tier 3 Integration Project - Image Classification Neural Network",
        "description": "CNN, RNN, Transformer를 활용한 다중 이미지 분류",
        "modules": list(range(31, 51)),
        "objectives": [
            "신경망 설계 및 학습",
            "CNN 아키텍처 이해",
            "시계열 데이터 처리",
            "Transformer 활용"
        ],
        "project_tasks": [
            "기본 신경망 구현 (NumPy에서)",
            "CNN을 이용한 이미지 분류",
            "전이학습을 이용한 성능 개선",
            "앙상블 딥러닝 모델 구축"
        ]
    },
    "Tier4": {
        "name": "NLP 프로젝트 - 감정 분석 및 텍스트 분류",
        "english_name": "Tier 4 Integration Project - Sentiment Analysis & Text Classification",
        "description": "단어 임베딩, Seq2Seq, BERT를 이용한 감정 분석",
        "modules": list(range(51, 66)),
        "objectives": [
            "텍스트 전처리",
            "단어 임베딩 활용",
            "Transformer 기반 모델 사용",
            "언어 모델 미세조정"
        ],
        "project_tasks": [
            "텍스트 데이터 전처리 및 토큰화",
            "Word2Vec 임베딩 학습",
            "사전학습 모델 미세조정",
            "감정 분류 모델 평가"
        ]
    },
    "Tier5": {
        "name": "컴퓨터 비전 프로젝트 - 객체 탐지 시스템",
        "english_name": "Tier 5 Integration Project - Object Detection System",
        "description": "YOLO, R-CNN, 분할을 이용한 객체 탐지",
        "modules": list(range(66, 81)),
        "objectives": [
            "이미지 처리 기초",
            "객체 탐지 알고리즘",
            "이미지 분할",
            "얼굴/자세 인식"
        ],
        "project_tasks": [
            "이미지 특성 검출",
            "YOLO를 이용한 실시간 객체 탐지",
            "인스턴스 분할 구현",
            "얼굴 인식 시스템 구축"
        ]
    },
    "Tier6": {
        "name": "강화학습 프로젝트 - 게임 AI 구축",
        "english_name": "Tier 6 Integration Project - Game AI Development",
        "description": "Q-Learning, DQN, Policy Gradient를 이용한 게임 AI",
        "modules": list(range(81, 91)),
        "objectives": [
            "RL 기초 개념",
            "Q-Learning 구현",
            "심층 강화학습",
            "정책 경사 방법"
        ],
        "project_tasks": [
            "간단한 게임에서 Q-Learning 구현",
            "DQN으로 복잡한 게임 학습",
            "Policy Gradient 방법 비교",
            "멀티 에이전트 강화학습"
        ]
    },
    "Tier7": {
        "name": "생성 AI 프로젝트 - 텍스트 및 이미지 생성",
        "english_name": "Tier 7 Integration Project - Generative AI (Text & Image)",
        "description": "GAN, VAE, Diffusion을 이용한 생성 모델",
        "modules": list(range(91, 101)),
        "objectives": [
            "생성 모델 이해",
            "GAN 학습",
            "VAE 구현",
            "확산 모델 활용"
        ],
        "project_tasks": [
            "기본 GAN 구현 및 학습",
            "조건부 GAN으로 제어 가능한 생성",
            "VAE를 이용한 이미지 변형",
            "확산 모델로 텍스트 기반 이미지 생성"
        ]
    }
}

def create_tier_project(tier_name, project_info):
    """Tier 프로젝트 생성"""
    base_path = Path("/home/user/education-ai-ml")
    project_path = base_path / f"tier_projects" / tier_name

    # 디렉토리 생성
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / "notebooks").mkdir(exist_ok=True)
    (project_path / "scripts").mkdir(exist_ok=True)
    (project_path / "data").mkdir(exist_ok=True)
    (project_path / "results").mkdir(exist_ok=True)

    # README 생성
    readme_content = f"""# {project_info['name']}
## {project_info['english_name']}

### 📚 프로젝트 개요 (Overview)

{project_info['description']}

### 🎯 학습 목표 (Learning Objectives)

{chr(10).join(f"- {obj}" for obj in project_info['objectives'])}

### 📋 포함된 모듈 (Included Modules)

Modules: {', '.join(str(m) for m in project_info['modules'])}

### 🔨 프로젝트 작업 (Project Tasks)

{chr(10).join(f"{i+1}. {task}" for i, task in enumerate(project_info['project_tasks']))}

### 📂 디렉토리 구조 (Directory Structure)

```
{tier_name}/
├── README.md                 # 프로젝트 설명
├── notebooks/                # Jupyter 노트북
├── scripts/                  # Python 스크립트
├── data/                     # 데이터셋
└── results/                  # 결과 및 모델
```

### 🚀 시작하기 (Getting Started)

1. 필수 모듈 학습 완료
2. 데이터셋 준비
3. 프로젝트 작업 진행
4. 결과 평가

### 📖 학습 시간 (Estimated Time)

- 전체 모듈 학습: 40-60시간
- 프로젝트 완성: 10-15시간
- **총 소요 시간: 50-75시간**

---

**Happy Learning!** 🚀
"""

    readme_path = project_path / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    # 프로젝트 메타데이터
    metadata = {
        "tier": tier_name,
        "name": project_info['name'],
        "english_name": project_info['english_name'],
        "description": project_info['description'],
        "modules": project_info['modules'],
        "n_modules": len(project_info['modules']),
        "objectives": project_info['objectives'],
        "tasks": project_info['project_tasks'],
        "created_at": datetime.now().isoformat(),
        "status": "in_progress",
        "progress": 0
    }

    metadata_path = project_path / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # 체크리스트 생성
    checklist = {
        "tier": tier_name,
        "created_at": datetime.now().isoformat(),
        "tasks": [
            {
                "id": i+1,
                "description": task,
                "completed": False,
                "subtasks": []
            }
            for i, task in enumerate(project_info['project_tasks'])
        ]
    }

    checklist_path = project_path / "checklist.json"
    with open(checklist_path, 'w', encoding='utf-8') as f:
        json.dump(checklist, f, ensure_ascii=False, indent=2)

    return True

def main():
    print("="*80)
    print("🚀 Tier별 통합 프로젝트 생성 중...")
    print("="*80)

    for tier_name, project_info in TIER_PROJECTS.items():
        if create_tier_project(tier_name, project_info):
            print(f"  ✅ {tier_name}: {project_info['name']}")

    print("\n" + "="*80)
    print("✨ Tier 프로젝트 생성 완료!")
    print("="*80)
    print("\n📊 생성된 프로젝트:")
    print(f"  - 7개 Tier별 통합 프로젝트")
    print(f"  - 각 프로젝트의 README, 메타데이터, 체크리스트")
    print(f"\n🎯 다음 단계:")
    print(f"  1. 각 프로젝트의 노트북 및 스크립트 구현")
    print(f"  2. 평가 시스템 자동화")
    print(f"  3. GitHub에 푸시")

if __name__ == "__main__":
    main()
