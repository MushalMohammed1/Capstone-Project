import streamlit as st
import pandas as pd
import altair as alt
import base64
import folium
from streamlit_folium import folium_static
import streamlit.components.v1 as components
from folium.plugins import MarkerCluster

######################################
# 1. PAGE CONFIG & DATA LOADING
######################################

st.set_page_config(page_title="ريـاض الرياض", layout="wide")
# Load your dataset
data_path = "Riyadh_Nurseries_updated.csv"
df = pd.read_csv(data_path)

# Load the comments dataset
comments_path = "test.csv"
comments_df = pd.read_csv(comments_path)

# Ensure 'Rates' and 'Reviews' are numeric
df["Rates"] = pd.to_numeric(df["Rates"], errors="coerce")
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

# Drop rows with missing Latitude or Longitude values
df.dropna(subset=["Latitude", "Longitude"], inplace=True)

######################################
# 2. HEADER IMAGE ENCODING
######################################

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode your header gif
img_base64 = get_base64_image("mushal.gif")
img_ab = get_base64_image("ab.gif")
# Encode your navbar logo
img_logo = get_base64_image("logo.png")  # Ensure "logo.png" is in the same folder

######################################
# 3. CUSTOM CSS & NAVBAR
######################################

st.markdown(
    """
 <style>
/* Smooth scrolling for the entire page */
html {
    scroll-behavior: smooth;
}

/* Set the background color to white */
.stApp {
    background: #ffffff; /* White background */
    background-size: cover;
    background-attachment: fixed;
}

/* Full-width header image with overlay */
.header-img-container {
    width: 100vw;
    margin-left: calc(-50vw + 50%);
    margin-top: -130px;
    overflow: hidden;
    position: relative;
    box-sizing: border-box;
}

.header-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.header-img-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 30%;
    background: linear-gradient(to top, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0));
    pointer-events: none;
}

.header-text-overlay {
    position: absolute;
    top: 1500px; /* Adjust this value to position the text vertically */
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: white;
    font-size: 2.5rem;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    z-index: 10; /* Ensure the text is above the image */
}

.header-text-overlay h1 {
    margin: 0;
    font-size: 2.5rem;
    direction: rtl;
}

/* Navbar styles */
.navbar {
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: #4694e2;
    height: 9rem;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    padding: 1rem 2rem;
    box-sizing: border-box;
}

.navbar img {
    height: 100px;
    width: 110px;
    margin-left: 20px;
    margin-top: 60px;
}

.navbar span {
    font-size: 1.5rem;
    color: black;
    font-weight: bold;
    font-family: 'Arial', sans-serif;
    margin-right: 20px;
    margin-top: 40px;
}

.navbar a {
    color: white;
    text-decoration: none;
    font-size: 1.8rem;
    padding: 1rem 2rem;
    margin-top: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.navbar a:hover {
    background-color: #0059b3;
}

/* Heading alignment for all titles */
h1, h2, h3, h4, h5, h6 {
    text-align: right;
    direction: rtl;
}

/* Nursery card styles */
.nursery-card {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    overflow: hidden;
    margin: 1rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.nursery-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.nursery-card-content {
    padding: 1.5rem;
    text-align: right;
    direction: rtl;
    font-family: 'Arial', sans-serif;
}

.nursery-card-content h3 {
    margin-bottom: 1rem;
    font-size: 1.75rem;
    color: #003366;
}

.nursery-card-content p {
    margin-bottom: 0.75rem;
    color: #555;
    font-size: 1.1rem;
}

.nursery-card-content a {
    color: #0077cc;
    text-decoration: none;
    transition: color 0.3s;
}

.nursery-card-content a:hover {
    color: #005499;
    text-decoration: underline;
}

/* Comment card styles */
.comment-card {
    background: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    overflow: hidden;
    margin: 1rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.comment-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.comment-card-content {
    padding: 1rem;
    text-align: right;
    direction: rtl;
    font-family: 'Arial', sans-serif;
}

.comment-card-content p {
    margin-bottom: 0.75rem;
    color: #555;
    font-size: 1rem;
}

/* Sentiment oval styles */
.sentiment-oval {
    background-color: #4CAF50;
    color: white;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.9rem;
}

.sentiment-oval.negative {
    background-color: #F44336;
}

.sentiment-oval.neutral {
    background-color: #FFC107;
}

/* Scrollable div for nursery cards and comments */
.scrollable-div {
    max-height: 500px;
    overflow-y: auto;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
}

/* Section styles */
.section {
    padding: 2rem 0;
}

/* Adjust content padding to account for fixed navbar */
.main-content {
    padding-top: 7rem;
}

/* Project name and description */
.header-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    text-align: center;
    font-size: 2.5rem;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

/* Analysis card styling */
.analysis-card {
    background-color: #f0f8ff;
    border: 2px solid #0077cc;
    border-radius: 10px;
    padding: 1rem;
    margin-top: 1rem;
    text-align: center;
}

.analysis-card h3 {
    margin-bottom: 0.5rem;
    color: #0077cc;
}

.analysis-card p {
    margin: 0.25rem 0;
    font-size: 1.1rem;
    color: #333;
}

/* Analysis container styling */
.analysis-container {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 10px;
}

.neighborhood-analysis-card {
    background-color: #e0f7fa;
    border: 2px solid #0097a7;
    border-radius: 10px;
    padding: 1rem;
    text-align: right;
    direction: rtl;
    flex: 1;
    min-width: 100px;
    width: 100px;
}

.neighborhood-analysis-card h3 {
    margin-bottom: 0.5rem;
    color: #0097a7;
    text-align: center;
    font-size: 1rem;
}

.neighborhood-analysis-card p {
    margin: 0.25rem 0;
    font-size: 1rem;
    text-align: center;
    color: #333;
}

.icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    text-align: center;
}

/* Container for side-by-side divs */
.side-by-side-container {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin: 1rem 0;
}

.side-by-side-container > div {
    width: 48%;
}

/* Sentiment buttons */
.sentiment-buttons {
    display: flex;
    justify-content: space-around;
    margin-top: 1rem;
}

.sentiment-button {
    background-color: #0077cc;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.sentiment-button.positive {
    background-color: green;
}

.sentiment-button.negative {
    background-color: red;
}

.sentiment-button.neutral {
    background-color: brown;
}

.sentiment-button:hover {
    opacity: 0.8;
}

.nursery-divider {
    border: 0;
    height: 1px;
    background: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0));
    margin: 2rem 0;
}

.nursery-card-content p {
    margin: 0.5rem 0; /* Adds spacing between paragraphs */
}

.nursery-card-content strong {
    margin-right: 0.5rem; /* Adds spacing after strong tags */
}
</style>

    """,
    unsafe_allow_html=True
)

