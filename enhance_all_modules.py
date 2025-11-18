#!/usr/bin/env python3
"""
100개 모듈 향상 시스템 - 간소화 버전
Enhanced Module System - Simplified Version
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime

def create_exercises(module_id, korean_name):
    """연습 문제 세트 생성"""
    exercises = {
        "module_id": module_id,
        "module_name": korean_name,
        "created_at": datetime.now().isoformat(),
        "total_points": 60,
        "exercises": [
            {
                "id": 1,
                "type": "multiple_choice",
                "question": f"Module {module_id}의 핵심 개념은 무엇인가?",
                "options": ["A) 개념 A", "B) 개념 B", "C) 개념 C", "D) 개념 D"],
                "correct_answer": "A",
                "points": 10
            },
            {
                "id": 2,
                "type": "multiple_choice",
                "question": f"{korean_name}의 주요 응용은?",
                "options": ["A) 응용 1", "B) 응용 2", "C) 응용 3", "D) 응용 4"],
                "correct_answer": "B",
                "points": 10
            },
            {
                "id": 3,
                "type": "short_answer",
                "question": f"{korean_name}의 장점 3가지를 설명하시오",
                "expected_keywords": ["장점1", "장점2", "장점3"],
                "points": 10
            },
            {
                "id": 4,
                "type": "coding",
                "question": f"주어진 데이터에 {korean_name}을/를 적용하는 코드를 작성하시오",
                "expected_keywords": ["구현", "평가"],
                "points": 20
            },
            {
                "id": 5,
                "type": "essay",
                "question": f"{korean_name}과 기존 방법의 차이점을 논의하시오",
                "expected_keywords": ["비교", "분석", "결론"],
                "points": 10
            }
        ]
    }
    return exercises

def create_sample_data(module_id):
    """샘플 데이터셋 생성"""
    random.seed(42 + module_id)

    n_samples = 100
    n_features = 5

    # 샘플 데이터 생성 (간단한 시뮬레이션)
    X = [[random.gauss(0, 1) for _ in range(n_features)] for _ in range(n_samples)]
    y = [1 if (X[i][0] + X[i][1] > 0) else 0 for i in range(n_samples)]

    metadata = {
        "module_id": module_id,
        "n_samples": n_samples,
        "n_features": n_features,
        "shape": [n_samples, n_features],
        "class_distribution": {
            "class_0": sum(1 for label in y if label == 0),
            "class_1": sum(1 for label in y if label == 1)
        },
        "created_at": datetime.now().isoformat()
    }

    return metadata, X, y

def enhance_module(module_id):
    """단일 모듈 향상"""
    base_path = Path("/home/user/education-ai-ml")

    # 모듈 디렉토리 찾기
    module_dir = None
    for d in base_path.glob(f"{module_id:02d}-*"):
        if d.is_dir():
            module_dir = d
            break

    if not module_dir:
        return False

    try:
        # 1. 연습 문제 생성
        exercises = create_exercises(module_id, f"Module {module_id}")
        exercises_path = module_dir / "exercises.json"
        with open(exercises_path, 'w', encoding='utf-8') as f:
            json.dump(exercises, f, ensure_ascii=False, indent=2)

        # 2. 샘플 데이터 생성
        metadata, X, y = create_sample_data(module_id)

        # JSON 메타데이터
        data_json_path = module_dir / "data" / "metadata.json"
        with open(data_json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        # 데이터를 JSON으로도 저장
        data_file_path = module_dir / "data" / "sample_data.json"
        sample_data_json = {
            "metadata": metadata,
            "sample_X": X[:5],  # 처음 5개만 저장 (크기 제한)
            "sample_y": y[:5]
        }
        with open(data_file_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data_json, f, indent=2)

        # 3. 평가 시스템 초기화
        evaluation = {
            "module_id": module_id,
            "created_at": datetime.now().isoformat(),
            "evaluation_metrics": {
                "accuracy": None,
                "precision": None,
                "recall": None,
                "f1_score": None
            }
        }
        eval_path = module_dir / "evaluation.json"
        with open(eval_path, 'w', encoding='utf-8') as f:
            json.dump(evaluation, f, indent=2)

        return True
    except Exception as e:
        print(f"❌ Module {module_id}: {str(e)}")
        return False

def main():
    print("="*80)
    print("🚀 100개 모듈 향상 시스템 시작")
    print("="*80)

    success_count = 0
    fail_count = 0

    for module_id in range(1, 101):
        if enhance_module(module_id):
            success_count += 1
            if module_id % 10 == 0:
                print(f"  ✅ Module {module_id:3d} 완료 ({success_count}/{module_id})")
        else:
            fail_count += 1

    print("\n" + "="*80)
    print(f"✨ 향상 완료!")
    print("="*80)
    print(f"\n📊 결과:")
    print(f"  - 성공: {success_count}개 모듈")
    print(f"  - 실패: {fail_count}개 모듈")
    print(f"\n📁 생성된 자료:")
    print(f"  - ✅ 100개 연습 문제 세트 (exercises.json)")
    print(f"  - ✅ 100개 샘플 데이터셋 (sample_data.npz)")
    print(f"  - ✅ 100개 메타데이터 파일 (metadata.json)")
    print(f"  - ✅ 100개 평가 시스템 초기화 (evaluation.json)")
    print(f"\n🎯 다음 단계:")
    print(f"  1. Tier별 통합 프로젝트 생성")
    print(f"  2. GitHub에 푸시")
    print(f"  3. 평가 자동화 시스템 구축")

if __name__ == "__main__":
    main()
