import streamlit as st
from transformers import MarianMTModel, MarianTokenizer

st.set_page_config(page_title="AI Translator", layout="centered")

st.title("🌐 English to Hindi Translator")
st.markdown("Enter English text and get the Hindi translation instantly.")

# Load model & tokenizer safely with Streamlit caching
@st.cache_resource
def load_model():
    model_name = "Helsinki-NLP/opus-mt-en-hi"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

def translate_text(text):
    tokens = tokenizer(text, return_tensors="pt", padding=True)
    output = model.generate(**tokens)
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Input field
text_input = st.text_area("Enter English Text:")

# Translate button
if st.button("Translate"):
    if text_input.strip():
        with st.spinner("Translating..."):
            translated = translate_text(text_input)
        st.success("Translated Text (Hindi):")
        st.markdown(f"**{translated}**")
    else:
        st.warning("Please enter some text.")
