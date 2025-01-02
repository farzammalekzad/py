import re
import numpy as np
import pandas as pd
from hazm import *
import timeit
import threading
import time


#df = pd.read_csv('/Users/farrr/Desktop/Desktop/project/data.csv') 
df = pd.read_csv('/Users/farrr/Desktop/Desktop/project/sample.csv') 
    
def show_status():
    while True:
        print("Status: Code is Running ...")
        time.sleep(5)

status_thread = threading.Thread(target=show_status, daemon=True)
status_thread.start()

def missing(df:pd.DataFrame) -> pd.DataFrame:
    print('Shape of DataFrame:', df.shape)
    missing_values = df.isnull().sum()
    indeices = df[df.isna().any(axis=1)].index.to_list()
    print(f"report of missing values: \n{missing_values}")
    print(f"Indices of rows with missing values: {indeices}")
    return df

def droping_white_space(df:pd.DataFrame) -> pd.DataFrame:
    blanks = []
    print(df)
    for no, row in df.iterrows():
        for col in df.columns:
            value = row[col]
            if isinstance(value, str) and value.isspace():
                blanks.append(no)
    print(f"Number of blanks: {len(blanks)}")
    print("Blank rows:", blanks)
    df = df.drop(index=blanks).reset_index(drop=True)
    return df

