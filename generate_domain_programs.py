#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 600 domain-specific programming projects (100 each for 6 domains)
Domains: Web Development, Mobile Development, Game Development, Data Engineering, Cloud & DevOps, Systems & Embedded
"""

import json
import os
from pathlib import Path

# Define 100 projects for Web Development
WEB_DEVELOPMENT_PROJECTS = {
    "web_001": {"name": "Static Portfolio Website", "lang": "HTML/CSS", "difficulty": "Beginner"},
    "web_002": {"name": "Responsive Blog Layout", "lang": "HTML/CSS/Bootstrap", "difficulty": "Beginner"},
    "web_003": {"name": "Personal Landing Page", "lang": "HTML/CSS/JavaScript", "difficulty": "Beginner"},
    "web_004": {"name": "Todo List Web App", "lang": "HTML/CSS/JavaScript", "difficulty": "Beginner"},
    "web_005": {"name": "Calculator App", "lang": "JavaScript", "difficulty": "Beginner"},
    "web_006": {"name": "Weather Widget", "lang": "JavaScript/API", "difficulty": "Intermediate"},
    "web_007": {"name": "Movie Search App", "lang": "JavaScript/REST API", "difficulty": "Intermediate"},
    "web_008": {"name": "Photo Gallery", "lang": "JavaScript/DOM", "difficulty": "Beginner"},
    "web_009": {"name": "Quiz Application", "lang": "JavaScript", "difficulty": "Intermediate"},
    "web_010": {"name": "Drawing Canvas App", "lang": "Canvas API", "difficulty": "Intermediate"},
    "web_011": {"name": "Chat Application", "lang": "Node.js/Socket.io", "difficulty": "Advanced"},
    "web_012": {"name": "E-commerce Store (Frontend)", "lang": "React/Redux", "difficulty": "Advanced"},
    "web_013": {"name": "Social Media Feed", "lang": "React/Firebase", "difficulty": "Advanced"},
    "web_014": {"name": "Video Streaming Platform", "lang": "React/Node.js", "difficulty": "Advanced"},
    "web_015": {"name": "Project Management Tool", "lang": "Vue.js/Express", "difficulty": "Advanced"},
    "web_016": {"name": "Music Streaming App", "lang": "Angular/WebAudio", "difficulty": "Advanced"},
    "web_017": {"name": "Collaborative Drawing Board", "lang": "WebSocket/Canvas", "difficulty": "Advanced"},
    "web_018": {"name": "Real-time Notification System", "lang": "Node.js/WebSocket", "difficulty": "Advanced"},
    "web_019": {"name": "API Documentation Site", "lang": "Next.js/MDX", "difficulty": "Intermediate"},
    "web_020": {"name": "Markdown Editor", "lang": "React/markdown-it", "difficulty": "Intermediate"},
    "web_021": {"name": "Code Snippet Manager", "lang": "Django/React", "difficulty": "Advanced"},
    "web_022": {"name": "Task Scheduler", "lang": "FastAPI/React", "difficulty": "Advanced"},
    "web_023": {"name": "Note-taking App", "lang": "Flutter Web", "difficulty": "Intermediate"},
    "web_024": {"name": "File Upload Manager", "lang": "Express/Multer", "difficulty": "Intermediate"},
    "web_025": {"name": "Real-time Multiplayer Game", "lang": "Phaser/Node.js", "difficulty": "Advanced"},
    "web_026": {"name": "Authentication System", "lang": "Django/JWT", "difficulty": "Intermediate"},
    "web_027": {"name": "Blog Platform", "lang": "Next.js/MongoDB", "difficulty": "Intermediate"},
    "web_028": {"name": "URL Shortener", "lang": "Flask/React", "difficulty": "Beginner"},
    "web_029": {"name": "Password Manager Web", "lang": "React/Encryption", "difficulty": "Advanced"},
    "web_030": {"name": "Analytics Dashboard", "lang": "React/Chart.js", "difficulty": "Advanced"},
    "web_031": {"name": "Fitness Tracker Web", "lang": "Vue.js/Firebase", "difficulty": "Intermediate"},
    "web_032": {"name": "Recipe Sharing Platform", "lang": "Django/PostgreSQL", "difficulty": "Intermediate"},
    "web_033": {"name": "Expense Tracker", "lang": "React/Firestore", "difficulty": "Intermediate"},
    "web_034": {"name": "Travel Planning App", "lang": "Next.js/Mapbox", "difficulty": "Advanced"},
    "web_035": {"name": "Job Board", "lang": "Ruby on Rails", "difficulty": "Advanced"},
    "web_036": {"name": "Forum Application", "lang": "Laravel/Vue", "difficulty": "Advanced"},
    "web_037": {"name": "Streaming Dashboard", "lang": "React/Three.js", "difficulty": "Advanced"},
    "web_038": {"name": "Learning Management System", "lang": "Django/React", "difficulty": "Advanced"},
    "web_039": {"name": "Real Estate Portal", "lang": "Next.js/Node.js", "difficulty": "Advanced"},
    "web_040": {"name": "Restaurant Ordering System", "lang": "React/Express", "difficulty": "Intermediate"},
    "web_041": {"name": "Appointment Booking", "lang": "Vue.js/Express", "difficulty": "Intermediate"},
    "web_042": {"name": "Employee Directory", "lang": "Angular/Spring", "difficulty": "Advanced"},
    "web_043": {"name": "Health Monitoring Dashboard", "lang": "React/D3.js", "difficulty": "Advanced"},
    "web_044": {"name": "Crypto Tracker", "lang": "Next.js/CoinGecko API", "difficulty": "Intermediate"},
    "web_045": {"name": "Inventory Management", "lang": "Django/PostgreSQL", "difficulty": "Intermediate"},
    "web_046": {"name": "Customer Support Chat", "lang": "React/Firebase", "difficulty": "Intermediate"},
    "web_047": {"name": "Event Management System", "lang": "Laravel/MySQL", "difficulty": "Advanced"},
    "web_048": {"name": "Freelance Marketplace", "lang": "Django/React", "difficulty": "Advanced"},
    "web_049": {"name": "Document Collaboration", "lang": "Node.js/MongoDB", "difficulty": "Advanced"},
    "web_050": {"name": "Survey Builder", "lang": "React/Express", "difficulty": "Intermediate"},
    "web_051": {"name": "Wiki Platform", "lang": "Next.js/PostgreSQL", "difficulty": "Advanced"},
    "web_052": {"name": "Code Collaboration Editor", "lang": "Node.js/Monaco", "difficulty": "Advanced"},
    "web_053": {"name": "Donation Platform", "lang": "Django/Stripe", "difficulty": "Intermediate"},
    "web_054": {"name": "Book Library System", "lang": "Flask/React", "difficulty": "Intermediate"},
    "web_055": {"name": "Meditation App Web", "lang": "Vue.js/WebAudio", "difficulty": "Intermediate"},
    "web_056": {"name": "Portfolio Builder", "lang": "Next.js/Firebase", "difficulty": "Intermediate"},
    "web_057": {"name": "Habit Tracker", "lang": "React/Supabase", "difficulty": "Intermediate"},
    "web_058": {"name": "News Aggregator", "lang": "Next.js/NewsAPI", "difficulty": "Beginner"},
    "web_059": {"name": "Movie Recommendation", "lang": "Django/React", "difficulty": "Intermediate"},
    "web_060": {"name": "Job Matching Algorithm", "lang": "Flask/React", "difficulty": "Advanced"},
    "web_061": {"name": "Peer-to-Peer Marketplace", "lang": "Node.js/React", "difficulty": "Advanced"},
    "web_062": {"name": "Virtual Classroom", "lang": "React/WebRTC", "difficulty": "Advanced"},
    "web_063": {"name": "Subscription Management", "lang": "Django/Stripe", "difficulty": "Intermediate"},
    "web_064": {"name": "Feedback Collection Tool", "lang": "Next.js/MongoDB", "difficulty": "Beginner"},
    "web_065": {"name": "URL QR Code Generator", "lang": "React/qrcode.js", "difficulty": "Beginner"},
    "web_066": {"name": "Email Campaign Tool", "lang": "Django/Celery", "difficulty": "Advanced"},
    "web_067": {"name": "Sleep Tracking Web", "lang": "React/Firebase", "difficulty": "Intermediate"},
    "web_068": {"name": "Time Zone Converter", "lang": "JavaScript/Moment.js", "difficulty": "Beginner"},
    "web_069": {"name": "Language Learning Platform", "lang": "Django/React", "difficulty": "Advanced"},
    "web_070": {"name": "Workout Progress Tracker", "lang": "Vue.js/Firebase", "difficulty": "Intermediate"},
    "web_071": {"name": "Car Rental System", "lang": "Laravel/Vue", "difficulty": "Advanced"},
    "web_072": {"name": "Wedding Planning Tool", "lang": "Next.js/MongoDB", "difficulty": "Intermediate"},
    "web_073": {"name": "Plant Care Reminder", "lang": "React/Node.js", "difficulty": "Beginner"},
    "web_074": {"name": "Financial Dashboard", "lang": "React/Redux/D3", "difficulty": "Advanced"},
    "web_075": {"name": "Pet Adoption Portal", "lang": "Django/React", "difficulty": "Intermediate"},
    "web_076": {"name": "Medication Reminder", "lang": "Vue.js/Express", "difficulty": "Beginner"},
    "web_077": {"name": "Travel Itinerary Planner", "lang": "Next.js/Google Maps", "difficulty": "Intermediate"},
    "web_078": {"name": "Home Automation Dashboard", "lang": "React/MQTT", "difficulty": "Advanced"},
    "web_079": {"name": "Art Gallery Showcase", "lang": "Next.js/Cloudinary", "difficulty": "Intermediate"},
    "web_080": {"name": "Bug Tracking System", "lang": "Django/React", "difficulty": "Intermediate"},
    "web_081": {"name": "Volunteer Matching", "lang": "Flask/React", "difficulty": "Intermediate"},
    "web_082": {"name": "Product Launch Page", "lang": "Next.js/Tailwind", "difficulty": "Beginner"},
    "web_083": {"name": "Meal Planning App", "lang": "React/Express", "difficulty": "Intermediate"},
    "web_084": {"name": "Crowdfunding Platform", "lang": "Django/React", "difficulty": "Advanced"},
    "web_085": {"name": "Accommodation Booking", "lang": "Next.js/Stripe", "difficulty": "Advanced"},
    "web_086": {"name": "Weight Loss Tracker", "lang": "Vue.js/Firebase", "difficulty": "Beginner"},
    "web_087": {"name": "Grocery Delivery App", "lang": "Node.js/React", "difficulty": "Advanced"},
    "web_088": {"name": "Community Forum", "lang": "Django/React", "difficulty": "Intermediate"},
    "web_089": {"name": "Memory Game Collection", "lang": "React/JavaScript", "difficulty": "Beginner"},
    "web_090": {"name": "Podcast Streaming", "lang": "Next.js/Node.js", "difficulty": "Advanced"},
    "web_091": {"name": "Complaint Management", "lang": "Flask/React", "difficulty": "Intermediate"},
    "web_092": {"name": "Skill Marketplace", "lang": "Django/React", "difficulty": "Advanced"},
    "web_093": {"name": "Movie Rating Platform", "lang": "Next.js/MongoDB", "difficulty": "Intermediate"},
    "web_094": {"name": "Debt Payoff Calculator", "lang": "React/Chart.js", "difficulty": "Beginner"},
    "web_095": {"name": "Mentorship Platform", "lang": "Django/React", "difficulty": "Advanced"},
    "web_096": {"name": "Travel Expense Splitter", "lang": "Vue.js/Firebase", "difficulty": "Intermediate"},
    "web_097": {"name": "Scholarship Finder", "lang": "Flask/React", "difficulty": "Intermediate"},
    "web_098": {"name": "Gym Management System", "lang": "Laravel/Vue", "difficulty": "Advanced"},
    "web_099": {"name": "Design Inspiration Gallery", "lang": "Next.js/Supabase", "difficulty": "Beginner"},
    "web_100": {"name": "Sustainable Shopping Guide", "lang": "React/Express", "difficulty": "Intermediate"},
}

# Define 100 projects for Mobile Development
MOBILE_DEVELOPMENT_PROJECTS = {
    "mobile_001": {"name": "Hello World App", "lang": "React Native", "difficulty": "Beginner"},
    "mobile_002": {"name": "Calculator App", "lang": "Flutter", "difficulty": "Beginner"},
    "mobile_003": {"name": "Todo List App", "lang": "React Native", "difficulty": "Beginner"},
    "mobile_004": {"name": "Weather App", "lang": "Flutter", "difficulty": "Beginner"},
    "mobile_005": {"name": "Note Taking App", "lang": "React Native", "difficulty": "Beginner"},
    "mobile_006": {"name": "Stopwatch App", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_007": {"name": "Alarm Clock App", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_008": {"name": "Image Gallery App", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_009": {"name": "Music Player", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_010": {"name": "QR Code Scanner", "lang": "Flutter/mobile_vision", "difficulty": "Intermediate"},
    "mobile_011": {"name": "Fitness Tracker", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_012": {"name": "Budget Planner", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_013": {"name": "Social Media App", "lang": "React Native/Firebase", "difficulty": "Advanced"},
    "mobile_014": {"name": "Chat Application", "lang": "Flutter/Firebase", "difficulty": "Advanced"},
    "mobile_015": {"name": "E-commerce App", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_016": {"name": "Video Streaming App", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_017": {"name": "Restaurant Ordering", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_018": {"name": "Ride Sharing App", "lang": "Flutter/Maps", "difficulty": "Advanced"},
    "mobile_019": {"name": "Job Search App", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_020": {"name": "Real Estate App", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_021": {"name": "Healthcare App", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_022": {"name": "Meditation App", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_023": {"name": "Travel Booking App", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_024": {"name": "Weather Forecast", "lang": "Flutter/Provider", "difficulty": "Intermediate"},
    "mobile_025": {"name": "Book Reader App", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_026": {"name": "Podcast App", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_027": {"name": "Dating App", "lang": "React Native/Firebase", "difficulty": "Advanced"},
    "mobile_028": {"name": "Gaming Leaderboard", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_029": {"name": "Password Manager", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_030": {"name": "Expense Tracking", "lang": "Flutter/Hive", "difficulty": "Intermediate"},
    "mobile_031": {"name": "Recipe App", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_032": {"name": "Pet Care App", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_033": {"name": "Habit Tracker", "lang": "React Native", "difficulty": "Beginner"},
    "mobile_034": {"name": "Language Learning", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_035": {"name": "News Reader", "lang": "React Native", "difficulty": "Beginner"},
    "mobile_036": {"name": "Plant Care", "lang": "Flutter", "difficulty": "Beginner"},
    "mobile_037": {"name": "Workout Tracker", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_038": {"name": "Water Reminder", "lang": "Flutter", "difficulty": "Beginner"},
    "mobile_039": {"name": "Sleep Tracker", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_040": {"name": "Meditation Guide", "lang": "Flutter/audio", "difficulty": "Intermediate"},
    "mobile_041": {"name": "News Aggregator", "lang": "React Native", "difficulty": "Beginner"},
    "mobile_042": {"name": "Stock Market Tracker", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_043": {"name": "Cryptocurrency App", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_044": {"name": "Coupon Finder", "lang": "Flutter", "difficulty": "Beginner"},
    "mobile_045": {"name": "Movie Database", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_046": {"name": "Documentary Streaming", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_047": {"name": "Sports Score App", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_048": {"name": "Workout Plans", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_049": {"name": "Nutrition Tracker", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_050": {"name": "Mental Health App", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_051": {"name": "Study Timer", "lang": "React Native", "difficulty": "Beginner"},
    "mobile_052": {"name": "Course Learning", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_053": {"name": "Quiz Master", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_054": {"name": "Flashcard App", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_055": {"name": "Journal App", "lang": "React Native", "difficulty": "Beginner"},
    "mobile_056": {"name": "Diary Maker", "lang": "Flutter", "difficulty": "Beginner"},
    "mobile_057": {"name": "Memory Game", "lang": "React Native", "difficulty": "Beginner"},
    "mobile_058": {"name": "Puzzle Game", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_059": {"name": "Drawing App", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_060": {"name": "Photo Editor", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_061": {"name": "Sticker Pack Creator", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_062": {"name": "Video Editor", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_063": {"name": "Voice Recorder", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_064": {"name": "Podcast Manager", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_065": {"name": "Audio Equalizer", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_066": {"name": "Music Composition", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_067": {"name": "Instrument Learning", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_068": {"name": "Karaoke App", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_069": {"name": "Handwriting Note", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_070": {"name": "Sketching App", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_071": {"name": "Augmented Reality App", "lang": "React Native/ARKit", "difficulty": "Advanced"},
    "mobile_072": {"name": "Virtual Try-on", "lang": "Flutter/ARCore", "difficulty": "Advanced"},
    "mobile_073": {"name": "AR Navigation", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_074": {"name": "Offline Mode App", "lang": "Flutter/SQLite", "difficulty": "Intermediate"},
    "mobile_075": {"name": "Push Notification", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_076": {"name": "Background Service", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_077": {"name": "Geolocation App", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_078": {"name": "Map Navigation", "lang": "Flutter/Google Maps", "difficulty": "Intermediate"},
    "mobile_079": {"name": "Proximity Alert", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_080": {"name": "Bluetooth Connector", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_081": {"name": "Smart Home Control", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_082": {"name": "IoT Dashboard", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_083": {"name": "Machine Learning App", "lang": "React Native/TFLite", "difficulty": "Advanced"},
    "mobile_084": {"name": "Vision Recognition", "lang": "Flutter/ML Kit", "difficulty": "Advanced"},
    "mobile_085": {"name": "Speech Recognition", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_086": {"name": "Chatbot App", "lang": "Flutter", "difficulty": "Advanced"},
    "mobile_087": {"name": "Translation App", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_088": {"name": "PDF Viewer", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_089": {"name": "Document Scanner", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_090": {"name": "File Manager", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_091": {"name": "Cloud Storage", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_092": {"name": "Backup Manager", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_093": {"name": "Device Info App", "lang": "React Native", "difficulty": "Beginner"},
    "mobile_094": {"name": "System Monitor", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_095": {"name": "Battery Optimizer", "lang": "React Native", "difficulty": "Intermediate"},
    "mobile_096": {"name": "Data Usage Monitor", "lang": "Flutter", "difficulty": "Intermediate"},
    "mobile_097": {"name": "App Installer", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_098": {"name": "Cache Cleaner", "lang": "Flutter", "difficulty": "Beginner"},
    "mobile_099": {"name": "Security Scanner", "lang": "React Native", "difficulty": "Advanced"},
    "mobile_100": {"name": "Device Automation", "lang": "Flutter", "difficulty": "Advanced"},
}

# Define 100 projects for Game Development
GAME_DEVELOPMENT_PROJECTS = {
    "game_001": {"name": "Pong Game", "engine": "Pygame", "difficulty": "Beginner"},
    "game_002": {"name": "Flappy Bird Clone", "engine": "Phaser", "difficulty": "Beginner"},
    "game_003": {"name": "Snake Game", "engine": "Pygame", "difficulty": "Beginner"},
    "game_004": {"name": "Tic Tac Toe", "engine": "JavaScript/Canvas", "difficulty": "Beginner"},
    "game_005": {"name": "Breakout Game", "engine": "Phaser", "difficulty": "Beginner"},
    "game_006": {"name": "Maze Runner", "engine": "Pygame", "difficulty": "Intermediate"},
    "game_007": {"name": "Space Shooter", "engine": "Phaser", "difficulty": "Intermediate"},
    "game_008": {"name": "Platformer Game", "engine": "Unity/C#", "difficulty": "Intermediate"},
    "game_009": {"name": "Top-Down RPG", "engine": "Godot", "difficulty": "Intermediate"},
    "game_010": {"name": "Match-3 Puzzle", "engine": "Phaser", "difficulty": "Intermediate"},
    "game_011": {"name": "Card Game", "engine": "Unity", "difficulty": "Intermediate"},
    "game_012": {"name": "Board Game Simulator", "engine": "Godot", "difficulty": "Intermediate"},
    "game_013": {"name": "Racing Game", "engine": "Unity", "difficulty": "Advanced"},
    "game_014": {"name": "3D Shooter", "engine": "Unreal Engine", "difficulty": "Advanced"},
    "game_015": {"name": "Survival Game", "engine": "Unity", "difficulty": "Advanced"},
    "game_016": {"name": "Roguelike Dungeon", "engine": "Godot", "difficulty": "Advanced"},
    "game_017": {"name": "Adventure Quest", "engine": "Unity", "difficulty": "Advanced"},
    "game_018": {"name": "Puzzle Platformer", "engine": "Godot", "difficulty": "Advanced"},
    "game_019": {"name": "Tower Defense", "engine": "Phaser", "difficulty": "Intermediate"},
    "game_020": {"name": "Real-Time Strategy", "engine": "Unity", "difficulty": "Advanced"},
    "game_021": {"name": "Turn-Based RPG", "engine": "Godot", "difficulty": "Advanced"},
    "game_022": {"name": "Dungeon Crawler", "engine": "Unity", "difficulty": "Advanced"},
    "game_023": {"name": "Rhythm Game", "engine": "Phaser", "difficulty": "Intermediate"},
    "game_024": {"name": "Music Game", "engine": "Unity", "difficulty": "Intermediate"},
    "game_025": {"name": "Fishing Simulator", "engine": "Godot", "difficulty": "Beginner"},
    "game_026": {"name": "Farming Simulator", "engine": "Unity", "difficulty": "Intermediate"},
    "game_027": {"name": "Cooking Game", "engine": "Phaser", "difficulty": "Beginner"},
    "game_028": {"name": "Restaurant Manager", "engine": "Unity", "difficulty": "Intermediate"},
    "game_029": {"name": "Shop Tycoon", "engine": "Godot", "difficulty": "Intermediate"},
    "game_030": {"name": "City Builder", "engine": "Unity", "difficulty": "Advanced"},
    "game_031": {"name": "Idle Clicker", "engine": "Phaser", "difficulty": "Beginner"},
    "game_032": {"name": "Incremental Game", "engine": "JavaScript", "difficulty": "Beginner"},
    "game_033": {"name": "Animal Care Game", "engine": "Unity", "difficulty": "Beginner"},
    "game_034": {"name": "Pet Breeding", "engine": "Godot", "difficulty": "Intermediate"},
    "game_035": {"name": "Slot Machine", "engine": "Phaser", "difficulty": "Beginner"},
    "game_036": {"name": "Poker Game", "engine": "Unity", "difficulty": "Intermediate"},
    "game_037": {"name": "Blackjack Game", "engine": "JavaScript", "difficulty": "Beginner"},
    "game_038": {"name": "Bingo Simulator", "engine": "Phaser", "difficulty": "Beginner"},
    "game_039": {"name": "Dice Game", "engine": "Pygame", "difficulty": "Beginner"},
    "game_040": {"name": "Dice Roller", "engine": "Unity", "difficulty": "Beginner"},
    "game_041": {"name": "Word Game", "engine": "Godot", "difficulty": "Intermediate"},
    "game_042": {"name": "Hangman Game", "engine": "Phaser", "difficulty": "Beginner"},
    "game_043": {"name": "Trivia Game", "engine": "Unity", "difficulty": "Intermediate"},
    "game_044": {"name": "Quiz Master", "engine": "Godot", "difficulty": "Intermediate"},
    "game_045": {"name": "Spelling Game", "engine": "Phaser", "difficulty": "Beginner"},
    "game_046": {"name": "Math Games", "engine": "JavaScript", "difficulty": "Beginner"},
    "game_047": {"name": "Memory Game", "engine": "Phaser", "difficulty": "Beginner"},
    "game_048": {"name": "Concentration Game", "engine": "Unity", "difficulty": "Beginner"},
    "game_049": {"name": "Charades App", "engine": "Godot", "difficulty": "Beginner"},
    "game_050": {"name": "20 Questions", "engine": "Phaser", "difficulty": "Intermediate"},
    "game_051": {"name": "Story Game", "engine": "Unity", "difficulty": "Intermediate"},
    "game_052": {"name": "Text Adventure", "engine": "Pygame", "difficulty": "Intermediate"},
    "game_053": {"name": "Interactive Fiction", "engine": "Godot", "difficulty": "Intermediate"},
    "game_054": {"name": "Visual Novel", "engine": "Renpy", "difficulty": "Intermediate"},
    "game_055": {"name": "Escape Room", "engine": "Unity", "difficulty": "Advanced"},
    "game_056": {"name": "Mystery Game", "engine": "Godot", "difficulty": "Advanced"},
    "game_057": {"name": "Detective Game", "engine": "Phaser", "difficulty": "Advanced"},
    "game_058": {"name": "Horror Game", "engine": "Unity", "difficulty": "Advanced"},
    "game_059": {"name": "Psychological Thriller", "engine": "Godot", "difficulty": "Advanced"},
    "game_060": {"name": "Zombie Apocalypse", "engine": "Unity", "difficulty": "Advanced"},
    "game_061": {"name": "Monster Hunter", "engine": "Unreal Engine", "difficulty": "Advanced"},
    "game_062": {"name": "Boss Battle Game", "engine": "Unity", "difficulty": "Intermediate"},
    "game_063": {"name": "Bullet Hell", "engine": "Godot", "difficulty": "Advanced"},
    "game_064": {"name": "Wave Defense", "engine": "Phaser", "difficulty": "Intermediate"},
    "game_065": {"name": "Horde Survivor", "engine": "Unity", "difficulty": "Intermediate"},
    "game_066": {"name": "Endless Runner", "engine": "Phaser", "difficulty": "Beginner"},
    "game_067": {"name": "Obstacle Course", "engine": "Godot", "difficulty": "Beginner"},
    "game_068": {"name": "Ball Rolling", "engine": "Unity", "difficulty": "Beginner"},
    "game_069": {"name": "Sliding Puzzle", "engine": "Phaser", "difficulty": "Beginner"},
    "game_070": {"name": "Sokoban", "engine": "Godot", "difficulty": "Intermediate"},
    "game_071": {"name": "Block Puzzle", "engine": "Unity", "difficulty": "Beginner"},
    "game_072": {"name": "Tetris Clone", "engine": "Phaser", "difficulty": "Beginner"},
    "game_073": {"name": "Jigsaw Puzzle", "engine": "Godot", "difficulty": "Intermediate"},
    "game_074": {"name": "Crossword Puzzle", "engine": "JavaScript", "difficulty": "Intermediate"},
    "game_075": {"name": "Sudoku Solver", "engine": "Python", "difficulty": "Intermediate"},
    "game_076": {"name": "Logic Puzzle", "engine": "Phaser", "difficulty": "Advanced"},
    "game_077": {"name": "Chess Game", "engine": "Unity", "difficulty": "Advanced"},
    "game_078": {"name": "Checkers Game", "engine": "Godot", "difficulty": "Advanced"},
    "game_079": {"name": "Go Game", "engine": "JavaScript", "difficulty": "Advanced"},
    "game_080": {"name": "Connect Four", "engine": "Phaser", "difficulty": "Intermediate"},
    "game_081": {"name": "Tic Tac Toe AI", "engine": "Python", "difficulty": "Intermediate"},
    "game_082": {"name": "AI Opponent", "engine": "Unity", "difficulty": "Advanced"},
    "game_083": {"name": "Multiplayer Game", "engine": "Godot", "difficulty": "Advanced"},
    "game_084": {"name": "Online Racing", "engine": "Unreal Engine", "difficulty": "Advanced"},
    "game_085": {"name": "Cooperative Game", "engine": "Unity", "difficulty": "Advanced"},
    "game_086": {"name": "Battle Royale", "engine": "Unreal Engine", "difficulty": "Advanced"},
    "game_087": {"name": "MOBA Game", "engine": "Unity", "difficulty": "Advanced"},
    "game_088": {"name": "MMO Prototype", "engine": "Godot", "difficulty": "Advanced"},
    "game_089": {"name": "Co-op Dungeon", "engine": "Phaser", "difficulty": "Advanced"},
    "game_090": {"name": "Team Shooter", "engine": "Unity", "difficulty": "Advanced"},
    "game_091": {"name": "Sports Game", "engine": "Unreal Engine", "difficulty": "Advanced"},
    "game_092": {"name": "Football Sim", "engine": "Unity", "difficulty": "Advanced"},
    "game_093": {"name": "Basketball Game", "engine": "Godot", "difficulty": "Intermediate"},
    "game_094": {"name": "Tennis Sim", "engine": "Phaser", "difficulty": "Intermediate"},
    "game_095": {"name": "Golf Game", "engine": "Unity", "difficulty": "Intermediate"},
    "game_096": {"name": "Bowling Game", "engine": "Godot", "difficulty": "Beginner"},
    "game_097": {"name": "Archery Game", "engine": "Phaser", "difficulty": "Beginner"},
    "game_098": {"name": "Darts Game", "engine": "JavaScript", "difficulty": "Beginner"},
    "game_099": {"name": "Shooting Range", "engine": "Unity", "difficulty": "Intermediate"},
    "game_100": {"name": "VR Game", "engine": "Unity/SteamVR", "difficulty": "Advanced"},
}

# Define 100 projects for Data Engineering
DATA_ENGINEERING_PROJECTS = {
    "data_001": {"name": "CSV Data Cleaning", "tools": "Pandas", "difficulty": "Beginner"},
    "data_002": {"name": "JSON Processing", "tools": "Python", "difficulty": "Beginner"},
    "data_003": {"name": "Data Validation", "tools": "Great Expectations", "difficulty": "Intermediate"},
    "data_004": {"name": "Database Design", "tools": "PostgreSQL", "difficulty": "Intermediate"},
    "data_005": {"name": "ETL Pipeline", "tools": "Apache Airflow", "difficulty": "Advanced"},
    "data_006": {"name": "Web Scraping", "tools": "Beautiful Soup", "difficulty": "Intermediate"},
    "data_007": {"name": "API Data Collection", "tools": "Requests", "difficulty": "Beginner"},
    "data_008": {"name": "Data Warehouse", "tools": "Snowflake", "difficulty": "Advanced"},
    "data_009": {"name": "Real-time Streaming", "tools": "Kafka", "difficulty": "Advanced"},
    "data_010": {"name": "Distributed Processing", "tools": "Apache Spark", "difficulty": "Advanced"},
    "data_011": {"name": "Data Partitioning", "tools": "Hive", "difficulty": "Intermediate"},
    "data_012": {"name": "Columnar Storage", "tools": "Parquet", "difficulty": "Intermediate"},
    "data_013": {"name": "Time Series Data", "tools": "InfluxDB", "difficulty": "Intermediate"},
    "data_014": {"name": "Graph Database", "tools": "Neo4j", "difficulty": "Advanced"},
    "data_015": {"name": "Document DB", "tools": "MongoDB", "difficulty": "Intermediate"},
    "data_016": {"name": "Vector Database", "tools": "Milvus", "difficulty": "Advanced"},
    "data_017": {"name": "Data Versioning", "tools": "DVC", "difficulty": "Intermediate"},
    "data_018": {"name": "Metadata Management", "tools": "Apache Atlas", "difficulty": "Advanced"},
    "data_019": {"name": "Data Cataloging", "tools": "Collibra", "difficulty": "Advanced"},
    "data_020": {"name": "Data Governance", "tools": "Apache Ranger", "difficulty": "Advanced"},
    "data_021": {"name": "Change Data Capture", "tools": "Debezium", "difficulty": "Advanced"},
    "data_022": {"name": "Data Replication", "tools": "Oracle GoldenGate", "difficulty": "Advanced"},
    "data_023": {"name": "Data Backup", "tools": "Backblaze", "difficulty": "Intermediate"},
    "data_024": {"name": "Disaster Recovery", "tools": "AWS DMS", "difficulty": "Advanced"},
    "data_025": {"name": "Data Migration", "tools": "Talend", "difficulty": "Advanced"},
    "data_026": {"name": "Data Transformation", "tools": "DBT", "difficulty": "Intermediate"},
    "data_027": {"name": "Feature Engineering", "tools": "Pandas", "difficulty": "Intermediate"},
    "data_028": {"name": "Data Aggregation", "tools": "SQL", "difficulty": "Beginner"},
    "data_029": {"name": "Data Deduplication", "tools": "Python", "difficulty": "Beginner"},
    "data_030": {"name": "Outlier Detection", "tools": "Python/Scikit-learn", "difficulty": "Intermediate"},
    "data_031": {"name": "Missing Data Handling", "tools": "Pandas", "difficulty": "Intermediate"},
    "data_032": {"name": "Data Normalization", "tools": "SQL", "difficulty": "Beginner"},
    "data_033": {"name": "Data Standardization", "tools": "Python", "difficulty": "Beginner"},
    "data_034": {"name": "Quality Metrics", "tools": "Great Expectations", "difficulty": "Intermediate"},
    "data_035": {"name": "Data Profiling", "tools": "Dataedo", "difficulty": "Intermediate"},
    "data_036": {"name": "Statistical Analysis", "tools": "SciPy", "difficulty": "Intermediate"},
    "data_037": {"name": "Correlation Analysis", "tools": "Pandas", "difficulty": "Beginner"},
    "data_038": {"name": "Hypothesis Testing", "tools": "StatsModels", "difficulty": "Intermediate"},
    "data_039": {"name": "A/B Testing", "tools": "Python", "difficulty": "Intermediate"},
    "data_040": {"name": "Causal Analysis", "tools": "Causal ML", "difficulty": "Advanced"},
    "data_041": {"name": "Time Series Analysis", "tools": "Statsmodels", "difficulty": "Intermediate"},
    "data_042": {"name": "Forecasting", "tools": "Prophet", "difficulty": "Intermediate"},
    "data_043": {"name": "Anomaly Detection", "tools": "Isolation Forest", "difficulty": "Intermediate"},
    "data_044": {"name": "Clustering", "tools": "K-means", "difficulty": "Intermediate"},
    "data_045": {"name": "Classification", "tools": "Scikit-learn", "difficulty": "Intermediate"},
    "data_046": {"name": "Regression Models", "tools": "XGBoost", "difficulty": "Intermediate"},
    "data_047": {"name": "Model Training", "tools": "PyTorch", "difficulty": "Advanced"},
    "data_048": {"name": "Model Evaluation", "tools": "Scikit-learn", "difficulty": "Intermediate"},
    "data_049": {"name": "Hyperparameter Tuning", "tools": "Optuna", "difficulty": "Advanced"},
    "data_050": {"name": "Model Deployment", "tools": "Docker", "difficulty": "Advanced"},
    "data_051": {"name": "Feature Store", "tools": "Feast", "difficulty": "Advanced"},
    "data_052": {"name": "Data Lake", "tools": "Delta Lake", "difficulty": "Advanced"},
    "data_053": {"name": "Data Mesh", "tools": "Custom Architecture", "difficulty": "Advanced"},
    "data_054": {"name": "Master Data Management", "tools": "Talend", "difficulty": "Advanced"},
    "data_055": {"name": "Data Integration", "tools": "Apache NiFi", "difficulty": "Advanced"},
    "data_056": {"name": "Service Meshes", "tools": "Istio", "difficulty": "Advanced"},
    "data_057": {"name": "API Gateway", "tools": "Kong", "difficulty": "Advanced"},
    "data_058": {"name": "Event Processing", "tools": "Kafka Streams", "difficulty": "Advanced"},
    "data_059": {"name": "Stream Processing", "tools": "Apache Flink", "difficulty": "Advanced"},
    "data_060": {"name": "Batch Processing", "tools": "Spark", "difficulty": "Advanced"},
    "data_061": {"name": "Lambda Architecture", "tools": "Spark + Kafka", "difficulty": "Advanced"},
    "data_062": {"name": "Kappa Architecture", "tools": "Kafka", "difficulty": "Advanced"},
    "data_063": {"name": "Data Pipelines", "tools": "Airflow", "difficulty": "Advanced"},
    "data_064": {"name": "Workflow Orchestration", "tools": "Argo", "difficulty": "Advanced"},
    "data_065": {"name": "Job Scheduling", "tools": "Cron/Scheduler", "difficulty": "Beginner"},
    "data_066": {"name": "Error Handling", "tools": "Python", "difficulty": "Intermediate"},
    "data_067": {"name": "Retry Mechanisms", "tools": "Python", "difficulty": "Intermediate"},
    "data_068": {"name": "Monitoring", "tools": "Prometheus", "difficulty": "Advanced"},
    "data_069": {"name": "Alerting", "tools": "AlertManager", "difficulty": "Advanced"},
    "data_070": {"name": "Logging", "tools": "ELK Stack", "difficulty": "Advanced"},
    "data_071": {"name": "Tracing", "tools": "Jaeger", "difficulty": "Advanced"},
    "data_072": {"name": "Performance Tuning", "tools": "Python", "difficulty": "Advanced"},
    "data_073": {"name": "Resource Optimization", "tools": "Kubernetes", "difficulty": "Advanced"},
    "data_074": {"name": "Containerization", "tools": "Docker", "difficulty": "Intermediate"},
    "data_075": {"name": "Orchestration", "tools": "Kubernetes", "difficulty": "Advanced"},
    "data_076": {"name": "Infrastructure as Code", "tools": "Terraform", "difficulty": "Advanced"},
    "data_077": {"name": "CI/CD Pipelines", "tools": "GitLab CI", "difficulty": "Advanced"},
    "data_078": {"name": "Testing Automation", "tools": "Pytest", "difficulty": "Intermediate"},
    "data_079": {"name": "Data Unit Tests", "tools": "Great Expectations", "difficulty": "Intermediate"},
    "data_080": {"name": "Integration Tests", "tools": "Python", "difficulty": "Advanced"},
    "data_081": {"name": "Security", "tools": "HashiCorp Vault", "difficulty": "Advanced"},
    "data_082": {"name": "Encryption", "tools": "PyCryptodome", "difficulty": "Advanced"},
    "data_083": {"name": "Access Control", "tools": "Apache Ranger", "difficulty": "Advanced"},
    "data_084": {"name": "Compliance", "tools": "Custom Solutions", "difficulty": "Advanced"},
    "data_085": {"name": "Audit Logging", "tools": "ELK Stack", "difficulty": "Advanced"},
    "data_086": {"name": "GDPR Compliance", "tools": "Python", "difficulty": "Advanced"},
    "data_087": {"name": "Data Privacy", "tools": "Differential Privacy", "difficulty": "Advanced"},
    "data_088": {"name": "Anonymization", "tools": "ARX", "difficulty": "Advanced"},
    "data_089": {"name": "PII Detection", "tools": "Presidio", "difficulty": "Advanced"},
    "data_090": {"name": "Data Masking", "tools": "Python", "difficulty": "Intermediate"},
    "data_091": {"name": "Documentation", "tools": "Markdown", "difficulty": "Beginner"},
    "data_092": {"name": "Data Lineage", "tools": "OpenLineage", "difficulty": "Advanced"},
    "data_093": {"name": "Impact Analysis", "tools": "Custom Solutions", "difficulty": "Advanced"},
    "data_094": {"name": "SLA Management", "tools": "Custom Solutions", "difficulty": "Advanced"},
    "data_095": {"name": "Cost Optimization", "tools": "Cloud Tools", "difficulty": "Advanced"},
    "data_096": {"name": "Capacity Planning", "tools": "Analytics", "difficulty": "Advanced"},
    "data_097": {"name": "Benchmarking", "tools": "Python", "difficulty": "Advanced"},
    "data_098": {"name": "Load Testing", "tools": "Apache JMeter", "difficulty": "Advanced"},
    "data_099": {"name": "Stress Testing", "tools": "Locust", "difficulty": "Advanced"},
    "data_100": {"name": "Data Innovation", "tools": "Experimental", "difficulty": "Advanced"},
}

# Define 100 projects for Cloud & DevOps
CLOUD_DEVOPS_PROJECTS = {
    "cloud_001": {"name": "Virtual Machine Setup", "platform": "AWS", "difficulty": "Beginner"},
    "cloud_002": {"name": "Cloud Storage", "platform": "GCP", "difficulty": "Beginner"},
    "cloud_003": {"name": "Database as Service", "platform": "Azure", "difficulty": "Beginner"},
    "cloud_004": {"name": "Load Balancing", "platform": "AWS ELB", "difficulty": "Intermediate"},
    "cloud_005": {"name": "Auto Scaling", "platform": "AWS ASG", "difficulty": "Intermediate"},
    "cloud_006": {"name": "Content Delivery", "platform": "CloudFront", "difficulty": "Beginner"},
    "cloud_007": {"name": "DNS Management", "platform": "Route 53", "difficulty": "Beginner"},
    "cloud_008": {"name": "Networking Setup", "platform": "VPC", "difficulty": "Intermediate"},
    "cloud_009": {"name": "Firewall Rules", "platform": "Security Groups", "difficulty": "Intermediate"},
    "cloud_010": {"name": "DDoS Protection", "platform": "AWS Shield", "difficulty": "Advanced"},
    "cloud_011": {"name": "VPN Setup", "platform": "AWS VPN", "difficulty": "Intermediate"},
    "cloud_012": {"name": "Hybrid Cloud", "platform": "AWS Outposts", "difficulty": "Advanced"},
    "cloud_013": {"name": "Multi-cloud Strategy", "platform": "Custom", "difficulty": "Advanced"},
    "cloud_014": {"name": "Cloud Migration", "platform": "AWS DMS", "difficulty": "Advanced"},
    "cloud_015": {"name": "Disaster Recovery", "platform": "AWS DR", "difficulty": "Advanced"},
    "cloud_016": {"name": "Backup Strategy", "platform": "AWS Backup", "difficulty": "Intermediate"},
    "cloud_017": {"name": "High Availability", "platform": "Multi-AZ", "difficulty": "Advanced"},
    "cloud_018": {"name": "Containerization", "platform": "Docker", "difficulty": "Intermediate"},
    "cloud_019": {"name": "Container Registry", "platform": "ECR", "difficulty": "Intermediate"},
    "cloud_020": {"name": "Kubernetes Cluster", "platform": "EKS", "difficulty": "Advanced"},
    "cloud_021": {"name": "Helm Charts", "platform": "Kubernetes", "difficulty": "Advanced"},
    "cloud_022": {"name": "Service Mesh", "platform": "Istio", "difficulty": "Advanced"},
    "cloud_023": {"name": "Serverless Functions", "platform": "Lambda", "difficulty": "Beginner"},
    "cloud_024": {"name": "API Gateway", "platform": "AWS API Gateway", "difficulty": "Intermediate"},
    "cloud_025": {"name": "Message Queues", "platform": "SQS", "difficulty": "Intermediate"},
    "cloud_026": {"name": "Event Streaming", "platform": "Kinesis", "difficulty": "Advanced"},
    "cloud_027": {"name": "Microservices", "platform": "ECS", "difficulty": "Advanced"},
    "cloud_028": {"name": "CI/CD Pipeline", "platform": "CodePipeline", "difficulty": "Advanced"},
    "cloud_029": {"name": "Infrastructure as Code", "platform": "CloudFormation", "difficulty": "Advanced"},
    "cloud_030": {"name": "Configuration Management", "platform": "Terraform", "difficulty": "Advanced"},
    "cloud_031": {"name": "Provisioning", "platform": "Ansible", "difficulty": "Advanced"},
    "cloud_032": {"name": "Container Orchestration", "platform": "Docker Swarm", "difficulty": "Intermediate"},
    "cloud_033": {"name": "Cluster Management", "platform": "Kubernetes", "difficulty": "Advanced"},
    "cloud_034": {"name": "Pod Autoscaling", "platform": "HPA", "difficulty": "Intermediate"},
    "cloud_035": {"name": "Resource Limits", "platform": "Kubernetes", "difficulty": "Intermediate"},
    "cloud_036": {"name": "StatefulSet", "platform": "Kubernetes", "difficulty": "Advanced"},
    "cloud_037": {"name": "DaemonSet", "platform": "Kubernetes", "difficulty": "Intermediate"},
    "cloud_038": {"name": "Job Scheduling", "platform": "Kubernetes CronJob", "difficulty": "Intermediate"},
    "cloud_039": {"name": "Persistent Volumes", "platform": "Kubernetes", "difficulty": "Intermediate"},
    "cloud_040": {"name": "Storage Classes", "platform": "Kubernetes", "difficulty": "Advanced"},
    "cloud_041": {"name": "Monitoring", "platform": "Prometheus", "difficulty": "Advanced"},
    "cloud_042": {"name": "Metrics Collection", "platform": "CloudWatch", "difficulty": "Intermediate"},
    "cloud_043": {"name": "Log Aggregation", "platform": "ELK Stack", "difficulty": "Advanced"},
    "cloud_044": {"name": "Distributed Tracing", "platform": "Jaeger", "difficulty": "Advanced"},
    "cloud_045": {"name": "Alert Management", "platform": "PagerDuty", "difficulty": "Advanced"},
    "cloud_046": {"name": "Dashboarding", "platform": "Grafana", "difficulty": "Advanced"},
    "cloud_047": {"name": "Security Scanning", "platform": "AWS Security Hub", "difficulty": "Advanced"},
    "cloud_048": {"name": "Compliance Monitoring", "platform": "Config", "difficulty": "Advanced"},
    "cloud_049": {"name": "Secret Management", "platform": "Secrets Manager", "difficulty": "Advanced"},
    "cloud_050": {"name": "Key Management", "platform": "KMS", "difficulty": "Advanced"},
    "cloud_051": {"name": "Identity Management", "platform": "IAM", "difficulty": "Intermediate"},
    "cloud_052": {"name": "Access Control", "platform": "RBAC", "difficulty": "Advanced"},
    "cloud_053": {"name": "Audit Logging", "platform": "CloudTrail", "difficulty": "Intermediate"},
    "cloud_054": {"name": "Vulnerability Scanning", "platform": "Inspector", "difficulty": "Advanced"},
    "cloud_055": {"name": "Patch Management", "platform": "Systems Manager", "difficulty": "Intermediate"},
    "cloud_056": {"name": "Backup Automation", "platform": "AWS Backup", "difficulty": "Intermediate"},
    "cloud_057": {"name": "Replication Setup", "platform": "S3 Replication", "difficulty": "Intermediate"},
    "cloud_058": {"name": "Geo-redundancy", "platform": "Multi-region", "difficulty": "Advanced"},
    "cloud_059": {"name": "Failover Testing", "platform": "Route 53", "difficulty": "Advanced"},
    "cloud_060": {"name": "RTO/RPO Planning", "platform": "DR Strategy", "difficulty": "Advanced"},
    "cloud_061": {"name": "Cost Analysis", "platform": "Cost Explorer", "difficulty": "Intermediate"},
    "cloud_062": {"name": "Resource Tagging", "platform": "AWS Tags", "difficulty": "Beginner"},
    "cloud_063": {"name": "Cost Optimization", "platform": "Compute Optimizer", "difficulty": "Advanced"},
    "cloud_064": {"name": "Reserved Instances", "platform": "AWS RI", "difficulty": "Intermediate"},
    "cloud_065": {"name": "Spot Instances", "platform": "Spot Fleet", "difficulty": "Intermediate"},
    "cloud_066": {"name": "Savings Plans", "platform": "AWS Savings", "difficulty": "Intermediate"},
    "cloud_067": {"name": "Usage Monitoring", "platform": "Trusted Advisor", "difficulty": "Beginner"},
    "cloud_068": {"name": "Budget Alerts", "platform": "Budgets", "difficulty": "Beginner"},
    "cloud_069": {"name": "Capacity Planning", "platform": "Analytics", "difficulty": "Advanced"},
    "cloud_070": {"name": "Performance Tuning", "platform": "Optimization", "difficulty": "Advanced"},
    "cloud_071": {"name": "Latency Reduction", "platform": "CloudFront", "difficulty": "Intermediate"},
    "cloud_072": {"name": "Database Optimization", "platform": "RDS", "difficulty": "Advanced"},
    "cloud_073": {"name": "Query Performance", "platform": "Performance Insights", "difficulty": "Advanced"},
    "cloud_074": {"name": "Connection Pooling", "platform": "RDS Proxy", "difficulty": "Advanced"},
    "cloud_075": {"name": "Caching Strategy", "platform": "ElastiCache", "difficulty": "Advanced"},
    "cloud_076": {"name": "Session Management", "platform": "DynamoDB", "difficulty": "Intermediate"},
    "cloud_077": {"name": "State Management", "platform": "State Machines", "difficulty": "Advanced"},
    "cloud_078": {"name": "Workflow Automation", "platform": "Step Functions", "difficulty": "Advanced"},
    "cloud_079": {"name": "Data Pipeline", "platform": "Glue", "difficulty": "Advanced"},
    "cloud_080": {"name": "ETL Jobs", "platform": "AWS Glue", "difficulty": "Advanced"},
    "cloud_081": {"name": "Batch Processing", "platform": "Batch", "difficulty": "Advanced"},
    "cloud_082": {"name": "Stream Processing", "platform": "Kinesis", "difficulty": "Advanced"},
    "cloud_083": {"name": "Analytics Setup", "platform": "Athena", "difficulty": "Intermediate"},
    "cloud_084": {"name": "Data Warehouse", "platform": "Redshift", "difficulty": "Advanced"},
    "cloud_085": {"name": "Machine Learning", "platform": "SageMaker", "difficulty": "Advanced"},
    "cloud_086": {"name": "AI Services", "platform": "Rekognition", "difficulty": "Advanced"},
    "cloud_087": {"name": "Serverless ML", "platform": "Lambda + Models", "difficulty": "Advanced"},
    "cloud_088": {"name": "Model Training", "platform": "SageMaker", "difficulty": "Advanced"},
    "cloud_089": {"name": "Model Deployment", "platform": "SageMaker", "difficulty": "Advanced"},
    "cloud_090": {"name": "A/B Testing", "platform": "Custom", "difficulty": "Intermediate"},
    "cloud_091": {"name": "Feature Flags", "platform": "Launch Darkly", "difficulty": "Intermediate"},
    "cloud_092": {"name": "Blue-Green Deployment", "platform": "CodeDeploy", "difficulty": "Advanced"},
    "cloud_093": {"name": "Canary Deployment", "platform": "CodeDeploy", "difficulty": "Advanced"},
    "cloud_094": {"name": "Rolling Deployment", "platform": "ASG", "difficulty": "Intermediate"},
    "cloud_095": {"name": "Rollback Strategy", "platform": "Custom", "difficulty": "Advanced"},
    "cloud_096": {"name": "Smoke Testing", "platform": "CodePipeline", "difficulty": "Intermediate"},
    "cloud_097": {"name": "Load Testing", "platform": "Load Testing Tool", "difficulty": "Advanced"},
    "cloud_098": {"name": "Chaos Engineering", "platform": "Gremlin", "difficulty": "Advanced"},
    "cloud_099": {"name": "Incident Response", "platform": "Custom", "difficulty": "Advanced"},
    "cloud_100": {"name": "Disaster Drills", "platform": "Custom", "difficulty": "Advanced"},
}

# Define 100 projects for Systems & Embedded
SYSTEMS_EMBEDDED_PROJECTS = {
    "sys_001": {"name": "Hello World", "platform": "Linux", "difficulty": "Beginner"},
    "sys_002": {"name": "File I/O Operations", "platform": "C", "difficulty": "Beginner"},
    "sys_003": {"name": "Process Management", "platform": "Unix", "difficulty": "Intermediate"},
    "sys_004": {"name": "Thread Programming", "platform": "POSIX", "difficulty": "Intermediate"},
    "sys_005": {"name": "Memory Management", "platform": "C", "difficulty": "Intermediate"},
    "sys_006": {"name": "Socket Programming", "platform": "TCP/IP", "difficulty": "Intermediate"},
    "sys_007": {"name": "Network Protocol", "platform": "C", "difficulty": "Advanced"},
    "sys_008": {"name": "Linux Kernel Module", "platform": "Linux", "difficulty": "Advanced"},
    "sys_009": {"name": "Device Driver", "platform": "C", "difficulty": "Advanced"},
    "sys_010": {"name": "System Call Implementation", "platform": "Linux", "difficulty": "Advanced"},
    "sys_011": {"name": "Arduino LED Control", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_012": {"name": "Arduino Sensors", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_013": {"name": "PWM Control", "platform": "Microcontroller", "difficulty": "Beginner"},
    "sys_014": {"name": "UART Communication", "platform": "Embedded C", "difficulty": "Intermediate"},
    "sys_015": {"name": "SPI Interface", "platform": "Embedded C", "difficulty": "Intermediate"},
    "sys_016": {"name": "I2C Communication", "platform": "Embedded C", "difficulty": "Intermediate"},
    "sys_017": {"name": "ADC Sampling", "platform": "Microcontroller", "difficulty": "Beginner"},
    "sys_018": {"name": "DAC Output", "platform": "Microcontroller", "difficulty": "Beginner"},
    "sys_019": {"name": "Timer Interrupt", "platform": "Embedded C", "difficulty": "Intermediate"},
    "sys_020": {"name": "Real-Time OS", "platform": "FreeRTOS", "difficulty": "Advanced"},
    "sys_021": {"name": "Motor Control", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_022": {"name": "Servo Control", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_023": {"name": "Stepper Motor", "platform": "Embedded C", "difficulty": "Intermediate"},
    "sys_024": {"name": "DC Motor PWM", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_025": {"name": "Robotics Platform", "platform": "ROS", "difficulty": "Advanced"},
    "sys_026": {"name": "Drone Control", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_027": {"name": "Robot Arm", "platform": "Robotic Arm Kit", "difficulty": "Advanced"},
    "sys_028": {"name": "Autonomous Vehicle", "platform": "Python", "difficulty": "Advanced"},
    "sys_029": {"name": "Temperature Monitoring", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_030": {"name": "Humidity Sensor", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_031": {"name": "Pressure Sensor", "platform": "Embedded C", "difficulty": "Beginner"},
    "sys_032": {"name": "Gas Sensor", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_033": {"name": "Motion Detection", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_034": {"name": "Distance Measurement", "platform": "Ultrasonic Sensor", "difficulty": "Beginner"},
    "sys_035": {"name": "Light Sensor", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_036": {"name": "Acceleration Monitoring", "platform": "IMU", "difficulty": "Intermediate"},
    "sys_037": {"name": "Gyroscope Control", "platform": "Embedded C", "difficulty": "Intermediate"},
    "sys_038": {"name": "GPS Tracking", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_039": {"name": "RFID Reader", "platform": "Embedded C", "difficulty": "Intermediate"},
    "sys_040": {"name": "NFC Interface", "platform": "Arduino", "difficulty": "Advanced"},
    "sys_041": {"name": "Bluetooth Module", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_042": {"name": "WiFi Module", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_043": {"name": "Cellular Modem", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_044": {"name": "MQTT Client", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_045": {"name": "CoAP Implementation", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_046": {"name": "Zigbee Node", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_047": {"name": "LoRaWAN Device", "platform": "Arduino", "difficulty": "Advanced"},
    "sys_048": {"name": "NB-IoT Module", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_049": {"name": "Data Logging", "platform": "EEPROM", "difficulty": "Intermediate"},
    "sys_050": {"name": "SD Card Interface", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_051": {"name": "LCD Display", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_052": {"name": "OLED Screen", "platform": "Embedded C", "difficulty": "Beginner"},
    "sys_053": {"name": "Touch Screen", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_054": {"name": "LED Matrix", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_055": {"name": "7-Segment Display", "platform": "Embedded C", "difficulty": "Beginner"},
    "sys_056": {"name": "Keyboard Input", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_057": {"name": "Button Debouncing", "platform": "Embedded C", "difficulty": "Intermediate"},
    "sys_058": {"name": "Rotary Encoder", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_059": {"name": "Joystick Control", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_060": {"name": "Potentiometer Reading", "platform": "Embedded C", "difficulty": "Beginner"},
    "sys_061": {"name": "LED Blinking", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_062": {"name": "RGB LED Control", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_063": {"name": "LED Fading", "platform": "Embedded C", "difficulty": "Beginner"},
    "sys_064": {"name": "LED Pattern Generator", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_065": {"name": "Traffic Light Controller", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_066": {"name": "Alarm System", "platform": "Embedded C", "difficulty": "Intermediate"},
    "sys_067": {"name": "Home Automation", "platform": "Arduino", "difficulty": "Advanced"},
    "sys_068": {"name": "Smart Lighting", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_069": {"name": "Smart Thermostat", "platform": "Arduino", "difficulty": "Advanced"},
    "sys_070": {"name": "Security System", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_071": {"name": "Lock Control", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_072": {"name": "Access Control", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_073": {"name": "Lighting Control", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_074": {"name": "Appliance Control", "platform": "Embedded C", "difficulty": "Intermediate"},
    "sys_075": {"name": "Energy Monitoring", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_076": {"name": "Power Management", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_077": {"name": "Battery Monitor", "platform": "Arduino", "difficulty": "Intermediate"},
    "sys_078": {"name": "Solar Charging", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_079": {"name": "Bootloader Implementation", "platform": "Assembly", "difficulty": "Advanced"},
    "sys_080": {"name": "Firmware Update", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_081": {"name": "OTA Update", "platform": "Arduino", "difficulty": "Advanced"},
    "sys_082": {"name": "Cryptography Module", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_083": {"name": "Authentication", "platform": "Arduino", "difficulty": "Advanced"},
    "sys_084": {"name": "Encryption", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_085": {"name": "Secure Boot", "platform": "ARM", "difficulty": "Advanced"},
    "sys_086": {"name": "Trusted Execution", "platform": "TEE", "difficulty": "Advanced"},
    "sys_087": {"name": "Hardware Security", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_088": {"name": "Performance Profiling", "platform": "C", "difficulty": "Advanced"},
    "sys_089": {"name": "Memory Optimization", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_090": {"name": "Power Optimization", "platform": "Arduino", "difficulty": "Advanced"},
    "sys_091": {"name": "Testing Framework", "platform": "C", "difficulty": "Intermediate"},
    "sys_092": {"name": "Debugging Techniques", "platform": "GDB", "difficulty": "Intermediate"},
    "sys_093": {"name": "JTAG Debugging", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_094": {"name": "Serial Debugging", "platform": "Arduino", "difficulty": "Beginner"},
    "sys_095": {"name": "Protocol Implementation", "platform": "C", "difficulty": "Advanced"},
    "sys_096": {"name": "Driver Development", "platform": "C", "difficulty": "Advanced"},
    "sys_097": {"name": "Hardware Abstraction", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_098": {"name": "Firmware Reverse Engineering", "platform": "Embedded C", "difficulty": "Advanced"},
    "sys_099": {"name": "Hardware Emulation", "platform": "QEMU", "difficulty": "Advanced"},
    "sys_100": {"name": "Custom Board Design", "platform": "Hardware Design", "difficulty": "Advanced"},
}

def create_project_structure(category, project_id, project_name, metadata):
    """Create directory structure for a project"""
    base_path = Path(f"{category}_{project_id}")
    base_path.mkdir(exist_ok=True)

    # Create README
    readme_content = f"""# {project_name}

