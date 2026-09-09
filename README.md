# 🏆 SportsHub

SportsHub is a simple sports magazine and article publishing website built with **Python, Streamlit and MongoDB**.

## Features

- 📰 Publish sports articles
- 🌍 Public worldwide access after deployment
- ⚽ Football, Cricket, Basketball, Tennis, F1 and more
- 🔎 Search articles
- 📖 Read full articles
- 🖼️ Add article image URLs
- 🔐 Admin dashboard
- 🗑️ Delete articles
- ☁️ Deploy on Streamlit Community Cloud

## 1. Create a MongoDB database

Create a free MongoDB Atlas account and create a database named:

`SportsHubDB`

Create a collection named:

`articles`

Get your MongoDB connection string. It will look similar to:

`mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/`

Do not put your real password inside this GitHub repository.

## 2. Test locally

Install the packages:

```bash
pip install -r requirements.txt
```

Create:

`.streamlit/secrets.toml`

Example:

```toml
MONGO_URI = "your_mongodb_connection_string"
MONGO_DB = "SportsHubDB"
ADMIN_PASSWORD = "your_admin_password"
```

Then run:

```bash
streamlit run app.py
```

## 3. Upload to GitHub

Upload these files to your GitHub repository:

- app.py
- requirements.txt
- README.md
- .gitignore

Do NOT upload `.streamlit/secrets.toml`.

## 4. Deploy on Streamlit Community Cloud

Open Streamlit Community Cloud and create a new app.

Select:

- Repository: your SportsHub GitHub repository
- Branch: main
- Main file: `app.py`

Before deploying, open the app's **Secrets** section and add:

```toml
MONGO_URI = "your_mongodb_connection_string"
MONGO_DB = "SportsHubDB"
ADMIN_PASSWORD = "your_admin_password"
```

Then deploy.

Your website will receive a public Streamlit URL that you can share worldwide.

## Important

The current version uses image URLs rather than uploading image files. This keeps the project simple. Later, you can add Cloudinary image uploads, article editing, comments, likes, user accounts and social sharing.