def delete_missing(df:pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    print('Shape after dropping missing values:', df.shape)

# start of phase 1
def userstory_check_first(userstory):
    #pattern_old = r"^به عنوان یک\s+(.+?)،?\s+من می‌خواهم\s+(.+?)\s+تا بتوانم\s+(.+?)\.$"
    #pattern_old2 = r"^به عنوان یک\s+(.+?)،?\s+من می‌خواهم\s+(.+?)\s+تا بتوانم\s+(.+)$"
    pattern = r"^به عنوان\s+(?:یک\s+)?(.+?)،?\s+من می‌خواهم\s+(.+?)\s+تا بتوانم\s+(.+?)$"


    match = re.match(pattern,userstory)
    if match:
        role = match.group(1).strip()
        capability = match.group(2).strip()
        objective = match.group(3).strip()
        #print("Role:", match.group(1).strip())
        #print("Capability:", match.group(2).strip())
        #print("Objective:", match.group(3).strip())
        return role, capability, objective
    else:
        #print("Invalid User Story")
        return None, None, None

def userstory_check_second(row):
    role, capability, objective = userstory_check_first(row['userstory'])
    return pd.Series({'role': role, 'capability': capability, 'objective': objective})

def userstory_check_final(df: pd.DataFrame) -> pd.DataFrame:
    print("shape of dataframe is: ",df.shape[0])
    #output_file = "/Users/farrr/Desktop/Desktop/project/userstoryanalysis.csv"
    df[['role', 'capability', 'objective']] = df.apply(userstory_check_second, axis=1)
    df_cleaned = df.dropna()
    #df_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("shape of dataframe after deleting invalid user story is: ",df_cleaned.shape[0])
    #print('all user stories are reviewed and valid userstories saved in userstoryanalysis.csv')
    return df_cleaned

def phase_one(df:pd.DataFrame) -> pd.DataFrame:
    #output_file = "/Users/farrr/Desktop/Desktop/project/phase_one.csv"
    df_cleaned = userstory_check_final(df)
    #df_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig')
    print('phase one is done')
    return df_cleaned

# end of phase 1

# start of phase 2
def phase_two(df:pd.DataFrame)->pd.DataFrame:
    #output_file = "/Users/farrr/Desktop/Desktop/project/phase_two.csv"
    corrected_informal_df = informal_normalize_dataframe(df)
    normalized_dataframe = normalize_dataframe(corrected_informal_df)
    tokenized_df = tokenize_dataframe(normalized_dataframe)
    stopwords_df = stopwords_dataframe(tokenized_df)
    lemma_df = lemmatizer_dataframe(stopwords_df)
    #lemma_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    return lemma_df



#end of phase 2

""" این تابع با توجه به اینکه بخش‌های مختلف داستان کاربری را جدا نمی‌کند فعلا در دستور کار نمی‌باشد
def userstory_check(df: pd.DataFrame) -> pd.DataFrame:
    output_file = "/Users/farrr/Desktop/Desktop/project/userstorycheck.csv"
    pattern = r"^به عنوان(.+)می‌خواهم(.+)بتوانم(.+)"
    pattern2 = r"^به عنوان\s+(.+?)،?\s+می‌خواهم\s+(.+?)\s+تا بتوانم\s+(.+?)\.$"
    df_filtered = df[df['userstory'].str.contains(pattern2, regex=True, na=False)]
    df_filtered.to_csv(output_file, index=False, encoding='utf-8-sig')
    return df_filtered """


""" این تابع تنها برای تست فاز ۱ نوشته شده بود
def check_function_userstory(userstories: list):
    # pattern = r"^\bبه عنوان\b(.+)\bمن می‌خواهم\b(.+)\bتا بتوانم\b(.+)"
    pattern = r"^به عنوان(.+)من می‌خواهم(.+)تا بتوانم(.+)"
    arr = []
    invalid_userstories = []
    correct_userstories = []
    count: int = 0
    t_count:int = 0
    f_count:int = 0
    for userstory in userstories:
        count += 1
        result = re.search(pattern,userstory)
        if result:
            t_count = t_count + 1
            correct_userstories.append(userstory)
        else:            
            f_count = f_count + 1
            arr.append(count)
            invalid_userstories.append([userstory,count])
    print("Status of UserStory : Number of Correct UserStory: ",t_count )
    print(f"Status of UserStory : Number of inCorrect UserStory: ",f_count, f"\nnumber of invalid userstories is: {arr}" )
    if invalid_userstories:
        print("\nInvalid User Stories:")
        for story in invalid_userstories:
            print("-", story)
    return correct_userstories """
    
def fix_persian_halfspace(df:pd.DataFrame) -> pd.DataFrame:
    half_space = '\u200c'
    df.loc[:,'userstory_halfspace'] = df['userstory'].str.replace(half_space,' ')
    #print(df)
    return df
    
""" def normalizer(df: pd.DataFrame) -> pd.DataFrame: #commented in order to use other functions
    normalizer = hazm.Normalizer()
    df['normalized_userstory'] = df['userstory'].apply(normalizer.normalize)
    output_file = "/Users/farrr/Desktop/Desktop/project/normalized_data.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    return df """

def tokenize(userstory):
     tokens = word_tokenize(userstory)
     return tokens

def tokenize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    #output_file = "/Users/farrr/Desktop/Desktop/project/tokenized_data.csv"
    df.loc[:,'tokenized_userstory'] = df['normalized_dataframe'].apply(tokenize)
    #df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print('Tokenization is done')
    return df

def informal_normalize(userstory):
    normalizer = InformalNormalizer()
    informal_normalized_text = normalizer.normalize(userstory)
    small_array = informal_normalized_text[0]
    first_elements = [inner[0] for inner in small_array if len(inner) > 0]
    normalized_text = ' '.join(first_elements)
    return normalized_text




def informal_normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    #output_file = "/Users/farrr/Desktop/Desktop/project/informal_normalized_data.csv"
    df.loc[:,'informal_normalized_userstory'] = df['userstory'].apply(informal_normalize)
    #df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print('Informal Normalization is done')
    return df

def normalize(userstory: str):
    normalizer = Normalizer()
    normalized_text = normalizer.normalize(userstory)
    return normalized_text

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    #output_file = "/Users/farrr/Desktop/Desktop/project/tokenized_data.csv"
    df.loc[:,'normalized_dataframe'] = df['informal_normalized_userstory'].apply(normalize)
    #df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print('Normalization is done')
    return df

def stopwords(tokens):
    stop_words = stopwords_list()
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def stopwords_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    #output_file = "/Users/farrr/Desktop/Desktop/project/stopwords_data.csv"
    df.loc[:,'stopwords_userstory'] = df['tokenized_userstory'].apply(stopwords)
    #df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print('Stopwords are removed')
    return df

def lemmatizer(tokens):
    lemmatizer = Lemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

def lemmatizer_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    #output_file = "/Users/farrr/Desktop/Desktop/project/lemmatized_data.csv"
    df.loc[:,'lemmatized_userstory'] = df['stopwords_userstory'].apply(lemmatizer)
    df.loc[:,'string_lemmatized_userstory'] = df['lemmatized_userstory'].apply(lambda x: ' '.join(x))
    #df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print('Lemmatization is done')
    return df


def main():
    output_file = "/Users/farrr/Desktop/Desktop/project/final.csv"
    phase_one_df = phase_one(df)
    phase_two_df = phase_two(phase_one_df)
    phase_two_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print ('all phases are done')

    #userstory_check_final(df)
    #df_half = fix_persian_halfspace(df)
    #filtered_df=userstory_check(df)
    #missing(filtered_df)
    #delete_missing(filtered_df)
    #droping_white_space(filtered_df)
    #normalize_dataframe(filtered_df)
    #tokenized_df = tokenize_dataframe(df)
    #stopwords_df = stopwords_dataframe(tokenized_df)
    #lemmatizer_dataframe(stopwords_df)
    
    



#main()
try:
    execution_time = timeit.timeit(main, number=1) 
    print(f"execution time is : {execution_time:.5f} seconds")
except KeyboardInterrupt:
    print('Code is terminated by user')
    exit()
finally:
    print('Finish the code see the result in final.csv')
    exit()


    






#filtered = userstory_check(df)
#userstory_check(df)
#missing(df)
#delete_missing(df)
#droping_white_space(df)
#fix_persian_halfspace(df)
#normalizer(df)
#informal_normalize(userstory)
