#!/usr/bin/env python3
"""
AI 튜터 시스템 - 자동 피드백 및 개인화 추천
AI Tutor System - Automated Feedback & Personalized Recommendations
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class AITutor:
    """AI 튜터"""

    def __init__(self):
        self.feedback_templates = self._init_feedback_templates()

    def _init_feedback_templates(self) -> Dict[str, str]:
        """피드백 템플릿 초기화"""
        return {
            "excellent": "뛰어난 성과입니다! 📊 핵심 개념을 완벽하게 이해했습니다. 다음 단계로 진행하세요.",
            "good": "좋은 성과입니다! 📈 대부분의 개념을 잘 이해했습니다. 약간의 복습이 도움될 수 있습니다.",
            "fair": "평범한 성과입니다. 📚 일부 개념에 대해 더 공부가 필요합니다. 복습 자료를 참고하세요.",
            "poor": "더 노력이 필요합니다. 💪 기본 개념부터 다시 학습하는 것을 추천합니다.",
            "incomplete": "작업을 완료하지 못했습니다. ⏳ 시간을 가지고 다시 시도해보세요."
        }

    def generate_feedback(self, module_id: int, score: float, answers: List[Dict]) -> Dict[str, Any]:
        """피드백 생성"""

        # 성과 평가
        if score >= 90:
            rating = "excellent"
        elif score >= 80:
            rating = "good"
        elif score >= 70:
            rating = "fair"
        elif score >= 50:
            rating = "poor"
        else:
            rating = "incomplete"

        # 오류 분석
        errors = self._analyze_errors(answers)

        # 개선 권고
        recommendations = self._generate_recommendations(module_id, score, errors)

        feedback = {
            "module_id": module_id,
            "timestamp": datetime.now().isoformat(),
            "overall_score": score,
            "rating": rating,
            "feedback": self.feedback_templates[rating],
            "errors_found": errors,
            "recommendations": recommendations,
            "next_steps": self._get_next_steps(module_id, score)
        }

        return feedback

    def _analyze_errors(self, answers: List[Dict]) -> List[Dict]:
        """오류 분석"""
        errors = []

        for i, answer in enumerate(answers):
            if answer.get("correct") == False:
                error_type = "wrong_answer"
                if answer.get("type") == "short_answer" and answer.get("keywords_found", 0) > 0:
                    error_type = "partial_answer"

                errors.append({
                    "question_id": i + 1,
                    "type": error_type,
                    "explanation": f"질문 {i+1}에서 개선이 필요합니다.",
                    "suggestion": "관련 개념을 다시 학습하는 것을 추천합니다."
                })

        return errors

    def _generate_recommendations(self, module_id: int, score: float, errors: List[Dict]) -> List[str]:
        """추천 생성"""
        recommendations = []

        # 점수 기반 추천
        if score < 70:
            recommendations.append(f"📚 Module {module_id}의 기본 개념을 다시 학습하세요.")
            recommendations.append("🔄 이전 모듈의 관련 내용을 복습하는 것을 추천합니다.")
        elif score < 80:
            recommendations.append(f"📖 Module {module_id}의 심화 자료를 살펴보세요.")
            recommendations.append("💡 개념을 더 깊이 있게 이해하기 위해 예제를 분석해보세요.")
        else:
            recommendations.append(f"🚀 다음 모듈로 진행해도 좋습니다.")
            recommendations.append("⭐ 고급 개념 학습에 도전해보세요.")

        # 오류 기반 추천
        if len(errors) > 3:
            recommendations.append("⚠️ 많은 오류가 발견되었습니다. 더 체계적인 학습을 추천합니다.")

        # 개별화 추천
        if module_id % 10 == 0:  # 10단위 마일스톤
            recommendations.append(f"🎯 Tier {(module_id-1)//10 + 1} 프로젝트를 시작할 준비가 되어 있습니다!")

        return recommendations

    def _get_next_steps(self, module_id: int, score: float) -> List[str]:
        """다음 단계"""
        next_steps = []

        if score >= 80:
            next_steps.append(f"다음 모듈: Module {module_id + 1}")
        else:
            next_steps.append(f"복습: Module {module_id} 반복 학습")

        # 현재 Tier 기반
        tier = (module_id - 1) // 10 + 1
        modules_in_tier = (module_id - 1) % 10 + 1

        if modules_in_tier == 10:
            next_steps.append(f"Tier {tier} 프로젝트 시작")

        next_steps.append("💬 질문이 있으시면 커뮤니티에 작성하세요.")

        return next_steps

class PersonalizedRecommendationEngine:
    """개인화 추천 엔진"""

    def __init__(self):
        self.learning_styles = {
            "visual": ["시각적 자료", "다이어그램", "그래프"],
            "auditory": ["비디오 튜토리얼", "음성 설명"],
            "kinesthetic": ["실습 프로젝트", "코드 작성"]
        }

    def analyze_learner_profile(self, progress_data: Dict) -> Dict[str, Any]:
        """학습자 프로필 분석"""

        modules_completed = progress_data.get("modules_completed", [])
        exercises = progress_data.get("exercises_completed", {})

        # 학습 속도 계산
        if len(modules_completed) > 0:
            avg_score = sum(e.get("score", 0) for e in exercises.values()) / len(exercises)
        else:
            avg_score = 0

        # 학습 스타일 추론
        learning_style = self._infer_learning_style(progress_data)

        # 강점과 약점
        strengths, weaknesses = self._identify_strengths_weaknesses(exercises)

        profile = {
            "total_modules": len(modules_completed),
            "average_score": avg_score,
            "learning_style": learning_style,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommended_approach": self._get_recommended_approach(learning_style),
            "speed": self._calculate_learning_speed(modules_completed)
        }

        return profile

    def _infer_learning_style(self, progress_data: Dict) -> str:
        """학습 스타일 추론"""
        # 간단한 휴리스틱 (실제로는 더 복잡한 분석 필요)
        modules = progress_data.get("modules_completed", [])

        if len(modules) > 50:
            return "kinesthetic"  # 많은 모듈을 완료했으면 실습형
        elif len(modules) > 25:
            return "visual"  # 중간 진도면 시각형
        else:
            return "auditory"  # 초기 학습자

    def _identify_strengths_weaknesses(self, exercises: Dict) -> tuple:
        """강점과 약점 파악"""
        strengths = []
        weaknesses = []

        if exercises:
            avg_score = sum(e.get("score", 0) for e in exercises.values()) / len(exercises)

            for module_id, result in list(exercises.items())[:5]:  # 최근 5개
                score = result.get("score", 0)
                if score >= 85:
                    strengths.append(f"Module {module_id}: 우수한 성과")
                elif score < 70:
                    weaknesses.append(f"Module {module_id}: 복습 필요")

        return strengths, weaknesses

    def _get_recommended_approach(self, learning_style: str) -> List[str]:
        """추천 학습 방식"""
        recommendations = {
            "visual": [
                "📊 시각적 다이어그램을 활용한 학습",
                "🎬 비디오 튜토리얼 시청",
                "📈 그래프와 차트를 통한 이해"
            ],
            "auditory": [
                "🎧 비디오 강의 청취",
                "💬 그룹 스터디 참여",
                "🗣️ 개념을 말로 설명해보기"
            ],
            "kinesthetic": [
                "💻 코드 작성 연습",
                "🔨 실습 프로젝트 진행",
                "🏆 도전 과제 해결"
            ]
        }
        return recommendations.get(learning_style, [])

    def _calculate_learning_speed(self, modules_completed: List) -> str:
        """학습 속도 계산"""
        if len(modules_completed) > 50:
            return "fast"
        elif len(modules_completed) > 25:
            return "moderate"
        else:
            return "slow"

    def generate_personalized_plan(self, profile: Dict) -> Dict[str, Any]:
        """개인화 학습 계획 생성"""

        total_modules = profile["total_modules"]
        speed = profile["speed"]
        learning_style = profile["learning_style"]

        if speed == "fast":
            weekly_modules = 4
        elif speed == "moderate":
            weekly_modules = 2
        else:
            weekly_modules = 1

        plan = {
            "learner_type": learning_style,
            "estimated_weeks_to_completion": (100 - total_modules) / weekly_modules,
            "weekly_modules": weekly_modules,
            "weekly_hours": weekly_modules * 3,
            "recommended_resources": self.learning_styles.get(learning_style, []),
            "focus_areas": profile["weaknesses"],
            "quick_wins": profile["strengths"],
            "milestone_goals": self._generate_milestones(total_modules)
        }

        return plan

    def _generate_milestones(self, current: int) -> List[Dict]:
        """마일스톤 생성"""
        milestones = [
            {"target": 25, "label": "Beginner", "reward": "Bronze Badge"},
            {"target": 50, "label": "Intermediate", "reward": "Silver Badge"},
            {"target": 75, "label": "Advanced", "reward": "Gold Badge"},
            {"target": 100, "label": "Master", "reward": "Master Badge"}
        ]

        active_milestones = [m for m in milestones if m["target"] > current]
        return active_milestones

def main():
    print("="*80)
    print("🚀 AI 튜터 시스템")
    print("="*80)

    # AI 튜터 초기화
    tutor = AITutor()
    recommendation_engine = PersonalizedRecommendationEngine()

    # 샘플 응답
    sample_answers = [
        {"id": 1, "correct": True, "type": "multiple_choice"},
        {"id": 2, "correct": True, "type": "multiple_choice"},
        {"id": 3, "correct": False, "type": "short_answer", "keywords_found": 1},
        {"id": 4, "correct": False, "type": "coding"},
        {"id": 5, "correct": True, "type": "essay"}
    ]

    # 피드백 생성
    print("\n📝 Module 15 피드백 생성")
    print("-"*80)

    feedback = tutor.generate_feedback(15, 75, sample_answers)

    print(f"\n📊 점수: {feedback['overall_score']}/100")
    print(f"🎯 평가: {feedback['rating']}")
    print(f"💬 피드백: {feedback['feedback']}")

    if feedback["errors_found"]:
        print(f"\n⚠️ 발견된 오류:")
        for error in feedback["errors_found"]:
            print(f"  - {error['explanation']}")
            print(f"    💡 {error['suggestion']}")

    print(f"\n✅ 추천 사항:")
    for i, rec in enumerate(feedback["recommendations"], 1):
        print(f"  {i}. {rec}")

    print(f"\n🚀 다음 단계:")
    for step in feedback["next_steps"]:
        print(f"  - {step}")

    # 개인화 추천
    print("\n\n" + "="*80)
    print("🎓 개인화 학습 계획")
    print("-"*80)

    learner_progress = {
        "modules_completed": list(range(1, 31)),
        "exercises_completed": {
            str(i): {"score": 75 + (i % 20)} for i in range(1, 31)
        }
    }

    profile = recommendation_engine.analyze_learner_profile(learner_progress)
    plan = recommendation_engine.generate_personalized_plan(profile)

    print(f"\n📊 학습자 프로필:")
    print(f"  진도: {profile['total_modules']}/100개 모듈")
    print(f"  평균 점수: {profile['average_score']:.1f}/100")
    print(f"  학습 스타일: {profile['learning_style']}")
    print(f"  학습 속도: {profile['speed']}")

    print(f"\n📈 개인화 학습 계획:")
    print(f"  주간 학습 모듈: {plan['weekly_modules']}개")
    print(f"  주간 학습 시간: {plan['weekly_hours']}시간")
    print(f"  완료 예상 기간: {plan['estimated_weeks_to_completion']:.1f}주")

    print(f"\n📚 추천 자료:")
    for resource in plan["recommended_resources"]:
        print(f"  - {resource}")

    print(f"\n🎯 다음 마일스톤:")
    for milestone in plan["milestone_goals"][:2]:
        print(f"  - {milestone['target']}개 모듈 완료: {milestone['label']} ({milestone['reward']})")

    # 데이터 저장
    tutor_dir = Path("/home/user/education-ai-ml") / "ai_tutor_data"
    tutor_dir.mkdir(exist_ok=True)

    with open(tutor_dir / "sample_feedback.json", 'w', encoding='utf-8') as f:
        json.dump(feedback, f, ensure_ascii=False, indent=2)

    with open(tutor_dir / "sample_profile.json", 'w', encoding='utf-8') as f:
        json.dump({"profile": profile, "plan": plan}, f, ensure_ascii=False, indent=2)

    print("\n" + "="*80)
    print("✨ AI 튜터 시스템 완료!")
    print("="*80)
    print("\n🎯 기능:")
    print("  - ✅ 자동 피드백 생성")
    print("  - ✅ 오류 분석 및 진단")
    print("  - ✅ 학습자 프로필 분석")
    print("  - ✅ 개인화 학습 계획")
    print("  - ✅ 학습 스타일 추론")
    print("  - ✅ 마일스톤 추적")

if __name__ == "__main__":
    main()
