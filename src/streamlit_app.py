import streamlit as st
import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
from transformers import pipeline
import base64
import os
import streamlit.components.v1 as components

# NLTK SAFE DOWNLOADER FOR LOCAL DEV 
@st.cache_resource(show_spinner=False)
def ensure_nltk_resources():
    required_packages = [
        'stopwords', 'punkt', 'punkt_tab', 'averaged_perceptron_tagger', 
        'averaged_perceptron_tagger_eng', 'wordnet'
    ]
    for pkg in required_packages:
        nltk.download(pkg, quiet=True)

ensure_nltk_resources()

# Initialize Preprocessing Tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
spell = SpellChecker()
wordnet_map = {"N": wordnet.NOUN, "V": wordnet.VERB, "J": wordnet.ADJ, "R": wordnet.ADV}

# Preprocessing Functions
def clean_text(text):
    text = str(text).lower().strip()
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_stopwords(text):
    return " ".join([word for word in text.split() if word not in stop_words])

def remove_special_characters(text):
    return re.sub(r'[^A-Za-z\s]', '', text)

def lemmatize_tokens(text):
    """Batch POS tagging — 136x faster than one-by-one."""
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)  # batch call — ONE network call for all tokens
    lemmas = []
    for token, tag in pos_tags:
        pos = tag[0].upper()
        lemma = lemmatizer.lemmatize(token, wordnet_map.get(pos, wordnet.NOUN))
        lemmas.append(lemma)
    return " ".join(lemmas)

def spell_check(text):
    """Call correction() once per word (not twice)."""
    words = text.split()
    checked_words = []
    for word in words:
        corrected = spell.correction(word)
        checked_words.append(corrected if corrected else word)
    return " ".join(checked_words)

def apply_preprocessing(text):
    text = clean_text(text)
    text = remove_stopwords(text)
    text = remove_special_characters(text)
    text = lemmatize_tokens(text)
    return text

# Models Initializations
import torch
device = 0 if torch.cuda.is_available() else -1

@st.cache_resource
def load_classification_model():
    return pipeline("text-classification", model="groupproj/group1-news-classifier-model", truncation=True, max_length=512, device=device)

@st.cache_resource
def load_sentiment_model():
    """3-class transformer sentiment: Positive / Neutral / Negative — much more accurate than VADER for news."""
    return pipeline(
        "text-classification",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        truncation=True,
        max_length=512,
        device=device
    )

def run_sentiment(texts):
    """Batch sentiment inference. Returns list of 'Positive'/'Neutral'/'Negative'."""
    model = load_sentiment_model()
    label_map = {
        "negative": "Negative",
        "neutral": "Neutral",
        "positive": "Positive",
        "LABEL_0": "Negative",
        "LABEL_1": "Neutral",
        "LABEL_2": "Positive"
    }
    results = model(texts, batch_size=16, truncation=True, max_length=512)
    return [label_map.get(r["label"].lower(), "Neutral") for r in results]

from transformers import AutoTokenizer, AutoModelForQuestionAnswering, AutoModelForSeq2SeqLM
import torch

@st.cache_resource
def load_summarizer():
    model_name = "sshleifer/distilbart-cnn-12-6"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

# QA Model Initialization
@st.cache_resource
def load_qa_model():
    model_name = "deepset/roberta-base-squad2-distilled"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    return tokenizer, model

# Function to answer a question
def answer_question(news_text, question):
    tokenizer, model = load_qa_model()
    inputs = tokenizer(question, str(news_text), return_tensors="pt", max_length=512, truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    start_idx = torch.argmax(outputs.start_logits)
    end_idx = torch.argmax(outputs.end_logits)
        
    if end_idx < start_idx:
        end_idx = start_idx
        
    answer_tokens = inputs["input_ids"][0][start_idx:end_idx + 1]
    answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)
    
    if not answer.strip() or answer == tokenizer.cls_token or answer == tokenizer.sep_token:
        return "Answer not clearly found in the text."
        
    return answer


import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time

# Streamlit UI Configurations
st.set_page_config(page_title="NEURONEWS", layout="wide", initial_sidebar_state="collapsed")

vanta_js = """
<script>
if (!parent.document.getElementById('vanta-bg')) {
    const script1 = parent.document.createElement('script');
    script1.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js";
    parent.document.head.appendChild(script1);

    script1.onload = () => {
        const script2 = parent.document.createElement('script');
        script2.src = "https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js";
        parent.document.head.appendChild(script2);
        
        script2.onload = () => {
            const bgDiv = parent.document.createElement('div');
            bgDiv.id = 'vanta-bg';
            bgDiv.style.position = 'fixed';
            bgDiv.style.top = '0';
            bgDiv.style.left = '0';
            bgDiv.style.width = '100vw';
            bgDiv.style.height = '100vh';
            bgDiv.style.zIndex = '-999';
            bgDiv.style.opacity = '0.35';
            parent.document.body.insertBefore(bgDiv, parent.document.body.firstChild);
            
            parent.window.VANTA.NET({
              el: "#vanta-bg",
              mouseControls: false,
              touchControls: false,
              gyroControls: false,
              minHeight: 200.00,
              minWidth: 200.00,
              scale: 1.00,
              scaleMobile: 1.00,
              color: 0x38bdf8,
              backgroundColor: 0x030b14,
              points: 8.00,
              maxDistance: 22.00,
              spacing: 20.00
            });
        }
    }
}
</script>
"""
components.html(vanta_js, width=0, height=0)

