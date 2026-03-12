# 📋 Pre-Deployment Checklist

Complete this checklist before deploying your dashboard to Streamlit Cloud.

---

## ✅ Local Testing

- [ ] Run `python 01_database_setup.py` — database created successfully
- [ ] Run `python 02_data_cleaning.py` — data validated with 0 errors
- [ ] Run `python 03_visualizations.py` — all 12 charts generated
- [ ] Run `streamlit run 04_dashboard.py` — dashboard loads at localhost:8501
- [ ] Test all filters (Year, Region, State, Top N slider)
- [ ] Verify CSV download button works
- [ ] Check all 12 charts load in dashboard tabs
- [ ] View KPI cards (Total, Avg, YoY Change)

---

## ✅ File Management

- [ ] All 4 Python scripts exist (01, 02, 03, 04)
- [ ] `Consumption.csv` is in the root directory
- [ ] `requirements.txt` contains all packages
- [ ] `.streamlit/config.toml` exists with theme settings
- [ ] `.gitignore` file created
- [ ] `README.md` updated with web deployment info
- [ ] `DEPLOYMENT_GUIDE.md` created

---

## ✅ Git & GitHub

- [ ] Repository initialized: `git init`
- [ ] All files staged: `git add .`
- [ ] Initial commit: `git commit -m "Initial commit"`
- [ ] Remote added: `git remote add origin <your-repo-url>`
- [ ] Pushed to GitHub: `git push -u origin main`
- [ ] Verify all files visible on GitHub.com
- [ ] Repository is PUBLIC (for Streamlit Cloud free tier)

---

## ✅ Streamlit Cloud Setup

- [ ] Created Streamlit account: https://streamlit.io/cloud
- [ ] Connected GitHub account to Streamlit Cloud
- [ ] Repository authorized for Streamlit access
- [ ] Ready to create new app

---

## ✅ Environment Compatibility

- [ ] Python version ≥ 3.7
- [ ] All packages in `requirements.txt` are PyPI-available
- [ ] No hardcoded absolute paths (all relative paths)
- [ ] No local-only dependencies
- [ ] Database file name is consistent (`consumption.db`)

---

## 🚀 Deployment

### To Deploy:

```bash
# 1. Ensure everything is pushed to GitHub
git status  # Should show "nothing to commit"

# 2. Go to https://streamlit.io/cloud

# 3. Click "New app"

# 4. Fill in the form:
#    Repository  → your-github-username/tableau
#    Branch      → main
#    Main file   → 04_dashboard.py

# 5. Click "Deploy"

# 6. Wait 2-3 minutes for deployment

# 7. Get your public URL
```

---

## ✅ Post-Deployment

- [ ] App deployed successfully
- [ ] Public URL obtained (e.g., https://your-app-xxxxx.streamlit.app)
- [ ] Dashboard loads without errors
- [ ] All filters work
- [ ] Charts display correctly
- [ ] CSV download functions
- [ ] Tested on mobile browser
- [ ] Ready to share with stakeholders

---

## 📧 Troubleshooting

### If Deployment Fails:

1. **Check Streamlit Cloud logs** for error messages
2. **Verify `requirements.txt`** has all packages
3. **Ensure `Consumption.csv` is committed to GitHub**
4. **Check `.gitignore` doesn't exclude important files**
5. **Rerun `git push` and restart deployment**

### If Dashboard is Slow:

- First load: Normal (builds database) — wait 30-60 seconds
- Subsequent loads: Should be instant
- Clear browser cache if needed

### If Filters Don't Work:

- Verify data loaded correctly in database
- Check browser console (F12) for errors
- Restart the Streamlit app

---

## 📊 Success Indicators

✅ You're ready when:
- [ ] All local tests pass
- [ ] All files on GitHub
- [ ] Dashboard deployed to public URL
- [ ] Anyone with the link can access it
- [ ] All features work on the web version
- [ ] README and guides are complete

---

## 🎉 What's Next?

After successful deployment:

1. **Share the URL** with your team/stakeholders
2. **Post on social media/LinkedIn** with the project link
3. **Embed in portfolio** or personal website
4. **Monitor usage** in Streamlit Cloud dashboard
5. **Update the dashboard** by pushing new changes to GitHub (auto-redeploy)

---

## 📝 Example Sharing Text

> 🌟 Just deployed my **India Electricity Consumption Analytics Dashboard**! 
> 
> ⚡ Interactive analysis of electricity consumption across all Indian states (2019-2020), with focus on COVID-19 lockdown impact.
> 
> 🔗 [View Dashboard](https://your-app-xxxxx.streamlit.app)
> 
> Tech: Python, Streamlit, Plotly, SQLite | Data: 16,587 records
> 
> #DataAnalytics #Python #Streamlit #DataViz

---

**Questions?** Refer to [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.
