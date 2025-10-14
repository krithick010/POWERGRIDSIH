# 🚀 Deploy Backend to Render.com

## Step-by-Step Guide to Deploy Your FastAPI Backend

---

## 📋 Prerequisites

Before you start:
- [ ] GitHub account
- [ ] Render.com account (sign up at https://render.com)
- [ ] Your code pushed to GitHub
- [ ] SMTP credentials (Gmail app password)
- [ ] Twilio credentials (Account SID, Auth Token, Phone Number)

---

## 🎯 Quick Deploy (Method 1 - Blueprint)

### Using render.yaml (Fastest)

1. **Push render.yaml to GitHub:**
   ```bash
   git add render.yaml
   git commit -m "Add Render blueprint configuration"
   git push origin main
   ```

2. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Click "New" → "Blueprint"

3. **Connect Repository:**
   - Select your GitHub repository
   - Render will auto-detect `render.yaml`
   - Click "Apply"

4. **Configure Environment Variables:**
   Render will prompt you to add:
   ```
   DATABASE_URL=<your-database-url>
   DB_HOST=<your-db-host>
   DB_NAME=powergrid_tickets
   DB_USER=<your-db-user>
   DB_PASSWORD=<your-db-password>
   SMTP_USER=krithickrobotics7@gmail.com
   SMTP_PASSWORD=<your-gmail-app-password>
   CHATBOT_FROM=krithickrobotics7@gmail.com
   TWILIO_ACCOUNT_SID=<your-twilio-sid>
   TWILIO_AUTH_TOKEN=<your-twilio-token>
   TWILIO_PHONE_NUMBER=+15855802717
   ```

5. **Deploy!**
   - Click "Create Services"
   - Wait 5-10 minutes for deployment
   - Get your backend URL!

---

## 🛠️ Manual Deploy (Method 2 - Step by Step)

### Step 1: Create Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect to GitHub"** (authorize if needed)

### Step 2: Select Repository

1. Find and select: **POWERGRIDSIH** repository
2. Click **"Connect"**

### Step 3: Configure Service

Fill in the following:

**Basic Settings:**
```
Name: powergrid-backend
Region: Oregon (US West)
Branch: main
Root Directory: backend
Runtime: Python 3
```

**Build & Deploy:**
```
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
```
Plan: Free (or upgrade as needed)
```

### Step 4: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add each of these:

**Database Configuration:**
```
DATABASE_URL = postgresql://user:password@host:5432/powergrid_tickets
DB_HOST = your-db-host
DB_PORT = 5432
DB_NAME = powergrid_tickets
DB_USER = your_db_user
DB_PASSWORD = your_db_password
```

**Email Configuration:**
```
SMTP_HOST = smtp.gmail.com
SMTP_PORT = 587
SMTP_USER = krithickrobotics7@gmail.com
SMTP_PASSWORD = your_gmail_app_password
CHATBOT_FROM = krithickrobotics7@gmail.com
```

**SMS Configuration (Twilio):**
```
TWILIO_ACCOUNT_SID = your_account_sid
TWILIO_AUTH_TOKEN = your_auth_token
TWILIO_PHONE_NUMBER = +15855802717
```

**Environment:**
```
ENVIRONMENT = production
PYTHON_VERSION = 3.12.2
```

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Watch the logs for any errors
4. Once deployed, you'll see: ✅ **"Live"**

### Step 6: Get Your Backend URL

Your backend will be available at:
```
https://powergrid-backend-XXXX.onrender.com
```

Copy this URL - you'll need it for Netlify!

---

## 🗄️ Database Setup

### Option A: Use Render PostgreSQL (Recommended)

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   ```
   Name: powergrid-db
   Database: powergrid_tickets
   User: powergrid_user
   Region: Oregon (same as backend)
   Plan: Free
   ```
3. Click **"Create Database"**
4. Wait for provisioning (~2 minutes)
5. Click the database → **"Info"** tab
6. Copy the **"Internal Database URL"**
7. Go back to your Web Service → **"Environment"**
8. Update `DATABASE_URL` with the copied URL

### Option B: Use External Database

If you have an existing PostgreSQL database:
1. Make sure it's accessible from the internet
2. Update the `DATABASE_URL` with your connection string
3. Ensure firewall allows Render IPs

---

## 🔧 Post-Deployment Configuration

### 1. Initialize Database Schema

After first deployment, you need to set up the database:

```bash
# SSH into Render shell (if available) or run locally then restore
# Option A: Use Render Shell
# Go to your service → Shell tab

# Option B: Connect remotely
psql $DATABASE_URL < scripts/01-create-schema.sql
psql $DATABASE_URL < scripts/02-seed-knowledge-base.sql
```

### 2. Test Your Backend

Visit these URLs to test:

**Health Check:**
```
https://your-backend-url.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-10-14T..."
}
```

**API Documentation:**
```
https://your-backend-url.onrender.com/docs
```

### 3. Update Netlify Frontend

Now update your Netlify site:

1. Go to Netlify Dashboard
2. Select your site
3. **Site Settings** → **Environment Variables**
4. Add/Update:
   ```
   NEXT_PUBLIC_API_URL = https://your-backend-url.onrender.com
   ```
5. **Deploys** → **Trigger Deploy** → **Deploy site**

---

## 📊 Monitoring & Logs

### View Logs

1. Go to your service in Render
2. Click **"Logs"** tab
3. Watch for:
   - ✅ `Application startup complete`
   - ✅ `Uvicorn running on`
   - ❌ Any errors in red

### Common Log Messages

**Success:**
```
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:10000
INFO: Database pool initialized!
INFO: AI models loaded!
```

**Errors to Watch For:**
```
❌ Connection refused (database not reachable)
❌ Authentication failed (wrong credentials)
❌ Module not found (missing dependency)
```

---

## ⚙️ Environment Variables Reference

Here's a complete list with examples:

```bash
# Required - Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DB_HOST=dpg-xxxxx.oregon-postgres.render.com
DB_PORT=5432
DB_NAME=powergrid_tickets
DB_USER=powergrid_user
DB_PASSWORD=your_secure_password

