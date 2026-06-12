# Libraries for data preparation
import pandas as pd # to handle the dataframe
from IPython.display import display # to format the output of a cell
from wordcloud import WordCloud # for generating the wordcloud in EDA
import matplotlib.pyplot as plt # for EDA output formatting
from sklearn.feature_extraction.text import CountVectorizer
import re # regex library
import string # for common string operations

# Libraries for text preprocessing 
# import nltk library
import nltk # Natural Language Toolkit
from nltk.corpus import stopwords # import the stopwords from nltk library
# nltk.download('stopwords') # Download stop words list and storing it locally
from nltk.stem import PorterStemmer # stemming
from nltk.stem import WordNetLemmatizer # lemmatizing
from nltk.corpus import wordnet # to get the synsets of English words
# nltk.download('wordnet')
from collections import Counter # to get the count
from spellchecker import SpellChecker #to check spellings 


# Import the libraries required for finetuning 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers import TrainingArguments, Trainer
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from transformers import EarlyStoppingCallback
from transformers import pipeline
from datasets import Dataset
import evaluate

from huggingface_hub import login
from huggingface_hub import notebook_login

#reading the excel files separately
business_df = pd.read_excel("Data/Data/Business.xlsx")
opinion_df = pd.read_excel("Data/Data/Opinion.xlsx")
political_df = pd.read_excel("Data/Data/Political_gossip.xlsx")
sports_df = pd.read_excel("Data/Data/Sports.xlsx")
world_df = pd.read_excel("Data/Data/World_news.xlsx")

# Initial glimpse of the excel files
# Glimpse of the Business News Excel file
print("Business News")
display(business_df.head(5))
display(business_df.info())

# Glimpse of the Personal Views Excel file
print("Personal Views")
display(opinion_df.head(5))
display(opinion_df.info())

# Glimpse of the Political News Excel file
print("Political News")
display(political_df.head(5))
display(political_df.info())

# Glimpse of the Sports News Excel file
print("Sports News")
display(sports_df.head(5))
display(sports_df.info()) 

# Glimpse of the International News Excel file
print("International News")
display(world_df.head(5))
display(world_df.info())        

# Business News
# Dropping title and Unnamed: 0 columns
business_df = business_df.drop(columns = ["title","Unnamed: 0"])

# Adding the class column
business_df["Class"] = "Business"

# drop duplicated records if any
business_df.drop_duplicates(keep="first", inplace=True)# any duplicates after the first occurance will be dropped

# drop null records
business_df.dropna(inplace=True)

# Viewing the updated dataset
business_df.head(5)

# Opinion News
# Dropping title and Unnamed: 0 columns
opinion_df = opinion_df.drop(columns = ["title","Unnamed: 0"])

# Adding the class column
opinion_df["Class"] = "Opinion"

# drop duplicated records if any
opinion_df.drop_duplicates(keep="first", inplace=True)# any duplicates after the first occurance will be dropped

# drop null records
opinion_df.dropna(inplace=True)

# Viewing the updated dataset
opinion_df.head(5)

# Political News
# Dropping title and Unnamed: 0 columns
political_df = political_df.drop(columns = ["title","Unnamed: 0"])

# Adding the class column
political_df["Class"] = "Political"

# drop duplicated records if any
political_df.drop_duplicates(keep="first", inplace=True)# any duplicates after the first occurance will be dropped

# drop null records
political_df.dropna(inplace=True)

# Viewing the updated dataset
political_df.head(5)

# Sports News
# Dropping title and Unnamed: 0 columns
sports_df = sports_df.drop(columns = ["title","Unnamed: 0"])

# Adding the class column
sports_df["Class"] = "Sports"

# drop duplicated records if any
sports_df.drop_duplicates(keep="first", inplace=True)# any duplicates after the first occurance will be dropped

# No null records to be removed

# Viewing the updated dataset
sports_df.head(5)

# World News
# Dropping title and Unnamed: 0 columns
world_df = world_df.drop(columns = ["title","Unnamed: 0"])

# Adding the class column
world_df["Class"] = "World"

# drop duplicated records if any
world_df.drop_duplicates(keep="first", inplace=True)# any duplicates after the first occurance will be dropped

# No null records to be removed

# Viewing the updated dataset
world_df.head(5)

# preparing a single DataFrame that contains all the records from all five files.
all_news_df = pd.concat([business_df, opinion_df, political_df, sports_df, world_df], ignore_index=True)

