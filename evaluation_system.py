#!/usr/bin/env python3
"""
자동 평가 시스템
Automated Evaluation System for 100 Modules
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class EvaluationSystem:
    """평가 시스템"""

    def __init__(self):
        self.base_path = Path("/home/user/education-ai-ml")
        self.results = []

    def load_exercises(self, module_id: int) -> Dict[str, Any]:
        """모듈의 연습 문제 로드"""
        module_dir = None
        for d in self.base_path.glob(f"{module_id:02d}-*"):
            if d.is_dir():
                module_dir = d
                break

        if not module_dir:
            return None

        exercises_path = module_dir / "exercises.json"
        if exercises_path.exists():
            with open(exercises_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def evaluate_module(self, module_id: int, answers: Dict[str, Any]) -> Dict[str, Any]:
        """모듈 평가"""
        exercises = self.load_exercises(module_id)
        if not exercises:
            return {"error": f"Module {module_id} exercises not found"}

        results = {
            "module_id": module_id,
            "timestamp": datetime.now().isoformat(),
            "total_questions": len(exercises.get("exercises", [])),
            "answered": len(answers),
            "correct": 0,
            "score": 0,
            "details": []
        }

        for exercise in exercises.get("exercises", []):
            ex_id = exercise.get("id")
            question_type = exercise.get("type")

            if ex_id not in answers:
                results["details"].append({
                    "exercise_id": ex_id,
                    "question": exercise.get("question"),
                    "type": question_type,
                    "status": "not_answered",
                    "points": 0
                })
                continue

            user_answer = answers[ex_id]

            if question_type == "multiple_choice":
                correct = user_answer == exercise.get("correct_answer")
                points = exercise.get("points", 10) if correct else 0

                results["correct"] += 1 if correct else 0
                results["score"] += points

                results["details"].append({
                    "exercise_id": ex_id,
                    "question": exercise.get("question"),
                    "type": question_type,
                    "status": "correct" if correct else "incorrect",
                    "user_answer": user_answer,
                    "correct_answer": exercise.get("correct_answer"),
                    "points": points,
                    "max_points": exercise.get("points", 10)
                })

            elif question_type == "short_answer":
                keywords = exercise.get("expected_keywords", [])
                found_keywords = sum(1 for kw in keywords if kw.lower() in str(user_answer).lower())
                points = exercise.get("points", 10) * (found_keywords / len(keywords)) if keywords else 0

                results["correct"] += 1 if found_keywords > 0 else 0
                results["score"] += int(points)

                results["details"].append({
                    "exercise_id": ex_id,
                    "question": exercise.get("question"),
                    "type": question_type,
                    "status": "partial" if found_keywords > 0 else "incorrect",
                    "user_answer": user_answer[:100] + "..." if len(str(user_answer)) > 100 else user_answer,
                    "keywords_found": found_keywords,
                    "total_keywords": len(keywords),
                    "points": int(points),
                    "max_points": exercise.get("points", 10)
                })

            elif question_type in ["coding", "essay"]:
                # 자유 응답 문제는 수동 채점이 필요
                results["details"].append({
                    "exercise_id": ex_id,
                    "question": exercise.get("question"),
                    "type": question_type,
                    "status": "pending_review",
                    "user_answer": user_answer[:100] + "..." if len(str(user_answer)) > 100 else user_answer,
                    "max_points": exercise.get("points", 20),
                    "note": "Manual grading required"
                })

        # 정확도 계산
        results["accuracy"] = (results["correct"] / results["total_questions"]) * 100 if results["total_questions"] > 0 else 0
        results["max_score"] = exercises.get("total_points", 100)
        results["percentage"] = (results["score"] / results["max_score"]) * 100 if results["max_score"] > 0 else 0

        return results

    def generate_report(self, results: Dict[str, Any]) -> str:
        """평가 결과 리포트 생성"""
        report = f"""
{'='*80}
Module {results['module_id']} - 평가 결과 (Evaluation Report)
{'='*80}

📊 요약 (Summary):
  - 총 문제: {results['total_questions']}개
  - 답변한 문제: {results['answered']}개
  - 정답: {results['correct']}개
  - 정확도: {results['accuracy']:.1f}%
  - 점수: {results['score']}/{results['max_score']} ({results['percentage']:.1f}%)

