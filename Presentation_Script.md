**Speaker:** Sasmika
**Estimated Time:** ~6 minutes
**Context:** Dinali just finished presenting her section. Sasmika takes over to do the live demo.

---

**[Slide to the Application / Open the App on Screen]**

"Thank you, Dinali! Hello everyone, I am Sasmika, and I will be taking you through the live demonstration of our application, NeuroNews, and explaining the core components and the tech stack we used to bring this to life.

As you can see on the screen, this is our landing page. We really wanted the user interface to feel modern, immersive, and professional. To achieve this, the frontend is built using **Streamlit**, which allows us to construct the web app entirely in Python. However, instead of settling for the default layout, we bypassed its limitations by heavily injecting custom HTML and CSS. We implemented modern UI design patterns like **Glassmorphism** for the frosted-glass cards you see here, and integrated a 3D JavaScript particle background powered by **Vanta.js** and **Three.js**. For our dynamic graphing components, we utilize **Plotly** and **Matplotlib**.

Looking at the home page, we give the user a very clear idea of what the application does. At its core, NeuroNews processes massive amounts of news data to give actionable intelligence. We broke the functionality down into three main cards here: News Classification, Smart Q&A, and Analytics. 

So let's go ahead and click on the **'INITIALIZE SYSTEM'** button to actually see this in action.

**(Click 'INITIALIZE SYSTEM' – navigate to the Upload page)**

Now we are inside the Data Upload Protocol. Here, users can drop in their raw dataset, like a CSV or Excel file containing hundreds of news articles. 

**(Upload a sample dataset into the uploader)**

Once the file is uploaded, you can see a quick preview of the raw data. Now, I'm going to click **'Initiate Neural Engine'**. 

**(Click the button and let the progress bar run)**

While this processes, let me explain what is happening under the hood. Our backend foundation relies on **Pandas** for high-speed data manipulation, matrix operations, and routing. At the core of our AI processing is **PyTorch**, serving as the deep learning framework to run advanced Transformer models integrated directly from the **Hugging Face Hub**. 
First, the data goes through a rigorous NLP preprocessing pipeline. We use the **NLTK (Natural Language Toolkit)** and **SpellChecker** libraries to aggressively clean the text. We perform noise reduction, regex filtering, stop-word removal, and efficient batch-level Part-of-Speech tagging with Lemmatization to give the models the cleanest possible input.

Once the data is structured, it is handed over to our first Transformer model. This is a custom fine-tuned neural network that categorizes every single news article into specific domain topics dynamically. By leveraging PyTorch's native batch-processing tensors, the inference executes blazingly fast.

**(Wait for the pipeline to complete and transition to the Export Hub)**

Alright, so the pipeline has completed successfully! As you can see, we are automatically navigated to the **Data Export Hub**. Here, the original dataset is shown, alongside the newly predicted target classes for each article. If the user wants to take this classified data to another software, they can neatly download it right here as a CSV.

But of course, we go way beyond just classifying. Let's move over to the **Smart Q&A Hub**.

**(Click on the Q&A tab from the top navigation bar)**

This is one of the most powerful features. Let's say you have a massive news article, and you don’t have the time to read it all. You can assign an article from the dropdown here as the 'Context Node'. 

**(Select an article from the dropdown box)**

Now, I can type a direct question about this news piece right into the query box. Let's ask: *(type a question relevant to the selected context, for example, 'What was the main corporate action?')* ... and click **Extract Answer Node**.

Under the hood, this uses **Deepset's RoBERTa model fine-tuned on SQuAD 2.0**. Instead of just generating text, this model actually acts as a reader—it scans the entire article, maps the context vectors, and pinpoints the exact span of words containing the answer, fetching it in milliseconds. And there we go! As we can see, it extracted the precise answer cleanly.

Next, let's explore the final module. Let's click on the **Insights Dashboard**.

**(Click the Insights tab from the top navigation bar)**

When dealing with thousands of news articles, raw data is very hard to digest. So, let me click **'Generate Neural Synthesis'**.

**(Click the generate button and wait for the dashboard to load)**

Again, we are utilizing deep learning here to extract deeper meaning.
First, we look at the 'Pulse Sentiment'. To figure out whether the overall news cycle is positive, negative, or neutral, we aren't using traditional dictionaries. Instead, we use a **Twitter-RoBERTa-base-sentiment** model. It understands context, sarcasm, and sentence structures natively. 

If we look at the top here, we have the **Executive Neural Synthesis**. This is generated by **DistilBART** (a sequence-to-sequence model). It takes the major chunks of our processed news data and mathematically distills it into a readable, short human-like narrative summary of the entire dataset.

And down here, as we can see, we have interactive visual dashboards powered by **Plotly** and **Matplotlib**. We have a Domain Distribution Radar showing the breakdown of categorized topics. Next to it, the Sentiment Deviation Matrix maps out the frequency of emotions extracted by RoBERTa. Finally, at the bottom, we visualize the Top Frequency Nodes and a Semantic Word Cloud, giving users an immediate, graphical understanding of the most prominent topics being reported on.

So, taking a step back, we’ve taken raw CSV text, structured it through NLTK, classified it, deeply analyzed user questions within it, extracted sentiment, summarized the narrative using multiple Hugging Face models, and presented it in an immersive dashboard. 

That concludes the technical demonstration of NeuroNews. Thank you for listening, and I’ll be happy to answer any questions!"
