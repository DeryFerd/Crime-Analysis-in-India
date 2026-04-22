import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Leaderboard", layout="centered")

st.title("🏆 GitHub Leaderboard")
st.markdown("### 🥇 Top Performers")

file_path = "leaderboard.csv"

# ================= LOAD DATA =================
if os.path.exists(file_path):

    df = pd.read_csv(file_path)

    # ---------------- SORT ----------------
    df = df.sort_values(by="Accuracy", ascending=False).reset_index(drop=True)

    # ---------------- RANK ----------------
    df["Rank"] = df.index + 1

    # ---------------- MEDALS ----------------
    def get_medal(rank):
        if rank == 1:
            return "🥇"
        elif rank == 2:
            return "🥈"
        elif rank == 3:
            return "🥉"
        else:
            return ""

    df["🏅"] = df["Rank"].apply(get_medal)

    # ---------------- FORMAT ACCURACY ----------------
    df["Accuracy"] = (df["Accuracy"] * 100).round(2).astype(str) + "%"

    # ---------------- REORDER ----------------
    df = df[["🏅", "Rank", "GitHub", "Model", "Accuracy"]]

    # ---------------- DISPLAY TABLE ----------------
    st.dataframe(df, use_container_width=True)

    # ================= OPTIONAL FEATURES =================

    # 🔍 Highlight user
    st.markdown("---")
    user = st.text_input("🔍 Enter your GitHub username to find your rank")

    if user:
        user_data = df[df["GitHub"].str.lower() == user.lower()]
        if not user_data.empty:
            st.success("🎯 Your Ranking:")
            st.dataframe(user_data, use_container_width=True)
        else:
            st.warning("User not found in leaderboard")

    # 📊 Graph
    st.markdown("---")
    st.subheader("📊 Accuracy Comparison")

    # Convert % back to float for graph
    temp_df = df.copy()
    temp_df["Accuracy"] = temp_df["Accuracy"].str.replace("%", "").astype(float)

    st.bar_chart(temp_df.set_index("GitHub")["Accuracy"])

else:
    st.warning("⚠️ No leaderboard data available yet. Train model and submit score first.")
