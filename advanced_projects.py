#!/usr/bin/env python3
"""
고급 및 크로스-Tier 프로젝트 템플릿
Advanced & Cross-Tier Integration Projects
"""

import json
from pathlib import Path
from datetime import datetime

ADVANCED_PROJECTS = {
    "capstone_data_science": {
        "name": "종합 데이터 과학 프로젝트 (Capstone)",
        "description": "Tier 1-2의 모든 기술을 활용한 실제 데이터 분석 프로젝트",
        "required_modules": list(range(1, 31)),
        "duration_weeks": 6,
        "difficulty": "Advanced",
        "objectives": [
            "실제 데이터셋 분석 및 정제",
            "다양한 ML 알고리즘 적용",
            "모델 비교 및 평가",
            "결과 시각화 및 보고서 작성"
        ],
        "deliverables": [
            "데이터 분석 보고서",
            "Python 코드 및 노트북",
            "시각화 자료",
            "최종 프레젠테이션"
        ]
    },

    "cross_tier_ml_to_dl": {
        "name": "머신러닝에서 딥러닝으로의 여정",
        "description": "전통 ML에서 딥러닝으로 전환하는 과정을 학습하는 크로스-Tier 프로젝트",
        "required_modules": list(range(11, 51)),
        "duration_weeks": 8,
        "difficulty": "Advanced",
        "objectives": [
            "전통 ML과 DL의 장단점 비교",
            "동일 문제를 두 방식으로 해결",
            "성능 비교 및 분석",
            "결론 및 권장사항 도출"
        ],
        "project_stages": [
            "Stage 1: 데이터 준비 (Tier 2)",
            "Stage 2: 전통 ML 모델 구축 (Tier 2)",
            "Stage 3: DL 모델 구축 (Tier 3)",
            "Stage 4: 성능 비교 및 분석",
            "Stage 5: 보고서 작성"
        ]
    },

    "nlp_end_to_end": {
        "name": "NLP 엔드-투-엔드 프로젝트",
        "description": "텍스트 수집부터 배포까지 전체 NLP 파이프라인 구축",
        "required_modules": list(range(51, 66)),
        "duration_weeks": 6,
        "difficulty": "Advanced",
        "objectives": [
            "텍스트 데이터 수집 및 정제",
            "임베딩 생성 및 표현",
            "모델 학습 및 튜닝",
            "배포 준비"
        ],
        "sub_projects": [
            "감정 분석 모델",
            "텍스트 분류기",
            "개체명 인식 시스템",
            "텍스트 생성 모델"
        ]
    },

    "computer_vision_pipeline": {
        "name": "컴퓨터 비전 통합 파이프라인",
        "description": "이미지 처리부터 고급 검출까지 완전한 CV 파이프라인",
        "required_modules": list(range(66, 81)),
        "duration_weeks": 7,
        "difficulty": "Advanced",
        "objectives": [
            "이미지 데이터 처리",
            "객체 탐지 모델 구축",
            "이미지 분할 적용",
            "실시간 처리 구현"
        ],
        "components": [
            "이미지 전처리 파이프라인",
            "YOLO 기반 객체 탐지",
            "Mask R-CNN 기반 분할",
            "실시간 비디오 처리"
        ]
    },

    "reinforcement_learning_game": {
        "name": "강화학습 게임 AI 개발",
        "description": "RL을 이용한 게임 플레이 AI 개발",
        "required_modules": list(range(81, 91)),
        "duration_weeks": 5,
        "difficulty": "Advanced",
        "objectives": [
            "게임 환경 설정",
            "RL 에이전트 설계",
            "학습 및 최적화",
            "성능 평가"
        ],
        "games": [
            "Grid World",
            "CartPole",
            "Atari Games",
            "Custom Game"
        ]
    },

    "generative_ai_app": {
        "name": "생성 AI 애플리케이션 개발",
        "description": "생성 AI를 이용한 실제 애플리케이션 개발",
        "required_modules": list(range(91, 101)),
        "duration_weeks": 6,
        "difficulty": "Advanced",
        "objectives": [
            "생성 모델 이해 및 구현",
            "이미지 생성 애플리케이션",
            "텍스트 생성 애플리케이션",
            "배포 및 최적화"
        ],
        "applications": [
            "텍스트-이미지 생성",
            "이미지 인페인팅",
            "스타일 전이",
            "텍스트 생성 챗봇"
        ]
    }
}