# Summary of the new data set
print(all_news_df.info())
print(all_news_df.head(5))
print(all_news_df.tail(5))

# Saving the final file as ‘Daily_Mirror_News.xlsx’
all_news_df.to_excel("Data/Data/Daily_Mirror_News.xlsx", index=False)

# Word Cloud 
# Combine all text data from the 'content' column into one large string. 
text = " ".join(all_news_df["content"].astype(str))

# Generating a visual representation of word frequencies
wordcloud = WordCloud(width=1000, height=600, colormap="inferno").generate(text)

# Rendering the plot using matplotlib features
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Word Cloud (Before Preprocessing)")
plt.show()

# Unigram
# Converting text into a bag-of-words
vectorizer = CountVectorizer()  # default = unigrams

# Fit the vectorizer to the 'content' column of all_news_df and transform the text into a sparse matrix
# Each row = a document/news article
# Each column = a unique word from the corpus
X = vectorizer.fit_transform(all_news_df["content"].astype(str))

# Getting the total frequency of each word in the entire dataset
sum_words = X.sum(axis=0)

# vectorizer.vocabulary_ maps each word to its column index in X
words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
# Sort the list of words in the descending order
words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)

# Print the top 10 most frequent words in the dataset
print(words_freq[:10])

# Bigram
# consider sequences of exactly 2 consecutive words
vectorizer = CountVectorizer(ngram_range=(2,2))
X = vectorizer.fit_transform(all_news_df["content"].astype(str))

sum_words = X.sum(axis=0)

bigrams = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
bigrams = sorted(bigrams, key=lambda x: x[1], reverse=True)

print(bigrams[:10])

# Trigram
# consider sequences of exactly 3 consecutive words
vectorizer = CountVectorizer(ngram_range=(3,3))
X = vectorizer.fit_transform(all_news_df["content"].astype(str))

sum_words = X.sum(axis=0)

bigrams = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
bigrams = sorted(bigrams, key=lambda x: x[1], reverse=True)

print(bigrams[:10])

# Text Length Distribution
# Making a copy of the original dataset to keep the original data intact
all_news_1_df = all_news_df.copy()

# Create a new column 'text_length' that stores the number of characters in each article
all_news_1_df["text_length"] = all_news_df["content"].astype(str).apply(len)

# Plot a histogram of text lengths to visualize their distribution
all_news_1_df["text_length"].hist(color="orange")
plt.title("Text Length Distribution (Before Preprocessing)")
plt.show()

# Mean Text Length by Class
all_news_1_df.groupby("Class")["text_length"].mean()

# Words that occur the most
# Select the top 10 most frequent words from the words_freq list
top_words = words_freq[:10]
df_words = pd.DataFrame(top_words, columns=["Word", "Frequency"])

# Create a bar chart of the top words
df_words.plot(x="Word", y="Frequency", kind="bar", color="orange")
plt.title("Top Words (Before Preprocessing)")
plt.xticks(rotation=45)
plt.show()

# Reading the excel into a new variable to proceed with preprocessing while the original file is kept intact
preprocess = pd.read_excel("Data/Data/Daily_Mirror_News.xlsx")

# display a single text record at 3rd index
preprocess.iloc[2]

preprocess["cleaned_content"] = preprocess["content"].str.lower()
preprocess.iloc[2]

preprocess["cleaned_content"] = preprocess["cleaned_content"].str.strip()
preprocess.iloc[2]


# observe the punctuations in the string library
string.punctuation

# punctuations to be removed

# define the function
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation)) # remove all the punctuations

# applying the function
preprocess["cleaned_content"] = preprocess["cleaned_content"].apply(remove_punctuation)
preprocess.iloc[2]

# Get the list of stop words
stop_words = set(stopwords.words('english'))
print(stop_words)

# define the function
def remove_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in stop_words])

# apply the function
preprocess["cleaned_content"] = preprocess["cleaned_content"].apply(lambda text: remove_stopwords(text))
preprocess.iloc[2]

# define the function
def remove_special_characters(text):
    return re.sub(r'[^A-Za-z\s]', '', text)

# apply the function
preprocess["cleaned_content"] = preprocess["cleaned_content"].apply(lambda text: remove_special_characters(text))
preprocess.iloc[235]