# Define the point_in_polygon function
def point_in_polygon(x, y, poly):
    """
    Determine if a point is inside a polygon using the Ray-Casting algorithm.

    Parameters:
    - x: float, the x-coordinate (longitude) of the point.
    - y: float, the y-coordinate (latitude) of the point.
    - poly: list of tuples, the coordinates of the polygon's vertices.

    Returns:
    - bool: True if the point is inside the polygon, False otherwise.
    """
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

# Navbar HTML + JavaScript for smooth scrolling with logo and project name
navbar_html = f"""
    <div class="navbar">
        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <img src="data:image/png;base64,{img_logo}" alt="Logo">
            <span style='color: #003366; font-size: 24px; font-weight: bold;'>
        ريـــــــاض الريــــــاض
    </span>
        </div>
    </div>
    <script>
    function scrollToSection(sectionId) {{
        document.getElementById(sectionId).scrollIntoView({{ behavior: 'smooth' }});
    }}
    </script>
"""
st.markdown(navbar_html, unsafe_allow_html=True)

# Main content wrapper
st.markdown('<div class="main-content">', unsafe_allow_html=True)

######################################
# 4. HEADER IMAGE
######################################

st.markdown(f"""
    <div class="header-img-container">
        <img src="data:image/png;base64,{img_base64}" class="header-img">
        <img src="data:image/gif;base64,{img_ab}" class="header-img">
        <div class="header-img-overlay"></div>
        <div class="header-text-overlay">
            <h1>بيئة آمنة، تعليم مميز، ورعاية مثالية. لأن طفلك يستحق الأفضل!</h1>
        </div>
    </div>
""", unsafe_allow_html=True)

######################################
# 6. STATISTICS (الإحصائيات) - Animated Counter (Client-Side)
######################################

st.markdown('<h1 style="text-align: center; direction: rtl; font-size: 3.5rem; color:#003366;">عدد الحضانات في الرياض</h1>', unsafe_allow_html=True)

# Use client-side JS with IntersectionObserver for the counter
target = df.shape[0]  # Total count of nurseries

