import streamlit as st
import pdfplumber

st.set_page_config(page_title="논문 리더기", layout="wide")
st.markdown("""
<style>
body {
    background-color: #fdfcfb;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #111;
}
.stMarkdown blockquote {
    border-left: 4px solid #888;
    padding-left: 12px;
    margin: 10px 0;
    font-size: 16px;
    line-height: 1.6;
    background-color: #f7f5f2;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

st.title("📖 논문 리더기 (스크롤형)")

# 세션 상태 초기화
if 'texts' not in st.session_state:
    st.session_state.texts = []

# 280자 단위 분할
def split_by_chars(text, max_len=280):
    return [text[i:i+max_len].strip() for i in range(0, len(text), max_len) if text[i:i+max_len].strip()]

# PDF 처리
@st.cache_data(show_spinner=False)
def extract_from_pdf(file):
    chunks = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                chunks.extend(split_by_chars(text))
    return chunks

# TXT 처리
@st.cache_data(show_spinner=False)
def extract_from_txt(file):
    text = file.read().decode("utf-8")
    return split_by_chars(text)

# 파일 업로드
uploaded_files = st.file_uploader(
    "📄 PDF 또는 TXT 업로드", 
    type=["pdf","txt"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.session_state.texts = []
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            chunks = extract_from_pdf(uploaded_file)
        else:
            chunks = extract_from_txt(uploaded_file)
        st.session_state.texts.extend(chunks)
    st.success(f"{len(st.session_state.texts)} 텍스트 조각 준비 완료!")

# 텍스트 표시 (스크롤형)
if st.session_state.texts:
    st.markdown("### 📄 본문 (처음부터 끝까지)")
    for i, chunk in enumerate(st.session_state.texts, 1):
        st.markdown(f"> {chunk}")
else:
    st.info("PDF 또는 TXT 파일을 업로드하세요.")
