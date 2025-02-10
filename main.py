from fastapi import FastAPI
from pydantic import BaseModel
import re
import numpy as np
import pandas as pd
from hazm import *
import timeit
import threading
import time
from enum import Enum
from patterns import *

app = FastAPI()

# مدل داده‌ای برای درخواست از سمت کاربر
class StoryRequest(BaseModel):
    story: str

# مدل داده‌ای برای پاسخ سرور
class StoryResponse(BaseModel):
    validity: str
    role: str
    capability: str
    goal: str
    normalized_story: str
    tokenized_story: str
    lemmatized_story: str
    non_functional_requirement: str
    other_non_functional_requirements: list


def userstory_check_first(userstory):
    pattern = r"^به عنوان\s+(?:یک\s+)?(.+?)،?\s+من می‌خواهم\s+(.+?)\s+تا بتوانم\s+(.+?)$"
    match = re.match(pattern,userstory)
    if match:
        role = match.group(1).strip()
        capability = match.group(2).strip()
        objective = match.group(3).strip()
        return role, capability, objective
    else:
        return None, None, None

def informal_normalize(userstory):
    normalizer = InformalNormalizer()
    informal_normalized_text = normalizer.normalize(userstory)
    small_array = informal_normalized_text[0]
    first_elements = [inner[0] for inner in small_array if len(inner) > 0]
    normalized_text = ' '.join(first_elements)
    return normalized_text

def normalize(userstory: str):
    normalizer = Normalizer()
    normalized_text = normalizer.normalize(userstory)
    return normalized_text

def tokenize(userstory):
     tokens = word_tokenize(userstory)
     return tokens

def stopwords(tokens):
    stop_words = stopwords_list()
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def lemmatizer(tokens):
    lemmatizer = Lemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    lemma_userstory = " ".join(lemmatized_tokens)
    return lemma_userstory
def userstory_nonfunctional(lemma_userstory: str) -> list: 
    arr = []
    matched = False
    pattern_type ='' 
    for p in learnability_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append({'type':p['type']})
                print('Nonfunctional user stories are extracted')
                pattern_type = learnability_pattern
                pattern_name = 'سهولت یادگیری'
                matched = True
                return arr, pattern_type, pattern_name
    if not matched:
        for p in Memorability_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append({'type':p['type']})
                print('Nonfunctional user stories are extracted')
                pattern_type = Memorability_pattern
                pattern_name = 'حفظ یادگیری'
                matched = True
                return arr, pattern_type, pattern_name
    if not matched:
        for p in error_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append({'type':p['type']})
                print('Nonfunctional user stories are extracted')
                pattern_type = error_pattern
                pattern_name = 'خطاها'
                matched = True
                return arr, pattern_type, pattern_name           
    if not matched:
        for p in efficiencyuse_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append({'type':p['type']})
                print('Nonfunctional user stories are extracted')
                pattern_type = efficiencyuse_pattern
                pattern_name = 'کارایی استفاده'
                matched = True
                return arr, pattern_type, pattern_name
    if not matched:
        for p in satisfaction_patterns:
            if re.search(p['pattern'], lemma_userstory):
                arr.append({'type':p['type']})
                print('Nonfunctional user stories are extracted')
                pattern_type = satisfaction_patterns
                pattern_name = 'رضایتمندی کاربر'
                matched = True
                return arr, pattern_type, pattern_name
            
def other_nonfunctional_requirements(pattern_type, lemma_userstory: str) -> list:
    arr = [] 
    for p in satisfaction_patterns:
        if pattern_type != satisfaction_patterns:
            if re.search(p['pattern'], lemma_userstory):
                arr.append('رضایتمندی کاربر')
    for p in learnability_pattern:
        if pattern_type != learnability_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append('سهولت یادگیری')
    for p in error_pattern:
        if pattern_type != error_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append('خطاها')      
    for p in efficiencyuse_pattern:
        if pattern_type != efficiencyuse_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append('کارایی استفاده') 
    for p in Memorability_pattern:
        if pattern_type != Memorability_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append('حفظ یادگیری')
    return arr
   

@app.post("/analyze-story", response_model=StoryResponse)
async def analyze_story(story_request: StoryRequest):
    role, capability, objective = userstory_check_first(story_request.story)
    if role and capability and objective:
        role, capability, objective = userstory_check_first(story_request.story)
        informal_normalized_story = informal_normalize(story_request.story)
        normalized_story = normalize(informal_normalized_story)
        tokenized_story = tokenize(normalized_story)
        stopword_story = stopwords(tokenized_story)
        #stopword_story = tokenized_story
        lemmatized_story = lemmatizer(stopword_story)
        nonfunctional_userstory, pattern_type, pattern_name = userstory_nonfunctional(lemmatized_story)
        other_non_functional_requirements = other_nonfunctional_requirements(pattern_type, lemmatized_story)
        
        return StoryResponse(
            validity="معتبر",
            role=role,
            capability=capability,
            goal=objective,
            normalized_story=normalized_story,
            tokenized_story=str(tokenized_story),
            lemmatized_story=lemmatized_story,
            non_functional_requirement=pattern_name,
            other_non_functional_requirements=other_non_functional_requirements,
        )
    else:
        validity = "غیر معتبر"
        role = ""
        capability = ""
        goal = ""
        return StoryResponse(
            validity="invalid",
            role="",
            capability="",
            goal="",
            normalized_story="",
            tokenized_story="",
            lemmatized_story="",
            non_functional_requirement="سرعت بارگذاری کمتر از ۲ ثانیه",
            other_non_functional_requirements="امنیت بالا و رمزنگاری داده‌ها",
        )
