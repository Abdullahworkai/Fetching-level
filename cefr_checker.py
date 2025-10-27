import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="CEFR Word Level Checker", page_icon="📚")

st.title("📚 CEFR Word Level Checker")
st.write("Enter a word to check its Common European Framework of Reference (CEFR) level")

# Get API key from environment or user input
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
    st.sidebar.markdown("[Get an API key](https://platform.openai.com/api-keys)")

def get_cefr_level_with_ai(word, api_key):
    """
    Uses OpenAI GPT to determine the CEFR level of a word
    """
    try:
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fast and cheap model
            messages=[{
                "role": "user",
                "content": f"""What is the CEFR level (A1, A2, B1, B2, C1, or C2) for the English word "{word}"?

Please respond in this exact format:
Word: {word}
CEFR Level: [level]
Explanation: [brief explanation of why this word is at this level]

Use your knowledge of common CEFR classifications from Cambridge, Oxford, and other authoritative sources."""
            }],
            max_tokens=300,
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        return result, None
        
    except Exception as e:
        return None, f"Error: {str(e)}"

# Input field
word_input = st.text_input("Enter a word:", placeholder="e.g., hello, sophisticated, ephemeral")

# Search button
if st.button("Check CEFR Level", type="primary"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar")
    elif word_input:
        with st.spinner(f"Analyzing '{word_input}'..."):
            result, error = get_cefr_level_with_ai(word_input, api_key)
            
            if error:
                st.error(error)
            elif result:
                st.success("✅ Analysis Complete")
                st.markdown(result)
    else:
        st.warning("Please enter a word to check")

# Information section
with st.expander("ℹ️ About CEFR Levels"):
    st.markdown("""
    **CEFR (Common European Framework of Reference) Levels:**
    
    - **A1** - Beginner: Basic words and phrases (e.g., "hello", "cat", "run")
    - **A2** - Elementary: Simple everyday expressions (e.g., "because", "yesterday")
    - **B1** - Intermediate: Common words for familiar topics (e.g., "environment", "although")
    - **B2** - Upper Intermediate: More complex language (e.g., "infrastructure", "demonstrate")
    - **C1** - Advanced: Sophisticated vocabulary (e.g., "ambiguous", "inherent")
    - **C2** - Proficient: Near-native level vocabulary (e.g., "ubiquitous", "ephemeral")
    """)

with st.expander("🔧 How to get an API key"):
    st.markdown("""
    1. Go to [platform.openai.com](https://platform.openai.com/api-keys)
    2. Sign up or log in
    3. Navigate to API Keys section
    4. Create a new API key
    5. Copy and paste it in the sidebar
    
    **Cost:** Very cheap - typically $0.0001-0.0003 per word lookup (using gpt-4o-mini)
    """)

st.divider()
st.caption("Powered by OpenAI GPT-4o-mini")
