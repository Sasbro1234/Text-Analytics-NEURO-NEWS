# NeuroNews: Streamlit Application Code Explanation

This document provides a simple, structured explanation of the codebase behind the NeuroNews web application (`streamlit_app.py`).

---

## 1. Library Imports and Setup
```python
import streamlit as st
import pandas as pd
import nltk
from transformers import pipeline
from spellchecker import SpellChecker
...
```
**Explanation:** 
This section loads all the fundamental tools required for the application. `streamlit` builds the web dashboard, `pandas` processes the tabular datasets, `nltk` acts as the engine for language processing tasks, and the `transformers` library provided by Hugging Face loads the deep learning AI models.

## 2. NLTK Resource Downloader
```python
@st.cache_resource(show_spinner=False)
def ensure_nltk_resources():
    required_packages = ['stopwords', 'punkt', 'punkt_tab', 'averaged_perceptron_tagger', ...]
    for pkg in required_packages:
        nltk.download(pkg, quiet=True)
ensure_nltk_resources()
```
**Explanation:** 
Some NLP operations require specific dictionaries. This code ensures that all required dictionaries (like 'stopwords' and parts-of-speech taggers) are downloaded to the server before the app starts running. The `@st.cache_resource` decorator ensures this heavy download check only runs once when the app is booted.

## 3. Text Preprocessing Functions
```python
def clean_text(text): ...
def remove_stopwords(text): ...
def lemmatize_tokens(text): ...
def apply_preprocessing(text): ...
```
**Explanation:** 
Before text can be fed into an AI, it needs to be "cleaned". This block contains several specific functions:
- `clean_text` makes words lowercase and drops punctuation.
- `remove_stopwords` removes common filler words like "the" and "an".
- `lemmatize_tokens` converts words to their root form (e.g., "running" becomes "run").
- `apply_preprocessing` groups all these individual steps into a single pipeline.

## 4. Deep Learning Model Initializations
```python
@st.cache_resource
def load_classification_model():
    return pipeline("text-classification", model="groupproj/group1-news-classifier-model", ...)

def run_sentiment(texts): ...
def load_summarizer(): ...
def load_qa_model(): ...
```
**Explanation:** 
This block handles loading the powerful Transformer models from Hugging Face into memory. 
- The text-classification pipeline categorizes articles.
- The `load_sentiment_model` extracts emotion (Positive/Negative/Neutral) using Twitter-RoBERTa.
- The `load_summarizer` function pulls DistilBART to generate article summaries. 
- The `load_qa_model` loads Deepset's RoBERTa trained on SQuAD to answer direct questions. Since these models are huge, they are heavily cached (`@st.cache_resource`).

## 5. User Interface (UI) and Custom Styling (CSS)
```python
st.set_page_config(page_title="NEURONEWS", layout="wide", ...)

vanta_js = """ ... <script> ... VANTA.NET(...) ... </script> ... """
components.html(vanta_js, width=0, height=0)

st.markdown("""<style> ... </style>""", unsafe_allow_html=True)
```
**Explanation:** 
This handles the entire visual presentation. First, it injects custom JavaScript to render an animated particle background loop (using Vanta.js). Afterwards, it injects hundreds of lines of custom CSS (`<style>`) which adds neon glow effects, removes standard Streamlit borders, implements custom fonts, and builds the "Glassmorphism" hover animations used by the application's cards.

## 6. Page Routing and Navigation Logic
```python
if "page" not in st.session_state:
    st.session_state.page = "home"

page_labels = {"home": "HOME", "upload": "UPLOAD", ...}
selected_label = st.radio(label="nav", options=list(page_labels.values()), ...)
```
**Explanation:** 
Because Streamlit conventionally loads everything on a single page, this code cleverly structures a multi-page app. It saves which page the user is currently on inside a memory variable (`st.session_state.page`). A custom-styled Radio Button acts as a top-navigation bar, re-routing the user to different blocks of code.

## 7. The Home Page (`page == "home"`)
```python
if st.session_state.page == "home":
    # HTML structuring for Dashboard descriptions and Glass-Cards
```
**Explanation:** 
Displays the landing page containing a welcoming overview and the interactive HTML cards (Classification, Q&A, Analytics), and renders the `INITIALIZE SYSTEM` button that shifts the app state to the Upload Page.

## 8. Data Upload & Classification Logic (`page == "upload"`)
```python
uploaded_file = st.file_uploader("Drop dataset matrix here", ...)
if st.button("Initiate Neural Engine"):
    # ThreadPool Executor running preprocessing
    # Batch processing with classifier model
```
**Explanation:** 
This renders a file uploader allowing users to upload datasets. When triggered, it implements a `ThreadPoolExecutor` to clean all texts in parallel across multiple CPU threads. It then pushes the clean text in groups (batches) to the classification model, filling up a visual progress bar as it goes. Finally, it saves the predictions to the data table and shifts the user to the Export Hub.

## 9. Smart Q&A Hub (`page == "qa"`)
```python
selected_option = st.selectbox("Assign Context Node", options)
question_input = st.text_area("Formulate Query", ...)
if st.button("Extract Answer Node"):
    answer = answer_question(full_article_text, question_input)
```
**Explanation:** 
Users select an article and type a question. The Python code passes both the text and the question into the Deepset-RoBERTa model setup earlier. The model identifies where inside the text the answer exists, string-formats it, and displays it for the user.

## 10. Analytics & Insights Hub (`page == "insights"`)
```python
@st.cache_data(show_spinner=False)
def compute_insights(texts_tuple):
    # Sentiment calculation, Summary generation, Common words finding

if st.session_state.page == "insights":
    # Plotly pie charts and bar charts creation
    # WordCloud rendering
```
**Explanation:** 
When the Insights button is toggled, an extremely heavy logic function `compute_insights()` triggers. It executes sentiment analysis on the data and forces the DistilBART model to write an overarching executive summary. Crucially, this function is backed by `@st.cache_data`, meaning the slow processing only happens once. Finally, it uses libraries like Application's `Plotly` and `WordCloud` to generate interactive mathematical bar charts and tag-clouds, finishing the data story!