📋 상세 결과 (Details):
"""

        for detail in results['details']:
            status = detail['status']
            ex_id = detail['exercise_id']

            if status == "correct":
                status_icon = "✅"
            elif status == "incorrect":
                status_icon = "❌"
            elif status == "partial":
                status_icon = "⚠️"
            elif status == "pending_review":
                status_icon = "📝"
            else:
                status_icon = "⭕"

            report += f"\n{status_icon} 문제 {ex_id}: {detail['question'][:50]}...\n"
            report += f"   타입: {detail['type']}\n"
            report += f"   상태: {status}\n"

            if 'points' in detail:
                report += f"   점수: {detail['points']}/{detail.get('max_points', 10)}\n"

        report += f"\n{'='*80}\n"
        return report

    def save_results(self, module_id: int, results: Dict[str, Any]):
        """결과 저장"""
        module_dir = None
        for d in self.base_path.glob(f"{module_id:02d}-*"):
            if d.is_dir():
                module_dir = d
                break

        if module_dir:
            results_path = module_dir / "evaluation_results.json"
            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

    def evaluate_all_modules(self) -> Dict[str, Any]:
        """모든 모듈 평가"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_modules": 100,
            "evaluated": 0,
            "average_score": 0,
            "module_results": []
        }

        total_score = 0

        for module_id in range(1, 101):
            # 더미 답변 생성 (실제로는 사용자 입력)
            dummy_answers = {}
            exercises = self.load_exercises(module_id)
            if exercises:
                for exercise in exercises.get("exercises", []):
                    ex_id = exercise.get("id")
                    if exercise.get("type") == "multiple_choice":
                        dummy_answers[ex_id] = exercise.get("correct_answer")
                    else:
                        dummy_answers[ex_id] = "Sample answer"

                results = self.evaluate_module(module_id, dummy_answers)
                self.save_results(module_id, results)
                summary["module_results"].append({
                    "module_id": module_id,
                    "score": results.get("score"),
                    "max_score": results.get("max_score"),
                    "percentage": results.get("percentage")
                })
                total_score += results.get("percentage", 0)
                summary["evaluated"] += 1

        summary["average_score"] = total_score / summary["evaluated"] if summary["evaluated"] > 0 else 0

        return summary

def main():
    print("="*80)
    print("🚀 자동 평가 시스템 실행 중...")
    print("="*80)

    evaluator = EvaluationSystem()

    # 샘플: Module 1 평가
    print("\n📝 Module 1 평가 예제:")
    sample_answers = {
        1: "A",
        2: "B",
        3: "장점 설명",
        4: "구현 코드",
        5: "비교 분석"
    }

    results = evaluator.evaluate_module(1, sample_answers)
    evaluator.save_results(1, results)

    report = evaluator.generate_report(results)
    print(report)

    # 전체 모듈 평가
    print("\n⏳ 전체 모듈 평가 중... (처음 10개만)")
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_modules": 100,
        "evaluated": 10,
        "sample_scores": []
    }

    for module_id in range(1, 11):
        dummy_answers = {}
        exercises = evaluator.load_exercises(module_id)
        if exercises:
            for exercise in exercises.get("exercises", []):
                ex_id = exercise.get("id")
                if exercise.get("type") == "multiple_choice":
                    dummy_answers[ex_id] = exercise.get("correct_answer")
                else:
                    dummy_answers[ex_id] = "Sample answer"

            results = evaluator.evaluate_module(module_id, dummy_answers)
            evaluator.save_results(module_id, results)
            summary["sample_scores"].append({
                "module_id": module_id,
                "percentage": results.get("percentage", 0)
            })

    # 요약 저장
    summary_path = Path("/home/user/education-ai-ml") / "evaluation_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n" + "="*80)
    print("✨ 평가 완료!")
    print("="*80)
    print("\n📊 평가 시스템 기능:")
    print("  - ✅ 객관식 자동 채점")
    print("  - ✅ 단답형 키워드 매칭")
    print("  - ✅ 서술형/코딩 문제 검토 대기")
    print("  - ✅ 상세 결과 리포트 생성")
    print("  - ✅ JSON 형식 결과 저장")
    print("\n🎯 평가 결과:")
    print(f"  - 평가된 모듈: {summary['evaluated']}/100")
    print(f"  - 평균 점수: {sum(s['percentage'] for s in summary['sample_scores'])/len(summary['sample_scores']):.1f}%")

if __name__ == "__main__":
    main()
