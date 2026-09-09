import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

st.set_page_config(
    page_title="SportsHub",
    page_icon="🏆",
    layout="wide"
)

# ---------- DATABASE ----------
@st.cache_resource
def get_database():
    client = MongoClient(st.secrets["MONGO_URI"])
    return client[st.secrets.get("MONGO_DB", "SportsHubDB")]

try:
    db = get_database()
    articles = db["articles"]
    db_status = True
except Exception:
    db_status = False

# ---------- STYLE ----------
st.markdown("""
<style>
.main-title {
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 0;
}
.subtitle {
    color: #777;
    font-size: 18px;
}
.article-card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("🏆 SportsHub")
page = st.sidebar.radio(
    "Menu",
    ["Home", "All Articles", "Publish Article", "Admin"]
)

categories = ["All", "Football", "Cricket", "Basketball", "Tennis", "F1", "Other"]

# ---------- HOME ----------
if page == "Home":
    st.markdown('<p class="main-title">🏆 SportsHub</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Your worldwide sports magazine</p>',
        unsafe_allow_html=True
    )
    st.divider()

    if not db_status:
        st.error("Database is not connected. Check your Streamlit Secrets.")
        st.stop()

    latest = list(
        articles.find().sort("published_at", -1).limit(6)
    )

    if not latest:
        st.info("No articles published yet. Go to 'Publish Article' to add your first article.")
    else:
        st.subheader("📰 Latest Articles")

        for article in latest:
            col1, col2 = st.columns([1, 2])

            with col1:
                if article.get("image_url"):
                    st.image(article["image_url"], use_container_width=True)
                else:
                    st.markdown("### 🏟️")

            with col2:
                st.markdown(f"## {article['title']}")
                st.write(
                    f"**{article['category']}** • "
                    f"By {article['author']} • "
                    f"{article['published_at'].strftime('%d %b %Y')}"
                )
                st.write(article["content"][:250] + "...")

                if st.button("Read Article", key=f"home_{article['_id']}"):
                    st.session_state["selected_article"] = str(article["_id"])
                    st.rerun()

# ---------- ALL ARTICLES ----------
elif page == "All Articles":
    st.title("📰 Sports Articles")

    if not db_status:
        st.error("Database is not connected. Check your Streamlit Secrets.")
        st.stop()

    search = st.text_input("🔎 Search articles")
    selected_category = st.selectbox("Category", categories)

    query = {}

    if selected_category != "All":
        query["category"] = selected_category

    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"content": {"$regex": search, "$options": "i"}},
            {"author": {"$regex": search, "$options": "i"}}
        ]

    result = list(articles.find(query).sort("published_at", -1))

    if not result:
        st.info("No articles found.")
    else:
        st.write(f"**{len(result)} article(s) found**")

        for article in result:
            with st.container(border=True):
                if article.get("image_url"):
                    st.image(article["image_url"], width=500)

                st.subheader(article["title"])
                st.caption(
                    f"{article['category']} | "
                    f"By {article['author']} | "
                    f"{article['published_at'].strftime('%d %b %Y')}"
                )

                if st.button("Read Full Article", key=f"read_{article['_id']}"):
                    st.session_state["selected_article"] = str(article["_id"])
                    st.rerun()

# ---------- READ ARTICLE ----------
if "selected_article" in st.session_state:
    article_id = st.session_state["selected_article"]

    try:
        article = articles.find_one({"_id": ObjectId(article_id)})

        if article:
            st.divider()
            st.title(article["title"])

            if article.get("image_url"):
                st.image(article["image_url"], use_container_width=True)

            st.caption(
                f"{article['category']} • "
                f"By {article['author']} • "
                f"{article['published_at'].strftime('%d %B %Y')}"
            )

            st.markdown(article["content"])

            if st.button("⬅️ Close Article"):
                del st.session_state["selected_article"]
                st.rerun()

    except Exception:
        pass

# ---------- PUBLISH ----------
elif page == "Publish Article":
    st.title("✍️ Publish a Sports Article")
    st.write("Publish your article so readers around the world can see it.")

    if not db_status:
        st.error("Database is not connected. Check your Streamlit Secrets.")
        st.stop()

    st.warning("This page should be protected with an admin password before public deployment.")

    with st.form("publish_form"):
        title = st.text_input("Article Title")
        author = st.text_input("Author Name")
        category = st.selectbox(
            "Category",
            ["Football", "Cricket", "Basketball", "Tennis", "F1", "Other"]
        )
        image_url = st.text_input(
            "Image URL (optional)",
            placeholder="https://example.com/image.jpg"
        )
        content = st.text_area(
            "Article Content",
            height=300,
            placeholder="Write your complete sports article here..."
        )

        publish = st.form_submit_button("🚀 Publish Article")

    if publish:
        if not title or not author or not content:
            st.error("Please enter the title, author and article content.")
        else:
            articles.insert_one({
                "title": title,
                "author": author,
                "category": category,
                "image_url": image_url,
                "content": content,
                "published_at": datetime.utcnow()
            })

            st.success("🎉 Article published successfully!")
            st.balloons()

# ---------- ADMIN ----------
elif page == "Admin":
    st.title("🔐 Admin Dashboard")

    password = st.text_input("Admin Password", type="password")

    correct_password = st.secrets.get("ADMIN_PASSWORD", "change-me")

    if password == correct_password:
        st.success("Admin access granted.")

        total = articles.count_documents({})
        st.metric("Total Published Articles", total)

        st.subheader("Published Articles")

        all_articles = list(
            articles.find().sort("published_at", -1)
        )

        for article in all_articles:
            col1, col2 = st.columns([5, 1])

            with col1:
                st.write(f"**{article['title']}**")
                st.caption(
                    f"{article['category']} • {article['author']}"
                )

            with col2:
                if st.button("Delete", key=f"delete_{article['_id']}"):
                    articles.delete_one({"_id": article["_id"]})
                    st.success("Article deleted.")
                    st.rerun()

    elif password:
        st.error("Incorrect password.")

st.sidebar.divider()
st.sidebar.caption("🌍 SportsHub • Worldwide Sports Magazine")
