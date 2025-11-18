#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Education AI/ML Platform - FastAPI Backend Server
Comprehensive learning platform with 668+ projects
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from database import engine, SessionLocal, init_db
from models import User, Course, Module, Project, UserProgress, Enrollment
from schemas import (
    UserCreate, UserLogin, UserResponse, CourseResponse,
    ModuleResponse, ProjectResponse, UserProgressResponse, EnrollmentResponse
)
from auth import create_access_token, get_current_user, hash_password, verify_password
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Education AI/ML Platform",
    description="Comprehensive learning platform with 668+ projects across AI/ML and programming",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============== Health Check ==============
@app.get("/health")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "service": "Education AI/ML Platform",
        "timestamp": datetime.utcnow().isoformat()
    }

# ============== Authentication Endpoints ==============
@app.post("/api/v1/auth/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """User registration endpoint"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "User registered successfully",
        "user": UserResponse.from_orm(db_user)
    }

@app.post("/api/v1/auth/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """User login endpoint"""
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(db_user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(db_user)
    }

@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.from_orm(current_user)

# ============== Course Endpoints ==============
@app.get("/api/v1/courses", response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of courses with pagination"""
    query = db.query(Course)

    if category:
        query = query.filter(Course.category == category)

    courses = query.offset(skip).limit(limit).all()
    return [CourseResponse.from_orm(course) for course in courses]

@app.get("/api/v1/courses/{course_id}", response_model=CourseResponse)
async def get_course_detail(course_id: int, db: Session = Depends(get_db)):
    """Get course details"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseResponse.from_orm(course)

@app.get("/api/v1/courses/{course_id}/modules", response_model=List[ModuleResponse])
async def get_course_modules(course_id: int, db: Session = Depends(get_db)):
    """Get modules for a course"""
    modules = db.query(Module).filter(Module.course_id == course_id).all()
    return [ModuleResponse.from_orm(module) for module in modules]

# ============== Module Endpoints ==============
@app.get("/api/v1/modules", response_model=List[ModuleResponse])
async def get_modules(
    skip: int = 0,
    limit: int = 20,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of modules"""
    query = db.query(Module)

    if difficulty:
        query = query.filter(Module.difficulty == difficulty)

    modules = query.offset(skip).limit(limit).all()
    return [ModuleResponse.from_orm(module) for module in modules]

@app.get("/api/v1/modules/{module_id}", response_model=ModuleResponse)
async def get_module_detail(module_id: int, db: Session = Depends(get_db)):
    """Get module details"""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return ModuleResponse.from_orm(module)

# ============== Project Endpoints ==============
@app.get("/api/v1/projects", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of projects with filters"""
    query = db.query(Project)

    if category:
        query = query.filter(Project.category == category)
    if difficulty:
        query = query.filter(Project.difficulty == difficulty)

    projects = query.offset(skip).limit(limit).all()
    return [ProjectResponse.from_orm(project) for project in projects]

@app.get("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    """Get project details"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse.from_orm(project)

@app.get("/api/v1/projects/category/{category}", response_model=List[ProjectResponse])
async def get_projects_by_category(
    category: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get projects by category"""
    projects = db.query(Project).filter(
        Project.category == category
    ).offset(skip).limit(limit).all()
    return [ProjectResponse.from_orm(project) for project in projects]

# ============== Enrollment Endpoints ==============
@app.post("/api/v1/enrollments")
async def enroll_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enroll in a course"""
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=course_id,
        enrolled_at=datetime.utcnow()
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return {
        "message": "Successfully enrolled in course",
        "enrollment": EnrollmentResponse.from_orm(enrollment)
    }

@app.get("/api/v1/enrollments", response_model=List[EnrollmentResponse])
async def get_user_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's enrollments"""
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id
    ).all()
    return [EnrollmentResponse.from_orm(e) for e in enrollments]

# ============== Progress Endpoints ==============
@app.post("/api/v1/progress")
async def update_progress(
    module_id: int,
    completion_percentage: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user progress on a module"""
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.module_id == module_id
    ).first()

    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            module_id=module_id,
            completion_percentage=completion_percentage,
            started_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(progress)
    else:
        progress.completion_percentage = completion_percentage
        progress.updated_at = datetime.utcnow()

    if completion_percentage == 100:
        progress.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(progress)

    return {
        "message": "Progress updated",
        "progress": UserProgressResponse.from_orm(progress)
    }

@app.get("/api/v1/progress", response_model=List[UserProgressResponse])
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's progress on all modules"""
    progress_list = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()
    return [UserProgressResponse.from_orm(p) for p in progress_list]

@app.get("/api/v1/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user dashboard with statistics"""
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id
    ).count()

    progress_list = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()

    completed = sum(1 for p in progress_list if p.completed_at is not None)
    in_progress = sum(1 for p in progress_list if p.completed_at is None and p.completion_percentage > 0)
    not_started = sum(1 for p in progress_list if p.completion_percentage == 0)

    avg_completion = sum(p.completion_percentage for p in progress_list) / len(progress_list) if progress_list else 0

    return {
        "user": UserResponse.from_orm(current_user),
        "statistics": {
            "enrolled_courses": enrollments,
            "completed_modules": completed,
            "in_progress_modules": in_progress,
            "not_started_modules": not_started,
            "average_completion": round(avg_completion, 2),
            "total_modules_tracked": len(progress_list)
        },
        "recent_activity": [
            UserProgressResponse.from_orm(p) for p in
            sorted(progress_list, key=lambda x: x.updated_at, reverse=True)[:5]
        ]
    }

# ============== Statistics Endpoints ==============
@app.get("/api/v1/statistics")
async def get_platform_statistics(db: Session = Depends(get_db)):
    """Get overall platform statistics"""
    total_users = db.query(User).count()
    total_courses = db.query(Course).count()
    total_modules = db.query(Module).count()
    total_projects = db.query(Project).count()

    return {
        "platform_statistics": {
            "total_users": total_users,
            "total_courses": total_courses,
            "total_modules": total_modules,
            "total_projects": total_projects,
            "learning_hours": (total_modules * 5),  # Estimated
            "timestamp": datetime.utcnow().isoformat()
        }
    }

@app.get("/api/v1/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get all project categories"""
    categories = db.query(Project.category).distinct().all()
    return {
        "categories": [cat[0] for cat in categories if cat[0]]
    }

# ============== Search Endpoints ==============
@app.get("/api/v1/search")
async def search(
    q: str,
    search_type: str = "all",
    db: Session = Depends(get_db)
):
    """Search courses, modules, and projects"""
    results = {}

    if search_type in ["all", "courses"]:
        courses = db.query(Course).filter(
            Course.name.ilike(f"%{q}%") | Course.description.ilike(f"%{q}%")
        ).limit(5).all()
        results["courses"] = [CourseResponse.from_orm(c) for c in courses]

    if search_type in ["all", "modules"]:
        modules = db.query(Module).filter(
            Module.name.ilike(f"%{q}%") | Module.description.ilike(f"%{q}%")
        ).limit(5).all()
        results["modules"] = [ModuleResponse.from_orm(m) for m in modules]

    if search_type in ["all", "projects"]:
        projects = db.query(Project).filter(
            Project.name.ilike(f"%{q}%") | Project.description.ilike(f"%{q}%")
        ).limit(5).all()
        results["projects"] = [ProjectResponse.from_orm(p) for p in projects]

    return results

# ============== Initialization ==============
@app.on_event("startup")
async def startup_event():
    """Initialize database and load sample data"""
    print("🚀 Starting Education AI/ML Platform...")
    init_db()
    load_initial_data()
    print("✅ Platform ready!")

def load_initial_data():
    """Load initial courses, modules, and projects from JSON files"""
    db = SessionLocal()
    try:
        # Check if data already loaded
        if db.query(Course).first():
            print("📊 Data already loaded, skipping initialization")
            return

        print("📚 Loading initial data...")

        # Load courses (create basic tier courses)
        courses_data = [
            ("Tier 1: Python Fundamentals", "Beginner", "Introduction to Python programming"),
            ("Tier 2: Data Science Basics", "Beginner", "Learn data manipulation and analysis"),
            ("Tier 3: Machine Learning", "Intermediate", "Core ML algorithms and concepts"),
            ("Tier 4: Deep Learning", "Intermediate", "Neural networks and deep architectures"),
            ("Tier 5: Advanced ML", "Advanced", "Advanced techniques and research topics"),
            ("Tier 6: Specialization", "Advanced", "Choose your specialization path"),
            ("Tier 7: Research & Innovation", "Advanced", "Cutting-edge AI/ML research"),
        ]

        for idx, (name, difficulty, description) in enumerate(courses_data, 1):
            course = Course(
                name=name,
                description=description,
                category="AI/ML Education",
                difficulty=difficulty,
                duration_hours=(idx * 50),
                created_at=datetime.utcnow()
            )
            db.add(course)

        db.commit()
        print("✅ Courses loaded")

        # Load modules (sample from existing modules)
        modules_to_add = [
            (1, "01-python-programming-fundamentals", "Python Programming Fundamentals", "Beginner"),
            (1, "02-data-structures-algorithms", "Data Structures & Algorithms", "Beginner"),
            (2, "06-pandas-data-manipulation", "Pandas Data Manipulation", "Beginner"),
            (2, "07-data-visualization", "Data Visualization", "Beginner"),
            (3, "11-supervised-learning", "Supervised Learning", "Intermediate"),
            (3, "12-unsupervised-learning", "Unsupervised Learning", "Intermediate"),
            (4, "21-neural-networks", "Neural Networks", "Intermediate"),
            (4, "22-convolutional-networks", "Convolutional Neural Networks", "Intermediate"),
            (5, "31-nlp-transformers", "NLP & Transformers", "Advanced"),
            (5, "32-reinforcement-learning", "Reinforcement Learning", "Advanced"),
        ]

        for course_id, module_code, module_name, difficulty in modules_to_add:
            module = Module(
                course_id=course_id,
                name=module_name,
                code=module_code,
                description=f"Comprehensive guide to {module_name.lower()}",
                difficulty=difficulty,
                duration_hours=40,
                content_url=f"/modules/{module_code}",
                created_at=datetime.utcnow()
            )
            db.add(module)

        db.commit()
        print("✅ Modules loaded")

        # Load projects from all categories
        project_categories = [
            ("practical_projects", "Web Development"),
            ("mobile_projects", "Mobile Development"),
            ("game_projects", "Game Development"),
            ("data_projects", "Data Engineering"),
            ("cloud_projects", "Cloud & DevOps"),
            ("system_projects", "Systems & Embedded"),
        ]

        project_count = 0
        for category_dir, category_name in project_categories:
            category_path = Path(f"/home/user/education-ai-ml/{category_dir}")
            if category_path.exists():
                for project_dir in sorted(category_path.iterdir())[:10]:  # Load first 10 from each
                    if project_dir.is_dir():
                        metadata_file = project_dir / "metadata.json"
                        if metadata_file.exists():
                            with open(metadata_file, 'r', encoding='utf-8') as f:
                                metadata = json.load(f)

                            project = Project(
                                name=metadata.get("name", project_dir.name),
                                description=f"Learn {metadata.get('name', project_dir.name).lower()}",
                                category=category_name,
                                difficulty=metadata.get("difficulty", "Intermediate"),
                                duration_weeks=metadata.get("duration_weeks", 2),
                                technology=metadata.get("technology", "Various"),
                                project_url=f"/projects/{category_dir}/{project_dir.name}",
                                created_at=datetime.utcnow()
                            )
                            db.add(project)
                            project_count += 1

        db.commit()
        print(f"✅ Loaded {project_count} projects from categories")

    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
