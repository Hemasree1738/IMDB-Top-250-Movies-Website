
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="IMDb Movie Dashboard", layout="wide")

st.title("IMDb Top 250 Movies Dashboard")

df = pd.read_csv("ToP 250 movies on imdb in 2026 (1).csv")


st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #101827;
}

[data-testid="stSidebar"] * {
    color: white;
}

.sidebar-title {
    background-color: #F5C518;
    color: black !important;
    font-size: 25px;
    font-weight: bold;
    text-align: center;
    padding: 8px;
    border-radius: 6px;
    margin-bottom: 10px;
}

.sidebar-subtitle {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 15px;
}

.sidebar-footer {
    background-color: #172235;
    padding: 12px;
    border-radius: 8px;
    font-size: 12px;
    line-height: 1.8;
}

.footer {
    text-align: center;
    padding: 15px;
    margin-top: 30px;
    background-color: #101827;
    color: white;
    border-radius: 8px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.markdown('<div class="sidebar-title">IMDb</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-subtitle">🎬 Movie Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🎬 Movie Explorer",
            "🔎 Movie Search (Form + Session State)"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    with st.expander("ℹ️ Dataset Information"):
        st.write("Top 250 Movies on IMDb (2026)")
        st.write("Rows:", df.shape[0])
        st.write("Columns:", df.shape[1])
        st.write(
            "This dataset contains top IMDb movies, including titles, ratings, votes, genres and worldwide gross."
        )

    st.divider()

    st.markdown("""
    <div class="sidebar-footer">
        <b>👨‍💻 Created By</b><br>
        Hemasree.R<br><br>
        <b>PRN:</b> 250200253<br>
        <b>Date:</b> 06-11-2026
    </div>
    """, unsafe_allow_html=True)


aliases = {
    "primaryTitle": "title",
    "movieTitle": "title",
    "genre": "genres",
    "countryOfOrigin": "countriesOfOrigin",
    "countries": "countriesOfOrigin"
}

for old, new in aliases.items():
    if old in df.columns and new not in df.columns:
        df.rename(columns={old: new}, inplace=True)

for col in ["title", "genres", "countriesOfOrigin"]:
    if col not in df.columns:
        df[col] = "Unknown"

for col in ["averageRating", "numVotes"]:
    if col not in df.columns:
        df[col] = 0
    df[col] = pd.to_numeric(df[col], errors="coerce")

if "grossWorldwide" not in df.columns:
    df["grossWorldwide"] = 0

df["grossWorldwide"] = pd.to_numeric(
    df["grossWorldwide"].astype(str).str.replace(r"[$,]", "", regex=True),
    errors="coerce"
)

df["title"] = df["title"].fillna("Unknown")
df["genres"] = df["genres"].fillna("Unknown")
df["countriesOfOrigin"] = df["countriesOfOrigin"].fillna("Unknown")

st.success("Dataset loaded successfully!")

# Q1

st.header("Q1. Dataset Loading and Initial Exploration")

st.subheader("First 10 Records")
st.dataframe(df.head(10), use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.write("Total Rows:", df.shape[0])
    st.write("Total Columns:", df.shape[1])

with col2:
    st.write("Column Names:", list(df.columns))
    st.write("Data Types:")
    st.write(df.dtypes)

st.subheader("Missing Values")
st.write(df.isnull().sum())

st.divider()

# Q2

st.header("Q2. Movie Analytics Dashboard")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Movies", len(df))

with c2:
    st.metric("Average Rating", round(df["averageRating"].mean(), 2))

with c3:
    st.metric("Highest Rating", df["averageRating"].max())

with c4:
    st.metric("Total Votes", f"{df['numVotes'].sum():,.0f}")

st.divider()

# Q3

st.header("Q3. Data Visualization")

tab1, tab2, tab3 = st.tabs([
    "Genre Analysis",
    "Rating Analysis",
    "Gross Collection"
])

with tab1:
    st.subheader("Number of Movies by Genre")

    genre_data = (
        df["genres"].dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    genre_count = genre_data.value_counts()

    st.bar_chart(
        genre_count,
        x_label="Genre",
        y_label="Number of Movies"
    )

with tab2:
    st.subheader("IMDb Rating Distribution")

    fig, ax = plt.subplots()

    ax.hist(
        df["averageRating"].dropna(),
        bins=15,
        edgecolor="black"
    )

    ax.set_xlabel("IMDb Rating")
    ax.set_ylabel("Number of Movies")
    ax.set_title("Distribution of IMDb Ratings")

    st.pyplot(fig)
    plt.close(fig)

    plt.figure(figsize=(8, 5))

    st.subheader("Rating vs Number of Votes")

    st.scatter_chart(
        df,
        x="averageRating",
        y="numVotes"
    )

with tab3:
    st.subheader("Top 10 Movies by Worldwide Gross")

    gross_top10 = df.sort_values(
        by="grossWorldwide",
        ascending=False
    ).head(10)

    st.bar_chart(
        gross_top10.set_index("title")["grossWorldwide"]
    )

    st.dataframe(
        gross_top10[["title", "grossWorldwide"]],
        use_container_width=True
    )

# Q4

st.header("Q4. Dashboard Layout and Additional Information")

with st.expander("Dataset Information"):
    st.write("Total Records:", df.shape[0])
    st.write("Total Columns:", df.shape[1])
    st.write("Column Names:", list(df.columns))
    st.dataframe(df.head())

st.divider()

st.info("Explore the IMDb Top 250 Movies Dashboard.")

# Q5

st.header("Q5. Interactive Movie Explorer")

genres = sorted(genre_data.unique().tolist())

countries = sorted(
    df["countriesOfOrigin"]
    .dropna()
    .astype(str)
    .str.split(",")
    .explode()
    .str.strip()
    .unique()
    .tolist()
)

min_rating = float(df["averageRating"].min())
max_rating = float(df["averageRating"].max())

if "genre_filter" not in st.session_state:
    st.session_state.genre_filter = "All"

if "country_filter" not in st.session_state:
    st.session_state.country_filter = []

if "rating_filter" not in st.session_state:
    st.session_state.rating_filter = (min_rating, max_rating)

if "votes_filter" not in st.session_state:
    st.session_state.votes_filter = 0

if "title_search" not in st.session_state:
    st.session_state.title_search = ""

if "sort_order" not in st.session_state:
    st.session_state.sort_order = "Descending"

if st.button("Reset Filters"):
    st.session_state.genre_filter = "All"
    st.session_state.country_filter = []
    st.session_state.rating_filter = (min_rating, max_rating)
    st.session_state.votes_filter = 0
    st.session_state.title_search = ""
    st.session_state.sort_order = "Descending"
    st.rerun()

selected_genre = st.selectbox(
    "Select Genre",
    ["All"] + genres,
    key="genre_filter"
)

selected_countries = st.multiselect(
    "Select Countries",
    countries,
    key="country_filter"
)

rating_range = st.slider(
    "Select IMDb Rating Range",
    min_value=min_rating,
    max_value=max_rating,
    value=(min_rating, max_rating),
    key="rating_filter"
)

min_votes = st.number_input(
    "Minimum Number of Votes",
    min_value=0,
    value=0,
    key="votes_filter"
)

search_title = st.text_input(
    "Search Movie Title",
    key="title_search"
)

sort_order = st.radio(
    "Sort IMDb Ratings",
    ["Ascending", "Descending"],
    key="sort_order"
)

filtered_df = df.copy()

if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df["genres"].str.contains(
            re.escape(selected_genre),
            case=False,
            na=False
        )
    ]

if selected_countries:
    filtered_df = filtered_df[
        filtered_df["countriesOfOrigin"].apply(
            lambda x: any(
                country.strip() in selected_countries
                for country in str(x).split(",")
            )
        )
    ]

filtered_df = filtered_df[
    (filtered_df["averageRating"] >= rating_range[0]) &
    (filtered_df["averageRating"] <= rating_range[1])
]

filtered_df = filtered_df[
    filtered_df["numVotes"] >= min_votes
]

if search_title:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(
            search_title,
            case=False,
            na=False
        )
    ]

filtered_df = filtered_df.sort_values(
    by="averageRating",
    ascending=(sort_order == "Ascending")
)

st.subheader("Filtered Movies")
st.metric("Total Movies Found", len(filtered_df))
st.dataframe(filtered_df, use_container_width=True)

st.divider()

# Q6

st.header("Q6. Session State and Form Handling")

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

if "search_submitted" not in st.session_state:
    st.session_state.search_submitted = False

with st.form("movie_search_form"):

    movie_title = st.text_input("Enter Movie Title")

    preferred_genre = st.selectbox(
        "Select Preferred Genre",
        ["All"] + genres
    )

    preferred_rating = st.slider(
        "Minimum IMDb Rating",
        min_value=0.0,
        max_value=10.0,
        value=7.0,
        step=0.1
    )

    submitted = st.form_submit_button("Search Movie")

if submitted:

    search_df = df[
        df["title"].str.contains(
            re.escape(movie_title),
            case=False,
            na=False
        )
    ].copy()

    if preferred_genre != "All":
        search_df = search_df[
            search_df["genres"].str.contains(
                re.escape(preferred_genre),
                case=False,
                na=False
            )
        ]

    search_df = search_df[
        search_df["averageRating"] >= preferred_rating
    ]

    if not search_df.empty:
        search_df = search_df.sort_values(
            by="averageRating",
            ascending=False
        )

        st.session_state.selected_movie = search_df.iloc[0].to_dict()
        st.session_state.search_submitted = True

    else:
        st.session_state.selected_movie = None
        st.session_state.search_submitted = True

if st.session_state.search_submitted:

    if st.session_state.selected_movie is not None:

        movie = st.session_state.selected_movie

        st.success("Movie found successfully!")

        st.subheader("Selected Movie Information")

        st.write("Movie Title:", movie["title"])
        st.write("Genre:", movie["genres"])
        st.write("IMDb Rating:", movie["averageRating"])
        st.write("Number of Votes:", movie["numVotes"])

    else:
        st.info("No matching movie found.")

st.markdown("""
<div class="footer">
    This is Created by Hemasree.R<br>
    PRN: 250200253<br>
    Date: 06-11-2026
</div>
""", unsafe_allow_html=True)
