import streamlit as st
import google.generativeai as genai
import plotly.graph_objs as go
from datetime import datetime, timedelta
from dotenv import load_dotenv
import re
import os

load_dotenv()

class AIRoadmapGenerator:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_comprehensive_roadmap(self, topic):
        """
        Generate a comprehensive learning roadmap using AI
        """
        prompt = f"""
        Create a comprehensive, structured learning roadmap for {topic}. 
        Provide a detailed roadmap in the following format:

        Roadmap Structure:
        1. Phase Name
        - Key Learning Objectives
        - Specific Topics to Cover
        - Estimated Time
        - Recommended Resources

        Example Format:
        1. Fundamentals Phase
        - Learn basic concepts
        - Cover essential skills
        - 4-6 weeks
        - Resources: Online courses, books

        Focus on creating a clear, progressive learning path from beginner to advanced level for {topic}.
        Ensure each phase builds upon the previous one.
        """

        try:
            # Generate content with safety settings
            generation_config = genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=3000
            )
            
            # Generate roadmap
            response = self.model.generate_content(
                prompt, 
                generation_config=generation_config
            )
            
            # Ensure we have a response
            if response and response.text:
                return response.text
            else:
                st.error("No response generated. Please try again.")
                return "Unable to generate roadmap."
        
        except Exception as e:
            st.error(f"Roadmap Generation Error: {e}")
            return f"Error generating roadmap: {e}"

    def create_roadmap_visualization(self, roadmap_text):
        """
        Create a simple visualization of the roadmap
        """
        # Extract phases using regex
        phase_pattern = r'(\d+\.\s*[^\n]+)(?:\n-[^\n]*)*'
        phases = re.findall(phase_pattern, roadmap_text)

        # Create Plotly figure
        fig = go.Figure()

        colors = [
            'rgb(46, 137, 205)', 'rgb(114, 44, 121)', 
            'rgb(198, 47, 105)', 'rgb(58, 200, 225)'
        ]

        start_date = datetime.now()
        for i, phase in enumerate(phases):
            # Estimate duration
            duration = 4 if i < 2 else 6
            
            end_date = start_date + timedelta(weeks=duration)
            
            fig.add_trace(go.Bar(
                x=[duration],
                y=[phase],
                orientation='h',
                marker_color=colors[i % len(colors)],
                name=phase,
                text=[f"{phase} ({duration} weeks)"],
                textposition='outside',
                hoverinfo='text',
                hovertext=f"{phase}\nEstimated Duration: {duration} weeks"
            ))
            
            start_date = end_date

        fig.update_layout(
            title='Learning Path Timeline',
            xaxis_title='Estimated Weeks',
            yaxis_title='Learning Phases',
            height=400,
            bargap=0.3,
        )

        return fig

def main():
    st.set_page_config(
        page_title="AI Roadmap Generator", 
        page_icon="🚀", 
        layout="wide"
    )

    # Initialize AI Roadmap Generator
    roadmap_generator = AIRoadmapGenerator()

    # Title and Description
    st.title("🤖 Universal AI Roadmap Generator")
    st.markdown("""
    Generate a comprehensive, personalized learning roadmap for ANY topic 
    using cutting-edge AI technology.
    """)

    # User Input for Roadmap Topic
    topic = st.text_input(
        "What topic do you want to create a roadmap for?", 
        placeholder="e.g., Machine Learning Engineer, Web3 Development, Digital Marketing..."
    )

    # Generate Roadmap Button
    if st.button("Generate AI Roadmap") and topic:
        with st.spinner("Crafting your personalized roadmap..."):
            try:
                # Generate Roadmap
                ai_roadmap = roadmap_generator.generate_comprehensive_roadmap(topic)
                
                # Display Raw Roadmap
                st.header(f"🗺️ Roadmap for {topic}")
                
                # Create Columns
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Timeline Visualization
                    try:
                        roadmap_chart = roadmap_generator.create_roadmap_visualization(ai_roadmap)
                        st.plotly_chart(roadmap_chart, use_container_width=True)
                    except Exception as viz_error:
                        st.error(f"Visualization Error: {viz_error}")
                
                with col2:
                    # Roadmap Statistics
                    phases = re.findall(r'(\d+\.\s*[^\n]+)', ai_roadmap)
                    st.metric("Total Phases", len(phases))
                    st.metric("Estimated Duration", f"{len(phases) * 4} weeks")
                
                # Detailed Roadmap Content
                st.header("Detailed Learning Phases")
                st.markdown(ai_roadmap)
                
            except Exception as e:
                st.error(f"Error generating roadmap: {e}")

    # Additional Guidance
    st.markdown("---")
    st.markdown("""
    ### 🌟 How to Use
    1. Enter any learning topic
    2. Click "Generate AI Roadmap"
    3. Get a comprehensive, personalized learning path
    
    ### 💡 Tips
    - Be specific about your learning goal
    - Topics can range from professional skills to hobbies
    - Roadmap includes phases, resources, and learning objectives
    """)

if __name__ == '__main__':
    main()