# Get the count of each word in cleaned_text
word_count = Counter(preprocess["cleaned_content"].str.split(expand=True).stack())

# Define a threshold for common words
n_common_words = 10
# Get a set of common words
common_words = set([word for (word,count) in word_count.most_common(n_common_words)])
print(common_words)

# define the function
def remove_common_words(text):
    return " ".join([word for word in str(text).split() if word not in common_words])

# apply the function
preprocess["cleaned_content"] = preprocess["cleaned_content"].apply(lambda text: remove_common_words(text))
preprocess.iloc[287]

# Define a threshold for rare words
n_rare_words = 50
# Get a set of rare words
rare_words = set([word for (word,count) in word_count.most_common()[:-n_rare_words-1:-1]])
print(rare_words)

# initial text
preprocess["cleaned_content"].iloc[1003]

# define the function
def remove_rare_words(text):
    return " ".join([word for word in str(text).split() if word not in rare_words])

preprocess["cleaned_content"] = preprocess["cleaned_content"].apply(lambda text: remove_rare_words(text))
preprocess["cleaned_content"].iloc[1003]

# initial text
preprocess['cleaned_content'].iloc[8]

# nltk.download('punkt_tab')

preprocess['tokenized_content'] = preprocess['cleaned_content'].apply(lambda text: nltk.word_tokenize(text))
# tokenized text
preprocess['tokenized_content'].iloc[2]

# lookup a word
wordnet.synsets('looking')

# nltk.download('averaged_perceptron_tagger_eng')

# initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# mapping for word types
wordnet_map = {"N":wordnet.NOUN,'V':wordnet.VERB,'J':wordnet.ADJ,'R':wordnet.ADV}

# define the function
def lemmatize_tokens(tokens):
    lemmas = []
    for token in tokens:
        pos_tag = nltk.pos_tag([token])[0][1][0].upper()  # Get the POS tag
        lemma = lemmatizer.lemmatize(token, wordnet_map.get(pos_tag, wordnet.NOUN))  # Lemmatize with the appropriate POS tag
        lemmas.append(lemma)
    return lemmas


# applying the function
preprocess['lematized_content'] = preprocess['tokenized_content'].apply(lambda text: lemmatize_tokens(text))
preprocess[['tokenized_content','lematized_content']].tail(5)

# initialize the spellchecker
spell = SpellChecker()

# define the function
def spell_check(text):
    words = text.split()
    checked_words = []
    for word in words:
        corrected_word = spell.correction(word)
        if corrected_word:
            checked_words.append(corrected_word)
        else:
            checked_words.append(word)  # If no correction found, keep the original word

    return ' '.join(checked_words)

# cleaned text
print(spell_check(preprocess['cleaned_content'].iloc[9]))

# Copying only the lemmatized_content and Class into a new dataframe
model_df = preprocess[['lematized_content', 'Class']].copy()

# Converting lematized_content column from a list to string
model_df['lematized_content'] = model_df['lematized_content'].apply(lambda x: ' '.join(x))

# Saving the final file as ‘Preprocessed_Daily_Mirror_News.xlsx’
model_df.to_excel("Data/Data/Preprocessed_Daily_Mirror_News.xlsx", index=False)

# Word Cloud 
# Combine all text data from the 'content' column into one large string
# This is required because WordCloud expects a single block of text
text = " ".join(preprocess["cleaned_content"].astype(str))

# Generating a visual representation of word frequencies
wordcloud = WordCloud(width=1000, height=600, colormap="inferno").generate(text)

# Rendering the plot using matplotlib features
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Word Cloud (After Preprocessing)")
plt.show()

# Bigram
# consider sequences of exactly 2 consecutive words
vectorizer = CountVectorizer(ngram_range=(2,2))
X = vectorizer.fit_transform(model_df["lematized_content"].astype(str))

sum_words = X.sum(axis=0)

bigrams = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
bigrams = sorted(bigrams, key=lambda x: x[1], reverse=True)

print(bigrams[:10])

# Text Length Distribution
# Making a copy of the original dataset to keep the original data intact
model_1_df = model_df.copy()

# Create a new column 'text_length' that stores the number of characters in each article
model_1_df["text_length"] = model_df["lematized_content"].astype(str).apply(len)

# Plot a histogram of text lengths to visualize their distribution
model_1_df["text_length"].hist(color="orange")
plt.title("Text Length Distribution (After Preprocessing)")
plt.show()

