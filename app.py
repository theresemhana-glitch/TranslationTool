import io
import streamlit as st
from deep_translator import MyMemoryTranslator
from gtts import gTTS

st.title("Language Translation Tool")

languages = MyMemoryTranslator(source="english", target="arabic").get_supported_languages(as_dict=True)
names = sorted(languages)

col1, col2 = st.columns(2)
with col1:
    source = st.selectbox("From", names, index=names.index("english"))
with col2:
    target = st.selectbox("To", names, index=names.index("arabic"))

text = st.text_area("Enter text", height=150, max_chars=500)

if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter some text first.")
    else:
        try:
            translator = MyMemoryTranslator(source=languages[source], target=languages[target])
            st.session_state.result = translator.translate(text)
            st.session_state.result_lang = languages[target].split("-")[0]
        except Exception as e:
            st.session_state.pop("result", None)
            st.error("Translation failed. Wait a moment and try again.")
            st.caption(str(e))

if "result" in st.session_state:
    st.subheader("Translation")
    st.code(st.session_state.result, language=None, wrap_lines=True)

    if st.button("🔊 Listen"):
        try:
            audio = io.BytesIO()
            gTTS(text=st.session_state.result, lang=st.session_state.result_lang).write_to_fp(audio)
            st.audio(audio.getvalue(), format="audio/mp3", autoplay=True)
        except Exception:
            st.warning("Text-to-speech isn't available for this language.")