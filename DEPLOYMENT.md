# Deployment Guide

This guide will help you deploy the Trial Chat app to Vercel (frontend) and Render (backend) completely for free.

---

## 🚀 Quick Start (10 minutes)

### Prerequisites
- GitHub account
- [Vercel account](https://vercel.com/signup) (free)
- [Render account](https://render.com/register) (free)

---

## 📦 Step 1: Backend Deployment (Render)

### 1.1 Push Code to GitHub
```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

### 1.2 Deploy to Render

1. Go to [https://dashboard.render.com/](https://dashboard.render.com/)
2. Click "New +"
3. Select "Web Service"
4. Connect your GitHub repository
5. Configure settings:
   - **Name**: `trial-chat-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

6. Add Environment Variables:
   - `OPENAI_API_KEY`: Your GitHub token
   - `OPENAI_BASE_URL`: `https://models.inference.ai.azure.com`
   - `OPENAI_MODEL`: `DeepSeek-V3-0324`
   - `PORT`: `8000`

7. Click "Deploy Web Service"

8. Wait for deployment (~3-5 minutes)
9. Copy the backend URL (e.g., `https://trial-chat-backend.onrender.com`)

### 1.3 Verify Backend
```bash
curl https://trial-chat-backend.onrender.com/health
# Should return: {"status":"ok"}
```

---

## 🎨 Step 2: Frontend Deployment (Vercel)

### 2.1 Deploy to Vercel

1. Go to [https://vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. Add Environment Variables:
   - `VITE_API_BASE_URL`: Your backend URL (from Step 1.9)
     - Example: `https://trial-chat-backend.onrender.com`

5. Click "Deploy"

6. Wait for deployment (~2-3 minutes)

### 2.2 Verify Frontend
Visit the Vercel URL provided (e.g., `https://trial-chat.vercel.app`)

---

## 🔧 Step 3: Troubleshooting

### Backend Issues

**Problem**: Deployment fails
- **Solution**: Check Render logs for error messages
- **Common Issues**:
  - Missing dependencies in `requirements.txt`
  - Invalid environment variables
  - Port not set correctly

**Problem**: API returns 404
- **Solution**: Verify the base URL is correct
- Check: `https://your-backend.onrender.com/health`

### Frontend Issues

**Problem**: "Failed to fetch"
- **Solution**: Check that `VITE_API_BASE_URL` is set correctly
- The URL must include `https://` and NOT have a trailing slash

**Problem**: Build fails
- **Solution**: Check Vercel logs
- Common Issues:
  - TypeScript errors
  - Missing dependencies

---

## 🔄 Step 4: Automatic Deployments

Both Vercel and Render support automatic deployments from GitHub:

1. Push changes to your repository
2. Both platforms will automatically rebuild and redeploy
3. Monitor deployment status in their dashboards

---

## 📊 Step 5: Monitoring

### Render Dashboard
- Service health
- CPU/RAM usage
- Request logs
- Error tracking

### Vercel Dashboard
- Build logs
- Analytics
- Domain settings
- Deployment history

---

## 💡 Step 6: Custom Domain (Optional)

### Backend (Render)
1. Go to Settings → Custom Domains
2. Add your domain
3. Update DNS records

### Frontend (Vercel)
1. Go to Settings → Domains
2. Add your domain
3. Vercel will configure SSL automatically

---

## 📝 Step 7: Cost Summary

| Service | Cost | Limits |
|---------|------|--------|
| Render (Free Tier) | $0 | 750 hours/month, 256MB RAM |
| Vercel (Hobby) | $0 | 100GB bandwidth/month |
| **Total** | **$0** | **Fully Free** |

---

## 🔒 Security Notes

1. **Never commit `.env` files** to Git
2. **Use environment variables** in Render/Vercel dashboards
3. **Rotate API keys** regularly
4. **Monitor logs** for suspicious activity

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🆘 Support

If you encounter issues:

1. Check deployment logs
2. Verify environment variables
3. Ensure ports are correct
4. Review this guide
5. Check platform documentation

---

**Deployment Complete! 🎉**
