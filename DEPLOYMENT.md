# POWERGRID SIH - Netlify Deployment Guide

## 🚀 Quick Deployment to Netlify

### Option 1: Netlify Drop (Drag & Drop)

1. **Build the project locally:**
   ```bash
   npm install
   npm run build
   ```

2. **The build output will be in the `out` folder**

3. **Go to [Netlify Drop](https://app.netlify.com/drop)**

4. **Drag and drop the `out` folder** to deploy instantly!

---

### Option 2: Connect Git Repository

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Netlify deployment"
   git push origin main
   ```

2. **Go to [Netlify](https://app.netlify.com)**

3. **Click "Add new site" → "Import an existing project"**

4. **Connect to GitHub and select your repository**

5. **Netlify will auto-detect settings from `netlify.toml`**

6. **Click "Deploy site"**

---

## ⚙️ Configuration

### Frontend (Already Configured)
- ✅ Static export enabled (`output: 'export'`)
- ✅ Images optimized for static deployment
- ✅ Build configuration in `netlify.toml`

### Backend Deployment
Your FastAPI backend needs to be deployed separately. Options:

#### Option A: Deploy Backend to Render/Railway/Fly.io

**Render.com (Recommended - Free tier available):**
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repo
4. Configure:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:** Add all your SMTP, Twilio, Database credentials

#### Option B: Deploy Backend to Vercel (Serverless)
1. Create `backend/vercel.json`
2. Deploy backend separately to Vercel
3. Get the backend URL

#### Option C: Keep Backend Local (Testing Only)
- Use ngrok to expose local backend
- `ngrok http 8000`
- Update `NEXT_PUBLIC_API_URL` in Netlify

---

## 🔧 Environment Variables

### Set in Netlify Dashboard:

1. Go to: **Site Settings → Environment Variables**

2. Add:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```

---

## 📝 Update After Backend Deployment

Once you have your backend URL, update `netlify.toml`:

```toml
[build.environment]
  NEXT_PUBLIC_API_URL = "https://your-actual-backend-url.com"
```

---

## 🧪 Test Locally Before Deploying

```bash
# Build
npm run build

# Test the static export
npx serve out -p 3000
```

---

## 📦 What Gets Deployed

- ✅ All static HTML, CSS, JS from Next.js
- ✅ Optimized images
- ✅ Client-side routing
- ✅ Dashboard and Chatbot UI

---

## ⚠️ Important Notes

1. **API calls will fail** until you deploy the backend and update `NEXT_PUBLIC_API_URL`
2. The frontend is **static** - all API logic runs on the backend
3. **Database** must be accessible from your backend deployment
4. **Email/SMS** credentials must be set in backend environment variables

---

## 🐛 Troubleshooting

### Build fails on Netlify?
- Check Node version (should be 18+)
- Make sure all dependencies are in `package.json`

### API calls not working?
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check CORS settings on your backend
- Ensure backend is deployed and accessible

### Redirect issues?
- Check `netlify.toml` redirects match your API routes
- Make sure backend URL is correct

---

## 🎯 Production Checklist

- [ ] Build succeeds locally (`npm run build`)
- [ ] Backend deployed and accessible
- [ ] Environment variables set in Netlify
- [ ] `NEXT_PUBLIC_API_URL` updated in code or Netlify env
- [ ] Database accessible from backend
- [ ] SMTP/Twilio credentials configured on backend
- [ ] Test login and ticket creation after deployment

---

## 🌐 Alternative: Full Stack Deployment

If you want both frontend and backend together:

### Use Vercel (supports both Next.js + Python API):
1. Deploy entire project to Vercel
2. Use Vercel's serverless functions for backend
3. Create `backend/api` structure compatible with Vercel

---

Need help with backend deployment? Let me know which platform you prefer!
