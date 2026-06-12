FROM python:3.10-slim

#Install System Dependencies as Root
USER root
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

#Create the specific User (UID 1000)
RUN useradd -m -u 1000 user

#Switch to the new User
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

#Copy requirements & Install 
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

#Download NLTK data securely strictly to User's Home
ENV NLTK_DATA=$HOME/nltk_data
RUN mkdir -p $HOME/nltk_data && \
    python3 -m nltk.downloader -d $HOME/nltk_data stopwords punkt punkt_tab averaged_perceptron_tagger averaged_perceptron_tagger_eng wordnet

#Copy the whole application
COPY --chown=user . $HOME/app/

#Setup Cache folders properly so it doesn't try to write to read-only folders
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
ENV HF_HOME=$HOME/huggingface
ENV TOKENIZERS_PARALLELISM=false

EXPOSE 7860

# Start Streamlit properly
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
