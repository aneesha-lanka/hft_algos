
# HFT Phase 0 + Phase 1 System

## ✅ What it Includes
- Live tick ingestion from Kite WebSocket
- Option chain & Greek extraction (REST + fallback)
- Kinesis `raw_ticks` stream for storage
- AWS Lambda signal generator → `processed_signals`
- Local consumer for ML pipeline

## 📦 Setup

### 1. Install requirements
```bash
pip install -r requirements.txt
```

### 2. Configure AWS
```bash
aws configure
```

### 3. Generate Access Token
```bash
python utils/generate_access_token.py
```

### 4. Start Stream
```bash
python run_phase_0.py
```

### 5. Lambda Setup
Deploy `lambda_handler.py` in AWS Lambda and connect it to your `raw_ticks` stream.

### 6. Local Signal Consumer
```bash
python ../phase_1/local_consumer/kinesis_local_consumer.py
```
