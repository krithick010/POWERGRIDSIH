# 🚀 Deploy Backend to Vercel (Serverless)

## 📋 Prerequisites

- Vercel account (free tier available)
- GitHub repository with your code
- Backend requirements and environment variables ready

---

## 🔧 Step-by-Step Deployment

### 1. **Prepare Backend Files**

✅ Already created:
- `backend/vercel.json` - Vercel configuration
- `backend/.vercelignore` - Files to exclude from deployment
- `backend/requirements.txt` - Python dependencies

### 2. **Deploy to Vercel**

#### Option A: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI globally
npm i -g vercel

# Navigate to backend directory
cd backend

# Login to Vercel
vercel login

# Deploy (first time)
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (Select your account)
# - Link to existing project? No
# - Project name? powergrid-backend (or your choice)
# - In which directory is your code? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

#### Option B: Using Vercel Dashboard

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..." → "Project"**
3. **Import your GitHub repository**
4. Configure:
   - **Root Directory:** `backend`
   - **Framework Preset:** Other
   - Vercel will auto-detect `vercel.json`
5. Click **"Deploy"**

---

## 🔐 Environment Variables

### Add in Vercel Dashboard:

Go to: **Project Settings → Environment Variables**

Add all these variables:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Gmail SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# Twilio SMS
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+15855802717

# API Configuration
ALLOWED_ORIGINS=https://your-netlify-site.netlify.app

# Python Version
PYTHON_VERSION=3.12
```

---

## ⚠️ Important Considerations

### 🚨 Limitations of Vercel Serverless:

1. **Cold Starts:** First request may be slow (serverless functions spin up)
2. **Execution Time Limit:** 10 seconds on free tier, 60 seconds on Pro
3. **Memory Limit:** 1024 MB on free tier
4. **AI Models:** Large models (transformers, torch) may exceed size limits
5. **File System:** Read-only, cannot write to disk
6. **Long-Running Tasks:** Not suitable for background jobs

### 🎯 Recommended For:
- ✅ Simple REST APIs
- ✅ CRUD operations
- ✅ Database queries
- ✅ Email/SMS notifications

### ❌ Not Recommended For:
- ❌ Large AI model inference (transformers, torch)
- ❌ Background task processing
- ❌ WebSocket connections
- ❌ File uploads/processing
- ❌ Long-running operations

---

## 🔄 Alternative: Hybrid Approach

**Option 1: Simplify Backend for Vercel**
- Remove AI classification features
- Use simple keyword matching instead
- Keep database, email, SMS functionality

**Option 2: Split Services**
- Deploy lightweight API to Vercel (CRUD, notifications)
- Deploy AI processing to Render/Railway (heavy operations)
- Use webhooks to connect them

**Option 3: Use Render Instead (Recommended for this project)**
- See `RENDER_DEPLOYMENT.md` for full guide
- Better suited for AI models and transformers
- No cold starts, persistent processes
- More memory and execution time

---

## 📝 Update Frontend After Deployment

Once deployed, you'll get a URL like: `https://powergrid-backend.vercel.app`

### Update in Netlify:

1. **Update `netlify.toml`:**
   ```toml
   [build.environment]
     NEXT_PUBLIC_API_URL = "https://powergrid-backend.vercel.app"
   ```

2. **Update redirects in `netlify.toml`:**
   ```toml
   [[redirects]]
     from = "/api/*"
     to = "https://powergrid-backend.vercel.app/api/:splat"
     status = 200
     force = true
   
   [[redirects]]
     from = "/chatbot"
     to = "https://powergrid-backend.vercel.app/chatbot"
     status = 200
     force = true
   
   [[redirects]]
     from = "/tickets/*"
     to = "https://powergrid-backend.vercel.app/tickets/:splat"
     status = 200
     force = true
   
   [[redirects]]
     from = "/kb/*"
     to = "https://powergrid-backend.vercel.app/kb/:splat"
     status = 200
     force = true
   ```

3. **Redeploy frontend on Netlify**

---

## 🧪 Test Your Deployment

```bash
# Test basic endpoint
curl https://powergrid-backend.vercel.app/

# Test chatbot
curl -X POST https://powergrid-backend.vercel.app/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test123"}'

# Test tickets
curl https://powergrid-backend.vercel.app/tickets
```

---

## 🐛 Troubleshooting

### Deployment fails?
- Check `vercel.json` syntax
- Ensure `requirements.txt` is valid
- Check build logs in Vercel dashboard

### Function timeout errors?
- AI models may be too slow for serverless
- Consider using Render instead
- Or remove AI features

### Memory exceeded?
- `torch` and `transformers` are very large
- May need to remove these dependencies
- Use simpler NLP libraries or rule-based logic

### Cold starts too slow?
- Upgrade to Vercel Pro for faster cold starts
- Or use Render for persistent server

---

## 💡 Recommendation for Your Project

Given your backend uses:
- **PyTorch** (428 MB)
- **Transformers** (large AI models)
- **Semantic search** with embeddings

**I strongly recommend using Render.com instead** (see `RENDER_DEPLOYMENT.md`):
- ✅ No cold starts
- ✅ Handles large dependencies
- ✅ Persistent processes
- ✅ Better for AI/ML workloads
- ✅ Free tier available

Vercel is excellent for simple APIs, but your backend's AI features are better suited for a traditional server deployment.

---

## 📚 Next Steps

**If continuing with Vercel:**
1. Simplify backend (remove AI models)
2. Deploy using steps above
3. Test thoroughly
4. Update frontend configuration

**If switching to Render (Recommended):**
1. Follow `RENDER_DEPLOYMENT.md`
2. Use `render.yaml` (already configured)
3. Deploy with full AI capabilities
4. Better performance and reliability

---

Need help deciding or want to simplify the backend for Vercel? Let me know!
