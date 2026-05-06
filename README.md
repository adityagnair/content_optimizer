# Creator Content Posting Optimization System

## Team Information
- **Team Name**: [Powerhouse3]
- **Year**: [First Year]
- **All-Female Team**: [No]

## Architecture Overview

**Instructions**: Describe your approach in 200 words or less. Address the following:
Content Posting Optimization SystemThis project implements a Multi-Objective Optimization Engine designed to maximize social media engagement through data-driven scheduling and platform selection. The system addresses the complex decision-making process of identifying peak performance windows for SHORT and LONG form content across platforms like Instagram and YouTube.  Architecture & FrameworkThe system is built with a modular Python-based architecture, utilizing a Decoupled Logic Layer to ensure high computational efficiency (target latency 1.0s).  Data Layer: Managed by data_loader.py, this layer ingests CSV-based datasets including creators.csv, platform_activity.csv, and historical_engagement.csv.  Optimization Engine: The recommender.py module executes a Joint Optimization Algorithm, simulating 48 unique (Platform Time Slot) combinations per content item to identify the global maximum engagement score.  Interface Layer: Supports both a CLI-driven utility for batch processing and a Flask/FastAPI backend (app.py) for real-time recommendation requests.  Optimization MethodsThe core logic utilizes a Weighted Scoring Heuristic (50% Engagement, 20% Timing, 15% Platform Quality, 15% Efficiency). It effectively balances creator-specific historical trends with real-time platform activity scores to provide deterministic POST_NOW or SCHEDULE decisions. 

---

*Keep your description concise and focused on your core decision-making logic.*

**Note:** Please do not change the format or spelling of anything in this README. The fields are extracted using a script, so any changes to the structure or formatting may break the extraction process.
