import streamlit as st
from phonetic_highlighter.phonetic_highlighter import highlight_phonetics


def main():
    icon = "assets/logo.png"
    st.set_page_config(
        page_title="Pronunciation Buddy",
        page_icon=icon,
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    st.title("Pronunciation Buddy")
    st.markdown(
        "Enter text and select a phonetic symbol to highlight the corresponding sounds. Watch the magic happen!"
    )

    text = st.text_area("Enter your text:")
    phonetic_symbol = st.selectbox(
        "Select the phonetic symbol to highlight:",
        [
            "æ (a)",
            "ð (th)",
            "θ (th)",
            "ʃ (sh)",
            "ʒ (s/zh)",
            "ŋ (ng)",
            "tʃ (ch)",
            "dʒ (j/d)",
            "ˈ (')",
        ],
    )

    if st.button("Highlight"):
        progress_text = "Highlighting in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        symbol = phonetic_symbol.split()[0]  # Extract the phonetic symbol
        highlighted_text = highlight_phonetics(text, symbol, my_bar)

        st.markdown(highlighted_text, unsafe_allow_html=True)
        st.balloons()


if __name__ == "__main__":
    main()
