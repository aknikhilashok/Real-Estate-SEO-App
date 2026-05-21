import streamlit as st
from openai import OpenAI
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Real Estate SEO & Hashtag Generator",
    page_icon="🏙️",
    layout="centered"
)

# --- HEADER ---
st.title("🏙️ Real Estate Project SEO Generator")
st.markdown("Generate high-converting SEO titles, meta descriptions, hashtags, and tweets using Grok AI.")

# --- SIDEBAR (API KEY) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Grok API Key (xAI)", type="password")
    st.markdown("Get your API key from [xAI Console](https://console.x.ai/).")

# --- MAIN FORM ---
with st.form("seo_form"):
    st.subheader("Project Details")
    
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name*", placeholder="e.g. Raghav Residency")
        city = st.selectbox("City*", ["Mumbai", "Delhi", "Bengaluru", "Pune", "Hyderabad", "Chennai", "Kolkata", "Other"])
        if city == "Other":
            city = st.text_input("Specify City")
    
    with col2:
        micro_market = st.text_input("Micro Market*", placeholder="e.g. Wadala, Andheri East")
        project_type = st.selectbox("Project Type*", ["Residential", "Commercial", "Mixed-Use"])

    config_options = st.multiselect(
        "Configuration*", 
        ["1 BHK", "1.5 BHK", "2 BHK", "2.5 BHK", "3 BHK", "4 BHK", "Penthouse", "Retail Shop", "Office Space"]
    )
    
    landmarks = st.text_area("Nearby Landmarks", placeholder="e.g. 5 mins from Atal Setu, near Eastern Freeway...")
    
    col3, col4 = st.columns(2)
    with col3:
        brand_positioning = st.selectbox(
            "Brand Positioning", 
            ["Affordable Luxury", "Ultra Luxury", "Premium", "Value Housing", "Boutique"]
        )
    with col4:
        usp = st.text_input("Unique Selling Proposition (USP)", placeholder="e.g. Sea-view apartments, Vastu compliant")

    submit_button = st.form_submit_button("Generate Content 🚀")

# --- AI GENERATION LOGIC ---
if submit_button:
    if not api_key:
        st.error("Please enter your Grok API key in the sidebar to continue.")
    elif not project_name or not city or not micro_market or not config_options:
        st.error("Please fill in all mandatory fields marked with *")
    else:
        with st.spinner("Generating SEO & Social Content with Grok..."):
            try:
                # Initialize OpenAI client with xAI's base URL
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.x.ai/v1",
                )

                # Construct the Prompt (Updated with Tweet Generation)
                prompt = f"""
                Act as an expert Real Estate Digital Marketer and SEO Specialist. 
                Generate high-converting SEO content, social media hashtags, and promotional tweets for an upcoming real estate project launch.
                
                Project Details:
                - Name: {project_name}
                - Location: {micro_market}, {city}
                - Type: {project_type}
                - Configurations: {', '.join(config_options)}
                - Landmarks: {landmarks}
                - Brand Positioning: {brand_positioning}
                - USP: {usp}
                
                Goal: Improve organic search visibility on Google and maximize impressions on social media.
                
                Please format your response strictly as follows:
                
                ### 1. SEO Title Tags (Provide 3 options, max 60 characters)
                ### 2. SEO Meta Descriptions (Provide 3 options, max 160 characters)
                ### 3. URL Slug Suggestion
                ### 4. Instagram / Facebook Hashtags (Provide 15-20 highly relevant local and real estate tags)
                ### 5. LinkedIn / X (Twitter) Hashtags (Provide 5-7 professional tags)
                ### 6. Promotional Tweets (Write 3 short, engaging tweets under 280 characters each. Incorporate the project USP, location, and the X hashtags generated in section 5. Use appropriate emojis.)
                """

                # Call Grok API
                response = client.chat.completions.create(
                    model="grok-beta", 
                    messages=[
                        {"role": "system", "content": "You are an expert SEO copywriter for real estate."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                # Display Results
                st.success("Content Generated Successfully!")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")