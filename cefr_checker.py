import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="CEFR Word Level Checker", page_icon="📚")

st.title("📚 CEFR Word Level Checker")
st.write("Enter a word to check its Common European Framework of Reference (CEFR) level")

def get_cefr_level(word):
    """
    Fetches the CEFR level of a word from cefrlookup.com
    """
    try:
        # Clean the word input
        word = word.strip().lower()
        
        # URL for cefrlookup.com search
        url = f"https://cefrlookup.com/search?word={word}"
        
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for CEFR level indicators in the page
        # This is a simple approach - you may need to adjust based on actual HTML structure
        level_indicators = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        
        page_text = soup.get_text()
        
        # Search for level mentions
        for level in level_indicators:
            if level in page_text:
                return level, url
        
        return "Not found", url
        
    except requests.RequestException as e:
        return f"Error: {str(e)}", None
    except Exception as e:
        return f"Error: {str(e)}", None

# Input field
word_input = st.text_input("Enter a word:", placeholder="e.g., hello, sophisticated, ephemeral")

# Search button
if st.button("Check CEFR Level", type="primary"):
    if word_input:
        with st.spinner(f"Searching for '{word_input}'..."):
            level, url = get_cefr_level(word_input)
            
            if "Error" in level:
                st.error(level)
            elif level == "Not found":
                st.warning(f"Could not determine CEFR level for '{word_input}'")
                if url:
                    st.info(f"Check manually: {url}")
            else:
                st.success(f"**Word:** {word_input}")
                st.success(f"**CEFR Level:** {level}")
                if url:
                    st.info(f"Source: {url}")
    else:
        st.warning("Please enter a word to check")

# Information section
with st.expander("ℹ️ About CEFR Levels"):
    st.markdown("""
    **CEFR (Common European Framework of Reference) Levels:**
    
    - **A1** - Beginner: Basic words and phrases
    - **A2** - Elementary: Simple everyday expressions
    - **B1** - Intermediate: Common words for familiar topics
    - **B2** - Upper Intermediate: More complex language
    - **C1** - Advanced: Sophisticated vocabulary
    - **C2** - Proficient: Near-native level vocabulary
    """)

st.divider()
st.caption("Data source: cefrlookup.com")
