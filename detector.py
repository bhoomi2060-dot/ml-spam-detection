# -*- coding: utf-8 -*-
"""
Created on Mon May 11 00:06:37 2026

@author: Admin
"""

import streamlit as st
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

ps = PorterStemmer()

def preprocess(text):
    text = str(text).lower()
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t.isalnum()]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    # tokens = [ps.stem(t) for t in tokens]  # comment out hai toh yahan bhi mat karo
    return " ".join(tokens)

folder = "models"
sms_model   = pickle.load(open(f"{folder}/sms_model.pkl", 'rb'))
tfidf_sms   = pickle.load(open(f"{folder}/tfidf_sms.pkl", 'rb'))
email_model = pickle.load(open(f"{folder}/email_model.pkl", 'rb'))
tfidf_email = pickle.load(open(f"{folder}/tfidf_email.pkl", 'rb'))

st.title("🛡️ Scam Detector")
st.subheader("Bhoomika & Nancy | ML Project")

option = st.radio("Select Type:", ["SMS", "Email"])
input_text = st.text_area("Enter message here:")

if st.button("Check"):
    if input_text.strip():
        processed = preprocess(input_text)
        if option == "SMS":
            vec = tfidf_sms.transform([processed])
            result = sms_model.predict(vec)[0]
        else:
            vec = tfidf_email.transform([processed])
            result = email_model.predict(vec)[0]
        
        if result == 1:
            st.error("🚨 SPAM detected!")
        else:
            st.success("✅ Safe message!")
    else:
        st.warning("Please enter some text!")
