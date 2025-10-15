# 🔧 Fix Render Memory Error (512MB Exceeded)

## ❌ Problem
```
Deploy failed: Ran out of memory (used over 512MB)
```

Your backend uses:
- **PyTorch**: ~300-400 MB
- **Transformers**: ~200-300 MB  
- **Sentence-Transformers**: ~100-200 MB
- **Total**: Easily exceeds 512MB free tier limit

---

## ✅ Solutions (Choose One)

### **Solution 1: Upgrade to Starter Plan (RECOMMENDED)**

Render's free tier has **512MB RAM limit**. You need more memory for AI models.

#### Upgrade to Starter Plan:
- **Cost**: $7/month
- **RAM**: 512MB → **2GB** (4x more memory)
- **No cold starts** (free tier sleeps after 15 minutes)
- **Better performance**

#### How to Upgrade:
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Select your `powergrid-backend` service
3. Click **"Settings"** tab
4. Scroll to **"Instance Type"**
5. Change from **"Free"** to **"Starter"** ($7/mo)
6. Click **"Save Changes"**
7. Redeploy your service

---

### **Solution 2: Optimize Dependencies (Stay on Free Tier)**

Remove AI features and use lightweight alternatives.

#### Create Lightweight Requirements:

Create `backend/requirements-light.txt`:
```txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.0
psycopg2-binary==2.9.9
python-dotenv==1.0.1
# Removed: transformers, torch, sentence-transformers
numpy==1.26.4
scikit-learn==1.5.2
python-multipart==0.0.12
aiosmtplib==3.0.2
twilio==9.3.0
```

#### Update Code to Remove AI:

**Option A: Simple Keyword Matching**
```python
# Replace AI classification with keyword matching
def classify_intent(message: str) -> str:
    message_lower = message.lower()
    
    # Ticket creation keywords
    if any(word in message_lower for word in ['issue', 'problem', 'complaint', 'fault', 'outage', 'not working']):
        return 'create_ticket'
    
    # Status check keywords
    elif any(word in message_lower for word in ['status', 'update', 'track', 'check']):
        return 'check_status'
    
    # Knowledge base keywords
    elif any(word in message_lower for word in ['how to', 'what is', 'help', 'guide', '?']):
        return 'knowledge_search'
    
    else:
        return 'general_query'
```

**Option B: Disable AI Features**
```python
# In ai_classifier.py
def classify_intent(text: str) -> str:
    return 'create_ticket'  # Default action

def extract_ticket_info(text: str) -> dict:
    return {
        'subject': text[:100],
        'description': text,
        'category': 'general'
    }
```

---

### **Solution 3: Use CPU-Only PyTorch (Reduce Memory)**

Install lighter version of PyTorch:

```txt
# In requirements.txt, replace:
torch>=2.2.0

# With CPU-only version:
torch==2.2.0+cpu --index-url https://download.pytorch.org/whl/cpu
```

This reduces PyTorch from ~400MB to ~200MB.

**Update `render.yaml` build command:**
```yaml
buildCommand: pip install --upgrade pip && pip install torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu && pip install -r requirements.txt
```

---

### **Solution 4: Lazy Load Models (Reduce Startup Memory)**

Modify `ai_classifier.py` to load models only when needed:

```python
from functools import lru_cache

# Global variables (don't load at startup)
_classifier = None
_tokenizer = None

@lru_cache(maxsize=1)
def get_classifier():
    """Load classifier only when first needed"""
    global _classifier, _tokenizer
    if _classifier is None:
        from transformers import pipeline
        _classifier = pipeline("zero-shot-classification", 
                              model="facebook/bart-large-mnli",
                              device=-1)  # Force CPU
    return _classifier

# Update all functions to use get_classifier() instead of direct access
def classify_intent(text: str) -> str:
    classifier = get_classifier()  # Lazy load
    result = classifier(text, candidate_labels=INTENT_LABELS)
    # ... rest of code
```

---

## 🎯 My Recommendation

### **For Production: Upgrade to Starter Plan ($7/mo)**

**Pros:**
- ✅ Keep all AI features
- ✅ No code changes needed
- ✅ Better performance (no cold starts)
- ✅ 2GB RAM (plenty of headroom)
- ✅ Professional deployment

**Cons:**
- 💵 Costs $7/month

### **For Demo/Testing: Use Lightweight Version**

**Pros:**
- ✅ Free hosting
- ✅ Core features work (tickets, email, SMS)
- ✅ Fast deployment

**Cons:**
- ❌ No AI classification
- ❌ No semantic search
- ❌ Limited intelligence

---

## 🚀 Quick Fix Steps

### **Option 1: Upgrade (5 minutes)**

1. Open [Render Dashboard](https://dashboard.render.com)
2. Click your service → **Settings**
3. Change **Instance Type**: Free → **Starter**
4. Save and redeploy
5. ✅ Done!

### **Option 2: Remove AI (15 minutes)**

```bash
# 1. Create lightweight requirements
cd backend
cat > requirements-light.txt << EOF
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.0
psycopg2-binary==2.9.9
python-dotenv==1.0.1
numpy==1.26.4
scikit-learn==1.5.2
python-multipart==0.0.12
aiosmtplib==3.0.2
twilio==9.3.0
EOF

# 2. Rename files
mv requirements.txt requirements-full.txt
mv requirements-light.txt requirements.txt

# 3. Update render.yaml
# (Change buildCommand to use requirements.txt)

# 4. Commit and push
git add .
git commit -m "Use lightweight dependencies for free tier"
git push origin main
```

---

## 📊 Memory Comparison

| Configuration | Memory Used | Render Plan | Cost |
|--------------|-------------|-------------|------|
| **Full AI** (PyTorch + Transformers) | ~600-800 MB | Starter | $7/mo |
| **CPU-only PyTorch** | ~400-500 MB | Free (may fail) | Free |
| **No AI** (keywords only) | ~100-150 MB | Free | Free |

---

## 🧪 Test Locally First

Before deploying, test memory usage:

```bash
cd backend

# Check memory usage
python -c "
import sys
import psutil
import os

# Start memory
start_mem = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

# Import heavy libraries
import torch
import transformers
import sentence_transformers

# End memory
end_mem = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

print(f'Memory used: {end_mem - start_mem:.0f} MB')
print(f'Total memory: {end_mem:.0f} MB')
"
```

---

## ❓ Which Solution Should You Choose?

**Choose Upgrade if:**
- You need AI features
- $7/month is acceptable
- This is for production/demo
- You want best performance

**Choose Lightweight if:**
- Budget is $0
- AI features not critical
- Just testing/learning
- Can use simple keyword matching

---

## 📞 Next Steps

Let me know which option you prefer:
1. **Upgrade to Starter** - I'll help configure
2. **Remove AI features** - I'll create lightweight version
3. **Try CPU-only PyTorch** - I'll update config
4. **Explore alternatives** - We can discuss other options

Which would you like to do?
