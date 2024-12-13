# 🚀 CourseCrafter: Your AI-Powered Learning Resource Finder

## Overview
CourseCrafter is an intelligent Streamlit application that helps you find the best learning resources on YouTube using AI-powered search optimization and insights. Whether you're looking to learn a new skill or dive deep into a topic, CourseCrafter assists you in discovering high-quality, beginner-friendly content.

## Features
- 🧠 AI-Powered Search Query Optimization
- 🎥 YouTube Content Search
- 📚 Personalized Learning Insights
- 🔍 Flexible Resource Filtering
  - Choose between individual videos or playlists
  - Customize number of results
- 📝 Comprehensive Learning Roadmap Generation

## Prerequisites
- Python 3.8+
- Google Cloud Project with:
  - YouTube Data API enabled
  - Google Gemini API access

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/JonathanJourney99/-CourseCrafter.git
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. API Key Setup
1. Create a `.env` file in the project root directory
2. Add your API keys:
```
YOUTUBE_API_KEY=your_youtube_data_api_key
GEMINI_API_KEY=your_google_gemini_api_key
```

#### Obtaining API Keys
- **YouTube Data API Key**:
  1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
  2. Create a new project
  3. Enable the YouTube Data API v3
  4. Create credentials (API Key)

- **Google Gemini API Key**:
  1. Visit [AI Studio](https://makersuite.google.com/app/apikey)
  2. Create a new API key

## Running the Application
```bash
streamlit run youtube_topic_finder.py
```

## Usage Tips
- Be specific about your learning goal
- Use clear, descriptive topics
- Experiment with different search types and result counts

## Security Notes
- Never commit your `.env` file to version control
- Keep your API keys confidential

## Troubleshooting
- Ensure all dependencies are installed
- Verify API keys are correct and active
- Check internet connectivity

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer
CourseCrafter is an educational tool and relies on third-party APIs. Resource quality may vary.