CROSS_TIER_INTEGRATIONS = {
    "tier1_2_foundation": {
        "name": "Tier 1-2 기초 통합",
        "modules": list(range(1, 31)),
        "project_name": "완전한 ML 파이프라인",
        "description": "데이터 수집부터 배포까지 전체 ML 워크플로우",
        "timeline": "8주"
    },

    "tier2_3_transition": {
        "name": "Tier 2-3 전환",
        "modules": list(range(11, 51)),
        "project_name": "전통 ML vs 딥러닝",
        "description": "같은 문제를 두 가지 방법으로 해결",
        "timeline": "10주"
    },

    "tier3_4_nlp_specialist": {
        "name": "Tier 3-4 NLP 전문화",
        "modules": list(range(31, 66)),
        "project_name": "고급 NLP 애플리케이션",
        "description": "Transformer 기반 NLP 시스템 구축",
        "timeline": "12주"
    },

    "tier3_5_multimodal": {
        "name": "Tier 3-5 멀티모달",
        "modules": list(range(31, 81)),
        "project_name": "비전-언어 모델",
        "description": "이미지와 텍스트를 함께 처리하는 모델",
        "timeline": "12주"
    },

    "tier4_7_generative": {
        "name": "Tier 4-7 생성 AI",
        "modules": list(range(51, 101)),
        "project_name": "멀티모달 생성 시스템",
        "description": "텍스트와 이미지를 생성하는 통합 시스템",
        "timeline": "14주"
    }
}