counter_html = f"""
<div id="counter" style="text-align: center; color: #2563eb; font-size: 3.5rem; font-weight: bold;">0</div>
<script>
// Function to animate the counter from start to end over a given duration (in ms)
function animateCounter(id, start, end, duration) {{
    var obj = document.getElementById(id);
    var range = end - start;
    var startTime = null;
    function step(timestamp) {{
        if (!startTime) startTime = timestamp;
        var progress = timestamp - startTime;
        var value = Math.floor(Math.min(progress / duration * range + start, end));
        obj.innerText = value;
        if (value < end) {{
            window.requestAnimationFrame(step);
        }}
    }}
    window.requestAnimationFrame(step);
}}

// Use IntersectionObserver to trigger the animation when the counter enters the viewport
var observer = new IntersectionObserver(function(entries, observer) {{
    if (entries[0].isIntersecting === true) {{
        animateCounter("counter", 0, {target}, 2000);
        observer.unobserve(entries[0].target);
    }}
}}, {{ threshold: [0.5] }});

// Start observing the counter element
observer.observe(document.getElementById("counter"));
</script>
"""

components.html(counter_html, height=150)

st.markdown("---")

######################################
# 7. ANALYSIS (تحليل الحضانات)
######################################

# Center the title "ريــاضــنــا"
st.markdown(
    """
    <div style="text-align: center; color:#003366;">
        <h1 style="display: inline-block; direction: rtl;">ريــاضــنــا</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Create a Folium map
m = folium.Map(location=[24.7136, 46.6753], zoom_start=11)

# Define polygon zones with coordinates in (latitude, longitude) format
zones = {
    "شمال الرياض": {
        "coords": [(24.93, 46.525), (24.965, 46.610), (24.740, 46.744), (24.696, 46.630)],
        "color": "blue"
    },
    "جنوب الرياض": {
        "coords": [(24.736, 46.753), (24.692, 46.631), (24.421, 46.786), (24.484, 46.925)],
        "color": "green"
    },
    "شرق الرياض": {
        "coords": [(24.504, 46.918), (24.541, 46.973), (24.710, 46.896), (24.811, 46.972), (24.938, 46.992), (24.820, 46.700)],
        "color": "red"
    },
    "غرب الرياض": {
        "coords": [(24.738, 46.592), (24.510, 46.733), (24.456, 46.476), (24.678, 46.388)],
        "color": "yellow"
    }
}

# Calculate statistics for each zone
zone_stats = {}
for zone, data in zones.items():
    # Filter nurseries within the zone
    zone_nurseries = df[df.apply(lambda row: point_in_polygon(row["Latitude"], row["Longitude"], data["coords"]), axis=1)]

    # Calculate statistics
    num_neighborhoods = zone_nurseries["Neighborhood"].nunique()
    num_nurseries = len(zone_nurseries)
    avg_rating = zone_nurseries["Rates"].mean()

    # Calculate sentiment counts
    zone_comments = comments_df[comments_df["url"].isin(zone_nurseries["url"])]
    sentiment_counts = zone_comments["Sentiment"].value_counts().to_dict()

    # Calculate positive and negative percentages
    total_sentiments = sum(sentiment_counts.values())
    positive_percentage = (sentiment_counts.get("Positive", 0) / total_sentiments) * 100 if total_sentiments > 0 else 0
    negative_percentage = (sentiment_counts.get("Negative", 0) / total_sentiments) * 100 if total_sentiments > 0 else 0
    neutral_percentage = (sentiment_counts.get("Neutral", 0) / total_sentiments) * 100 if total_sentiments > 0 else 0

    # Store the statistics
    zone_stats[zone] = {
        "num_neighborhoods": num_neighborhoods,
        "num_nurseries": num_nurseries,
        "avg_rating": avg_rating,
        "sentiment_counts": sentiment_counts,
        "positive_percentage": positive_percentage,
        "negative_percentage": negative_percentage,
        "neutral_percentage": neutral_percentage
    }

# Add polygons to the map with updated info
for zone, data in zones.items():
    stats = zone_stats[zone]
    info = (f"عدد الأحياء: {stats['num_neighborhoods']}🏠<br>"
            f"عدد الحضانات: {stats['num_nurseries']} 🏫<br>"
            f"متوسط التقييم: {stats['avg_rating']:.2f}⭐<br>"
            f"نسبة التعليقات الإيجابية: {stats['positive_percentage']:.2f}% 👍<br>"
            f"نسبة التعليقات السلبية: {stats['negative_percentage']:.2f}% 👎<br>"
            f"نسبة التعليقات المحايدة: {stats['neutral_percentage']:.2f}% 😐")

            
    folium.Polygon(
        locations=data["coords"],
        color=data["color"],
        fill=True,
        fill_color=data["color"],
        fill_opacity=0.4,
        popup=folium.Popup(info, max_width=300),  # Increase popup size
        tooltip=zone
    ).add_to(m)

# Show the map in Streamlit with full width
st.markdown('<div style="width: 100%; margin: 0 auto;">', unsafe_allow_html=True)
folium_static(m, width=1550)  # Optional: Set a large pixel width for clarity, but '100%' in Map ensures responsiveness
st.markdown('</div>', unsafe_allow_html=True)

######################################
# 8. FILTERING & MAP (تصفية الحضانات & موقع الحضانات)
######################################

# Create a header row with two columns so that the headers "موقع الحضانات" and "تصفية الحضانات" appear on the same line.
header_col1, header_col2 = st.columns(2)
with header_col1:
    st.markdown("<h1 style='color: #003366;'>هنا الحضانات القريبة لحيك</h1>", unsafe_allow_html=True)

with header_col2:
    st.markdown("<h1 style='color: #003366;'>دور حضانة طفلك المناسبة</h1>", unsafe_allow_html=True)

# Create two columns: left for the map, right for filtering options.
map_col, filter_col = st.columns([3, 1])

# Filtering options in the right column.
with filter_col:
    unique_neighborhoods = sorted(df["Neighborhood"].dropna().unique().tolist())
    neighborhood_options = ["كل الأحياء"] + unique_neighborhoods
    selected_neighborhood = st.selectbox("وين حيك", neighborhood_options)

    # Define the topics
    topics = [
        'الأسعار', 'الأنشطة', 'الاِدارة', 'البيئة', 'التعليم', 'الشكر و الامتنان',
        'الكادر التعليمي', 'النظافة', 'تجربة الطفل',
    ]

    # Use a multi-select widget for topics, placed under selected_neighborhood
    selected_topics = st.multiselect("وش يهمك فيه؟", topics)

    selected_rate = st.select_slider(
        "من وين ودك يتراوح التقييم؟ ",
        options=[round(x * 0.1, 1) for x in range(0, 51)],
        value=0.0
    )
    selected_reviews = st.select_slider("ودك تحدد عدد المراجعات؟", options=list(range(int(df["Reviews"].max()) + 1)))

    filtered = df.copy()
    if selected_neighborhood != "كل الأحياء":
        filtered = filtered[filtered["Neighborhood"].str.strip() == selected_neighborhood.strip()]
    filtered = filtered[(filtered["Rates"] >= selected_rate) & (filtered["Reviews"] >= selected_reviews)]

    # Filter nurseries based on the selected topics
    if selected_topics:
        # Filter comments_df to include only rows where any of the selected topics are 1
        filtered_comments = comments_df[comments_df[selected_topics].any(axis=1)]
        filtered_urls = filtered_comments["url"].unique()
        filtered = filtered[filtered["url"].isin(filtered_urls)]

    # If a specific neighborhood is selected, display analysis for it inside styled cards with icons
    if selected_neighborhood != "كل الأحياء":
        neighborhood_data = df[df["Neighborhood"].str.strip() == selected_neighborhood.strip()]
        n_count = neighborhood_data.shape[0]
        avg_rate = neighborhood_data["Rates"].mean()
        min_rate = neighborhood_data["Rates"].min()
        max_rate = neighborhood_data["Rates"].max()
        avg_reviews = neighborhood_data["Reviews"].mean()
        min_reviews = neighborhood_data["Reviews"].min()
        max_reviews = neighborhood_data["Reviews"].max()
        analysis_html = f"""
        <div class="analysis-container">
            <div class="neighborhood-analysis-card">
                <div class="icon">🏠</div>
                <h3>عدد الحضانات</h3>
                <p>{n_count}</p>
            </div>
            <div class="neighborhood-analysis-card">
                <div class="icon">⭐</div>
                <h3>متوسط التقييم</h3>
                <p>{avg_rate:.2f}</p>
            </div>
            <div class="neighborhood-analysis-card">
                <div class="icon">📊</div>
                <h3>نطاق المراجعات</h3>
                <p>{min_reviews:.0f} - {max_reviews:.0f}</p>
            </div>
        </div>
        """
        st.markdown('<h3 style="text-align: center;">تحليلات حيك</h3>', unsafe_allow_html=True)
        st.markdown(analysis_html, unsafe_allow_html=True)

# Map in the left column.
with map_col:
    # Determine the map center and zoom level based on the selected neighborhood
    if selected_neighborhood != "كل الأحياء":
        neighborhood_data = filtered[filtered["Neighborhood"].str.strip() == selected_neighborhood.strip()]
        if not neighborhood_data.empty:
            map_center = [neighborhood_data["Latitude"].mean(), neighborhood_data["Longitude"].mean()]
            zoom_level = 14  # Zoom in closer for a specific neighborhood
        else:
            map_center = [24.7136, 46.6753]
            zoom_level = 10.8
    else:
        map_center = [24.7136, 46.6753]
        zoom_level = 10.8

    # Create a map centered around the determined location
    map_nurseries = folium.Map(location=map_center, zoom_start=zoom_level, width='100%', height='100%')

    # Add markers to the map
    for _, row in filtered.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"{row['Name']}\cdot ({row['Rates']}⭐)<br>{row['Phone']}<br><a href='{row['Website']}' target='_blank'>Website</a>",
            tooltip=row["Name"]
        ).add_to(map_nurseries)

    # Display the map
    folium_static(map_nurseries)

# Wrap the nursery cards and comments in a scrollable div
st.markdown('<hr class="nursery-divider">', unsafe_allow_html=True)
st.markdown('<h3 style="color:#003366;">وش قالوا اهل حيك؟</h3>', unsafe_allow_html=True)

# Display the specific nursery card first
for i, row in filtered.iterrows():
    # Filter comments for the current nursery
    nursery_comments = comments_df[comments_df["url"] == row["url"]]
    
    # Filter comments based on selected topics
    if selected_topics:
        nursery_comments = nursery_comments[nursery_comments[selected_topics].any(axis=1)]

    # Calculate sentiment percentages
    sentiment_counts = nursery_comments["Sentiment"].value_counts(normalize=True) * 100
    positive_percentage = sentiment_counts.get("Positive", 0)
    negative_percentage = sentiment_counts.get("Negative", 0)
    neutral_percentage = sentiment_counts.get("Neutral", 0)

    # Determine the height of the nursery card based on the number of comments
    comments_count = min(3, len(nursery_comments))  # Display up to 3 comments
    card_height = 300 + comments_count * 100  # Adjust the base height and increment as needed

    # Create two columns for each nursery card and comments
    nursery_col, comments_col = st.columns(2)
    with nursery_col:
        card_html = f"""
      <div class="nursery-card" style="height: {card_height}px;">
    <div class="nursery-card-content">
        <h3>{row['Name']}</h3>
        <p>
            <strong>التقييم:</strong> {row['Rates']} ⭐ |
            <strong>المراجعات:</strong> {row['Reviews']} |
            <strong>النوع:</strong> {row['Type']} |
            <strong>الهاتف:</strong> <a href="tel:{row['Phone']}">{row['Phone']}</a>
        </p>
        <p>
            <strong>الحي:</strong> {row['Neighborhood']}<br>
            <strong>الموقع:</strong> <a href="{row['url']}" target="_blank">زر موقعنا</a><br>
            <strong>الموقع الإلكتروني:</strong> <a href="{row['Website']}" target="_blank">زيارة الموقع</a>
        </p>
        <p>
            <strong>نسبة التعليقات الإيجابية:</strong> {positive_percentage:.2f}% 👍 |
            <strong>نسبة التعليقات السلبية:</strong> {negative_percentage:.2f}% 👎
            <p>
            <strong>نسبة التعليقات المحايدة:</strong> {neutral_percentage:.2f}% 😐
            </p>
        </p>
    </div>
</div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    with comments_col:
        if not nursery_comments.empty:
            # Display only the first three comments
            for index, (_, c_row) in enumerate(nursery_comments.iterrows()):
                if index < 3:
                    sentiment_color = "green" if c_row["Sentiment"] == "Positive" else "red" if c_row["Sentiment"] == "Negative" else "yellow"
                    comment_html = f"""
                    <div class="comment-card">
                        <div class="comment-card-content">
                            <p>{c_row['Comments']}</p>
                            <p><span class="sentiment-oval {c_row['Sentiment'].lower()}">{c_row['Sentiment']}</span></p>
                        </div>
                    </div>
                    """
                    st.markdown(comment_html, unsafe_allow_html=True)

    # Add a horizontal line after each nursery card and comments section
    st.markdown('<hr class="nursery-divider">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)