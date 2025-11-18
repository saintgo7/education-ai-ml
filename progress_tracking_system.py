#!/usr/bin/env python3
"""
학습자 진도 추적 시스템
Learner Progress Tracking System
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

class ProgressTracker:
    """학습 진도 추적"""

    def __init__(self, learner_id: str):
        self.learner_id = learner_id
        self.created_at = datetime.now().isoformat()
        self.progress = {
            "learner_id": learner_id,
            "created_at": self.created_at,
            "modules_completed": [],
            "modules_in_progress": [],
            "exercises_completed": {},
            "projects_completed": [],
            "total_hours": 0,
            "streak_days": 0,
            "badges": [],
            "level": 1
        }

    def update_module_progress(self, module_id: int, status: str) -> None:
        """모듈 진도 업데이트"""
        if status == "completed":
            if module_id not in self.progress["modules_completed"]:
                self.progress["modules_completed"].append(module_id)
            if module_id in self.progress["modules_in_progress"]:
                self.progress["modules_in_progress"].remove(module_id)
        elif status == "in_progress":
            if module_id not in self.progress["modules_in_progress"]:
                self.progress["modules_in_progress"].append(module_id)

    def update_exercise_score(self, module_id: int, score: float) -> None:
        """연습 문제 점수 업데이트"""
        self.progress["exercises_completed"][str(module_id)] = {
            "score": score,
            "timestamp": datetime.now().isoformat(),
            "status": "completed" if score >= 70 else "needs_review"
        }

    def add_hours(self, hours: float) -> None:
        """학습 시간 추가"""
        self.progress["total_hours"] += hours

    def complete_project(self, project_name: str) -> None:
        """프로젝트 완료"""
        self.progress["projects_completed"].append({
            "name": project_name,
            "completed_at": datetime.now().isoformat()
        })

    def update_level(self) -> None:
        """레벨 업데이트"""
        modules_completed = len(self.progress["modules_completed"])
        if modules_completed >= 50:
            self.progress["level"] = 3  # 고급
        elif modules_completed >= 25:
            self.progress["level"] = 2  # 중급
        else:
            self.progress["level"] = 1  # 초급

    def check_badges(self) -> List[str]:
        """배지 확인 및 추가"""
        new_badges = []

        # 모듈 완료 배지
        completed = len(self.progress["modules_completed"])
        if completed == 10 and "first_10" not in self.progress["badges"]:
            new_badges.append("first_10")
        if completed == 25 and "quarter_complete" not in self.progress["badges"]:
            new_badges.append("quarter_complete")
        if completed == 50 and "halfway" not in self.progress["badges"]:
            new_badges.append("halfway")
        if completed == 100 and "master" not in self.progress["badges"]:
            new_badges.append("master")

        # 프로젝트 완료 배지
        projects = len(self.progress["projects_completed"])
        if projects >= 3 and "project_master" not in self.progress["badges"]:
            new_badges.append("project_master")

        # 연속 학습 배지
        if self.progress["streak_days"] >= 7 and "one_week_streak" not in self.progress["badges"]:
            new_badges.append("one_week_streak")

        self.progress["badges"].extend(new_badges)
        return new_badges

    def get_summary(self) -> Dict[str, Any]:
        """진도 요약"""
        completed = len(self.progress["modules_completed"])
        in_progress = len(self.progress["modules_in_progress"])
        exercises_done = len(self.progress["exercises_completed"])

        avg_exercise_score = 0
        if exercises_done > 0:
            scores = [s["score"] for s in self.progress["exercises_completed"].values()]
            avg_exercise_score = sum(scores) / len(scores)

        return {
            "learner_id": self.learner_id,
            "level": self.progress["level"],
            "modules_completed": completed,
            "modules_in_progress": in_progress,
            "total_modules": 100,
            "completion_percentage": (completed / 100) * 100,
            "exercises_completed": exercises_done,
            "average_exercise_score": avg_exercise_score,
            "projects_completed": len(self.progress["projects_completed"]),
            "total_hours": self.progress["total_hours"],
            "badges": self.progress["badges"],
            "next_milestone": self._get_next_milestone(completed)
        }

    def _get_next_milestone(self, completed: int) -> Dict[str, Any]:
        """다음 마일스톤 계산"""
        milestones = [10, 25, 50, 100]
        for milestone in milestones:
            if completed < milestone:
                return {
                    "milestone": milestone,
                    "remaining": milestone - completed,
                    "badge": self._milestone_to_badge(milestone)
                }
        return {
            "milestone": 100,
            "remaining": 0,
            "badge": "master",
            "message": "모든 모듈을 완료했습니다!"
        }

    @staticmethod
    def _milestone_to_badge(milestone: int) -> str:
        """마일스톤을 배지로 변환"""
        mapping = {10: "first_10", 25: "quarter_complete", 50: "halfway", 100: "master"}
        return mapping.get(milestone, "unknown")

def create_sample_learners():
    """샘플 학습자 생성"""
    learners = {}

    # 초급 학습자
    learner1 = ProgressTracker("learner_001")
    learner1.progress["modules_completed"] = list(range(1, 6))  # 5개 완료
    learner1.progress["modules_in_progress"] = [6, 7]
    learner1.add_hours(15)
    for i in range(1, 6):
        learner1.update_exercise_score(i, 85)
    learners["learner_001"] = learner1

    # 중급 학습자
    learner2 = ProgressTracker("learner_002")
    learner2.progress["modules_completed"] = list(range(1, 26))  # 25개 완료
    learner2.progress["modules_in_progress"] = [26, 27, 28]
    learner2.add_hours(75)
    for i in range(1, 26):
        learner2.update_exercise_score(i, 80 + (i % 20))
    learner2.complete_project("Tier1")
    learners["learner_002"] = learner2

    # 고급 학습자
    learner3 = ProgressTracker("learner_003")
    learner3.progress["modules_completed"] = list(range(1, 51))  # 50개 완료
    learner3.progress["modules_in_progress"] = [51, 52]
    learner3.add_hours(150)
    for i in range(1, 51):
        learner3.update_exercise_score(i, 88)
    learner3.complete_project("Tier1")
    learner3.complete_project("Tier2")
    learner3.complete_project("Tier3")
    learners["learner_003"] = learner3

    return learners

def generate_leaderboard(learners: Dict[str, ProgressTracker]) -> List[Dict]:
    """리더보드 생성"""
    leaderboard = []

    for learner_id, tracker in learners.items():
        summary = tracker.get_summary()
        leaderboard.append({
            "rank": 0,  # 나중에 채워짐
            "learner_id": learner_id,
            "level": summary["level"],
            "modules_completed": summary["modules_completed"],
            "badges": len(summary["badges"]),
            "hours": summary["total_hours"],
            "completion_percentage": summary["completion_percentage"]
        })

    # 순위 정렬
    leaderboard.sort(key=lambda x: x["completion_percentage"], reverse=True)
    for i, entry in enumerate(leaderboard, 1):
        entry["rank"] = i

    return leaderboard

def main():
    print("="*80)
    print("🚀 학습자 진도 추적 시스템")
    print("="*80)

    # 샘플 학습자 생성
    learners = create_sample_learners()

    # 각 학습자의 진도 요약
    print("\n📊 학습자별 진도:")
    print("-"*80)

    for learner_id, tracker in learners.items():
        summary = tracker.get_summary()
        tracker.update_level()
        tracker.check_badges()

        print(f"\n🎓 {learner_id}")
        print(f"  레벨: {'⭐' * summary['level']}")
        print(f"  모듈 진도: {summary['modules_completed']}/{summary['total_modules']} ({summary['completion_percentage']:.1f}%)")
        print(f"  연습 문제: {summary['exercises_completed']}개 (평균 점수: {summary['average_exercise_score']:.1f}/100)")
        print(f"  완료 프로젝트: {summary['projects_completed']}개")
        print(f"  총 학습 시간: {summary['total_hours']}시간")
        print(f"  배지: {len(summary['badges'])}개 - {', '.join(summary['badges'][:3])}")
        print(f"  다음 목표: {summary['next_milestone']['milestone']}개 모듈 (남은 개수: {summary['next_milestone']['remaining']})")

    # 리더보드
    print("\n\n" + "="*80)
    print("🏆 리더보드 (순위)")
    print("="*80)

    leaderboard = generate_leaderboard(learners)

    for entry in leaderboard:
        level_stars = "⭐" * entry["level"]
        print(f"{entry['rank']}위 | {entry['learner_id']:15s} | {level_stars:5s} | "
              f"모듈: {entry['modules_completed']:2d}/100 | "
              f"진도: {entry['completion_percentage']:5.1f}% | "
              f"배지: {entry['badges']}개 | "
              f"시간: {entry['hours']}h")

    # 진도 데이터 저장
    progress_dir = Path("/home/user/education-ai-ml") / "learner_data"
    progress_dir.mkdir(exist_ok=True)

    for learner_id, tracker in learners.items():
        progress_file = progress_dir / f"{learner_id}_progress.json"
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(tracker.progress, f, ensure_ascii=False, indent=2)

    # 리더보드 저장
    leaderboard_file = progress_dir / "leaderboard.json"
    with open(leaderboard_file, 'w', encoding='utf-8') as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)

    print("\n" + "="*80)
    print("✨ 진도 추적 완료!")
    print("="*80)
    print("\n📁 저장된 파일:")
    print(f"  - 학습자별 진도: learner_data/{{learner_id}}_progress.json")
    print(f"  - 리더보드: learner_data/leaderboard.json")
    print("\n🎯 기능:")
    print("  - ✅ 모듈별 진도 추적")
    print("  - ✅ 연습 문제 점수 기록")
    print("  - ✅ 프로젝트 완료 추적")
    print("  - ✅ 배지 시스템")
    print("  - ✅ 레벨 업그레이드")
    print("  - ✅ 리더보드 (순위)")
    print("  - ✅ 마일스톤 추적")

if __name__ == "__main__":
    main()