def create_advanced_project_template(project_key, project_info):
    """고급 프로젝트 템플릿 생성"""

    project_dir = Path("/home/user/education-ai-ml") / "advanced_projects" / project_key
    project_dir.mkdir(parents=True, exist_ok=True)

    # 프로젝트 README
    readme = f"""# {project_info['name']}

## 프로젝트 개요

{project_info['description']}

## 필수 모듈

- 모듈 {project_info['required_modules'][0]}-{project_info['required_modules'][-1]} ({len(project_info['required_modules'])}개)

## 학습 목표

{chr(10).join(f"- {obj}" for obj in project_info['objectives'])}

## 프로젝트 구성

### 폴더 구조

```
{project_key}/
├── README.md                 # 프로젝트 설명
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_development.ipynb
│   ├── 03_evaluation.ipynb
│   └── 04_deployment.ipynb
├── scripts/
│   ├── data_pipeline.py
│   ├── model.py
│   ├── evaluate.py
│   └── deploy.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── models/
│   ├── checkpoints/
│   └── final_model.pkl
├── results/
│   ├── metrics.json
│   ├── visualizations/
│   └── report.md
└── requirements.txt
```

## 예상 소요 시간

- **총 기간**: {project_info['duration_weeks']}주
- **주당 시간**: 15-20시간
- **총 시간**: {project_info['duration_weeks'] * 18}시간

## 평가 기준

| 항목 | 배점 | 설명 |
|------|------|------|
| 데이터 분석 | 20점 | 데이터 이해 및 전처리 |
| 모델 개발 | 30점 | 알고리즘 구현 및 최적화 |
| 평가 | 20점 | 성능 지표 및 분석 |
| 문서화 | 15점 | 코드 및 보고서 품질 |
| 프레젠테이션 | 15점 | 최종 발표 및 설명 |

## 제출물

{chr(10).join(f"- {deliverable}" for deliverable in project_info.get('deliverables', []))}

## 리소스

- 튜토리얼: [튜토리얼 링크]
- 데이터셋: [데이터셋 링크]
- 참고 논문: [논문 링크]

## FAQ

### Q: 프로젝트 시작 시점은?
A: 모든 필수 모듈을 완료한 후 시작하세요.

### Q: 팀 프로젝트인가?
A: 개인 프로젝트이지만, 팀으로 진행할 수도 있습니다.

### Q: 피드백을 받을 수 있나?
A: 커뮤니티 포럼에서 피드백을 요청할 수 있습니다.

---

**Happy Learning!** 🚀
"""

    with open(project_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme)

    # 프로젝트 메타데이터
    metadata = {
        "project_key": project_key,
        "name": project_info['name'],
        "description": project_info['description'],
        "required_modules": project_info['required_modules'],
        "duration_weeks": project_info['duration_weeks'],
        "difficulty": project_info['difficulty'],
        "created_at": datetime.now().isoformat(),
        "status": "available",
        "objectives": project_info['objectives']
    }

    with open(project_dir / "metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # 체크리스트
    checklist = {
        "project": project_key,
        "created_at": datetime.now().isoformat(),
        "milestones": [
            {"week": 1, "task": "프로젝트 계획 및 데이터 수집", "completed": False},
            {"week": 2, "task": "데이터 탐색 및 분석", "completed": False},
            {"week": 3, "task": "모델 개발 (1단계)", "completed": False},
            {"week": 4, "task": "모델 개발 (2단계)", "completed": False},
            {"week": 5, "task": "모델 평가 및 최적화", "completed": False},
            {"week": 6, "task": "최종 보고서 및 배포", "completed": False}
        ]
    }

    with open(project_dir / "checklist.json", 'w', encoding='utf-8') as f:
        json.dump(checklist, f, ensure_ascii=False, indent=2)

    return True

def main():
    print("="*80)
    print("🚀 고급 프로젝트 및 크로스-Tier 통합 프로젝트 생성")
    print("="*80)

    # 고급 프로젝트 생성
    print("\n1️⃣ 고급 프로젝트 생성:")
    for project_key, project_info in ADVANCED_PROJECTS.items():
        if create_advanced_project_template(project_key, project_info):
            print(f"  ✅ {project_info['name']}")

    # 크로스-Tier 통합 프로젝트 메타데이터
    cross_tier_dir = Path("/home/user/education-ai-ml") / "cross_tier_projects"
    cross_tier_dir.mkdir(exist_ok=True)

    print("\n2️⃣ 크로스-Tier 통합 프로젝트 생성:")
    for key, info in CROSS_TIER_INTEGRATIONS.items():
        metadata = {
            "key": key,
            "name": info['name'],
            "modules": info['modules'],
            "project_name": info['project_name'],
            "description": info['description'],
            "timeline": info['timeline'],
            "created_at": datetime.now().isoformat()
        }

        with open(cross_tier_dir / f"{key}.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"  ✅ {info['name']}: {info['project_name']}")

    print("\n" + "="*80)
    print("✨ 프로젝트 생성 완료!")
    print("="*80)

    print("\n📊 생성된 프로젝트:")
    print(f"\n🎯 고급 프로젝트 ({len(ADVANCED_PROJECTS)}개):")
    for key, info in ADVANCED_PROJECTS.items():
        print(f"  - {info['name']} ({info['difficulty']} / {info['duration_weeks']}주)")

    print(f"\n🔗 크로스-Tier 프로젝트 ({len(CROSS_TIER_INTEGRATIONS)}개):")
    for key, info in CROSS_TIER_INTEGRATIONS.items():
        print(f"  - {info['name']}: {info['project_name']}")

    print("\n🎯 특징:")
    print("  - ✅ 완전한 프로젝트 템플릿")
    print("  - ✅ 상세한 README 및 가이드")
    print("  - ✅ 주간 마일스톤 및 체크리스트")
    print("  - ✅ 평가 기준 및 제출물 명시")
    print("  - ✅ 크로스-Tier 연계 학습")

if __name__ == "__main__":
    main()
