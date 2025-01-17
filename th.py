import re
import numpy as np
import pandas as pd
from hazm import *
import timeit
import threading
import time
from enum import Enum

class regex(Enum):
    want_terms = r'(خواست#خواه)'
    able_terms = r'(توانست#توان)'
    training_terms = r'(آموزش|آموزشی|دوره آموزشی|تربیت|کارگاه|آموزشگاه|آموزش‌دهی|کلاس)'
    task_terms = r'(وظایف|کارها|امور|وظیفه|فعالیت|مسئولیت|وظیفه‌محور|کاربردها|عملیات|عملیات‌ها)'
    learning_terms = r'(یادگیری|فهمیدن|فهم|درک|آموختن|آموزش دیدن|فراگیری|شناخت|مسلط|آگاه)'
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
    order_terms = r'(سفارش|درخواست|رزرو|سفار)'
    ease_terms = r'(به‌سادگی|به‌راحتی|راحتی|سادگی|سریع|سرعت|به‌سرعت|ساده|بدون دردسر)'
    compensation_terms = r'(جبرانی|ناهماهنگی|آشفتگی|سرگشتگی|سردرگمی|تعادل‌بخشی|جبران خسارت)'
    #restore_terms = r'(بازگرداندن|بازگردان)'
    error_terms = r'(خطا|اشتباه|غلط|نقص|ایراد|مشکل)'
    performance_terms = r'(عملکرد|کارکرد|بازدهی|پرفورمنس|کارایی|بهره‌وری)'
    skill_terms = r'(مهارت|مهارت‌ها|توانایی|قابلیت|مهارت‌آموزی|توانمندی)'
    issue_terms = r'(مشکل|اشکال|چالش|معضل|دشواری|نقص|دردسر)'
    describe_terms = r'(توضیح|توضیحات|شرح|بیان|توضیح دادن|تعریف)'
    have_terms = r'(داشت|دار|دارای|برخورداری از|دریافت|به‌دست آوردن)'
    right_terms = r'(صحیح|درست|صحت|درستی|بی‌خطا|بی‌اشتباه)'
    follow_terms = r'(پیگیری|پیگیر|دنبال کردن|ردیابی)'
    presentation_terms = r'(ارایه|نمایش|پیش‌نمایش|ارائه‌دهی|معرفی)'
    ui_terms = r'(رابط کاربری|رابط گرافیکی|رابط کاربر|رابط گرافیک)'
    customize_terms = r'(سفارشی‌سازی|سفارشی|سفارشی‌کردن|شخصی‌سازی)'
    need_terms = r'(نیاز|نیازمندی|نیازها|نیازمندی‌ها|نیازهای)'
    identification_terms = r'(شناسایی|شناساندن|شناسایی کردن|شناسایی‌کردن)'
    product_terms = r'(محصول|محصولات|محصولات نرم‌افزاری|محصول نرم‌افزاری|کالا|کالاها)'
    buy_terms = r'(خرید|خریداری|خرید کردن|خریداری کردن)'
    time_terms = r'(زمان|زمان‌بندی|زمان‌برنامه‌ریزی|زمان‌بندی‌کردن|وقت)'
    long_terms = r'(طولانی|طولانی‌مدت|طولانی‌مدتی|بلند|بلندمدت|بلند‌مدت)'
    search_terms = r'(جستجو|جستجوی|جستجو کردن|جستجوی کردن)'
    Feature_terms = r'(ویژگی|ویژگی‌ها|ویژگی‌های|ویژگی‌های نرم‌افزار|ویژگی نرم‌افزار)'
    address_terms = r'(آدرس|آدرس‌ها|آدرس‌های|آدرس‌های اینترنتی|آدرس اینترنتی)'
    receive_terms = r'(دریافت|دریافت کردن|دریافت نمودن|دریافت‌کردن)'
    delivery_terms = r'(تحویل|تحویل دادن|تحویل نمودن|تحویل‌دادن)'
    add_terms= r'(اضافه|اضافه کردن|افزودن|افزودن به|اضافه نمودن)'
    grading_terms= r'(رتبه|رتبه‌بندی|اولویت|اولویت‌بندی|مرتب|مرتب کردن)'
    status_terms= r'(وضعیت|وضعیت‌ها|وضعیت‌های|وضعیت‌های نرم‌افزار|وضعیت نرم‌افزار)'
    future_terms= r'(آینده|آینده‌نگری|آینده‌نگری کردن|آینده‌نگری‌کردن)'
    subscription_terms= r'(اشتراک|اشتراک‌ گذارد|اشتراک‌گذاری|اشتراک‌گذاری‌کردن)'
    discount_terms= r'(تخفیف|تخفیفات|تخفیف‌ها|تخفیف‌های|تخفیف‌های ویژه)'
    language_terms= r'(زبان|زبان‌ها|زبان‌های|زبان‌های برنامه‌نویسی|زبان برنامه‌نویسی)'
    site_terms= r'(سایت|سایت‌ها|سایت‌های|سایت‌های اینترنتی|سایت اینترنتی)'
    content_terms= r'(محتوا|محتوای|محتوای سایت|محتوای وب|محتوای وب‌سایت|مفهوم)'
    study_terms= r'(مطالعه|مطالعه کردن|مطالعه‌کردن|خواندن|خواندن مطالب|خواندن مطالب)'
    account_terms= r'(حساب|حساب‌ها|حساب‌های|حساب‌های کاربری|حساب کاربری| حساب‌های اجتماعی| حساب اجتماعی)'
    code_terms= r'(کد|کد تخفیف|کد تخفیفی|کد تخفیف‌ها|کد تخفیف‌های|کد تخفیف‌های ویژه)'
    observe_terms= r'(مشاهده|مشاهده کردن|مشاهده‌کردن|نگاه کردن|نگاه‌کردن)'
    detail_terms= r'(جزئیات|جزئیات بیشتر|جزئیات بیشتری|جزئیات بیشتری|جزئیات بیشتری)'
    decision_terms= r'(تصمیم|تصمیم‌گیری|تصمیم‌گیری کردن|تصمیم‌گیری‌کردن|انتخاب)'
    experience_terms= r'(تجربه|تجربه‌ها|تجربه‌های|تجربه‌های کاربری|تجربه کاربری|تجربیات)'
    filter_terms= r'(فیلتر|فیلتر کردن|فیلتر‌کردن|پالایش|پالایش کردن|پالایش‌کردن)'
    size_terms= r'(اندازه|اندازه‌ها|اندازه‌های|اندازه‌های مختلف|اندازه مختلف|سایز)'
    read_terms= r'(خواندن|خواندن مطالب|خواندن مطالب|مطالعه|مطالعه کردن)'
    notification_terms= r'(اطلاعیه|اطلاعیه‌ها|اطلاعیه‌های|اطلاعیه‌های جدید|اطلاعیه جدید|اعلان|اعلان‌ها|اعلان‌های|اعلان‌های جدید|اعلان جدید|هشدار)'
    based_terms = r'(پایه|اساس|مبنا|بنیاد|بنیادی|اساسی|مبنایی)'
    inventory_terms = r'(انبار|انبارها|انبارهای|انبارهای موجود|انبار موجود|موجودی)'
    shopping_cart_terms = r'(سبد خرید|سبد خریدها|سبد خریدهای|سبد خریدهای موجود|سبد خرید موجود|سبد خریدهای موجود)'
    invoice_terms = r'(فاکتور|فاکتورها|فاکتورهای|فاکتورهای موجود|فاکتور موجود|فاکتورهای موجود)'
    submit_terms = r'(ارسال|ارسال کردن|ارسال‌کردن|ارسال نمودن|ارسال‌نمودن)'
    legal_terms = r'(قانونی|قوانین|حقوقی|مقررات)'
    favourite_terms = r'(مورد علاقه|مورد علاقه‌ها|مورد علاقه‌های|مورد علاقه‌های کاربری|مورد علاقه کاربری|مورد علاقه‌های کاربری|علاقه‌مندی|علاقه مندی)'
    result_terms= r'(نتیجه|نتایج|نتیجه‌ها|نتایج|نتیجه‌های|نتایج|نتیجه‌های موجود|نتایج موجود)'
    confident_terms= r'(اطمینان)'
    find_terms = r'(یافتن|یافتن محصول|یافتن محصولات|یافتن محصولات|پیدا کردن|پیداکردن)'
    simple_terms= r'(ساده|ساده‌تر|ساده‌ترین|بسیار ساده|بسیار ساده‌تر|بسیار ساده‌ترین)'
    terminate_terms= r'(پایان|پایان دادن|لغو|لغو کردن|پایان دادن به|پایان دادن به|)'
    Simultaneously_terms= r'(همزمان)'
    automated_terms= r'(خودکار|خودکارسازی|خودکارسازی شده|خودکارسازی‌شده)'
    satisfaction_terms= r'(رضایت|رضایت‌بخشی|رضایت‌بخش|رضایت‌بخشی|رضایت‌بخش)'
    notuseability_terms= r'(سرعت بارگذاری|زمان پاسخ‌دهی|عملکرد بهینه|منابع سیستم|داده امن|حریم خصوصی|رمزنگاری|محرمانگی|پایداری سیستم|اطلاعات دست رفت|عملکرد پایدار|بازیابی خطا|کاربر نیاز|صفحه‌خوان|چندزبانگی)'



