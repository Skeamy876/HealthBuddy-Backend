# HealthBuddy-Backend
AI Symptom Checker and Recommendation Engine

# 🧠 AI Health Symptom Checker + Recommendation Engine

A voice-enabled AI assistant that accepts symptom input (voice or text), analyzes them using a LangChain agent powered by Gemini models, and returns ICD-10-based condition predictions, urgency scores, and treatment recommendations.

## 🌐 Overview

This project aims to:

- Enable users to describe symptoms via voice or text.
- Retrieve probable conditions from ICD-10 + medical data.
- Offer relevant treatment suggestions and urgency levels.
- Use Retrieval-Augmented Generation (RAG) for high-quality responses.
- Remain fully open-source and privacy-conscious.

---

## 🚀 Features

- ✅ Symptom input via text or voice
- ✅ Whisper-based Speech-to-Text (STT) - tbd
- ✅ Gemini-powered diagnosis logic
- ✅ LangChain agent + RAG pipeline
- ✅ ICD-10 Code Mapping + Sync
- ✅ Recommendations + Urgency Scoring
- ✅ Coqui TTS voice output - tbd
- ✅ Frontend with React + Tailwind UI

---

## 🏗️ Architecture

```plaintext
User Input (Voice/Text)
   ↓
Whisper STT - tbd ( API)
   ↓
LangChain Agent → Gemini 1.5 Pro
            ↘
    RAG: ICD-10 + Medline + Mayo
            ↓
Recommendations (Text)
   ↓
Coqui TTS tbd (Voice Output)

---

## 🔒 Rate Limiting

The API includes session-based rate limiting for production environments:

- **Production Environment** (`ENVIRONMENT=Prod` or `ENVIRONMENT=production`): 5 requests per session
- **Non-Production Environments**: Unlimited requests

### Session Identification

Sessions are identified using:
1. `session-id` header (recommended)
2. `x-session-id` header (alternative)
3. Client IP address (fallback)

### Usage Examples

```bash
# With session ID (recommended)
curl -H "session-id: your-session-id" http://localhost:8000/

# Alternative header
curl -H "x-session-id: your-session-id" http://localhost:8000/

# Without session header (uses IP as fallback)
curl http://localhost:8000/
```

### Rate Limit Response

When the rate limit is exceeded, the API returns HTTP 429 with:

```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 5 requests per session allowed in production environment",
  "session_id": "your-session-id"
}
```

