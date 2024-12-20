# University FAQ Chatbot (Master’s Capstone)

## Overview
This chatbot, named **LUBot**, was developed to assist students at Lakehead University with FAQs related to admissions, immigration, events, and important dates. By integrating natural language processing and web scraping, it eliminates the need for students to manually search the university’s website for information.

## Features
- **Natural Language Understanding (NLU):** Built using Rasa's DIET Classifier for intent recognition and entity extraction, achieving an F1-score of 0.986.  
- **Dynamic Information Retrieval:**
  - **Holidays:** Extracts and retrieves Lakehead University's annual holidays using scraped and preprocessed data.  
  - **Events from Facebook:** Scrapes posts from Lakehead University's official Facebook page and uses Doc2Vec embeddings to display relevant events.  
  - **Professor Search:** Allows users to find faculty details, research interests, and contact information.  
  - **Admissions and More:** Provides information on admissions, application tracking, tuition, housing, and other student resources dynamically.  
- **Fallback and Confidence Handling:** Implements a two-stage fallback mechanism for out-of-scope intents and confidence thresholding for better response accuracy.
- **Feedback Collection:** Stores user feedback and conversation history for continuous improvement of chatbot performance.   

## Implementation Details
- **Pipeline:** Utilized tokenization, featurization, and classification via Rasa's modular pipeline with WhitespaceTokenizer, CountVectorFeaturizer, and LexicalSyntacticFeaturizer.  
- **Customization:** Custom actions for retrieving holiday and admissions data, enhancing conversational accuracy.  
- **Web Interface:** Developed using React.js, HTML5, and CSS3, hosted on AWS EC2 with Dockerized NLU, action, and front-end servers.  
- **Database Integration (Optional):** Designed with SQLite3 to store user feedback and conversation history for potential improvement of training data.  

## Tools and Technologies
- **Frameworks:** Rasa, React.js  
- **Languages:** Python3, JavaScript  
- **Libraries:** Pandas, BeautifulSoup, Facebook-Scraper  
- **Hosting:** AWS EC2, Docker  
- **Model:** DIET Classifier with hyperparameters optimized for intent classification and response generation.  

Currently, LUBot uses in-memory storage during user interactions. Future iterations can integrate a dedicated database to store conversation history, enabling dataset expansion and model retraining for improved performance.

