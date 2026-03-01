# Vercel Deployment Guide

## Issues Fixed ✅

1. **NumPy Version Conflict**: Updated from `numpy==1.24.3` to `numpy>=1.26.0`
2. **TensorFlow Compatibility**: Downgraded from `tensorflow==2.20.0` to `tensorflow==2.15.0` for better stability
3. **Python Version**: Added `.python-version` file specifying Python 3.11
4. **Serverless Configuration**: Created proper Vercel serverless function structure

## Files Added for Vercel Deployment

- `.python-version` - Specifies Python 3.11
- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function handler
- `api/__init__.py` - Makes api directory a Python package
- `app_production.py` - Production-ready Flask app

## Deployment Steps

### 1. Connect Your Repository to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import your GitHub repository: `https://github.com/SahayaShynika/AI-assisted-breast-cancer-screening-system`
4. Vercel will automatically detect the Python framework

### 2. Configure Environment Variables

In Vercel dashboard, add these environment variables:

```
SECRET_KEY=your-secure-secret-key-here
DATABASE_URL=sqlite:///breast_cancer_demo.db
```

**Note**: For production, you might want to use a proper database service and set the DATABASE_URL accordingly.

### 3. Deploy

1. Click "Deploy" - Vercel will build and deploy automatically
2. Wait for deployment to complete (usually 2-5 minutes)
3. Your app will be available at: `https://your-app-name.vercel.app`

## What to Expect

### Build Process
- ✅ Python 3.11 will be used
- ✅ Dependencies will be installed from `requirements.txt`
- ✅ Model file (37MB) will be included
- ✅ Serverless function will be created

### Runtime
- ✅ Flask app will run as serverless function
- ✅ Static files will be served from `static/` directory
- ✅ Database will use SQLite (for demo purposes)

## Post-Deployment Checklist

1. **Test Basic Functionality**
   - Visit your deployed URL
   - Try login with demo credentials
   - Test image upload and prediction

2. **Verify Model Loading**
   - Visit `https://your-app-name.vercel.app/model_status`
   - Should return: `{"status": "loaded", "message": "Model loaded successfully"}`

3. **Check File Uploads**
   - Upload a test image
   - Verify prediction results appear

## Troubleshooting

### If Build Fails

1. **Check Logs**: Look at Vercel build logs
2. **Dependencies**: Ensure all packages in `requirements.txt` are compatible
3. **Python Version**: Verify `.python-version` contains `3.11`

### If Runtime Errors

1. **Model Loading**: Check if model file is accessible
2. **Database**: Verify database creation permissions
3. **Static Files**: Ensure template paths are correct

## Performance Considerations

### Model Size
- The model is 37MB - this may affect cold start times
- Consider using a CDN for the model file in production

### Database
- SQLite is fine for demo/development
- For production, consider PostgreSQL or MySQL

### Scaling
- Vercel serverless functions scale automatically
- Monitor usage in Vercel dashboard

## Alternative Deployment Options

If Vercel doesn't work well with the large model file, consider:

1. **Render.com** - Better for larger applications
2. **Heroku** - Traditional deployment option
3. **DigitalOcean** - Full server control

## Next Steps

1. Deploy to Vercel using the steps above
2. Test all functionality
3. Monitor performance and logs
4. Consider optimizations based on usage patterns

---

**Note**: The deployment includes a production-ready version that handles environment variables and database configuration automatically.