#Step 1: Load the preprocessed dataset
df = pd.read_excel("Data/Data/Preprocessed_Daily_Mirror_News.xlsx")
df.head()

#Step 2: Encode labels 
le = LabelEncoder()
df["Class"] = le.fit_transform(df["Class"])
 
id_to_label = {
    0: "Business",
    1: "Opinion",
    2: "Political",
    3: "Sports",
    4: "World"
}

label_to_id = {
    "Business": 0,
    "Opinion": 1,
    "Political": 2,
    "Sports": 3,
    "World": 4
}
print(id_to_label)


#Step 3: train and validation split
X_train, X_val, y_train, y_val = train_test_split(
    df["lematized_content"],
    df["Class"],
    test_size=0.2,
    random_state=42,
    stratify=df["Class"]
)

#Step 4: Converting the original df to a data structure that is easy to handle using transformers
train_dataset = Dataset.from_dict({"text": list(X_train),"label": list(y_train)})

val_dataset = Dataset.from_dict({"text": list(X_val),"label": list(y_val)})

print(train_dataset)

print(val_dataset)

# Login to hugging face group account
login("YOUR_HUGGINGFACE_TOKEN_HERE")

# Step 5: Load tokenizer and model
model_name = "distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(
    model_name,
    num_labels=5,
    id2label=id_to_label,    
    label2id=label_to_id      
)

#Step 6: Tokenize the dataset
def tokenize_function(example):
    return tokenizer(
        example["text"],
        padding="max_length",
        truncation=True,
        max_length=128
    )

tokenized_train_dataset = train_dataset.map(tokenize_function, batched=True)
tokenized_val_dataset = val_dataset.map(tokenize_function, batched=True)

#Step 7: Evaluation metrics
accuracy_metric = evaluate.load("accuracy")
precision_metric = evaluate.load("precision")
recall_metric = evaluate.load("recall")
f1_metric = evaluate.load("f1")

def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=1)
    
    return {
        "accuracy": accuracy_metric.compute(predictions=preds, references=p.label_ids)["accuracy"],
        "precision": precision_metric.compute(predictions=preds, references=p.label_ids, average="weighted")["precision"],
        "recall": recall_metric.compute(predictions=preds, references=p.label_ids, average="weighted")["recall"],
        "f1": f1_metric.compute(predictions=preds, references=p.label_ids, average="weighted")["f1"],
    }

#Step 8: Trainer setup

args = TrainingArguments(
    output_dir="Model_Output", # Directory where model checkpoints and outputs will be saved
    run_name="news_classifier", # Name of the training run
    eval_strategy="epoch",  # Evaluate the model after each full pass (epoch) through the dataset
    save_strategy="epoch",  # Save the model after each epoch 
    per_device_train_batch_size=4,  # Number of samples processed at once during training (smaller = less memory usage)
    per_device_eval_batch_size=4,   # Number of samples processed at once during evaluation
    num_train_epochs=3,           # Total number of times the model will see the entire dataset 
    learning_rate=2e-5,          # Controls how fast the model updates weights (optimal for BERT-based models)
    weight_decay=0.01,       #prevent overfitting
    logging_steps=50,        # Logs training progress every 50 steps
    seed=42,                # Ensures reproducibility of results (same random behavior each run)
    load_best_model_at_end=True   # Loads the best-performing model based on validation results
)

trainer = Trainer(
    model=model,   #The pre-trained DistilBERT model to be fine-tuned
    args=args,   
    train_dataset=tokenized_train_dataset,  # Tokenized dataset used for training the model
    eval_dataset=tokenized_val_dataset,  # Tokenized dataset used for evaluating model performance
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
)

# Step 9: Train the model
train_output = trainer.train()
print(train_output)

# Login to Hugging Face
notebook_login()

# Save model and Tokenizer locally
trainer.save_model("news_model")
tokenizer.save_pretrained("news_model")

model.push_to_hub("groupproj/group1-news-classifier-model")
tokenizer.push_to_hub("groupproj/group1-news-classifier-model")

pipe = pipeline("text-classification", model="groupproj/group1-news-classifier-model")

pipe("Sri Lanka won the cricket match yesterday")

pipe("It is clear that the government needs to take stronger action to address corruption.")

pipe ("Sources say that a senior minister may soon resign due to internal party conflicts.")

pipe("Stock market prices increased significantly due to strong investor confidence.")

