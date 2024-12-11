import streamlit as st
import os
import googleapiclient.discovery
import google.generativeai as genai
from typing import List, Dict

from dotenv import load_dotenv

load_dotenv()

# API Setup Functions
def get_youtube_service():

    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        st.error("YouTube API Key not found. Please set the YOUTUBE_API_KEY environment variable.")
        return None
    
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
    return youtube

def get_gemini_service():

    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        st.error("Gemini API Key not found. Please set the GEMINI_API_KEY environment variable.")
        return None
    
    genai.configure(api_key=gemini_api_key)
    return genai.GenerativeModel('gemini-pro')

def refine_search_query(original_query: str, model) -> str:

    try:
        prompt = f"""
        Given the user's learning request: '{original_query}'
        
        Please transform this into a precise, concise YouTube search query that:
        - Focuses on high-quality, beginner-friendly content
        - Extracts the core learning topic
        - Adds relevant search modifiers to find the best tutorial or course
        
        Return ONLY the refined search query, without any additional text or explanation.
        
        Examples:
        Input: "I want to learn python"
        Output: "Best Python Programming Tutorial for Beginners Full Course"
        
        Input: "machine learning basics"
        Output: "Complete Machine Learning Course for Beginners"
        """
        
        response = model.generate_content(prompt)
        refined_query = response.text.strip()
        
        return refined_query if refined_query else original_query
    except Exception as e:
        st.error(f"Error refining search query: {e}")
        return original_query

def generate_topic_insight(topic: str, model) -> str:

    try:
        prompt = f"""
        For the topic '{topic}', provide a comprehensive beginner's guide that includes:
        
        1. What is this topic about?
        2. Why is it important to learn?
        3. Key learning milestones for beginners
        4. Recommended learning path and resources
        5. Practical tips for getting started
        
        Write in a motivational, clear, and encouraging tone.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating topic insight: {e}")
        return "Unable to generate topic insight."

def search_youtube_content(youtube_service, query: str, content_type: str = 'video', max_results: int = 10) -> List[Dict]:
    try:
        search_response = youtube_service.search().list(
            q=query,
            type=content_type,
            part='id,snippet',
            maxResults=max_results,
            order='relevance',  # Most relevant results
            safeSearch='strict'  # Ensure educational content
        ).execute()
        
        results = []
        for item in search_response.get('items', []):
            # Direct link to video or playlist
            if content_type == 'video':
                link = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            else:
                link = f"https://www.youtube.com/playlist?list={item['id']['playlistId']}"
            
            result = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'link': link,
                'channel': item['snippet']['channelTitle']
            }
            results.append(result)
        
        return results
    
    except Exception as e:
        st.error(f"An error occurred while searching YouTube: {e}")
        return []

def display_results(results: List[Dict], topic_insight: str = None):
    if not results:
        st.warning("No results found.")
        return
    
    # Display topic insight if available
    if topic_insight:
        with st.expander("🧠 Learning Roadmap", expanded=True):
            st.write(topic_insight)
    
    st.subheader("🎥 Top Learning Resources")
    
    for result in results:
        col1, col2 = st.columns([1, 3])
        
        with col1:
              st.image(result['thumbnail'], use_column_width=True)
        with col2:
            # Highlight the video title with a link
            st.markdown(f"### [{result['title']}]({result['link']})")
            
            # Show channel name
            st.caption(f"Channel: {result['channel']}")
            
            # Truncate description if too long
            desc = result['description'][:200] + '...' if len(result['description']) > 200 else result['description']
            st.write(desc)
        
        # Direct YouTube button
        st.markdown(f"[🚀 Watch Now]({result['link']})", unsafe_allow_html=True)
        
        st.markdown("---")

def main():

    st.title("🚀 Learn Anything : CourseCrafter!!")
    
    # Sidebar configuration
    st.sidebar.header("🔍 Search Settings")
    content_type = st.sidebar.selectbox(
        "Resource Type", 
        ["Videos", "Playlists"], 
        help="Choose between individual tutorial videos or complete courses"
    )
    max_results = st.sidebar.slider(
        "Number of Resources", 
        min_value=5, 
        max_value=25, 
        value=10, 
        help="Select how many learning resources to display"
    )
    
    # Learning topic input
    topic = st.text_input("📚 What do you want to learn today?", 
                          placeholder="e.g., 'I want to learn Python programming from scratch'")
    
    # Search button
    if st.button("🔍 Find Best Learning Resources"):
        # Validate input
        if not topic:
            st.warning("Please describe the topic you want to learn.")
            return
        
        # Initialize services
        youtube_service = get_youtube_service()
        gemini_model = get_gemini_service()
        
        if not youtube_service or not gemini_model:
            return
        
        # Refine search query
        with st.spinner("🧠 Optimizing your learning search..."):
            refined_query = refine_search_query(topic, gemini_model)
        
        # Generate topic insight
        with st.spinner("✨ Generating learning insights..."):
            topic_insight = generate_topic_insight(topic, gemini_model)
        
        # Perform search
        st.write(f"🔎 Searching for top {content_type.lower()} about: {refined_query}")
        results = search_youtube_content(
            youtube_service, 
            refined_query, 
            content_type='video' if content_type == 'Videos' else 'playlist',
            max_results=max_results
        )
        
        # Display results with topic insight
        display_results(results, topic_insight)

    # Sidebar additional information
    st.sidebar.markdown("""
    ### 🎓 Learning Tips
    - Be specific about what you want to learn
    - Choose resources matching your skill level
    - Combine multiple resources
    
    ### 🔑 API Keys Required
    - YouTube Data API key
    - Google Gemini API key
    """)

if __name__ == '__main__':
    main()