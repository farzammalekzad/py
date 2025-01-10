import re
import numpy as np
import pandas as pd
from hazm import *
import timeit
import threading
import time


#df = pd.read_csv('/Users/farrr/Desktop/Desktop/project/data.csv') 
#df = pd.read_csv('/Users/farrr/Desktop/Desktop/project/sample.csv') 
df = pd.read_csv('/Users/farrr/Desktop/Desktop/project/final.csv') 


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

#end of phase 2

#start of phase 3
def userstory_nonfunctional(lemma_userstory: str) -> list:
    arr = []
    training_terms = r'(آموزش|آموزشی|دوره آموزشی|تربیت|کارگاه|آموزشگاه|آموزش‌دهی|کلاس)'
    task_terms = r'(وظایف|کارها|امور|وظیفه|فعالیت|مسئولیت|وظیفه‌محور|کاربردها)'
    learning_terms = r'(یادگیری|گیر|گرفت|فهمیدن|فهم|درک|آموختن|آموزش دیدن|فراگیری|شناخت|مسلط)'
    use_terms = r'(استفاده|بهره‌برداری|بهره‌گیری|کاربرد|به‌کارگیری|به‌کار بردن|به‌کار گرفتن)'
    feedback_terms = r'(فیدبک|بازخورد|نظر|بازخوردهای کاربران|انتقاد سازنده|پاسخ)'
    clear_terms = r'(واضح|شفاف|روشن|بی‌ابهام|ساده|سرراست|گویا|بدون پیچیدگی)'
    fast_terms = r'(سریع|سرعت|فوری|بی‌درنگ|چابک|تند|شتاب)'
    help_terms = r'(کمک|یاری|راهنمایی|حمایت|پشتیبانی|همراهی)'
    question_terms = r'(سوال|پرسش|استعلام|درخواست اطلاعات|ابهام)'
    guide_terms = r'(راهنما|راهنمایی|دستورالعمل|کتابچه راهنما|هندبوک|مستندات|راهنمای کاربر|راهبری)'
    suggestion_terms = r'(پیشنهاد|توصیه|ایده|نکته|مشاوره|نظر)'
    minimal_terms = r'(مینیمال|ساده|کمینه|مختصر|بی‌زحمت|کاربردی)'
    design_terms = r'(طراحی|ساختار|چیدمان|قالب|طرح‌بندی|نقشه)'
    setting_terms = r'(تنظیمات|پیکربندی|کنفیگ|پاراگراف‌ها|تنظیم)'
    restore_terms = r'(بازگرداندن|بازگردان|بازسازی|ترمیم|برگرداندن)'
    wrong_terms = r'(غلط|صحیح|درست|اشتباه|خطا|نادرست|بی‌دقتی)'
    prevention_terms = r'(جلوگیری|ممانعت|پیشگیری|سد کردن|بازداری|مهار)'
    change_terms = r'(تغییر|تغییرات|اصلاح|بازنگری|دگرگونی)'
    preview_terms = r'(پیش نمایش|پیش‌نمایش)'
    accuracy_terms = r'(صحت|درستی|صحیح|درست|بی‌خطا|بی‌نقص)'
    able_terms = r'(توانست|توان)'
    again_terms = r'(مجدد|بازگشت|برگردم|دوباره|از نو|تکرار)'
    continue_terms = r'(ادامه|پیشبرد|دنبال کردن|ادامه دادن|پیش‌روی)'
    previous_terms = r'(قبلی|گذشته|فعالیت‌های قبلی|پیشین|سوابق قبلی|کارهای گذشته)'
    event_terms = r'(رویدادها|سوابق|سابقه|تاریخچه|اتفاقات|حوادث|فعالیت‌ها)'
    access_terms = r'(دستیابی|دسترسی|راه‌یابی|ورود|اتصال به|باز کردن)'
    review_terms = r'(مرور|بازبینی|بررسی|ارزیابی|نگاه مجدد|مرور کردن)'
    update_terms = r'(آپدیت|ارتقا|بازسازی|بروزرسانی|به‌روزرسانی|بهبود|به‌روز)'
    reference_terms = r'(مراجع|مرجع|منابع|مآخذ|ارجاعات|اشارات|استنادها)'
    progress_terms = r'(پیشرفت|پیشروی|ترقی|رشد|بهبود|حرکت رو به جلو)'
    save_terms = r'(حفظ|بایگانی|ذخیره|سیو|نگهداری|ثبت)'
    path_terms = r'(مسیر|راه|جهت‌گیری|روش|راهکار|جهت)'
    order_terms = r'(سفارش|درخواست|رزرو)'
    ease_terms = r'(به‌سادگی|به‌راحتی|راحتی|سادگی|سریع|سرعت|به‌سرعت|ساده|بدون دردسر)'
    compensation_terms = r'(جبرانی|ناهماهنگی|آشفتگی|سرگشتگی|سردرگمی|تعادل‌بخشی|جبران خسارت)'
    restore_terms = r'(بازگرداندن|بازگردان)'
    error_terms = r'(خطا|اشتباه|غلط|نقص|ایراد|مشکل)'
    performance_terms = r'(عملکرد|کارکرد|بازدهی|پرفورمنس|کارایی|بهره‌وری)'
    skill_terms = r'(مهارت|مهارت‌ها|توانایی|قابلیت|مهارت‌آموزی|توانمندی)'
    issue_terms = r'(مشکل|اشکال|چالش|معضل|دشواری|نقص)'
    describe_terms = r'(توضیح|توضیحات|شرح|بیان|توضیح دادن|تعریف)'
    have_terms = r'(داشت|دار|دارای|برخورداری از|دریافت|به‌دست آوردن)'
    right_terms = r'(صحیح|درست|صحت|درستی|بی‌خطا|بی‌اشتباه)'
    follow_terms = r'(پیگیری|پیگیر|دنبال کردن|ردیابی)'
    presentation_terms = r'(ارایه|نمایش|پیش‌نمایش|ارائه‌دهی|معرفی)'
    ui_terms = r'(رابط کاربری|رابط گرافیکی|رابط کاربر|رابط گرافیک)'
    customize_terms = r'(سفارشی‌سازی|سفارشی|سفارشی‌کردن|شخصی‌سازی)'
    need_terms = r'(نیاز|نیازمندی|نیازها|نیازمندی‌ها|نیازهای)'
    identification_terms = r'(شناسایی|شناساندن|شناسایی کردن|شناسایی‌کردن)'


    pattern = [
        {'type': 'learning skill 00', 'pattern':fr'{training_terms}.+{learning_terms}.+{use_terms}'},
        {'type': 'learning skill 02', 'pattern':fr'{guide_terms}.+{access_terms}.+{learning_terms}.+{use_terms}'},
        {'type': 'learning skill 03', 'pattern':fr'{clear_terms}.+{ease_terms}.+{fast_terms}.+{learning_terms}'},
        {'type': 'learning skill 04', 'pattern':fr'({fast_terms}.+{learning_terms}.+{use_terms})'},
        {'type': 'learning skill 05', 'pattern':fr'({issue_terms}.+{question_terms}.+{help_terms}.+{ease_terms})'},
        {'type': 'learning skill 06', 'pattern':fr'({describe_terms}.+{task_terms}.+{learning_terms})'},
        {'type': 'learning skill 07', 'pattern':fr'({training_terms}.+{ease_terms}.+{learning_terms})'},
        {'type': 'learning skill 08', 'pattern':fr'({feedback_terms}.+{learning_terms})'},
        {'type': 'learning skill 09', 'pattern':fr'({performance_terms}.+{learning_terms}.+{use_terms})'},
        {'type': 'learning skill 11', 'pattern':fr'({learning_terms}.+{use_terms}.+{fast_terms})'},
        {'type': 'learning skill 12', 'pattern':fr'({question_terms}.+{have_terms}.+{ease_terms}.+{learning_terms})'},
        {'type': 'learning skill 13', 'pattern':fr'({guide_terms}.+{ease_terms}.+{performance_terms}.+{fast_terms})'},
        {'type': 'learning skill 14', 'pattern':fr'({learning_terms}.+{ease_terms}.+{use_terms})'},
        {'type': 'learning skill 15', 'pattern':fr'({minimal_terms}.+{design_terms}.+{ease_terms})'},
        {'type': 'learning skill 16', 'pattern':fr'({setting_terms}.+{restore_terms}.+{wrong_terms}.+({prevention_terms}|{use_terms}))'},
        {'type': 'learning skill 17', 'pattern':fr'({ease_terms}.+({learning_terms}|آشنا).+{use_terms})'},
        {'type': 'learning skill 18', 'pattern':fr'({task_terms}.+{suggestion_terms}.+{ease_terms}.+{learning_terms})'},
        {'type': 'learning skill 19', 'pattern':fr'({guide_terms}.+{ease_terms}.+{learning_terms})'},
        {'type': 'leafning skill 20', 'pattern':fr'({ease_terms}.+{order_terms}.+{setting_terms}.+{ease_terms})'},
        {'type': 'learning skill 21', 'pattern':fr'({change_terms}.+{preview_terms}.+{right_terms}.+{ease_terms})'},
        {'type': 'learning skill 22', 'pattern':fr'({save_terms}.+(توانست|توان).+{again_terms}.+{continue_terms})'},#error
        {'type': 'learning skill 23', 'pattern':fr'({guide_terms}.+{ease_terms}.+{use_terms}.+{compensation_terms})'},
        {'type': 'learning skill 24', 'pattern':fr'({training_terms}.+{learning_terms}.+{progress_terms})'},
        {'type': 'learning skill 25', 'pattern':fr'({guide_terms}.+{save_terms}.+{previous_terms}.+{review_terms})'},
        {'type': 'learning skill 26', 'pattern':fr'({training_terms}.+{path_terms}.+{ease_terms}.+{continue_terms})'},
        {'type': 'learning skill 27', 'pattern':fr'({previous_terms}.+{event_terms}.+{access_terms}.+({review_terms}|{follow_terms}))'},
        {'type': 'learning skill 28', 'pattern':fr'({update_terms}.+({describe_terms}|{guide_terms}).+{ease_terms}.+{learning_terms}.+{use_terms})'},
        {'type': 'learning skill 29', 'pattern':fr'({training_terms}.+{reference_terms}.+{ease_terms}?.+{learning_terms})'},
        {'type': 'learning skill 30', 'pattern':fr'({learning_terms}.+{save_terms}.+{progress_terms}.+{ease_terms}.+{again_terms})'},
        {'type': 'learning skill 31', 'pattern':fr'({reference_terms}?.+{training_terms}.+{access_terms}.+({guide_terms}|{describe_terms}).+{ease_terms})'},
        {'type': 'learning skill 32', 'pattern':fr'(({learning_terms}|{training_terms}).+{presentation_terms}.+{learning_terms}.+{use_terms})'},
        {'type': 'learning skill 33', 'pattern':fr'({training_terms}.+{reference_terms}.+{learning_terms})'},
        {'type': 'learning skill 34', 'pattern':fr'({guide_terms}.+{task_terms}.+{able_terms}.+{learning_terms})'},
        {'type': 'learning skill 35', 'pattern':fr'({guide_terms}.+{learning_terms}.+{task_terms})'},
        {'type': 'learning skill 36', 'pattern':fr'({ui_terms}.+{clear_terms}.+{ease_terms}.+{training_terms}.+{learning_terms})'},
        {'type': 'learning skill 37', 'pattern':fr'({customize_terms}.+{setting_terms}.+{ease_terms}.+({task_terms}|{access_terms}))'},
        {'type': 'learning skill 38', 'pattern':fr'({update_terms}.+({learning_terms}|{training_terms}).+{update_terms}.+{change_terms}.+{learning_terms})'},
        {'type': 'learning skill 39', 'pattern':fr'({training_terms}.+{identification_terms}.+({guide_terms}|{describe_terms}).+{ease_terms}.+{use_terms})'},

    ]
    for p in pattern:
        if re.search(p['pattern'], lemma_userstory):
            arr.append({'type':p['type']})
            print('Nonfunctional user stories are extracted')
    return arr

def userstory_nonfunctional_identification(df: pd.DataFrame):
    output_file = "/Users/farrr/Desktop/Desktop/project/nonfunctional_userstory.csv"
    df.loc[:,'nonfunctional_userstory'] = df['string_lemmatized_userstory'].apply(userstory_nonfunctional)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print('All Nonfunctional user stories are extracted')

def test():
    userstory_nonfunctional_identification(df)
    print('phase 3 is done')
#end of phase 3



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
    execution_time = timeit.timeit(test, number=1) 
    print(f"execution time is {execution_time:.5f} seconds")
except KeyboardInterrupt:
    print('Code is terminated by user')
    exit()
finally:
    print('see the result in final.csv')
    exit()


    






#filtered = userstory_check(df)
#userstory_check(df)
#missing(df)
#delete_missing(df)
#droping_white_space(df)
#fix_persian_halfspace(df)
#normalizer(df)
#informal_normalize(userstory)