# Custom CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap');

    html { scroll-behavior: smooth; }

    :root {
        --bg: #030b14;
        --text: #e0f2fe;
        --text-muted: #7dd3fc;
        --border: rgba(56, 189, 248, 0.3);
        --card-bg: rgba(4, 20, 40, 0.6);
        --accent: #38bdf8;
        --accent-glow: rgba(56, 189, 248, 0.6);
        --radius: 15px;
    }

    body { margin: 0; }
    
    [data-testid="stAppViewContainer"] {
        background-color: transparent !important;
        font-family: 'Rajdhani', sans-serif !important;
        color: var(--text) !important;
        animation: fadeIn 1s ease-out;
    }

    .stApp { background-color: transparent !important; }
    [data-testid="stHeader"] { background: transparent !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stSidebar"] { display: none !important; }

    /* Layout Spacing */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
        max-width: 1100px !important;
        margin: 0 auto;
    }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    /* Typography */
    h1, h2, h3, h4, .main-title, .section-header {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        color: var(--text) !important;
    }
    
    .main-title {
        font-size: clamp(2rem, 5vw, 3.5rem) !important;
        color: #38bdf8 !important;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        text-shadow: 0px 0px 15px rgba(56, 189, 248, 0.8), 0 0 30px rgba(56, 189, 248, 0.4);
        letter-spacing: 2px;
        animation: glowPulse 3s infinite alternate;
    }
    
    @keyframes glowPulse { from { text-shadow: 0 0 10px rgba(56,189,248,0.5); } to { text-shadow: 0 0 25px rgba(56,189,248,0.9), 0 0 40px rgba(56,189,248,0.5); } }

    .sub-title {
        font-size: clamp(0.9rem, 3vw, 1.2rem) !important;
        color: var(--text-muted) !important;
        text-align: center;
        font-weight: 500;
        margin-bottom: 3.5rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    .section-header {
        font-size: clamp(1.3rem, 4vw, 1.8rem) !important;
        color: #38bdf8 !important;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 15px;
        border-bottom: 1px solid rgba(56, 189, 248, 0.3);
        padding-bottom: 12px;
        text-shadow: 0 0 10px rgba(125, 211, 252, 0.8);
        letter-spacing: 1px;
    }

    /* ── NAV BAR STYLING & INTERACTION ── */
    div.element-container:has(div[data-testid="stRadio"]), [data-testid="stVerticalBlock"] > div:has(div[data-testid="stRadio"]) {
        position: sticky !important;
        top: 10px !important;
        z-index: 999999 !important;
        height: auto !important;
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        pointer-events: none !important;
        margin-bottom: 25px !important;
        padding-bottom: 10px !important;
    }

    div[data-testid="stRadio"] {
        pointer-events: auto !important;
        background: rgba(4, 20, 40, 0.95) !important;
        border: 2px solid rgba(56, 189, 248, 0.8) !important;
        border-radius: 99px !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.3), inset 0 0 10px rgba(56, 189, 248, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        max-width: 95vw !important;
        scrollbar-width: none;
    }
    div[data-testid="stRadio"]::-webkit-scrollbar { display: none; }

    div[data-testid="stRadio"] > label:first-child, div[data-testid="stRadio"] input[type="radio"], div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: inline-flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 0px !important;
        align-items: center !important;
    }

    div[data-testid="stRadio"] > div > label {
        display: flex !important;
        align-items: center !important;
        padding: clamp(10px, 2vw, 13px) clamp(16px, 3vw, 34px) !important;
        border-radius: 0 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: clamp(0.7rem, 2vw, 0.88rem) !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        color: rgba(125, 211, 252, 0.8) !important;
        transition: all 0.4s ease !important;
        white-space: nowrap !important;
        background: transparent !important;
        margin: 0 !important;
    }

    div[data-testid="stRadio"] > div > label:hover {
        background: rgba(56, 189, 248, 0.3) !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5) !important;
    }

    div[data-testid="stRadio"] > div > label:has(input:checked) {
        background: rgba(56, 189, 248, 0.45) !important;
        color: #ffffff !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.6) !important;
    }

    div[data-testid="stRadio"] * { pointer-events: auto !important; cursor: pointer !important; }

    [data-testid="stHorizontalBlock"] { pointer-events: none !important; }
    [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] { pointer-events: auto !important; }
    .stApp, section[data-testid="stMain"], section[data-testid="stMain"] > div, [data-testid="stAppViewContainer"] { overflow: visible !important; overflow-x: hidden !important;}
    
    [data-testid="stExpander"] > div:first-child { padding: 0px 16px !important; min-height: 48px !important; display: flex !important; align-items: center !important; }

    /* Cards & Elements */
    .card, .status-card, [data-testid="stMetric"], [data-testid="stExpander"], [data-testid="stFileUploader"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: clamp(15px, 4vw, 28px) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.2), inset 0 0 15px rgba(56, 189, 248, 0.1) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        margin-bottom: 25px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    [data-testid="stMetric"]:hover, [data-testid="stExpander"]:hover, [data-testid="stFileUploader"]:hover, .card:hover {
        transform: translateY(-5px) scale(1.01) !important;
        box-shadow: 0 15px 40px rgba(56, 189, 248, 0.45), inset 0 0 30px rgba(56, 189, 248, 0.25) !important;
        border-color: #38bdf8 !important;
    }
    
    [data-testid="stPlotlyChart"], [data-testid="stImage"] {
        background: rgba(4, 20, 40, 0.2) !important;
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        border-radius: var(--radius) !important;
        padding: 10px !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.05), inset 0 0 10px rgba(56, 189, 248, 0.02) !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.4s ease !important;
        overflow: hidden !important;
    }
    
    [data-testid="stPlotlyChart"]:hover, [data-testid="stImage"]:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 40px rgba(56, 189, 248, 0.35), inset 0 0 30px rgba(56, 189, 248, 0.2) !important;
        border-color: rgba(56, 189, 248, 0.6) !important;
        background: rgba(4, 20, 40, 0.5) !important;
    }
    
    /* Buttons */
    div.element-container:has(div[data-testid="stButton"]), [data-testid="stVerticalBlock"] > div:has(div[data-testid="stButton"]) {
        display: flex !important; justify-content: center !important; width: 100% !important;
    }
    
    .stButton>button {
        background: rgba(2, 132, 199, 0.2) !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-size: clamp(0.9rem, 2vw, 1.1rem) !important;
        font-weight: 700 !important;
        font-family: 'Orbitron', sans-serif !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        width: 100% !important;
        max-width: 300px !important;
    }
    .stButton>button:hover {
        background: rgba(56, 189, 248, 0.9) !important;
        color: #030b14 !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.8) !important;
        transform: scale(1.05) !important;
    }
    .stButton>button:active { transform: scale(0.95) !important; }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #e0f2fe !important;
        font-weight: 700 !important;
        font-size: clamp(1.8rem, 5vw, 2.8rem) !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.6) !important;
    }
    [data-testid="stMetricLabel"] {
        color: #7dd3fc !important;
        font-weight: 600 !important;
        font-size: clamp(0.8rem, 2vw, 1rem) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background: rgba(4, 20, 40, 0.6) !important;
        border: 1px solid var(--border) !important;
        color: #e0f2fe !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-family: 'Rajdhani', sans-serif !important;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus, .stSelectbox>div>div>div:focus, .stNumberInput>div>div>input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.3), inset 0 2px 5px rgba(0,0,0,0.2) !important;
        background: rgba(10, 30, 60, 0.8) !important;
    }
    
    /* Instruction Box */
    .instruction-box {
        background: rgba(2, 132, 199, 0.1);
        border: 1px dashed rgba(56, 189, 248, 0.5);
        border-radius: 8px;
        padding: clamp(15px, 4vw, 24px);
        margin-bottom: 28px;
        color: #7dd3fc;
        font-size: clamp(0.95rem, 2vw, 1.1rem);
        line-height: 1.6;
        font-family: 'Rajdhani', sans-serif;
        box-shadow: inset 0 0 20px rgba(56, 189, 248, 0.05);
    }

    /* Processing Architecture */
    .processing-list { display: flex; flex-direction: column; align-items: center; gap: 12px; margin: 25px 0; font-family: 'Rajdhani', sans-serif;}
    .processing-step { background: rgba(2, 132, 199, 0.2); border: 1px solid rgba(56, 189, 248, 0.3); padding: 12px 20px; border-radius: 8px; color: #e0f2fe; font-weight: 600; font-size: clamp(0.9rem, 2vw, 1.1rem); display: flex; align-items: center; gap: 15px; width: 100%; max-width: 320px; box-shadow: 0 0 15px rgba(56, 189, 248, 0.15); animation: slideIn 0.8s ease-out forwards; opacity: 0; transition: all 0.3s ease; }
    .processing-step:hover { background: rgba(56, 189, 248, 0.3); transform: scale(1.05); box-shadow: 0 10px 25px rgba(56, 189, 248, 0.4); }
    .processing-step:nth-child(1) { animation-delay: 0.1s; } .processing-step:nth-child(3) { animation-delay: 0.3s; } .processing-step:nth-child(5) { animation-delay: 0.5s; } .processing-step:nth-child(7) { animation-delay: 0.7s; } .processing-step:nth-child(9) { animation-delay: 0.9s; }
    .step-arrow { color: rgba(56, 189, 248, 0.6); font-size: 1.5rem; animation: fadeInArrow 0.5s ease forwards, bounce 2s infinite; opacity: 0; }
    
    @keyframes slideIn { from { transform: translateY(-30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    @keyframes fadeInArrow { from { opacity: 0; } to { opacity: 1; } }
    @keyframes bounce { 0%, 20%, 50%, 80%, 100% { transform: translateY(0); } 40% { transform: translateY(7px); } 60% { transform: translateY(4px); } }

    /* Glassmorphism Home Cards */
    .cards-container { display: flex; justify-content: center; align-items: stretch; gap: 20px; margin-top: 40px; flex-wrap: wrap; margin-bottom: 30px; width: 100%; }
    .glass-card {
        position: relative; width: 100%; max-width: 280px; height: 320px;
        background: rgba(4, 20, 40, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px; overflow: hidden;
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        box-shadow: 0 15px 35px rgba(0,0,0,0.5), inset 0 0 15px rgba(56, 189, 248, 0.1);
        backdrop-filter: blur(12px); display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .glass-card .bg-glow { position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, rgba(56, 189, 248, 0.15), transparent 70%); opacity: 0; transition: 0.5s; }
    .glass-card:hover .bg-glow { opacity: 1; }
    .glass-card:hover { transform: translateY(-12px); border-color: rgba(56, 189, 248, 0.8); box-shadow: 0 25px 50px rgba(56, 189, 248, 0.3), inset 0 0 20px rgba(56, 189, 248, 0.2); }
    .glass-card .icon-contain { font-size: 3.5rem; color: #38bdf8; transition: 0.5s; z-index: 2; margin-bottom: 15px; }
    .glass-card h3 { font-family: 'Orbitron', sans-serif; color: #fff; font-size: 1.25rem; z-index: 2; text-align: center; padding: 0 10px; transition: 0.5s; }
    .glass-card .content-box { position: absolute; bottom: -100%; width: 100%; height: 50%; padding: 20px; background: rgba(4, 20, 40, 0.95); border-top: 1px solid rgba(56, 189, 248, 0.5); transition: 0.5s; display: flex; align-items: center; text-align: center; justify-content: center;}
    .glass-card:hover .content-box { bottom: 0; }
    .glass-card:hover h3 { transform: translateY(-60px); }
    .glass-card:hover .icon-contain { transform: translateY(-60px) scale(0.85); color: #fff; }
    .content-box p { color: #e0f2fe; font-family: 'Rajdhani', sans-serif; font-size: 1.05rem; }

    .home-desc {
        font-size: clamp(1rem, 3vw, 1.35rem); color: #e0f2fe; max-width: 850px; text-align: center; margin: 0 auto; line-height: 1.8; 
        background: rgba(4, 20, 40, 0.6); padding: clamp(15px, 4vw, 30px); border-radius: 15px; border: 1px solid rgba(56,189,248,0.3); 
        box-shadow: 0 0 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(56,189,248,0.1); font-family: 'Rajdhani', sans-serif;
    }
    
    .nn-download-btn {
        display: block !important;
        margin: 0 auto !important;
        background: rgba(2, 132, 199, 0.2) !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 14px 32px !important;
        font-size: clamp(0.9rem, 2vw, 1.1rem) !important;
        font-family: 'Orbitron', sans-serif !important;
        width: auto !important;
        max-width: 300px !important;
        text-align: center !important;
        box-sizing: border-box !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
        margin-top: 10px;
    }
    .nn-download-btn:hover {
        background: rgba(56, 189, 248, 0.9) !important;
        color: #030b14 !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.8) !important;
        transform: scale(1.02);
        text-decoration: none !important;
    }

    /* Mobile Responsive Adjustments */
    @media (max-width: 768px) {
        .glass-card { height: 260px; max-width: 320px; }
        .glass-card:hover h3 { transform: translateY(-40px); }
        .glass-card:hover .icon-contain { transform: translateY(-40px) scale(0.85); }
        .glass-card h3 { font-size: 1.1rem; }
        div[data-testid="stRadio"] > div > label { padding: 10px 15px !important; }
        [data-testid="stMetricValue"] { font-size: 2.2rem !important; }
        .card, .status-card, [data-testid="stMetric"], [data-testid="stExpander"], [data-testid="stFileUploader"] {
            padding: 20px !important;
        }
        .main-title { font-size: 2.5rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ── Session State Init ────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

if "df" in st.session_state:
    df = st.session_state.df
else:
    df = None

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 0 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("""
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 50vh; animation: slideIn 1s ease-out; margin-top: 30px;">
            <div class="main-title" style="font-size: 5rem !important;"><i class="fa-solid fa-brain"></i> NEURONEWS</div>
            <div class="sub-title" style="font-size: 1.6rem !important; margin-bottom: 2rem;"><i class="fa-solid fa-microchip"></i> AI-Powered News Analytics Engine</div>
            <p class="home-desc">
                <b>Welcome to NeuroNews!</b><br>
                Understanding large amounts of news data has never been easier. 
                Instead of reading hundreds of articles manually, simply upload your dataset here.<br><br>
                Our AI engine will instantly read, categorize, and analyze the emotions behind the news for you. You can quickly see whether the news trends are positive or negative, identify clear topics, and even ask direct questions to get summarized answers right from your data!
            </p>
            <div class="cards-container">
                <div class="glass-card">
                    <div class="bg-glow"></div>
                    <div class="icon-contain"><i class="fa-solid fa-layer-group"></i></div>
                    <h3>News Classification</h3>
                    <div class="content-box">
                        <p>Automatically separates vast amounts of news into clear topics, saving you countless hours of reading.</p>
                    </div>
                </div>
                <div class="glass-card">
                    <div class="bg-glow"></div>
                    <div class="icon-contain"><i class="fa-solid fa-comments"></i></div>
                    <h3>Smart Q&A</h3>
                    <div class="content-box">
                        <p>Ask a question about any uploaded news article, and our AI will find and highlight the exact answer for you.</p>
                    </div>
                </div>
                <div class="glass-card">
                    <div class="bg-glow"></div>
                    <div class="icon-contain"><i class="fa-solid fa-chart-line"></i></div>
                    <h3>INSIGHTS</h3>
                    <div class="content-box">
                        <p>Explore easy-to-read charts showing the overall sentiment (positive/negative) and key trending words in your data.</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("INITIALIZE SYSTEM", key="start_btn"):
        st.session_state.page = "upload"
        st.rerun()

else:
    # HEADER TITLE
    st.markdown('<div class="main-title"><i class="fa-solid fa-brain"></i> NEURONEWS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title"><i class="fa-solid fa-microchip"></i> Advanced Text Analytics Pipeline</div>', unsafe_allow_html=True)

    # ── NAVIGATION BAR ───────────────────────────────────────────────────────────
    page_labels = {
        "home":     "HOME",
        "upload":   "UPLOAD",
        "export":   "EXPORT HUB",
        "qa":       "Q&A",
        "insights": "INSIGHTS",
    }
    label_to_key = {v: k for k, v in page_labels.items()}
    
    try:
        current_index = list(page_labels.keys()).index(st.session_state.page)
    except (ValueError, KeyError):
        current_index = 0
    
    selected_label = st.radio(
        label="nav",
        options=list(page_labels.values()),
        index=current_index,
        horizontal=True,
        label_visibility="collapsed",
    )
    
    selected_key = label_to_key[selected_label]
    if selected_key != st.session_state.page:
        st.session_state.page = selected_key
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "upload":
    st.markdown('<div class="section-header"><i class="fa-solid fa-cloud-arrow-up"></i> Data Upload Protocol</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="instruction-box">
        <strong style="color:#ffffff; font-size:1.1rem;"><i class="fa-solid fa-bolt"></i> Initiate System Engine:</strong><br><br>
        The ultimate dashboard to analyze news dynamically. Drop your <code>.csv</code> or <code>.xlsx</code> with news blocks (must have a <code>content</code> or <code>text</code> column). Let our AI do the heavy lifting with maximum effects.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("PREPROCESSING ARCHITECTURE"):
        st.markdown("""
    <div class="processing-list">
        <div class="processing-step"><i class="fa-solid fa-volume-xmark"></i> <span>1. Noise Reduction</span></div>
        <div class="step-arrow"><i class="fa-solid fa-angles-down"></i></div>
        <div class="processing-step"><i class="fa-solid fa-filter"></i> <span>2. Feature Filtering</span></div>
        <div class="step-arrow"><i class="fa-solid fa-angles-down"></i></div>
        <div class="processing-step"><i class="fa-solid fa-ban"></i> <span>3. Stopwords Removal</span></div>
        <div class="step-arrow"><i class="fa-solid fa-angles-down"></i></div>
        <div class="processing-step"><i class="fa-solid fa-seedling"></i> <span>4. Lemmatization</span></div>
        <div class="step-arrow"><i class="fa-solid fa-angles-down"></i></div>
        <div class="processing-step"><i class="fa-solid fa-spell-check"></i> <span>5. Spell Check</span></div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop dataset matrix here", type=["csv", "xlsx"], key="file_uploader_main")

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            st.session_state.temp_df = pd.read_csv(uploaded_file)
        else:
            st.session_state.temp_df = pd.read_excel(uploaded_file)
            
    if "temp_df" in st.session_state:
        temp_df = st.session_state.temp_df
        st.markdown(f"<div class='status-card' style='border-left: 5px solid #00e5ff;'><i class='fa-solid fa-check-double' style='color:#38bdf8; margin-right:10px;'></i> <b>System Engaged</b> &mdash; Successfully ingested {len(temp_df)} records.</div>", unsafe_allow_html=True)
        
        has_content = "content" in temp_df.columns or "text" in temp_df.columns
        if has_content:
            text_col = "content" if "content" in temp_df.columns else "text"
            
            
            st.dataframe(temp_df.head(5), use_container_width=True)
            
            if st.button("Initiate Neural Engine"):
                status_text = st.empty()
                progress_bar = st.progress(0)
                total_records = len(temp_df)
                # ── PHASE 1: Preprocessing (0 → 50%) ─────────────────────────────
                status_text.markdown("<div style='color:#7dd3fc; font-size:1rem; font-weight:bold;'><i class='fa-solid fa-satellite-dish'></i> &nbsp;Loading AI models — please wait...</div>", unsafe_allow_html=True)
                classifier = load_classification_model()  # cached after first call

                from concurrent.futures import ThreadPoolExecutor

                texts_list = temp_df[text_col].astype(str).tolist()

                def process_text_inline(text):
                    return apply_preprocessing(text)[:512]

                status_text.markdown("<div style='color:#7dd3fc; font-size:1rem; font-weight:bold;'><i class='fa-solid fa-microchip'></i> Phase 1/2 — Preprocessing (Parallelized)...</div>", unsafe_allow_html=True)
                with ThreadPoolExecutor() as executor:
                    processed_texts = list(executor.map(process_text_inline, texts_list))
                progress_bar.progress(0.5)

                # ── PHASE 2: Batch Classification (50 → 100%) ────────────────────
                status_text.markdown("<div style='color:#7dd3fc; font-size:1rem; font-weight:bold;'><i class='fa-solid fa-brain'></i> Phase 2/2 — Running AI Classification on all articles...</div>", unsafe_allow_html=True)
                batch_size = 16
                predictions = []
                for batch_start in range(0, total_records, batch_size):
                    batch = processed_texts[batch_start: batch_start + batch_size]
                    batch_results = classifier(batch, batch_size=batch_size, truncation=True, max_length=512)
                    predictions.extend([r['label'] for r in batch_results])
                    done = min(batch_start + batch_size, total_records)
                    pct2 = int(50 + (done / total_records) * 50)  # 50 → 100%
                    status_text.markdown(f"<div style='color:#7dd3fc; font-size:1rem; font-weight:bold;'><i class='fa-solid fa-brain'></i> Phase 2/2 — Classifying... {pct2}%</div>", unsafe_allow_html=True)
                    progress_bar.progress(pct2 / 100)

                status_text.markdown("<div style='color:#38bdf8; font-weight:800; margin-top:10px; font-size:1.2rem; text-shadow:0 0 10px rgba(56,189,248,0.5);'><i class='fa-solid fa-check'></i> Neural Pipeline Optimal — Classification Complete!</div>", unsafe_allow_html=True)
                temp_df['preprocessed_text'] = processed_texts
                temp_df['class'] = predictions
                st.session_state.df = temp_df
                st.session_state.page = "export"
                st.rerun()
        else:
            st.error("Protocol Error: Feature `content` or `text` is completely missing from payload.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DATA EXPORT HUB
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "export":
    st.markdown('<div class="section-header"><i class="fa-solid fa-file-export"></i> Data Export Hub</div>', unsafe_allow_html=True)

    if df is not None:
        text_col = "content" if "content" in df.columns else "text"
        st.dataframe(df[[text_col, 'class']].head(10), use_container_width=True)
        
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f"""
        <a href="data:file/csv;base64,{b64}" download="output.csv" class="nn-download-btn">
           <i class="fa-solid fa-download" style="margin-right:8px;"></i> Download Export Matrix
        </a>
        """, unsafe_allow_html=True)
        

    else:
        st.markdown("<div class='instruction-box'><i class='fa-solid fa-lock'></i> Hub Locked. Please upload and process a dataset from the <b>Upload</b> page first.</div>", unsafe_allow_html=True)
        if st.button("Go to Upload", key="btn_go_up_1"):
            st.session_state.page = "upload"
            st.session_state.pop("nav", None)
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — INTELLIGENT Q&A
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "qa":
    st.markdown("<div class='section-header'><i class='fa-solid fa-brain'></i> Intelligent Q&A Hub</div>", unsafe_allow_html=True)

    if df is not None:
        st.markdown("""
        <div class="instruction-box">
            Select a context block below and ask anything. Our RoBERTa-based deep learning node will instantly slice through the matrix to pinpoint the exact answer.
        </div>
        """, unsafe_allow_html=True)
        
        text_col = "content" if "content" in df.columns else "text"
        
        options = [f"Article {i+1}: {str(row[text_col])[:80]}..." for i, row in df.iterrows()]
        st.markdown("<style>div[data-testid='stSelectbox'] { width: 100% !important; } div[data-testid='stSelectbox'] > div { width: 100% !important; }</style>", unsafe_allow_html=True)
        selected_option = st.selectbox("Assign Context Node", options)
        selected_index = options.index(selected_option)
        
        # Show full article context
        full_article_text = str(df.loc[selected_index, text_col])
        with st.expander("View Full Article Context", expanded=False):
            st.markdown(f"<div style='color:#e0f2fe; line-height:1.8; font-size:1rem; font-family: Rajdhani, sans-serif; white-space: pre-wrap;'>{full_article_text}</div>", unsafe_allow_html=True)
        
        question_input = st.text_area("Formulate Query", placeholder="e.g., What was the main corporate action?")
        
        if st.button("Extract Answer Node"):
            if question_input.strip():
                with st.spinner("Extracting answer from context..."):
                    answer = answer_question(full_article_text, question_input)
                st.markdown(f"<div style='margin-top:25px; padding:25px; background:rgba(56,189,248,0.1); border-radius:16px; border:1px solid var(--border); box-shadow: inset 0 0 20px rgba(56,189,248,0.05); text-align: left;'><strong style='color:#fff; font-family:Orbitron, sans-serif; font-size:1.1rem; text-shadow:0 0 10px rgba(56,189,248,0.4);'><i class='fa-solid fa-bolt'></i> AI Decoded Answer:</strong><br><br><span style='color:#f5f5f7; line-height:1.8; font-size:1.05rem; font-family: Rajdhani, sans-serif;'>{answer}</span></div>", unsafe_allow_html=True)
        
    else:
        st.markdown("<div class='instruction-box'><i class='fa-solid fa-lock'></i> Q&A Hub Locked. Please upload and process a dataset from the <b>Upload</b> page first.</div>", unsafe_allow_html=True)
        if st.button("Go to Upload", key="btn_go_up_2"):
            st.session_state.page = "upload"
            st.session_state.pop("nav", None)
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — INSIGHTS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

# Cache insights generation to load instantly next time
@st.cache_data(show_spinner=False)
def compute_insights(texts_tuple):
    # Sentiment Extraction
    sentiment_labels = run_sentiment(list(texts_tuple))
    sentiments = {
        'Positive': sentiment_labels.count('Positive'),
        'Negative': sentiment_labels.count('Negative'),
        'Neutral':  sentiment_labels.count('Neutral')
    }
    majority_sentiment = max(sentiments, key=sentiments.get) if sentiments else 'Neutral'

    all_text = " ".join(texts_tuple).lower()
    words = re.findall(r'\b[a-z]{3,}\b', all_text)
    words = [w for w in words if w not in stop_words]
    from collections import Counter
    top_words = Counter(words).most_common(8)

    # Summarization (Optimized for HuggingFace Spaces CPU limits)
    combined_text = " ".join(texts_tuple)[:1500]
    tokenizer_summ, model_summ = load_summarizer()
    inputs_ids = tokenizer_summ(combined_text, max_length=512, return_tensors="pt", truncation=True)
    with torch.no_grad():
        summary_ids = model_summ.generate(inputs_ids["input_ids"], num_beams=3, min_length=20, max_length=100, early_stopping=True)
    summary = tokenizer_summ.decode(summary_ids[0], skip_special_tokens=True)

    return sentiment_labels, sentiments, majority_sentiment, top_words, summary, all_text

if st.session_state.page == "insights":
    st.markdown("<div class='section-header'><i class='fa-solid fa-chart-line'></i> Core Insights & Analytics</div>", unsafe_allow_html=True)

    if df is not None:
        col_dash, _ = st.columns([1, 2])
        with col_dash:
            trigger_dash = st.button("Generate Neural Synthesis")
            
        if trigger_dash:
            st.session_state.show_insights = True

        if st.session_state.get("show_insights", False):
            text_col = "content" if "content" in df.columns else "text"
            class_counts = df['class'].value_counts()
            total_articles = len(df)
            dominant_category = class_counts.idxmax()

            texts_tuple = tuple(df[text_col].astype(str).tolist())
            
            with st.spinner("Processing Neural Insights & Caching..."):
                sentiment_labels, sentiments, majority_sentiment, top_words, summary, all_text = compute_insights(texts_tuple)

            # --- METRICS ROW ---
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Matrix Scans", total_articles)
            with m2:
                st.metric("Dominant Sector", dominant_category)
            with m3:
                st.metric("Pulse Sentiment", majority_sentiment)

            st.markdown("<hr style='border-color: rgba(56,189,248,0.2); margin: 25px 0;'>", unsafe_allow_html=True)

            # --- SUMMARY CARD ---
            st.markdown(f"<div class='card' style='background:rgba(56,189,248,0.1); border-color:rgba(56,189,248,0.5);'><h3 style='margin-bottom:15px; text-shadow:0 0 10px rgba(56,189,248,0.5);'>Executive Neural Synthesis</h3><p style='color:#fff; line-height:1.7; font-size:1.15rem; font-weight:500;'>{summary}</p></div>", unsafe_allow_html=True)

            # --- CHARTS ROW ---
            r1, r2 = st.columns([1, 1], gap="large")
            
            with r1:
                st.markdown("<h4 style='margin-bottom:15px; color:#7dd3fc;'>Domain Distribution Radar</h4>", unsafe_allow_html=True)
                fig_pie = px.pie(values=class_counts.values, names=class_counts.index, hole=0.6,
                                 color_discrete_sequence=['#00b4d8', '#0077b6', '#03045e', '#90e0ef', '#caf0f8'])
                fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'), 
                                      showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
                                      height=320, margin=dict(t=40, b=0, l=0, r=0))
                fig_pie.update_traces(marker=dict(line=dict(color='#030816', width=2)))
                st.plotly_chart(fig_pie, use_container_width=True)

            with r2:
                st.markdown("<h4 style='margin-bottom:20px; color:#7dd3fc;'>Sentiment Deviation Matrix</h4>", unsafe_allow_html=True)
                sentiments_df = pd.DataFrame({'Sentiment': ['Positive', 'Negative', 'Neutral'], 'Count': [sentiments['Positive'], sentiments['Negative'], sentiments['Neutral']]})
                fig_bar = px.bar(sentiments_df, x='Count', y='Sentiment', orientation='h', color='Sentiment', color_discrete_map={'Positive': '#00e5ff', 'Negative': '#ff4d88', 'Neutral': '#4db8ff'})
                fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'), showlegend=False, height=320, bargap=0.5, margin=dict(t=30, b=0, l=0, r=0))
                fig_bar.update_traces(marker_line_width=0, width=0.4)
                st.plotly_chart(fig_bar, use_container_width=True)
                
                df_sentiment = df.copy()
                df_sentiment['sentiment'] = list(sentiment_labels)
                csv_sent = df_sentiment.to_csv(index=False)
                b64_sent = base64.b64encode(csv_sent.encode()).decode()
                st.markdown(f'<a href="data:file/csv;base64,{b64_sent}" download="sentiment_labelled_news.csv" class="nn-download-btn"><i class="fa-solid fa-download" style="margin-right:8px;"></i> Download Sentiment Data</a>', unsafe_allow_html=True)
                
            st.markdown("<hr style='border-color: rgba(56,189,248,0.2); margin: 25px 0;'>", unsafe_allow_html=True)

            # --- TEXT ANALYSIS ROW ---
            w1, w2 = st.columns([1, 2], gap="large")
            with w1:
                html_nodes = "<h4 style='margin-bottom:20px; color:#7dd3fc;'>Top Frequency Nodes</h4><div class='card'>"
                for w, freq in top_words:
                    html_nodes += f"<div style='display:flex; justify-content:space-between; padding:12px 0; border-bottom:1px solid rgba(56,189,248,0.2); color:#fff; font-weight:500;'><span>{w.capitalize()}</span><span style='color:#38bdf8; font-weight:800;'>{freq}</span></div>"
                html_nodes += "</div>"
                st.markdown(html_nodes, unsafe_allow_html=True)
                
            with w2:
                st.markdown("<h4 style='margin-bottom:20px; color:#7dd3fc;'>Semantic Cloud Visualization</h4>", unsafe_allow_html=True)
                wc = WordCloud(width=1000, height=450, background_color='#030816', colormap='Blues').generate(all_text)
                fig, ax = plt.subplots(figsize=(10, 4.5))
                ax.imshow(wc, interpolation='bilinear')
                ax.axis("off")
                fig.patch.set_facecolor('none')
                st.pyplot(fig)

    else:
        st.markdown("<div class='instruction-box'><i class='fa-solid fa-lock'></i> Analytics Locked. Please upload and process a dataset from the <b>Upload</b> page first.</div>", unsafe_allow_html=True)
        if st.button("Go to Upload", key="btn_go_up_3"):
            st.session_state.page = "upload"
            st.session_state.pop("nav", None)
            st.rerun()

st.markdown("<p style='text-align: center; color: rgba(56,189,248,0.5); font-size: 0.9rem; margin-top: 5rem; font-weight:700; font-family: Orbitron; letter-spacing: 2px;'>GROUP 01 &copy; 2026</p>", unsafe_allow_html=True)
