# Patio

**Repo:** `~/Downloads/Patio`  
**GitHub:** https://github.com/nseluga/patio  
**Status:** active

One-line purpose: Full-stack social betting app for backyard games (Caps, Beerball, Pong, Campus Golf) — place bets against friends (PvP) or the House (CPU), track live bets, climb leaderboard.

## Overview

An end-to-end web application demonstrating complete software engineering execution: user auth, real-time bet management, database design, API design, and multi-platform deployment.

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | React 19, React Router, Axios, Lucide React |
| Backend | Python Flask, JWT auth, SQLAlchemy ORM |
| Database | Supabase (PostgreSQL) |
| Deployment | Vercel (frontend) + Render (backend) |

## Features

- **Authentication:** JWT-based login & registration
- **PvP Bets:** Create custom bets against friends; accept/reject bets
- **House Bets:** Automated odds generation with ~4% house edge (Pong, Beerball, Caps)
- **Live Bet Tracking:** Enter game stats in real-time; confirm results
- **Leaderboard:** Per-player win/loss records, balance, ROI
- **Profile:** Bet history, profile photo, personal stats
- **Bet Generation:** Game-specific odds models (pong_bet_generation.py, beerball_bet_generation.py, caps_bet_generation.py)

## Goals

- Ship a **complete, working product** users can actually deploy and play
- Demonstrate **full-stack engineering:** frontend, backend, database, deployment pipeline
- Build **real-time collaboration** (friends betting simultaneously)
- Design **extensible game system** (easy to add new games and bet types)
- Showcase **responsible engineering practices** (auth, API design, error handling)

## Project Structure

```
Patio/
├── server.js                    # Node entry
├── package.json / package-lock.json
├── backend/
│   ├── app.py                   # Flask app
│   ├── auth.py                  # JWT login/register
│   ├── db.py                    # Database connection
│   ├── models.py                # SQLAlchemy models
│   ├── *_bet_generation.py      # Game-specific odds
│   ├── stats_utils.py           # Utilities
│   ├── requirements.txt          # Python deps
│   └── .flaskenv
├── public/                      # Static assets
├── src/                         # React frontend (if present)
├── PLAN.md / PROGRESS.md        # Development tracking
├── Procfile                     # Heroku/Render deployment config
└── .env.example                 # Template for env vars
```

## Deployment

**Frontend → Vercel**
- Framework auto-detected (Create React App)
- Env var: `REACT_APP_API_URL` → backend URL

**Backend → Render**
- Build: `pip install -r backend/requirements.txt`
- Start: `flask --app backend/app run --host=0.0.0.0 --port=$PORT`
- Database: Supabase PostgreSQL connection string

## Current Status

Deployed and playable. Actively maintained.

## Open Questions

- Additional game types (Campus Golf, KanJam, etc.) — odds model design
- Real-money vs. play-money version; payment integration if applicable
- Mobile app (native React Native vs. PWA)
- Analytics dashboard (house stats, player trends over time)

## Key Files

- `backend/models.py` — database schema (User, Bet, Game, etc.)
- `backend/*_bet_generation.py` — odds algorithms
- `backend/auth.py` — JWT login/register flow
- `CLAUDE.md` — development context and conventions
- `PLAN.md` / `PROGRESS.md` — active development notes

## Links

- **GitHub:** https://github.com/nseluga/patio
- **Live:** [deployed URL — fill in if public]
- **Tech stack:** React 19 + Flask + Supabase + Vercel + Render
