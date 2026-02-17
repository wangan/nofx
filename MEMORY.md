# Memory

## 🎯 Project: $100k Trading Challenge
- **Start Date**: 2026-01-27
- **Current Equity**: $156.63 (as of 2026-02-18 03:00)
- **Goal**: Reach $100,000 using AI automated trading system.

## ⚙️ System Configuration
- **Agent**: OpenClaw (Antigravity)
- **Database**: `/app/nofx-stack/nofx/data/data.db`
- **Notifications**: Telegram (ID: `1049260243`) via Cron + `hourly_report.py`.

## 📜 Development & Deployment Protocol
- **Code Modification**: Always modify the **Go source code** (`.go` files) for strategy logic, prompt handling, and execution rules.
- **Git Workflow**: After every optimization or iteration (code change), **commit and push** to the forked repository (`wangan/nofx`).
- **Build Process**: Do NOT use hot-patching (DB direct edits) for permanent changes.
    1. Modify Source Code.
    2. Rebuild Docker Image (`docker build -t nofx-trading .`).
    3. Restart Container (`docker restart nofx-trading`).
- **Strategy Evolution**:
    - New strategies must be **additive/complementary** to existing successful logic.
    - Avoid replacing working logic entirely; instead, add conditional branches (e.g., "If Trending -> Use Logic A; If Ranging -> Use Logic B").
    - Goal: A robust "All-Weather" strategy portfolio.

## 🧠 Strategy & Rules
- **Mode**: "Sniper Mode" (High conviction, low frequency).
- **Hard Rules**:
    - **Anti-Chasing**: [FATAL RULE] No Shorting if RSI(4H) < 30. No Longing if RSI(4H) > 70.
    - **Trend Following (New)**: If 1H EMA20 > EMA50 (Golden Cross), treat as Bullish regardless of 4H.
    - **RSI Exception**: If 1H Trend is confirmed Bullish, allow holding/longing even if RSI > 70 (Momentum > Mean Reversion).

## 🐛 Known Issues & Bugs
- **2026-02-06**: **Ghost Position Bug** (Fixed in `auto_trader.go`).
- **2026-02-07**: **Macro Bias** (AI fighting strong uptrends due to 4H bearish bias). Addressed via "Force Follow" trend logic.

## 📝 Recent Lessons
- **Market Structure**: "Shorting the hole" (momentum chasing) is the primary cause of losses. Wait for bounces to EMA20/50.
- **Strategy Bias**: Pure mean-reversion fails in strong V-shape recoveries. Need "Momentum Override" logic.