## Category: {category.replace('_', ' ').title()}
## ID: {project_id}

### Overview
{project_name} is a comprehensive learning project that covers essential concepts in {category.lower()} development.

### Learning Objectives
- Understand core principles
- Implement practical solutions
- Apply best practices

### Skills Covered
- Technical Implementation
- Problem Solving
- Code Quality

### Prerequisites
- Basic programming knowledge
- Development environment setup
- Fundamental computer science concepts

### Project Structure
```
{project_id}/
├── README.md
├── metadata.json
├── notebooks/
│   └── project.ipynb
└── requirements.txt
```

### Getting Started
1. Review the project objectives
2. Complete the Jupyter notebook
3. Implement all requirements
4. Test your solution

### Deliverables
- Functional implementation
- Documentation
- Test cases

### Resources
- Official documentation
- Tutorials and guides
- Community forums

### Assessment
- Code review
- Functionality testing
- Best practice evaluation

---
*Last Updated: 2025-11-18*
"""

    (base_path / "README.md").write_text(readme_content)

    # Create metadata.json
    metadata_json = {
        "id": project_id,
        "name": project_name,
        "category": category,
        "difficulty": metadata.get("difficulty", "Intermediate"),
        "duration_weeks": 2 if metadata.get("difficulty") == "Beginner" else 4 if metadata.get("difficulty") == "Intermediate" else 6,
        "technologies": metadata.get("lang") or metadata.get("engine") or metadata.get("platform") or metadata.get("tools", ""),
        "objectives": ["Understand core concepts", "Implement solution", "Test thoroughly"],
        "skills": ["Programming", "Problem Solving", "Best Practices"],
        "prerequisites": ["Basic programming", "Environment setup"],
        "deliverables": ["Working code", "Documentation", "Tests"]
    }

    (base_path / "metadata.json").write_text(json.dumps(metadata_json, indent=2, ensure_ascii=False))

    # Create notebooks directory and starter notebook
    notebooks_dir = base_path / "notebooks"
    notebooks_dir.mkdir(exist_ok=True)

    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {project_name}\n", f"\n", "This notebook guides you through the project implementation."]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 1. Learning Objectives\n", f"\n- Objective 1\n", "- Objective 2\n", "- Objective 3"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# Setup and imports\n", "# Add your imports here"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 2. Main Implementation\n", "\n", "Implement your solution here."]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# Your implementation code here\n", "pass"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 3. Testing\n", "\n", "Test your implementation."]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# Test your code\n", "# assert condition, 'error message'"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Summary\n", "\nYou have completed this project!"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.9.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    (notebooks_dir / "project.ipynb").write_text(json.dumps(notebook_content, indent=2, ensure_ascii=False))

def main():
    print("=" * 80)
    print("🚀 600개 도메인별 프로젝트 생성 중...")
    print("=" * 80)

    all_projects = {
        "practical_projects": WEB_DEVELOPMENT_PROJECTS,
        "mobile_projects": MOBILE_DEVELOPMENT_PROJECTS,
        "game_projects": GAME_DEVELOPMENT_PROJECTS,
        "data_projects": DATA_ENGINEERING_PROJECTS,
        "cloud_projects": CLOUD_DEVOPS_PROJECTS,
        "system_projects": SYSTEMS_EMBEDDED_PROJECTS,
    }

    domain_names = {
        "practical_projects": "Web Development",
        "mobile_projects": "Mobile Development",
        "game_projects": "Game Development",
        "data_projects": "Data Engineering",
        "cloud_projects": "Cloud & DevOps",
        "system_projects": "Systems & Embedded",
    }

    # Create main domain directories
    for domain_dir in all_projects.keys():
        Path(domain_dir).mkdir(exist_ok=True)

    total_count = 0
    domain_stats = {}

    # Generate projects for each domain
    for domain_key, projects in all_projects.items():
        domain_name = domain_names[domain_key]
        domain_path = Path(domain_key)
        domain_count = 0

        print(f"\n📂 {domain_name} 프로젝트 생성 중...")

        for project_id, project_data in projects.items():
            project_name = project_data["name"]

            # Create subdirectory for project within domain
            project_dir = domain_path / f"{project_id}"
            project_dir.mkdir(parents=True, exist_ok=True)

            # Create README
            readme_content = f"""# {project_name}