# Required - Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=krithickrobotics7@gmail.com
SMTP_PASSWORD=your_16_char_app_password
CHATBOT_FROM=krithickrobotics7@gmail.com

# Required - SMS
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+15855802717

# Required - Environment
ENVIRONMENT=production
PYTHON_VERSION=3.12.2

# Optional - For Testing
TEST_NOTIFICATION_EMAIL=your_test@gmail.com
```

---

## 🔒 Security Best Practices

1. **Never commit credentials to GitHub**
   - Use environment variables only
   - Check `.gitignore` includes `.env`

2. **Use strong database passwords**
   - Auto-generated by Render is best

3. **Rotate secrets regularly**
   - Gmail app passwords
   - Twilio auth tokens

4. **Enable HTTPS only**
   - Render does this automatically

---

## 🐛 Troubleshooting

### Deployment Fails

**Error: "Build failed"**
```
Solution: Check requirements.txt has all dependencies
Fix: Make sure torch version is >=2.2.0 (not 2.5.0)
```

**Error: "Start command failed"**
```
Solution: Verify start command is exactly:
uvicorn main:app --host 0.0.0.0 --port $PORT
Note: Use $PORT (Render sets this automatically)
```

### Database Connection Fails

**Error: "Connection refused"**
```
Solution: 
1. Check DATABASE_URL is correct
2. Ensure database is in same region
3. Use "Internal Database URL" not external
```

**Error: "Authentication failed"**
```
Solution: 
1. Verify DB_USER and DB_PASSWORD
2. Make sure database exists
3. Check user has proper permissions
```

### Application Errors

**Error: "Module not found"**
```
Solution: 
1. Check dependency is in requirements.txt
2. Clear build cache and redeploy
3. Check Python version matches (3.12.2)
```

**Error: "AI models failed to load"**
```
Solution: 
1. This is normal on first start (downloads models)
2. Wait 2-3 minutes for models to download
3. Check logs for "AI models loaded!"
```

---

## 💰 Pricing

**Free Tier Includes:**
- ✅ 750 hours/month (enough for 1 service running 24/7)
- ✅ Automatic deploys from GitHub
- ✅ Free SSL certificate
- ✅ 100GB bandwidth/month
- ⚠️ Service may sleep after 15 mins of inactivity
- ⚠️ First request after sleep takes 30-60 seconds

**To Prevent Sleep:**
- Upgrade to Starter plan ($7/month)
- Or use a service like UptimeRobot to ping every 10 minutes

---

## 🎉 Success Checklist

- [ ] Backend deployed to Render
- [ ] Database created and connected
- [ ] All environment variables configured
- [ ] Health endpoint returns 200 OK
- [ ] API docs accessible at /docs
- [ ] Logs show "Application startup complete"
- [ ] Frontend updated with backend URL
- [ ] Test ticket creation works
- [ ] Email notifications working
- [ ] SMS notifications working

---

## 📞 Support

**Render.com Issues:**
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

**Application Issues:**
- Check backend/README.md
- Review application logs
- Test endpoints in /docs

---

## 🔄 Continuous Deployment

Your backend will automatically redeploy when you:
1. Push changes to GitHub main branch
2. Render detects changes
3. Runs build command
4. Restarts service with new code

To disable auto-deploy:
1. Service Settings → Build & Deploy
2. Toggle "Auto-Deploy" to OFF

---

## 🚀 Next Steps

1. ✅ Deploy backend to Render
2. ✅ Get your backend URL
3. ✅ Update Netlify environment variable
4. ✅ Test the complete application
5. 🎉 You're live!

---

Need help? Check the logs first, they usually tell you exactly what's wrong!
