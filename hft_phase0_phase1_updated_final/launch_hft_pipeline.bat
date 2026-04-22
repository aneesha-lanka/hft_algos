@echo off
title 🚀 Launching HFT Pipeline - Phase 0 & Phase 1 (WebSocket, Kinesis, Screener)
color 0A

echo ============================================================
echo       HIGH FREQUENCY TRADING PIPELINE - PHASE 0 & 1
echo ============================================================

:: Step 1: Check AWS credentials
echo 🔐 Checking AWS CLI credentials...
python phase_0_full/utils/aws_check.py

:: Step 2: Generate Kite API access token
echo 🔑 Generating Kite API token (manual step if needed)...
python phase_0_full/utils/generate_access_token.py

:: Step 3: Launch Phase 0 (WebSocket + Kinesis)
echo 🔁 Starting live tick stream to Kinesis...
python -m phase_0_full.run_phase_0

:: Step 4: Launch Phase 1 Screener
echo 📊 Running Signal Screener Logic (VWAP, SMA, OI)...
python phase_1/phase_1_screener/signal_engine.py

:: Optional: Start Dashboard UI (Uncomment if Streamlit installed)
:: echo 📈 Launching Live Screener Dashboard...
:: streamlit run phase_1_screener/dashboard_app.py

pause