## Domain: {domain_name}
## Project ID: {project_id}

### Overview
{project_name} is a comprehensive learning project for {domain_name.lower()}.

### Project Details
- **Difficulty**: {project_data.get('difficulty', 'Intermediate')}
- **Technology**: {project_data.get('lang') or project_data.get('engine') or project_data.get('platform') or project_data.get('tools', 'Various')}
- **Duration**: 2-6 weeks

### Learning Objectives
- Master core concepts
- Implement practical skills
- Apply industry best practices

### Getting Started
1. Review project requirements
2. Set up your development environment
3. Complete the learning notebook
4. Implement the solution

### Resources
- Jupyter Notebook: `notebooks/project.ipynb`
- Project Metadata: `metadata.json`

---
Created: 2025-11-18
"""
            (project_dir / "README.md").write_text(readme_content)

            # Create metadata.json
            metadata_json = {
                "id": project_id,
                "name": project_name,
                "domain": domain_name,
                "difficulty": project_data.get('difficulty', 'Intermediate'),
                "duration_weeks": 2 if project_data.get('difficulty') == 'Beginner' else 4 if project_data.get('difficulty') == 'Intermediate' else 6,
                "technology": project_data.get('lang') or project_data.get('engine') or project_data.get('platform') or project_data.get('tools', ''),
                "skills": ["Implementation", "Problem Solving", "Best Practices"],
                "deliverables": ["Code", "Documentation", "Tests"]
            }
            (project_dir / "metadata.json").write_text(json.dumps(metadata_json, indent=2, ensure_ascii=False))

            # Create notebook
            notebooks_dir = project_dir / "notebooks"
            notebooks_dir.mkdir(exist_ok=True)

            notebook = {
                "cells": [
                    {
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [f"# {project_name}\n", f"\n## {domain_name}"]
                    },
                    {
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": ["## Learning Objectives\n", "- Understand concepts\n", "- Implement solution\n", "- Test thoroughly"]
                    },
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": ["# Setup and imports\n", "pass"]
                    },
                    {
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": ["## Implementation\n", "Add your code below."]
                    },
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": ["# Your implementation\n", "pass"]
                    }
                ],
                "metadata": {
                    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.9.0"}
                },
                "nbformat": 4,
                "nbformat_minor": 4
            }
            (notebooks_dir / "project.ipynb").write_text(json.dumps(notebook, indent=2, ensure_ascii=False))

            domain_count += 1
            total_count += 1

            if domain_count % 20 == 0:
                print(f"  ✅ {domain_count}개 프로젝트 생성 완료")

        domain_stats[domain_name] = domain_count
        print(f"✅ {domain_name}: {domain_count}개 완료")

    # Create master catalog
    catalog = {
        "total_projects": total_count,
        "domains": domain_stats,
        "domains_detail": {
            "web_development": list(WEB_DEVELOPMENT_PROJECTS.keys()),
            "mobile_development": list(MOBILE_DEVELOPMENT_PROJECTS.keys()),
            "game_development": list(GAME_DEVELOPMENT_PROJECTS.keys()),
            "data_engineering": list(DATA_ENGINEERING_PROJECTS.keys()),
            "cloud_devops": list(CLOUD_DEVOPS_PROJECTS.keys()),
            "systems_embedded": list(SYSTEMS_EMBEDDED_PROJECTS.keys()),
        }
    }

    Path("domain_catalog.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False))

    print("\n" + "=" * 80)
    print("✨ 완료!")
    print("=" * 80)
    print(f"\n📊 생성 통계:")
    for domain, count in domain_stats.items():
        print(f"  - {domain}: {count}개")
    print(f"\n총 프로젝트: {total_count}개")
    print(f"📁 저장 위치: 각 도메인별 디렉토리")
    print(f"📋 마스터 카탈로그: domain_catalog.json")

if __name__ == "__main__":
    main()
