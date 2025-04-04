import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
import os

# Page Configuration
st.set_page_config(
    page_title="IPL Match Predictor",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Base styles */
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        background-color: #f5f7f9;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Header animations */
    h1 {
        animation: fadeIn 1s ease-out;
    }

    h3 {
        animation: fadeIn 1.2s ease-out;
    }

    /* Team selection animations */
    .stSelectbox>div>div>div {
        background-color: white;
        border-radius: 5px;
        animation: fadeIn 1.4s ease-out;
    }

    .stImage {
        animation: fadeIn 1.6s ease-out;
    }

    /* Button animations */
    .stButton>button {
        background-color: white;
        color: black;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
        animation: fadeIn 1.8s ease-out;
    }

    .stButton>button:hover {
        background-color: white;
        color: #ef4444;
        border-color: #ef4444;
        box-shadow: 0 4px 8px rgba(239, 68, 68, 0.2);
        animation: pulse 1s infinite;
    }

    /* Metric animations */
    .stMetric {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        animation: fadeIn 2s ease-out;
    }

    /* Gauge chart animation */
    .js-plotly-plot {
        animation: fadeIn 2.2s ease-out;
    }

    /* Success/Warning/Error message animations */
    .stSuccess {
        animation: slideIn 0.5s ease-out;
    }

    .stWarning {
        animation: slideIn 0.5s ease-out;
    }

    .stError {
        animation: slideIn 0.5s ease-out;
    }

    /* Loading spinner animation */
    .stSpinner>div {
        animation: rotate 1s linear infinite;
    }

    /* Sidebar animations */
    .css-1d391kg {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: fadeIn 1.4s ease-out;
    }

    /* Number input animations */
    .stNumberInput>div>div>input {
        background-color: white;
        border-radius: 5px;
        animation: fadeIn 1.6s ease-out;
    }

    /* Hover effects */
    .stMetric:hover {
        transform: translateY(-5px);
        transition: transform 0.3s ease;
    }

    .stImage:hover {
        transform: scale(1.05);
        transition: transform 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Load Model
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "pipe.pkl")
    with open(model_path, "rb") as f:
        pipe = pickle.load(f)
except Exception as e:
    st.error(f"🚨 Error loading model: {str(e)}")
    st.stop()

# Team Logos - Updated with more reliable URLs
team_logos = {
    "Sunrisers Hyderabad": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgFNUOHxX-5sofC3Iioht3A6_naxWEImhNUKs6eU6xqjxYJjOa1OLc_hxKRkckg_F6bnG2XzSrAsKQpgYpeXPzFkwNLHQwS5xVrYaL7aKn155nR2J0dPCunLn4LrR8d-bLjqfaLhpAG2tGRZF4RuWgblEy_1DhbmszchchOWOs3ZwAZ_Lj-1bT535Ye/w400-h300/Original%20Sunrisers%20Hyderabad%20PNG-SVG%20File%20Download%20Free%20Download.png",
    "Mumbai Indians": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhcIHFJONN-c6wVsb8I0TI5u1He8Vh5aUlmZ7vPzd6paraXfCf5r-bNdOoT3rqBA5S8Yu3DwefbB4C_Utu6a4E1XUXtdo28k2ViLDYs2fDS7cG9LO0S6ESd5pEZrE1GvYAf6M0_dTs9OibYMQAwkOQZvALvo-ggMxtTh_4JINiQsYeBWtQ0APFedzCZ/w400-h219/Original%20Mumbai%20Indians%20PNG-SVG%20File%20Download%20Free%20Download.png",
    "Royal Challengers Bangalore": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgEMirAmSelGzQqwMqkzMifgCNy9asa4lGjk7tFe7WlVAQ3NU7eGj8nP0c-NRXNY6ZN5FgrDJV0k_UjOLa8rUHJDfEzFsj9qxgL_DxfB0y4RlFli0AnCxNqWXZ9wCATAZ1FBoZafwsUWddYNpVOyBEAxK7yIdLy4OkVjkUMEDErfWKE_54Rt2WW9iXL/w271-h400/Original%20Royal%20Challengers%20Bangalore%20PNG-SVG%20File%20Download%20Free%20Download.png",
    "Kolkata Knight Riders": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhw4FPuHDf0g4n2Gaf_prBrTXdS7GO6zGVcS-Lx4ioHzH-HUUGm5gY7Sj2vmy_6HwxtSZ2fojvZrXqCUIljlZy_aenyml7DLwx3mRXTS-qWBHsBFpt85nq8Y7__HB6uK3JystxJDwx0KoLubgsAIWIH6xXoh2nxjLDM2bNV08uHlBj3zy6SQmfSIUuZ/w260-h400/Original%20Kolkata%20Knight%20Riders%20PNG-SVG%20File%20Download%20Free%20Download.png",
    "Chennai Super Kings": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhn3plcgt5OnAx_VelXAj9Z8TWBiqg6B-xgCJ__kuFeXr1ClntuhvVu0IugURU6TfyHk9qUuECEpos1E5ayEmx0fAupMIvNLQnLOwavDhBYxkIwvRv9cmm7_qHZmlcSwr3Un-hJpy92AooR9Qn77PUcr4yRgAORYwoTBjTYOmyYlHbZ0nDyaL3HWqUk/w400-h330/Original%20Chennai%20Super%20Fun%20Logo%20PNG%20-%20SVG%20File%20Download%20Free%20Download.png",
    "Rajasthan Royals": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgHxGVAL3asVmq-N8vAbTJ0Wk1C7WQNO4yr_O-7dIDgrszmr7L1ODXPuc5IzB8VGr941igDjeEX8OSZ1db2sDpn5uziRk1BVYAVRZBltH4A5FJGhfjmn8PzDLcP7qxCXVyuYQr1uaLktAqoNefxAgjVGXGXIcec8WYXBO4lB-4vtCCmcu2C9RhG5XXm/w400-h354/Original%20Rajasthan%20Royals%20Logo%20PNG-SVG%20File%20Download%20Free%20Download.png",
    "Delhi Capitals": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixNFCNIFm0aH1xUBTkbrLQdE__aSNP32JP1zsee3iJW5va96W_r3qyl486fHQilJQjaVBJt0Fl0xAawdBD4duYEg6Sj-MgCNvVfWuA3UpO4oXBr4qt8WeaaS2Fhtbac8mfzE_euPhJ9hQUVxAgWQDLG1WgrJaSv1I2L4XgNGvFoxrdWQq_LUi82XIw/w348-h400/Original%20Delhi%20Capitals%20Logo%20PNG-SVG%20File%20Download%20Free%20Download.png",
    "Kings XI Punjab": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjWofXDOj6B3eYR3eBKQaPeJjTsblyohHrqK1JO4BEojD0u_Izr_2kIxmrI7Oli8_EvW9tNxB4Qi_OotqkyIWTkOsg6xIroj5U39vvmbGDPSJJXkSn5mzAF58_Mz5Fg8uIrXfJnXWlWrqSig2uxfuUGCrV3wPlZwuZ1OtWVXZUhWYeIzJyrH7klLVer/w311-h400/Original%20Punjab%20Kings%20PNG-SVG%20File%20Download%20Free%20Download.png"
}

# Cities and Venues from the dataset
venues = [
    'Ahmedabad - Narendra Modi Stadium',
    'Bangalore - M Chinnaswamy Stadium',
    'Chandigarh - Punjab Cricket Association Stadium',
    'Chennai - MA Chidambaram Stadium',
    'Delhi - Feroz Shah Kotla',
    'Dharamsala - Himachal Pradesh Cricket Association Stadium',
    'Hyderabad - Rajiv Gandhi International Stadium',
    'Indore - Holkar Cricket Stadium',
    'Jaipur - Sawai Mansingh Stadium',
    'Kolkata - Eden Gardens',
    'Lucknow - Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium',
    'Mumbai - Wankhede Stadium',
    'Mumbai - Brabourne Stadium',
    'Mumbai - DY Patil Stadium',
    'Pune - Maharashtra Cricket Association Stadium',
    'Ranchi - JSCA International Stadium',
    'Visakhapatnam - Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
    'Dubai - Dubai International Cricket Stadium',
    'Sharjah - Sharjah Cricket Stadium',
    'Abu Dhabi - Sheikh Zayed Stadium'
]

# Main Header with better styling
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏏 IPL Match Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4B5563;'>AI-Powered Cricket Match Analysis</h3>", unsafe_allow_html=True)
st.markdown("<hr style='height: 2px; border: none; background-color: #E5E7EB; margin: 20px 0;'>", unsafe_allow_html=True)

# Sidebar with improved styling
with st.sidebar:
    st.markdown("<h2 style='color: #1E3A8A;'>Match Configuration</h2>", unsafe_allow_html=True)
    
    # Team Selection
    st.markdown("<h3 style='color: #4B5563;'>Select Teams</h3>", unsafe_allow_html=True)
    
    # Teams side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h5 style='color: #1E3A8A;'>🏏 Batting Team</h5>", unsafe_allow_html=True)
        batting_team = st.selectbox("Select batting team", sorted(team_logos.keys()), label_visibility="collapsed")
        try:
            st.image(team_logos[batting_team], width=100, caption=batting_team)
        except Exception as e:
            st.info(f"{batting_team}")
    
    with col2:
        st.markdown("<h5 style='color: #1E3A8A;'>🎯 Bowling Team</h5>", unsafe_allow_html=True)
        # Filter out the batting team from bowling team options
        bowling_options = [team for team in sorted(team_logos.keys()) if team != batting_team]
        bowling_team = st.selectbox("Select bowling team", bowling_options, label_visibility="collapsed")
        try:
            st.image(team_logos[bowling_team], width=100, caption=bowling_team)
        except Exception as e:
            st.info(f"{bowling_team}")
    
    # Display warning if teams are the same (should not happen with the filter, but just in case)
    if batting_team == bowling_team:
        st.error("⚠️ Batting team and bowling team cannot be the same!")
        st.stop()
    
    st.markdown("<hr style='height: 2px; border: none; background-color: #E5E7EB; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Match Details
    st.markdown("<h3 style='color: #4B5563;'>Match Details</h3>", unsafe_allow_html=True)
    
    # Two-column layout for match details
    col1, col2 = st.columns(2)
    
    with col1:
        venue = st.selectbox("📍 Match Venue", sorted(venues))
        target = st.number_input("🎯 Target Score", min_value=50, max_value=300, value=160)
    
    with col2:
        score = st.number_input("🏏 Current Score", min_value=0, max_value=target, value=min(75, target))
        wickets = st.number_input("❌ Wickets Fallen", min_value=0, max_value=10, value=3)
    
    # Initialize session state for overs if not exists
    if 'overs' not in st.session_state:
        st.session_state.overs = 10.0

    # Full-width overs input
    overs = st.number_input(
        "🕐 Overs Completed",
        min_value=0.1,
        max_value=20.0,
        value=st.session_state.overs,
        step=0.1,
        format="%.1f"
    )
    
    # Validate and adjust overs input
    if overs > 0:
        whole_overs = int(overs)
        decimal_part = overs - whole_overs
        
        # If decimal part is greater than 0.6, set to next whole number
        if decimal_part > 0.6:
            overs = whole_overs + 1.0
            st.session_state.overs = overs
    
    st.markdown("<hr style='height: 2px; border: none; background-color: #E5E7EB; margin: 20px 0;'>", unsafe_allow_html=True)

# Prediction Button with improved styling
predict = st.button("🔮 Predict Win Probability", use_container_width=True)
        
# Main Content Area
if predict:
    with st.spinner("Analyzing match data..."):
        # Calculate match statistics
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets_remaining = 10 - wickets
        current_run_rate = round(score / overs, 2) if overs > 0 else 0
        required_run_rate = round((runs_left * 6) / balls_left, 2) if balls_left > 0 else 0
        
        # Prepare input data
        # Extract city name from venue (format: "City - Stadium")
        city = venue.split(' - ')[0]

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],  # Using extracted city name
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_remaining],
            'total_runs_x': [target],
            'cur_run_rate': [current_run_rate],
            'req_run_rate': [required_run_rate]
        })
        
        # Get prediction
        result = pipe.predict_proba(input_df)
        win_prob = result[0][1] * 100
        
        # Display Results with improved styling
        st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>Match Analysis</h2>", unsafe_allow_html=True)
        
        # Win Probability Gauge with improved styling
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=win_prob,
            title={'text': f"{batting_team} Win Probability", 'font': {'size': 24, 'color': '#1E3A8A'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#1E3A8A"},
                'bar': {'color': "#4CAF50"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#E5E7EB",
                'steps': [
                    {'range': [0, 30], 'color': "#EF4444"},
                    {'range': [30, 70], 'color': "#F59E0B"},
                    {'range': [70, 100], 'color': "#10B981"}
                ],
                'threshold': {
                    'line': {'color': "#4CAF50", 'width': 4},
                    'thickness': 0.75,
                    'value': win_prob
                }
            }
        ))
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=60, b=40),
            font=dict(size=16)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Match Statistics in columns with improved styling
        st.markdown("<h3 style='text-align: center; color: #4B5563;'>Match Statistics</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Run Rate", f"{current_run_rate:.2f}")
            st.metric("Required Run Rate", f"{required_run_rate:.2f}")
        
        with col2:
            st.metric("Runs Left", runs_left)
            st.metric("Balls Left", int(balls_left))
        
        with col3:
            st.metric("Wickets Remaining", wickets_remaining)
            st.metric("Target", target)
        
        # Match Situation Analysis with improved styling
        st.markdown("<h3 style='text-align: center; color: #4B5563;'>Match Situation</h3>", unsafe_allow_html=True)
        
        # Detailed match situation analysis based on win probability
        if win_prob > 90:
            st.success(f"🏆 {batting_team} is in a commanding position with {win_prob:.1f}% win probability! They are cruising towards victory!")
        elif win_prob > 75:
            st.success(f"🔥 {batting_team} is in a strong position with {win_prob:.1f}% win probability! They have the upper hand in this match!")
        elif win_prob > 60:
            st.success(f"👍 {batting_team} has a slight advantage with {win_prob:.1f}% win probability! They need to maintain their momentum!")
        elif win_prob > 45:
            st.info(f"⚖️ The match is evenly balanced with {win_prob:.1f}% win probability for {batting_team}! Every ball counts!")
        elif win_prob > 30:
            st.warning(f"⚠️ {bowling_team} has the upper hand! {batting_team} needs to accelerate with {win_prob:.1f}% win probability!")
        elif win_prob > 15:
            st.warning(f"😰 {batting_team} is in trouble with {win_prob:.1f}% win probability! They need a miracle to win this!")
        else:
            st.error(f"❌ {batting_team} is in deep trouble with {win_prob:.1f}% win probability! {bowling_team} is dominating the match!")

        # Additional match insights
        st.markdown("<h4 style='text-align: center; color: #4B5563;'>Match Insights</h4>", unsafe_allow_html=True)
        
        # Wicket analysis
        if wickets_remaining >= 7:
            st.success(f"🎯 {batting_team} has plenty of wickets in hand ({wickets_remaining} remaining)")
        elif wickets_remaining >= 4:
            st.info(f"⚡ {batting_team} has {wickets_remaining} wickets remaining - need to be careful")
        else:
            st.warning(f"⚠️ {batting_team} is running out of wickets ({wickets_remaining} remaining)")

        # Target analysis
        if runs_left < 30:
            st.success(f"🎯 Just {runs_left} runs needed! {batting_team} is close to victory!")
        elif runs_left < 60:
            st.info(f"🎯 {runs_left} runs needed - {batting_team} needs to stay focused")
        else:
            st.warning(f"🎯 {runs_left} runs still needed - {batting_team} has a big task ahead")