#df = pd.read_csv('/Users/farrr/Desktop/Desktop/project/data.csv') 
#df = pd.read_csv('/Users/farrr/Desktop/Desktop/project/sample2.csv') 
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
    want_terms = r'(خواست#خواه)'
    able_terms = r'(توانست#توان)'
    training_terms = r'(آموزش|آموزشی|دوره آموزشی|تربیت|کارگاه|آموزشگاه|آموزش‌دهی|کلاس)'
    task_terms = r'(وظایف|کارها|امور|وظیفه|فعالیت|مسئولیت|وظیفه‌محور|کاربردها|عملیات|عملیات‌ها)'
    learning_terms = r'(یادگیری|گیر|گرفت|فهمیدن|فهم|درک|آموختن|آموزش دیدن|فراگیری|شناخت|مسلط|آگاه)'
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
    order_terms = r'(سفارش|درخواست|رزرو|سفار)'
    ease_terms = r'(به‌سادگی|به‌راحتی|راحتی|سادگی|سریع|سرعت|به‌سرعت|ساده|بدون دردسر)'
    compensation_terms = r'(جبرانی|ناهماهنگی|آشفتگی|سرگشتگی|سردرگمی|تعادل‌بخشی|جبران خسارت)'
    restore_terms = r'(بازگرداندن|بازگردان)'
    error_terms = r'(خطا|اشتباه|غلط|نقص|ایراد|مشکل)'
    performance_terms = r'(عملکرد|کارکرد|بازدهی|پرفورمنس|کارایی|بهره‌وری)'
    skill_terms = r'(مهارت|مهارت‌ها|توانایی|قابلیت|مهارت‌آموزی|توانمندی)'
    issue_terms = r'(مشکل|اشکال|چالش|معضل|دشواری|نقص|دردسر)'
    describe_terms = r'(توضیح|توضیحات|شرح|بیان|توضیح دادن|تعریف)'
    have_terms = r'(داشت|دار|دارای|برخورداری از|دریافت|به‌دست آوردن)'
    right_terms = r'(صحیح|درست|صحت|درستی|بی‌خطا|بی‌اشتباه)'
    follow_terms = r'(پیگیری|پیگیر|دنبال کردن|ردیابی)'
    presentation_terms = r'(ارایه|نمایش|پیش‌نمایش|ارائه‌دهی|معرفی)'
    ui_terms = r'(رابط کاربری|رابط گرافیکی|رابط کاربر|رابط گرافیک)'
    customize_terms = r'(سفارشی‌سازی|سفارشی|سفارشی‌کردن|شخصی‌سازی)'
    need_terms = r'(نیاز|نیازمندی|نیازها|نیازمندی‌ها|نیازهای)'
    identification_terms = r'(شناسایی|شناساندن|شناسایی کردن|شناسایی‌کردن)'
    product_terms = r'(محصول|محصولات|محصولات نرم‌افزاری|محصول نرم‌افزاری|کالا|کالاها)'
    buy_terms = r'(خرید|خریداری|خرید کردن|خریداری کردن)'
    time_terms = r'(زمان|زمان‌بندی|زمان‌برنامه‌ریزی|زمان‌بندی‌کردن|وقت)'
    long_terms = r'(طولانی|طولانی‌مدت|طولانی‌مدتی|بلند|بلندمدت|بلند‌مدت)'
    search_terms = r'(جستجو|جستجوی|جستجو کردن|جستجوی کردن)'
    Feature_terms = r'(ویژگی|ویژگی‌ها|ویژگی‌های|ویژگی‌های نرم‌افزار|ویژگی نرم‌افزار)'
    address_terms = r'(آدرس|آدرس‌ها|آدرس‌های|آدرس‌های اینترنتی|آدرس اینترنتی)'
    receive_terms = r'(دریافت|دریافت کردن|دریافت نمودن|دریافت‌کردن)'
    delivery_terms = r'(تحویل|تحویل دادن|تحویل نمودن|تحویل‌دادن)'
    add_terms= r'(اضافه|اضافه کردن|افزودن|افزودن به|اضافه نمودن)'
    grading_terms= r'(رتبه|رتبه‌بندی|اولویت|اولویت‌بندی|مرتب|مرتب کردن)'
    status_terms= r'(وضعیت|وضعیت‌ها|وضعیت‌های|وضعیت‌های نرم‌افزار|وضعیت نرم‌افزار)'
    future_terms= r'(آینده|آینده‌نگری|آینده‌نگری کردن|آینده‌نگری‌کردن)'
    subscription_terms= r'(اشتراک|اشتراک‌ گذارد|اشتراک‌گذاری|اشتراک‌گذاری‌کردن)'
    discount_terms= r'(تخفیف|تخفیفات|تخفیف‌ها|تخفیف‌های|تخفیف‌های ویژه)'
    language_terms= r'(زبان|زبان‌ها|زبان‌های|زبان‌های برنامه‌نویسی|زبان برنامه‌نویسی)'
    site_terms= r'(سایت|سایت‌ها|سایت‌های|سایت‌های اینترنتی|سایت اینترنتی)'
    content_terms= r'(محتوا|محتوای|محتوای سایت|محتوای وب|محتوای وب‌سایت|مفهوم)'
    study_terms= r'(مطالعه|مطالعه کردن|مطالعه‌کردن|خواندن|خواندن مطالب|خواندن مطالب)'
    account_terms= r'(حساب|حساب‌ها|حساب‌های|حساب‌های کاربری|حساب کاربری| حساب‌های اجتماعی| حساب اجتماعی)'
    code_terms= r'(کد|کد تخفیف|کد تخفیفی|کد تخفیف‌ها|کد تخفیف‌های|کد تخفیف‌های ویژه)'
    observe_terms= r'(مشاهده|مشاهده کردن|مشاهده‌کردن|نگاه کردن|نگاه‌کردن)'
    detail_terms= r'(جزئیات|جزئیات بیشتر|جزئیات بیشتری|جزئیات بیشتری|جزئیات بیشتری)'
    decision_terms= r'(تصمیم|تصمیم‌گیری|تصمیم‌گیری کردن|تصمیم‌گیری‌کردن|انتخاب)'
    experience_terms= r'(تجربه|تجربه‌ها|تجربه‌های|تجربه‌های کاربری|تجربه کاربری|تجربیات)'
    filter_terms= r'(فیلتر|فیلتر کردن|فیلتر‌کردن|پالایش|پالایش کردن|پالایش‌کردن)'
    size_terms= r'(اندازه|اندازه‌ها|اندازه‌های|اندازه‌های مختلف|اندازه مختلف|سایز)'
    read_terms= r'(خواندن|خواندن مطالب|خواندن مطالب|مطالعه|مطالعه کردن)'
    notification_terms= r'(اطلاعیه|اطلاعیه‌ها|اطلاعیه‌های|اطلاعیه‌های جدید|اطلاعیه جدید|اعلان|اعلان‌ها|اعلان‌های|اعلان‌های جدید|اعلان جدید|هشدار)'
    based_terms = r'(پایه|اساس|مبنا|بنیاد|بنیادی|اساسی|مبنایی)'
    inventory_terms = r'(انبار|انبارها|انبارهای|انبارهای موجود|انبار موجود|موجودی)'
    shopping_cart_terms = r'(سبد خرید|سبد خریدها|سبد خریدهای|سبد خریدهای موجود|سبد خرید موجود|سبد خریدهای موجود)'
    invoice_terms = r'(فاکتور|فاکتورها|فاکتورهای|فاکتورهای موجود|فاکتور موجود|فاکتورهای موجود)'
    submit_terms = r'(ارسال|ارسال کردن|ارسال‌کردن|ارسال نمودن|ارسال‌نمودن)'
    legal_terms = r'(قانونی|قوانین|حقوقی|مقررات)'
    favourite_terms = r'(مورد علاقه|مورد علاقه‌ها|مورد علاقه‌های|مورد علاقه‌های کاربری|مورد علاقه کاربری|مورد علاقه‌های کاربری|علاقه‌مندی|علاقه مندی)'
    result_terms= r'(نتیجه|نتایج|نتیجه‌ها|نتایج|نتیجه‌های|نتایج|نتیجه‌های موجود|نتایج موجود)'
    confident_terms= r'(اطمینان)'
    find_terms = r'(یافتن|یافتن محصول|یافتن محصولات|یافتن محصولات|پیدا کردن|پیداکردن)'
    simple_terms= r'(ساده|ساده‌تر|ساده‌ترین|بسیار ساده|بسیار ساده‌تر|بسیار ساده‌ترین)'
    terminate_terms= r'(پایان|پایان دادن|لغو|لغو کردن|پایان دادن به|پایان دادن به|)'
    Simultaneously_terms= r'(همزمان)'
    automated_terms= r'(خودکار|خودکارسازی|خودکارسازی شده|خودکارسازی‌شده)'
    satisfaction_terms= r'(رضایت|رضایت‌بخشی|رضایت‌بخش|رضایت‌بخشی|رضایت‌بخش)'
    notuseability_terms= r'(سرعت بارگذاری|زمان پاسخ‌دهی|عملکرد بهینه|منابع سیستم|داده امن|حریم خصوصی|رمزنگاری|محرمانگی|پایداری سیستم|اطلاعات دست رفت|عملکرد پایدار|بازیابی خطا|کاربر نیاز|صفحه‌خوان|چندزبانگی)'




    pattern = [
         {'type': 'learning skill 00', 'pattern':fr'{training_terms}.+{learning_terms}.+{use_terms}'},
         {'type': 'learning skill 02', 'pattern':fr'{guide_terms}.+{access_terms}.+{learning_terms}.+{use_terms}'},
         {'type': 'learning skill 03', 'pattern':fr'{clear_terms}.+{regex.ease_terms}.+{fast_terms}.+{learning_terms}'},
         {'type': 'learning skill 04', 'pattern':fr'({fast_terms}.+{learning_terms}.+{use_terms})'},
         {'type': 'learning skill 05', 'pattern':fr'({issue_terms}.+{question_terms}.+{help_terms}.+{regex.ease_terms})'},
         {'type': 'learning skill 06', 'pattern':fr'({describe_terms}.+{task_terms}.+{learning_terms})'},
         {'type': 'learning skill 07', 'pattern':fr'({training_terms}.+{regex.ease_terms}.+{learning_terms})'},
         {'type': 'learning skill 08', 'pattern':fr'({feedback_terms}.+{learning_terms})'},
         {'type': 'learning skill 09', 'pattern':fr'({performance_terms}.+{learning_terms}.+{use_terms})'},
         {'type': 'learning skill 11', 'pattern':fr'({learning_terms}.+{use_terms}.+{fast_terms})'},
         {'type': 'learning skill 12', 'pattern':fr'({question_terms}.+{have_terms}.+{regex.ease_terms}.+{learning_terms})'},
         {'type': 'learning skill 13', 'pattern':fr'({guide_terms}.+{regex.ease_terms}.+{performance_terms}.+{fast_terms})'},
         {'type': 'learning skill 14', 'pattern':fr'({learning_terms}.+{regex.ease_terms}.+{use_terms})'},
         {'type': 'learning skill 15', 'pattern':fr'({minimal_terms}.+{design_terms}.+{regex.ease_terms})'},
         {'type': 'learning skill 16', 'pattern':fr'({setting_terms}.+{restore_terms}.+{wrong_terms}.+({prevention_terms}|{use_terms}))'},
         {'type': 'learning skill 17', 'pattern':fr'({regex.ease_terms}.+({learning_terms}|آشنا).+{use_terms})'},
         {'type': 'learning skill 18', 'pattern':fr'({task_terms}.+{suggestion_terms}.+{regex.ease_terms}.+{learning_terms})'},
         {'type': 'learning skill 19', 'pattern':fr'({guide_terms}.+{regex.ease_terms}.+{learning_terms})'},
         {'type': 'leafning skill 20', 'pattern':fr'({regex.ease_terms}.+{order_terms}.+{setting_terms}.+{regex.ease_terms})'},
         {'type': 'learning skill 21', 'pattern':fr'({change_terms}.+{preview_terms}.+{right_terms}.+{regex.ease_terms})'},
         {'type': 'learning skill 22', 'pattern':fr'({save_terms}.+{able_terms}.+{again_terms}.+{continue_terms})'},
         {'type': 'learning skill 23', 'pattern':fr'({guide_terms}.+{regex.ease_terms.value}.+{use_terms}.+{compensation_terms})'},
         {'type': 'learning skill 24', 'pattern':fr'({training_terms}.+{learning_terms}.+{progress_terms})'},
         {'type': 'learning skill 25', 'pattern':fr'({guide_terms}.+{save_terms}.+{previous_terms}.+{review_terms})'},
         {'type': 'learning skill 26', 'pattern':fr'({training_terms}.+{path_terms}.+{regex.ease_terms}.+{continue_terms})'},
         {'type': 'learning skill 27', 'pattern':fr'({previous_terms}.+{event_terms}.+{access_terms}.+({review_terms}|{follow_terms}))'},
         {'type': 'learning skill 28', 'pattern':fr'({update_terms}.+({describe_terms}|{guide_terms}).+{regex.ease_terms}.+{learning_terms}.+{use_terms})'},
         {'type': 'learning skill 29', 'pattern':fr'({training_terms}.+{reference_terms}.+{regex.ease_terms}?.+{learning_terms})'},
         {'type': 'learning skill 30', 'pattern':fr'({learning_terms}.+{save_terms}.+{progress_terms}.+{regex.ease_terms}.+{again_terms})'},
         {'type': 'learning skill 31', 'pattern':fr'({reference_terms}?.+{training_terms}.+{access_terms}.+({guide_terms}|{describe_terms}).+{regex.ease_terms})'},
         {'type': 'learning skill 32', 'pattern':fr'(({learning_terms}|{training_terms}).+{presentation_terms}.+{learning_terms}.+{use_terms})'},
         {'type': 'learning skill 33', 'pattern':fr'({training_terms}.+{reference_terms}.+{learning_terms})'},
         {'type': 'learning skill 34', 'pattern':fr'({guide_terms}.+{task_terms}.+{able_terms}.+{learning_terms})'},
         {'type': 'learning skill 35', 'pattern':fr'({guide_terms}.+{learning_terms}.+{task_terms})'},
         {'type': 'learning skill 36', 'pattern':fr'({ui_terms}.+{clear_terms}.+{regex.ease_terms}.+{training_terms}.+{learning_terms})'},
         {'type': 'learning skill 37', 'pattern':fr'({customize_terms}.+{setting_terms}.+{regex.ease_terms}.+({task_terms}|{access_terms}))'},
         {'type': 'learning skill 38', 'pattern':fr'({update_terms}.+({learning_terms}|{training_terms}).+{update_terms}.+{change_terms}.+{learning_terms})'},
         {'type': 'learning skill 39', 'pattern':fr'({training_terms}.+{identification_terms}.+({guide_terms}|{describe_terms}).+{regex.ease_terms}.+{use_terms})'},
         {'type': 'learning skill 40', 'pattern':fr'({guide_terms}.+{product_terms}.+{able_terms}.+{right_terms}.+{use_terms})'},
         {'type': 'learning skill 41', 'pattern':fr'({regex.want_terms.value}.+{regex.change_terms.value}.+{regex.terminate_terms.value}.+{regex.able_terms.value}.+{wrong_terms}.+{learning_terms})'},
         {'type': 'learning skill 42', 'pattern':fr'({want_terms}.+{ui_terms}.+{clear_terms}.+{regex.able_terms.value}.+{search_terms}.+{Feature_terms}.+{learning_terms})'},
         {'type': 'learning skill 43', 'pattern':fr'({regex.able_terms.value}.+({regex.guide_terms.value}|{regex.training_terms.value}|{regex.learning_terms.value}))'},
         {'type': 'learning skill 44', 'pattern':fr'({regex.want_terms.value}.+({regex.guide_terms.value}|{regex.learning_terms.value}|{regex.training_terms.value}).+{regex.able_terms.value}.+{regex.ease_terms.value}(.+{regex.use_terms.value}?))'},


        #efficiency
        {'type': 'efficiency skill 00', 'pattern':fr'({regex.able_terms.value}.+{regex.ease_terms.value}?.+{product_terms}.+{buy_terms}.+{issue_terms}.+{time_terms}.+{search_terms}.+{long_terms})'},
        {'type': 'efficiency skill 01', 'pattern':fr'({regex.able_terms.value}.+{regex.ease_terms.value}?.+{product_terms}.+{Feature_terms}.+{search_terms})'},
        {'type': 'efficiency skill 02', 'pattern':fr'({address_terms}.+{delivery_terms}.+{regex.ease_terms.value}.+{add_terms}.+{order_terms})'},
        {'type': 'efficiency skill 03', 'pattern':fr'({regex.able_terms.value}.+{product_terms}.+{Feature_terms}.+{grading_terms}.+{regex.ease_terms.value})'},
        {'type': 'efficiency skill 04', 'pattern':fr'({regex.able_terms.value}.+{status_terms}.+{order_terms}.+{follow_terms}.+{time_terms}.+{delivery_terms})'},
        {'type': 'efficiency skill 05', 'pattern':fr'({regex.able_terms.value}.+{product_terms}.+{future_terms}.+{save_terms}.+{regex.ease_terms.value})'},
        {'type': 'efficiency skill 06', 'pattern':fr'({subscription_terms}.+{regex.able_terms.value}.+{discount_terms}.+{learning_terms})'},
        {'type': 'efficiency skill 07', 'pattern':fr'({language_terms}.+{site_terms}.+{regex.able_terms.value}.+{content_terms}.+{study_terms})'},
        {'type': 'efficiency skill 08', 'pattern':fr'({regex.able_terms.value}.+{account_terms}.+{access_terms}.+{regex.ease_terms.value})'},
        {'type': 'efficiency skill 09', 'pattern':fr'({regex.able_terms.value}.+{code_terms}.+{discount_terms}.+{buy_terms})'},
        {'type': 'efficiency skill 10', 'pattern':fr'({regex.able_terms.value}.+{detail_terms}.+{product_terms}.+{observe_terms}.+{decision_terms})'},
        {'type': 'efficiency skill 11', 'pattern':fr'({regex.able_terms.value}.+{experience_terms}.+{subscription_terms}.+{update_terms}?)'},
        {'type': 'efficiency skill 12', 'pattern':fr'({search_terms}.+{filter_terms}.+{product_terms})'},
        {'type': 'efficiency skill 13', 'pattern':fr'({size_terms}.+{product_terms}.+{fast_terms}.+{decision_terms}.+{buy_terms})'},
        {'type': 'efficiency skill 14', 'pattern':fr'({fast_terms}.+{guide_terms}.+{product_terms}.+{read_terms}.+{use_terms})'},
        {'type': 'efficiency skill 15', 'pattern':fr'({notification_terms}.+{status_terms}.+{order_terms}.+{learning_terms})'},
        {'type': 'efficiency skill 16', 'pattern':fr'({search_terms}.+{based_terms}.+{grading_terms}.+{regex.able_terms.value}.+{product_terms})'},
        {'type': 'efficiency skill 17', 'pattern':fr'({product_terms}.+{based_terms}.+{observe_terms}.+{regex.ease_terms.value})'},
        {'type': 'efficiency skill 18', 'pattern':fr'({code_terms}.+{discount_terms}.+{buy_terms}.+{discount_terms})'},
        {'type': 'efficiency skill 19', 'pattern':fr'({inventory_terms}.+{shopping_cart_terms}.+{time_terms}.+{observe_terms}.+{product_terms})'},
        {'type': 'efficiency skill 20', 'pattern':fr'({want_terms}.+{invoice_terms}.+{buy_terms}.+{observe_terms}.+{regex.able_terms.value}.+{detail_terms}.+{buy_terms})'},
        {'type': 'efficiency skill 21', 'pattern':fr'({want_terms}.+({experience_terms}|{suggestion_terms}).+{buy_terms}.+{subscription_terms}.+{regex.able_terms.value}.+{learning_terms})'},
        {'type': 'efficiency skill 22', 'pattern':fr'({want_terms}.+({experience_terms}|{suggestion_terms}).+{regex.able_terms.value}.+{experience_terms}.+{subscription_terms})'},
        {'type': 'efficiency skill 23', 'pattern':fr'({want_terms}.+{submit_terms}.+{decision_terms}.+{regex.able_terms.value}.+{product_terms}.+{time_terms}.+{receive_terms})'},
        {'type': 'efficiency skill 24', 'pattern':fr'({want_terms}.+{legal_terms}.+{fast_terms}.+{observe_terms}.+{regex.able_terms.value}.+({legal_terms}|{task_terms}).+{learning_terms})'},
        {'type': 'efficiency skill 25', 'pattern':fr'({want_terms}.+{product_terms}.+{favourite_terms}.+{regex.able_terms.value}.+{regex.ease_terms.value}.+({buy_terms}|{access_terms}))'},
        {'type': 'efficiency skill 26', 'pattern':fr'({want_terms}.+{notification_terms}.+{product_terms}.+{regex.able_terms.value}.+{discount_terms}.+{buy_terms})'},
        {'type': 'efficiency skill 27', 'pattern':fr'({want_terms}.+{product_terms}.+{based_terms}.+{search_terms}.+{regex.able_terms.value}.+{product_terms}.+{regex.ease_terms.value}.+{find_terms})'},
        {'type': 'efficiency skill 28', 'pattern':fr'({want_terms}.+{content_terms}.+{clear_terms}.+{regex.able_terms.value}.+{regex.ease_terms.value}.+{use_terms})'},
        {'type': 'efficiency skill 29', 'pattern':fr'({want_terms}.+{fast_terms}.+{access_terms}.+{regex.able_terms.value}.+{time_terms}.+{access_terms})'},
        {'type': 'efficiency skill 30', 'pattern':fr'({want_terms}.+{product_terms}.+{based_terms}.+{search_terms}.+{regex.able_terms.value}.+{product_terms}.+{regex.ease_terms.value})'},
        {'type': 'efficiency skill 31', 'pattern':fr'({want_terms}.+{content_terms}.+{clear_terms}.+{regex.able_terms.value}.+{regex.ease_terms.value}.+{use_terms})'},
        {'type': 'efficiency skill 32', 'pattern':fr'({want_terms}.+{preview_terms}.+{Feature_terms}.+{regex.able_terms.value}.+{result_terms}.+{confident_terms})'},
        {'type': 'efficiency skill 33', 'pattern':fr'({want_terms}.+{ui_terms}.+({clear_terms}|{simple_terms}).+{regex.able_terms.value}.+{regex.ease_terms.value}.+{task_terms})'},
        {'type': 'efficiency skill 34', 'pattern':fr'({want_terms}.+({search_terms}|{filter_terms}).+{regex.able_terms.value}.+{result_terms}.+{regex.ease_terms.value}.+{find_terms})'},
        {'type': 'efficiency skill 35', 'pattern':fr'({want_terms}.+{change_terms}.+{terminate_terms}.+{regex.able_terms.value}.+{wrong_terms}.+{learning_terms})'},
        {'type': 'efficiency skill 36', 'pattern':fr'({want_terms}.+{task_terms}.+{observe_terms}.+{regex.able_terms.value}.+{regex.ease_terms.value}.+{again_terms})'},
        {'type': 'efficiency skill 37', 'pattern':fr'({want_terms}.+{task_terms}.+{Simultaneously_terms}.+{regex.able_terms.value}.+(({fast_terms}.+{time_terms})|({time_terms}.+{fast_terms})))'},
        {'type': 'efficiency skill 38', 'pattern':fr'({want_terms}.+{task_terms}.+{observe_terms}.+{regex.able_terms.value}.+{regex.ease_terms.value}.+{again_terms})'},


        



        

        


        

        




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


#userstory checked with useability nonfunctional requirements

def userstory_useability(lemma_userstory: str):
    arr = []
    pattern = [
        #useability 
        {'type': 'useability', 'pattern':fr'({regex.able_terms.value}.+({regex.ease_terms.value}|{regex.fast_terms.value}|{regex.clear_terms.value}|{regex.automated_terms.value}|{regex.simple_terms.value}|{regex.time_terms.value}|{regex.learning_terms.value}))'},


        #not useability
        {'type': 'not useability', 'pattern':fr'({regex.notuseability_terms.value})'},
    ]
    matched = False
    for p in pattern:
        if re.search(p['pattern'], lemma_userstory):
            arr.append({'type':p['type']})
            print('user stories are checked')
            matched=True
            break
    if not matched:
        arr.append({'type': 'need to be checked'})
    return arr


def userstory_useability_check(df: pd.DataFrame):
    output_file = "/Users/farrr/Desktop/Desktop/project/useability_userstory.csv"
    df.loc[:,'useability_userstory'] = df['string_lemmatized_userstory'].apply(userstory_useability)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print('All Useability user stories are identified')
   

def test():
    userstory_useability_check(df)
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
