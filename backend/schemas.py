#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ============== User Schemas ==============
class UserCreate(BaseModel):
    """User creation schema"""
    email: EmailStr
    username: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ============== Course Schemas ==============
class CourseResponse(BaseModel):
    """Course response schema"""
    id: int
    name: str
    description: str
    category: str
    difficulty: str
    duration_hours: int
    instructor: Optional[str] = None
    rating: float = 0.0
    created_at: datetime

    class Config:
        from_attributes = True

# ============== Module Schemas ==============
class ModuleResponse(BaseModel):
    """Module response schema"""
    id: int
    course_id: int
    name: str
    code: str
    description: str
    difficulty: str
    duration_hours: int
    content_url: str
    created_at: datetime

    class Config:
        from_attributes = True

# ============== Project Schemas ==============
class ProjectResponse(BaseModel):
    """Project response schema"""
    id: int
    name: str
    description: str
    category: str
    difficulty: str
    duration_weeks: int
    technology: str
    skills: Optional[str] = None
    project_url: str
    rating: float = 0.0
    created_at: datetime

    class Config:
        from_attributes = True

# ============== Enrollment Schemas ==============
class EnrollmentResponse(BaseModel):
    """Enrollment response schema"""
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    completed_at: Optional[datetime] = None
    progress_percentage: int

    class Config:
        from_attributes = True

# ============== Progress Schemas ==============
class UserProgressResponse(BaseModel):
    """User progress response schema"""
    id: int
    user_id: int
    module_id: int
    completion_percentage: int
    score: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: datetime

    class Config:
        from_attributes = True

# ============== Auth Schemas ==============
class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    """Token data schema"""
    user_id: Optional[int] = None

# ============== Statistics Schemas ==============
class StatisticsResponse(BaseModel):
    """Statistics response schema"""
    total_users: int
    total_courses: int
    total_modules: int
    total_projects: int
    learning_hours: int
    timestamp: datetime
