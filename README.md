# Text Analytics News Classifier

This project is a text analytics and machine learning application that processes news articles and classifies them into one of five categories: Business, Opinion, Political, Sports, and World. It fine-tunes a DistilBERT model to perform the classification.

## Project Structure

- `extract.py`: Contains the data preprocessing pipeline, exploratory data analysis (EDA), model training using Hugging Face Transformers, and model evaluation.
- `src/streamlit_app.py`: A Streamlit web application that provides an interface to interact with the trained model for classifying news text.
- `test_app.py` & `src/update_app.py`: Scripts for testing and updating the application logic.
- `Data/`: Contains the initial datasets and preprocessed datasets.

## Requirements

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

## Running the Application

To launch the web interface, execute the following command:

```bash
streamlit run src/streamlit_app.py
```
