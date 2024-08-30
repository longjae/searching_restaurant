import os

import streamlit as st
from dotenv import load_dotenv

from searching import search_restaurant

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    st.title("동네 식당 검색기")
    content = st.text_input("검색하고 싶은 동네를 입력해주세요")
    
    if st.button("검색"):
        with st.spinner("검색중입니다..."):
            result = search_restaurant(content)
            st.write(result)
            
if __name__ == "__main__":
    main()