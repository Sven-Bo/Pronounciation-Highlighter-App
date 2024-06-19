from phonetic_highlighter.phonetic_scraper import get_phonetics
import streamlit as st

# Mapping of phonetic symbols to possible characters
phonetic_to_char = {
    "æ": ["a"],
    "ð": ["th"],
    "θ": ["th"],
    "ʃ": ["sh"],
    "ʒ": ["s", "zh"],
    "ŋ": ["ng"],
    "tʃ": ["ch"],
    "dʒ": ["j", "d"],
    "ˈ": ["'"],
}


def highlight_phonetics(text, phonetic_symbol, progress_bar):
    highlighted_text = ""
    words = text.split()
    total_words = len(words)

    for idx, word in enumerate(words):
        phonetics = get_phonetics(word)
        if phonetics:
            possible_chars = phonetic_to_char.get(phonetic_symbol, [phonetic_symbol])
            highlighted_word = word
            start = 0

            while True:
                index = phonetics.find(phonetic_symbol, start)
                if index == -1:
                    break

                # Heuristic to map phonetic index to word index
                word_index = -1
                for i in range(len(word) - len(phonetic_symbol) + 1):
                    if any(word[i : i + len(c)].lower() == c for c in possible_chars):
                        word_index = i
                        break

                if word_index != -1:
                    end_index = word_index + len(phonetic_symbol)
                    highlighted_word = (
                        highlighted_word[:word_index]
                        + f"<u>{highlighted_word[word_index:end_index]}</u>"
                        + highlighted_word[end_index:]
                    )
                start = index + len(phonetic_symbol)

            highlighted_text += highlighted_word + " "
        else:
            highlighted_text += word + " "

        # Update progress
        progress_bar.progress((idx + 1) / total_words)

    return highlighted_text.strip()
