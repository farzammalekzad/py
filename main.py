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
    non_functional_requirement: list
    other_non_functional_requirements: str

class regex(Enum):
    want_terms = r'(خواست#خواه)'
    able_terms = r'(توانست#توان)'
    training_terms = r'(آموزش|آموزشی|دوره آموزشی|تربیت|کارگاه|آموزشگاه|آموزش‌دهی|کلاس)'
    task_terms = r'(وظایف|کارها|امور|وظیفه|فعالیت|مسئولیت|وظیفه‌محور|کاربردها|عملیات|عملیات‌ها)'
    learning_terms = r'(یادگیری|فهمیدن|فهم|درک|آموختن|آموزش دیدن|فراگیری|شناخت|مسلط|آگاه|یاد گرفت)'
    use_terms = r'(استفاده|بهره‌برداری|بهره‌گیری|کاربرد|به‌کارگیری|به‌کار بردن|به‌کار گرفتن|انجام|تکمیل)'
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
    wrong_terms = r'(غلط|صحیح|درست|اشتباه|نادرست|بی‌دقتی|ناقص)'
    prevention_terms = r'(جلوگیری|ممانعت|پیشگیری|سد کردن|بازداری|مهار|مانع)'
    change_terms = r'(تغییر|تغییرات|اصلاح|بازنگری|دگرگونی|درست)'
    preview_terms = r'(پیش نمایش|پیش‌نمایش)'
    accuracy_terms = r'(صحت|درستی|صحیح|درست|بی‌خطا|بی‌نقص)'
    again_terms = r'(مجدد|بازگشت|برگردم|دوباره|از نو|تکرار)'
    continue_terms = r'(ادامه|پیشبرد|دنبال کردن|ادامه دادن|پیش‌روی)'
    previous_terms = r'(قبلی|گذشته|فعالیت‌های قبلی|پیشین|سوابق قبلی|کارهای گذشته)'
    event_terms = r'(رویدادها|سوابق|سابقه|تاریخچه|اتفاقات|حوادث|فعالیت‌ها)'
    access_terms = r'(دستیابی|دسترسی|راه‌یابی|ورود|اتصال به|باز کردن|دسترس)'
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
    error_terms = r'(خطا|نقص|ایراد|مشکل|ناقص)'
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
    site_terms= r'(سایت|سایت‌ها|سایت‌های|سایت‌های اینترنتی|سایت اینترنتی|نرم‌افزار|نرم افزار)'
    content_terms= r'(محتوا|محتوای|محتوای سایت|محتوای وب|محتوای وب‌سایت|مفهوم)'
    study_terms= r'(مطالعه|مطالعه کردن|مطالعه‌کردن|خواندن|خواندن مطالب|خواندن مطالب)'
    account_terms= r'(حساب|حساب‌ها|حساب‌های|حساب‌های کاربری|حساب کاربری| حساب‌های اجتماعی| حساب اجتماعی)'
    code_terms= r'(کد|کد تخفیف|کد تخفیفی|کد تخفیف‌ها|کد تخفیف‌های|کد تخفیف‌های ویژه)'
    observe_terms= r'(مشاهده|مشاهده کردن|مشاهده‌کردن|نگاه کردن|نگاه‌کردن)'
    detail_terms= r'(جزئیات|جزئیات بیشتر|جزئیات بیشتری|جزئیات بیشتری|جزئیات بیشتری)'
    decision_terms= r'(تصمیم|تصمیم‌گیری|تصمیم‌گیری کردن|تصمیم‌گیری‌کردن|انتخاب)'
    experience_terms= r'(تجربه|تجربه‌ها|تجربه‌های|تجربه‌های کاربری|تجربه کاربری|تجربیات|تجربه استفاده)'
    filter_terms= r'(فیلتر|فیلتر کردن|فیلتر‌کردن|پالایش|پالایش کردن|پالایش‌کردن)'
    size_terms= r'(اندازه|اندازه‌ها|اندازه‌های|اندازه‌های مختلف|اندازه مختلف|سایز)'
    read_terms= r'(خواندن|خواندن مطالب|خواندن مطالب|مطالعه|مطالعه کردن)'
    notification_terms= r'(اطلاعیه|اطلاعیه‌ها|اطلاعیه‌های|اطلاعیه‌های جدید|اطلاعیه جدید|اعلان|اعلان‌ها|اعلان‌های|اعلان‌های جدید|اعلان جدید|هشدار|اعلام|پیشنهاد|پیام)'
    based_terms = r'(پایه|اساس|مبنا|بنیاد|بنیادی|اساسی|مبنایی)'
    inventory_terms = r'(انبار|انبارها|انبارهای|انبارهای موجود|انبار موجود|موجودی)'
    shopping_cart_terms = r'(سبد خرید|سبد خریدها|سبد خریدهای|سبد خریدهای موجود|سبد خرید موجود|سبد خریدهای موجود)'
    invoice_terms = r'(فاکتور|فاکتورها|فاکتورهای|فاکتورهای موجود|فاکتور موجود|فاکتورهای موجود)'
    submit_terms = r'(ارسال|ارسال کردن|ارسال‌کردن|ارسال نمودن|ارسال‌نمودن)'
    legal_terms = r'(قانونی|قوانین|حقوقی|مقررات)'
    favourite_terms = r'(مورد علاقه|مورد علاقه‌ها|مورد علاقه‌های|مورد علاقه‌های کاربری|مورد علاقه کاربری|مورد علاقه‌های کاربری|علاقه‌مندی|علاقه مندی)'
    result_terms= r'(نتیجه|نتایج|نتیجه‌ها|نتایج|نتیجه‌های|نتایج|نتیجه‌های موجود|نتایج موجود)'
    confident_terms= r'(اطمینان|مطمئن|مطمین)'
    find_terms = r'(یافتن|یافتن محصول|یافتن محصولات|یافتن محصولات|پیدا کردن|پیداکردن)'
    simple_terms= r'(ساده|ساده‌تر|ساده‌ترین|بسیار ساده|بسیار ساده‌تر|بسیار ساده‌ترین)'
    terminate_terms= r'(پایان|پایان دادن|لغو|لغو کردن|پایان دادن به|پایان دادن به|)'
    Simultaneously_terms= r'(همزمان)'
    automated_terms= r'(خودکار|خودکارسازی|خودکارسازی شده|خودکارسازی‌شده)'
    satisfaction_terms= r'(رضایت|رضایت‌بخشی|رضایت‌بخش|رضایت‌بخشی|رضایت‌بخش)'
    notuseability_terms= r'(سرعت بارگذاری|زمان پاسخ‌دهی|عملکرد بهینه|منابع سیستم|داده امن|حریم خصوصی|رمزنگاری|محرمانگی|پایداری سیستم|اطلاعات دست رفت|عملکرد پایدار|بازیابی خطا|کاربر نیاز|صفحه‌خوان|چندزبانگی)'
    efficiency_terms= r'(زمان کمتر|بهینه|کاهش تلاش|کمترین کلیک|تاخیر کمتر|اتلاف وقت|تلاش|کارایی|تاخیر|معطلی|کارآمد|دقت بیشتر|دقت)'
    #efficiency_terms= r'(سریع|بی‌درنگ|چابک|در لحظه|اتلاف وقت|تلاش|کارایی|وقفه|وقت اضافی)'
    efficienct_verbs= r'(کاهش|افزایش|بیشتر|کمتر)'
    default_terms= r'(پیش‌فرض|پیش‌فرض‌ها|پیش‌فرض‌های|پیش‌فرض‌های نرم‌افزار|پیش‌فرض نرم‌افزار|گزینه پیش‌فرض)'
    click_terms= r'(کلیک|کلیک کردن|کلیک‌کردن|کلیک نمودن|کلیک‌نمودن|دکمه|دکمه‌ها|دکمه‌های|دکمه‌های نرم‌افزار|دکمه نرم‌افزار)'
    shortcut_terms= r'(میانبرهای نرم‌افزار|میانبر نرم‌افزار|میانبرهای نرم‌افزار|میانبر کیبورد|میانبر صفحه‌کلید|میانبر)'
    recovery_terms= r'(بازیابی)'
    reminder_terms= r'(یادآوری|یادآوری‌ها|یادآوری‌های|یادآوری‌های نرم‌افزار|یادآوری نرم‌افزار|یادآوری‌های نرم‌افزار|یادآوری)'
    duplicate_terms= r'(تکرار|تکرار کردن|تکرار‌کردن|تکرار نمودن|تکرار‌نمودن|مجدد|دوباره)'
    Forgetfulness_terms= r'(فراموشی|فراموشی‌ها|فراموشی‌های|فراموشی جلوگیری|فراموش)'
    improve_terms= r'(بهبود|بهبودی|بهبودی‌ها|بهبودی‌های|بهبودی‌های نرم‌افزار|بهبود نرم‌افزار)'
    timeoflearning_terms = r'(زمان آموزش|زمان آموزشی|زمان آموزش‌ها|زمان آموزش‌های|زمان آموزش‌های نرم‌افزار|زمان آموزش نرم‌افزار|زمان یادگیری)'
    refer_terms= r'(مراجعه|مراجعه کردن|مراجعه‌کردن|مراجعه نمودن|مراجعه‌نمودن)'
    keepon_terms= r'(ادامه|ادامه دادن|ادامه‌دادن|ادامه نمودن|ادامه‌نمودن)'
    errornotification_terms= r'(پیام خطا|هشدار خطا|پیام خطای)'
    tell_terms= r'(گفتن|گفتن به|گفتن به کاربر|گفتن به کاربران|گفتن به کاربران|گفتن به کاربران نرم‌افزار|گفتن به کاربر نرم‌افزار|گفت|گو)'
    solve_terms= r'(حل|حل کردن|حل‌کردن|حل نمودن|حل‌نمودن|برطرف|رفع)'
    dangerious_terms= r'(خطرناک|خطرناکی|خطرناکی‌ها|خطرناکی‌های|خطرناکی‌های نرم‌افزار|خطرناکی نرم‌افزار|خطرناکی‌های نرم‌افزار)'
    weak_terms= r'(ضعیف|ضعیفی|ضعیفی‌ها|ضعیفی‌های|ضعیفی‌های نرم‌افزار|ضعیفی نرم‌افزار|ضعیفی‌های نرم‌افزار)'
    strong_terms= r'(قوی|قویی|قویی‌ها|قویی‌های|قویی‌های نرم‌افزار|قویی نرم‌افزار|قویی‌های نرم‌افزار)'
    execute_terms= r'(اجرا|اجرا کردن|اجرا‌کردن|اجرا نمودن|اجرا‌نمودن|انجام|انجام دادن|انجام‌دادن|انجام نمودن|انجام‌نمودن|برقرار کردن|برقرار|پیاده‌سازی| پیاده سازی|مستقر|استقرار)'
    informed_terms= r'(آگاه|آگاهی|آگاهی‌ها|آگاهی‌های|مطلع|اطلاع)'
    support_terms= r'(پشتیبانی|پشتیبانی کردن|پشتیبانی‌کردن|پشتیبانی نمودن|پشتیبانی‌نمودن|حمایت|حمایت کردن|حمایت‌کردن|حمایت نمودن|حمایت‌نمودن)'
    good_terms= r'(خوب|خوبی|خوبی‌ها|بهتر|بهتری|راحت)'
    satisfaction_terms_pattern= r'(راحتی استفاده|کاربرپسند|سادگی|ناوبری آسان|قابل فهم|بدون پیچیدگی|قابلیت شهودی|یادگیری آسان|بدون نیاز به آموزش|کمترین کلیک ممکن|سرعت بالا|انجام سریع وظایف|کاهش تلاش کاربر|بدون نیاز به ورود اطلاعات اضافی|فرآیند یکپارچه|بازخورد فوری|نمایش پیام‌های واضح|راهنمایی کاربر|پیش‌بینی نیازهای کاربر|کنترل کامل بر عملیات|قابل بازگشت|سازگاری با دستگاه‌های مختلف|دسترسی‌پذیری|قابل استفاده در موبایل و دسکتاپ|امکان شخصی‌سازی|سازگاری با مرورگرهای مختلف|حداقل خطاهای کاربر|نمایش پیغام‌های خطای شفاف|راهنمایی گام‌به‌گام|کاهش بار شناختی کاربر|ورود اطلاعات با کمترین تلاش|ارائه پیشنهادهای هوشمند|تجربه راحت|احساس اطمینان|تجربه کاربری|لذت|تجربه شخصی|رضایت|رضایت بخش|احساس رضایت|راحت|راحتی)'

def userstory_nonfunctional(lemma_userstory: str) -> list:
     
    arr = []
    matched = False
    learnability_pattern = [
          {'type': 'learnability 00', 'pattern':fr'{regex.training_terms.value}.+{regex.learning_terms.value}.+{regex.use_terms.value}'},
          {'type': 'learnability 02', 'pattern':fr'{regex.guide_terms.value}.+{regex.access_terms.value}.+{regex.learning_terms.value}.+{regex.use_terms.value}'},
          {'type': 'learnability 03', 'pattern':fr'{regex.clear_terms.value}.+{regex.ease_terms}.+{regex.fast_terms.value}.+{regex.learning_terms.value}'},
          {'type': 'learnability 04', 'pattern':fr'({regex.fast_terms.value}.+{regex.learning_terms.value}.+{regex.use_terms.value})'},
          {'type': 'learnability 05', 'pattern':fr'({regex.issue_terms.value}.+{regex.question_terms.value}.+{regex.help_terms.value}.+{regex.ease_terms})'},
          {'type': 'learnability 06', 'pattern':fr'({regex.describe_terms.value}.+{regex.task_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 07', 'pattern':fr'({regex.training_terms.value}.+{regex.ease_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 08', 'pattern':fr'({regex.feedback_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 09', 'pattern':fr'({regex.performance_terms.value}.+{regex.learning_terms.value}.+{regex.use_terms.value})'},
          {'type': 'learnability 11', 'pattern':fr'({regex.learning_terms.value}.+{regex.use_terms.value}.+{regex.fast_terms.value})'},
          {'type': 'learnability 12', 'pattern':fr'({regex.question_terms.value}.+{regex.have_terms.value}.+{regex.ease_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 13', 'pattern':fr'({regex.guide_terms.value}.+{regex.ease_terms.value}.+{regex.performance_terms.value}.+{regex.fast_terms.value})'},
          {'type': 'learnability 14', 'pattern':fr'({regex.learning_terms.value}.+{regex.ease_terms.value}.+{regex.use_terms.value})'},
          {'type': 'learnability 15', 'pattern':fr'({regex.minimal_terms.value}.+{regex.design_terms.value}.+{regex.ease_terms.value})'},
          {'type': 'learnability 16', 'pattern':fr'({regex.setting_terms.value}.+{regex.restore_terms.value}.+{regex.wrong_terms.value}.+({regex.prevention_terms.value}|{regex.use_terms.value}))'},
          {'type': 'learnability 17', 'pattern':fr'({regex.ease_terms.value}.+({regex.learning_terms.value}|آشنا).+{regex.use_terms.value})'},
          {'type': 'learnability 18', 'pattern':fr'({regex.task_terms.value}.+{regex.suggestion_terms.value}.+{regex.ease_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 19', 'pattern':fr'({regex.guide_terms.value}.+{regex.ease_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 20', 'pattern':fr'({regex.ease_terms.value}.+{regex.order_terms.value}.+{regex.setting_terms.value}.+{regex.ease_terms.value})'},
          {'type': 'learnability 21', 'pattern':fr'({regex.change_terms.value}.+{regex.preview_terms.value}.+{regex.right_terms.value}.+{regex.ease_terms.value})'},
          {'type': 'learnability 22', 'pattern':fr'({regex.save_terms.value}.+{regex.able_terms.value}.+{regex.again_terms.value}.+{regex.continue_terms.value})'},
          {'type': 'learnability 23', 'pattern':fr'({regex.guide_terms.value}.+{regex.ease_terms.value}.+{regex.use_terms.value}.+{regex.compensation_terms.value})'},
          {'type': 'learnability 24', 'pattern':fr'({regex.training_terms.value}.+{regex.learning_terms.value}.+{regex.progress_terms.value})'},
          {'type': 'learnability 25', 'pattern':fr'({regex.guide_terms.value}.+{regex.save_terms.value}.+{regex.previous_terms.value}.+{regex.review_terms.value})'},
          {'type': 'learnability 26', 'pattern':fr'({regex.training_terms.value}.+{regex.path_terms.value}.+{regex.ease_terms.value}.+{regex.continue_terms.value})'},
          {'type': 'learnability 27', 'pattern':fr'({regex.previous_terms.value}.+{regex.event_terms.value}.+{regex.access_terms.value}.+({regex.review_terms.value}|{regex.follow_terms.value}))'},
          {'type': 'learnability 28', 'pattern':fr'({regex.update_terms.value}.+({regex.describe_terms.value}|{regex.guide_terms.value}).+{regex.ease_terms.value}.+{regex.learning_terms.value}.+{regex.use_terms.value})'},
          {'type': 'learnability 29', 'pattern':fr'({regex.training_terms.value}.+{regex.reference_terms.value}.+{regex.ease_terms.value}?.+{regex.learning_terms.value})'},
          {'type': 'learnability 30', 'pattern':fr'({regex.learning_terms.value}.+{regex.save_terms.value}.+{regex.progress_terms.value}.+{regex.ease_terms.value}.+{regex.again_terms.value})'},
          {'type': 'learnability 31', 'pattern':fr'({regex.reference_terms.value}?.+{regex.training_terms.value}.+{regex.access_terms.value}.+({regex.guide_terms.value}|{regex.describe_terms.value}).+{regex.ease_terms.value})'},
          {'type': 'learnability 32', 'pattern':fr'(({regex.learning_terms.value}|{regex.training_terms.value}).+{regex.presentation_terms.value}.+{regex.learning_terms.value}.+{regex.use_terms.value})'},
          {'type': 'learnability 33', 'pattern':fr'({regex.training_terms.value}.+{regex.reference_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 34', 'pattern':fr'({regex.guide_terms.value}.+{regex.task_terms.value}.+{regex.able_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 35', 'pattern':fr'({regex.guide_terms.value}.+{regex.learning_terms.value}.+{regex.task_terms.value})'},
          {'type': 'learnability 36', 'pattern':fr'({regex.ui_terms.value}.+{regex.clear_terms.value}.+{regex.ease_terms.value}.+{regex.training_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 37', 'pattern':fr'({regex.customize_terms.value}.+{regex.setting_terms.value}.+{regex.ease_terms.value}.+({regex.task_terms.value}|{regex.access_terms.value}))'},
          {'type': 'learnability 38', 'pattern':fr'({regex.update_terms.value}.+({regex.learning_terms.value}|{regex.training_terms.value}).+{regex.update_terms.value}.+{regex.change_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 39', 'pattern':fr'({regex.training_terms.value}.+{regex.identification_terms.value}.+({regex.guide_terms.value}|{regex.describe_terms.value}).+{regex.ease_terms.value}.+{regex.use_terms.value})'},
          {'type': 'learnability 40', 'pattern':fr'({regex.guide_terms.value}.+{regex.product_terms.value}.+{regex.able_terms.value}.+{regex.right_terms.value}.+{regex.use_terms.value})'},
          {'type': 'learnability 41', 'pattern':fr'({regex.want_terms.value}.+{regex.change_terms.value}.+{regex.terminate_terms.value}.+{regex.able_terms.value}.+{regex.wrong_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 42', 'pattern':fr'({regex.want_terms.value}.+{regex.ui_terms.value}.+{regex.clear_terms.value}.+{regex.able_terms.value}.+{regex.search_terms.value}.+{regex.Feature_terms.value}.+{regex.learning_terms.value})'},
          {'type': 'learnability 43', 'pattern':fr'({regex.able_terms.value}.+({regex.guide_terms.value}|{regex.training_terms.value}|{regex.learning_terms.value}))'},
          {'type': 'learnability 44', 'pattern':fr'({regex.want_terms.value}.+({regex.guide_terms.value}|{regex.learning_terms.value}|{regex.training_terms.value}).+{regex.able_terms.value}.+{regex.ease_terms.value}(.+{regex.use_terms.value}?))'},
    ]

    Memorability_pattern = [
        {'type': 'Memorability 00', 'pattern':fr'({regex.want_terms.value}.+{regex.event_terms.value}.+{regex.task_terms.value}.+{regex.able_terms.value}.+{regex.ease_terms.value}.*({regex.recovery_terms.value}|{regex.reminder_terms.value}))'},
        {'type': 'Memorability 01', 'pattern':fr'({regex.want_terms.value}.+{regex.event_terms.value}.+{regex.task_terms.value}.+{regex.able_terms.value}.+{regex.ease_terms.value}.*{regex.access_terms.value}.+{regex.reminder_terms.value})'},
        {'type': 'Memorability 02', 'pattern':fr'({regex.want_terms.value}.+{regex.progress_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+{regex.continue_terms.value})'},
        {'type': 'Memorability 03', 'pattern':fr'({regex.want_terms.value}.+{regex.setting_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+{regex.need_terms.value}.+{regex.duplicate_terms.value})'},
        {'type': 'Memorability 04', 'pattern':fr'({regex.want_terms.value}.+{regex.reminder_terms.value}.+{regex.use_terms.value}.+{regex.able_terms.value}.+({regex.ease_terms.value}|{regex.fast_terms.value}).+{regex.Forgetfulness_terms.value})'},
        {'type': 'Memorability 05', 'pattern':fr'({regex.want_terms.value}.+{regex.Feature_terms.value}.+{regex.reminder_terms.value}.+{regex.able_terms.value}.+{regex.use_terms.value}.+{regex.Forgetfulness_terms.value})'},
        #{'type': 'Memorability 06', 'pattern':fr'({regex.progress_terms.value}.+{regex.observe_terms.value}.+{regex.confident_terms.value}.+{regex.learning_terms.value})'},
        {'type': 'Memorability 07', 'pattern':fr'({regex.want_terms.value}.+{regex.training_terms.value}.+{regex.update_terms.value}.+{regex.able_terms.value}.+{regex.learning_terms.value}.+{regex.improve_terms.value})'},
        {'type': 'Memorability 08', 'pattern':fr'({regex.want_terms.value}.+{regex.shortcut_terms.value}.+{regex.fast_terms.value}.+{regex.able_terms.value}.+{regex.learning_terms.value}.+({regex.improve_terms.value}|{regex.efficienct_verbs.value}))'},
        {'type': 'Memorability 09', 'pattern':fr'({regex.want_terms.value}.+{regex.training_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+{regex.previous_terms.value}.+{regex.review_terms.value})'},
        {'type': 'Memorability 10', 'pattern':fr'({regex.want_terms.value}.+{regex.automated_terms.value}.*{regex.reminder_terms.value}.+{regex.able_terms.value}.+{regex.ease_terms.value}.*{regex.learning_terms.value})'},
        {'type': 'Memorability 11', 'pattern':fr'({regex.want_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+{regex.continue_terms.value})'},
        {'type': 'Memorability 12', 'pattern':fr'({regex.want_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+{regex.previous_terms.value}.+{regex.review_terms.value})'},
        {'type': 'Memorability 13', 'pattern':fr'({regex.want_terms.value}.+{regex.search_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+{regex.access_terms.value}.+{regex.reminder_terms.value})'},
        {'type': 'Memorability 14', 'pattern':fr'({regex.want_terms.value}.+(({regex.guide_terms.value}.+{regex.access_terms.value})|({regex.access_terms.value}.+{regex.guide_terms.value})).+{regex.able_terms.value}.+{regex.Forgetfulness_terms.value}.+{regex.learning_terms.value})'},
        {'type': 'Memorability 15', 'pattern':fr'({regex.want_terms.value}.+{regex.event_terms.value}.+{regex.able_terms.value}.+{regex.fast_terms.value}.+{regex.improve_terms.value})'},
        {'type': 'Memorability 16', 'pattern':fr'({regex.want_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+(({regex.setting_terms.value}.+?{regex.duplicate_terms.value})|{regex.setting_terms.value}).*{regex.ease_terms.value}.*{regex.use_terms.value})'},
        {'type': 'Memorability 17', 'pattern':fr'({regex.want_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+({regex.ease_terms.value}|{regex.fast_terms.value}).+{regex.refer_terms.value})'},
        {'type': 'Memorability 18', 'pattern':fr'({regex.want_terms.value}.+{regex.guide_terms.value}.+{regex.able_terms.value}.+({regex.ease_terms.value}|{regex.fast_terms.value}).+{regex.learning_terms.value}.+{regex.Forgetfulness_terms.value})'},
        {'type': 'Memorability 19', 'pattern':fr'({regex.want_terms.value}.+{regex.observe_terms.value}.+{regex.able_terms.value}.+?{regex.time_terms.value}.+{regex.ease_terms.value}.+{regex.keepon_terms.value})'},
        {'type': 'Memorability 20', 'pattern':fr'({regex.want_terms.value}.+({regex.previous_terms.value}|{regex.event_terms.value}).+({regex.observe_terms.value}|{regex.presentation_terms.value}).+{regex.able_terms.value}.+({regex.ease_terms.value}|{regex.fast_terms.value}).+{regex.again_terms.value}.+{regex.keepon_terms.value})'},
        {'type': 'Memorability 21', 'pattern':fr'({regex.want_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+({regex.reminder_terms.value}|{regex.Forgetfulness_terms.value}|{regex.access_terms.value}))'},
        {'type': 'Memorability 22', 'pattern':fr'({regex.want_terms.value}.+{regex.guide_terms.value}.+{regex.automated_terms.value}.+{regex.able_terms.value}.+{regex.Forgetfulness_terms.value}.+{regex.learning_terms.value})'},
        {'type': 'Memorability 23', 'pattern':fr'({regex.want_terms.value}.+{regex.guide_terms.value}.+{regex.able_terms.value}.+{regex.Forgetfulness_terms.value})'},
        {'type': 'Memorability 24', 'pattern':fr'({regex.want_terms.value}.+{regex.wrong_terms.value}.+{regex.able_terms.value}.+{regex.reminder_terms.value}.+{regex.change_terms.value})'},
        {'type': 'Memorability 25', 'pattern':fr'({regex.want_terms.value}.+{regex.event_terms.value}.+({regex.save_terms.value}|{regex.access_terms.value}).+{regex.able_terms.value}.+{regex.previous_terms.value}.*{regex.review_terms.value})'},
        {'type': 'Memorability 26', 'pattern':fr'({regex.want_terms.value}.+{regex.previous_terms.value}.+{regex.reminder_terms.value}.+{regex.able_terms.value}.+({regex.review_terms.value}|{regex.Forgetfulness_terms.value}))'},
        {'type': 'Memorability 27', 'pattern':fr'({regex.want_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+{regex.efficienct_verbs.value})'},
        {'type': 'Memorability 28', 'pattern':fr'({regex.want_terms.value}.+{regex.notification_terms.value}.+{regex.able_terms.value}.+{regex.Forgetfulness_terms.value})'},
        {'type': 'Memorability 29', 'pattern':fr'({regex.want_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+({regex.previous_terms.value}|{regex.again_terms.value}))'},
        {'type': 'Memorability 30', 'pattern':fr'({regex.want_terms.value}.+{regex.reminder_terms.value}.+{regex.able_terms.value}.+{regex.use_terms.value})'},


    ]

    error_pattern = [
        {'type': 'error 00', 'pattern':fr'({regex.want_terms.value}.+{regex.errornotification_terms.value}.+{regex.able_terms.value}.+({regex.wrong_terms.value}|{regex.error_terms.value}).+({regex.identification_terms.value}|{regex.change_terms.value}))'},
        {'type': 'error 01', 'pattern':fr'({regex.want_terms.value}.+{regex.wrong_terms.value}.+({regex.tell_terms.value}|{regex.notification_terms.value}).+{regex.able_terms.value}.+{regex.error_terms.value}.+{regex.prevention_terms.value})'},
        {'type': 'error 02', 'pattern':fr'({regex.want_terms.value}.+{regex.wrong_terms.value}.+{regex.tell_terms.value}.+{regex.able_terms.value}.+{regex.error_terms.value}.+{regex.change_terms.value})'},
        {'type': 'error 03', 'pattern':fr'({regex.want_terms.value}.+{regex.wrong_terms.value}.+{regex.able_terms.value}.+{regex.error_terms.value}.+{regex.prevention_terms.value})'},
        {'type': 'error 04', 'pattern':fr'({regex.want_terms.value}.+{regex.error_terms.value}.+{regex.presentation_terms.value}.+{regex.able_terms.value}.+{regex.error_terms.value}.+{regex.wrong_terms.value})'},
        {'type': 'error 05', 'pattern':fr'({regex.want_terms.value}.+{regex.error_terms.value}.+{regex.able_terms.value}.+{regex.error_terms.value}.+{regex.wrong_terms.value})'},
        {'type': 'error 06', 'pattern':fr'({regex.want_terms.value}.+{regex.error_terms.value}.+{regex.able_terms.value}.+{regex.error_terms.value}.+{regex.wrong_terms.value})'},
        {'type': 'error 07', 'pattern':fr'({regex.want_terms.value}.+{regex.wrong_terms.value}.+{regex.automated_terms.value}.*({regex.identification_terms.value}|{regex.change_terms.value}).+{regex.able_terms.value}.+({regex.error_terms.value}|{regex.wrong_terms.value}).+{regex.prevention_terms.value})'},
        {'type': 'error 08', 'pattern':fr'({regex.want_terms.value}.+{regex.notification_terms.value}.+{regex.prevention_terms.value}.+{regex.able_terms.value}.+{regex.error_terms.value}.+{regex.prevention_terms.value})'},
        {'type': 'error 09', 'pattern':fr'({regex.want_terms.value}.+{regex.notification_terms.value}.+{regex.wrong_terms.value}.+{regex.able_terms.value}.+{regex.error_terms.value}.+{regex.identification_terms.value})'},
        {'type': 'error 10', 'pattern':fr'({regex.want_terms.value}.+{regex.notification_terms.value}.+{regex.error_terms.value}.+{regex.able_terms.value}.+{regex.again_terms.value})'},
        {'type': 'error 11', 'pattern':fr'({regex.want_terms.value}.+({regex.error_terms.value}|{regex.wrong_terms.value}).+{regex.change_terms.value}.+{regex.able_terms.value}.+({regex.error_terms.value}|{regex.solve_terms.value}))'},
        {'type': 'error 12', 'pattern':fr'({regex.want_terms.value}.+({regex.notification_terms.value}|{regex.errornotification_terms.value}).+{regex.able_terms.value}.+({regex.prevention_terms.value}|{regex.solve_terms.value}))'}, #برای برخی از داستان‌های کاربری با موضوعات غیر مرتبط ست می‌شود
        {'type': 'error 13', 'pattern':fr'({regex.want_terms.value}.+{regex.wrong_terms.value}.+{regex.tell_terms.value}.+{regex.able_terms.value}.+{regex.change_terms.value})'},
        {'type': 'error 14', 'pattern':fr'({regex.want_terms.value}.+({regex.wrong_terms.value}|{regex.error_terms.value}).+{regex.able_terms.value}.+({regex.identification_terms.value}|{regex.solve_terms.value}))'},
        {'type': 'error 15', 'pattern':fr'({regex.want_terms.value}.+{regex.wrong_terms.value}.+{regex.change_terms.value}.+{regex.able_terms.value}.+({regex.use_terms.value}|{regex.solve_terms.value}))'},
        {'type': 'error 16', 'pattern':fr'({regex.want_terms.value}.+{regex.task_terms.value}.*{regex.dangerious_terms.value}.+{regex.able_terms.value}.+{regex.wrong_terms.value}.+{regex.prevention_terms.value})'},
        {'type': 'error 17', 'pattern':fr'({regex.want_terms.value}.+{regex.wrong_terms.value}.+{regex.prevention_terms.value}.+{regex.able_terms.value}.+{regex.wrong_terms.value})'},
        {'type': 'error 18', 'pattern':fr'({regex.want_terms.value}.+({regex.weak_terms.value}|{regex.strong_terms.value}).+{regex.feedback_terms.value}.+{regex.able_terms.value}.+({regex.strong_terms.value}|{regex.weak_terms.value}).+({regex.prevention_terms.value}|{regex.solve_terms.value}|{regex.task_terms.value}))'},
        {'type': 'error 19', 'pattern':fr'({regex.want_terms.value}.+{regex.notification_terms.value}.+{regex.able_terms.value}.+({regex.wrong_terms.value}|{regex.error_terms.value}|{regex.change_terms.value}))'},
        {'type': 'error 20', 'pattern':fr'({regex.want_terms.value}.+{regex.wrong_terms.value}.+{regex.able_terms.value}.+{regex.change_terms.value})'},
        {'type': 'error 21', 'pattern':fr'({regex.want_terms.value}.+{regex.notification_terms.value}.+{regex.able_terms.value}.+{regex.informed_terms.value}.+({regex.execute_terms.value}|{regex.review_terms.value}))'},
        {'type': 'error 22', 'pattern':fr'({regex.want_terms.value}.+{regex.notification_terms.value}.+{regex.able_terms.value}.+({regex.execute_terms.value}|{regex.review_terms.value}))'},
        {'type': 'error 23', 'pattern':fr'({regex.want_terms.value}.+({regex.error_terms.value}|{regex.question_terms.value}).+{regex.support_terms.value}.+{regex.able_terms.value}.+{regex.error_terms.value}.+({regex.change_terms.value}|{regex.solve_terms.value}|{regex.prevention_terms.value}))'},
        {'type': 'error 24', 'pattern':fr'({regex.want_terms.value}.+({regex.error_terms.value}|{regex.question_terms.value}).+{regex.support_terms.value}.+{regex.able_terms.value}.+{regex.error_terms.value})'},






    ]
    
    
    efficiencyuse_pattern = [


        #efficiency
         {'type': 'efficiencyuse 00', 'pattern':fr'({regex.able_terms.value}.+{regex.ease_terms.value}?.+{regex.product_terms.value}.+{regex.buy_terms.value}.+{regex.issue_terms.value}.+{regex.time_terms.value}.+{regex.search_terms.value}.+{regex.long_terms.value})'},
         {'type': 'efficiencyuse 01', 'pattern':fr'({regex.able_terms.value}.+{regex.ease_terms.value}?.+{regex.product_terms.value}.+{regex.Feature_terms.value}.+{regex.search_terms.value})'},
         {'type': 'efficiencyuse 02', 'pattern':fr'({regex.address_terms.value}.+{regex.delivery_terms.value}.+{regex.ease_terms.value}.+{regex.add_terms.value}.+{regex.order_terms.value})'},
         {'type': 'efficiencyuse 03', 'pattern':fr'({regex.able_terms.value}.+{regex.product_terms.value}.+{regex.Feature_terms.value}.+{regex.grading_terms.value}.+{regex.ease_terms.value})'},
         {'type': 'efficiencyuse 04', 'pattern':fr'({regex.able_terms.value}.+{regex.status_terms.value}.+{regex.order_terms.value}.+{regex.follow_terms.value}.+{regex.time_terms.value}.+{regex.delivery_terms.value})'},
         {'type': 'efficiencyuse 05', 'pattern':fr'({regex.able_terms.value}.+{regex.product_terms.value}.+{regex.future_terms.value}.+{regex.save_terms.value}.+{regex.ease_terms.value})'},
         {'type': 'efficiencyuse 06', 'pattern':fr'({regex.subscription_terms.value}.+{regex.able_terms.value}.+{regex.discount_terms.value}.+{regex.learning_terms.value})'},
         {'type': 'efficiencyuse 07', 'pattern':fr'({regex.language_terms.value}.+{regex.site_terms.value}.+{regex.able_terms.value}.+(({regex.content_terms.value}.+{regex.study_terms.value})|({regex.experience_terms.value}.+{regex.customize_terms.value})|{regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})|({regex.fast_terms.value}|{regex.use_terms.value})))'},
         {'type': 'efficiencyuse 08', 'pattern':fr'({regex.able_terms.value}.+{regex.account_terms.value}.+{regex.access_terms.value}.+{regex.ease_terms.value})'},
         {'type': 'efficiencyuse 09', 'pattern':fr'({regex.able_terms.value}.+{regex.code_terms.value}.+{regex.discount_terms.value}.+{regex.buy_terms.value})'},
         {'type': 'efficiencyuse 10', 'pattern':fr'({regex.able_terms.value}.+{regex.detail_terms.value}.+{regex.product_terms.value}.+{regex.observe_terms.value}.+{regex.decision_terms.value})'},
         {'type': 'efficiencyuse 11', 'pattern':fr'({regex.able_terms.value}.+{regex.experience_terms.value}.+{regex.subscription_terms.value}.+{regex.update_terms.value}?)'},
         {'type': 'efficiencyuse 12', 'pattern':fr'({regex.search_terms.value}.+{regex.filter_terms.value}.+{regex.product_terms.value})'},
         {'type': 'efficiencyuse 13', 'pattern':fr'({regex.size_terms.value}.+{regex.product_terms.value}.+{regex.fast_terms.value}.+{regex.decision_terms.value}.+{regex.buy_terms.value})'},
         {'type': 'efficiencyuse 14', 'pattern':fr'({regex.fast_terms.value}.+{regex.guide_terms.value}.+{regex.product_terms.value}.+{regex.read_terms.value}.+{regex.use_terms.value})'},
         {'type': 'efficiencyuse 15', 'pattern':fr'({regex.notification_terms.value}.+{regex.status_terms.value}.+{regex.order_terms.value}.+{regex.learning_terms.value})'},
         {'type': 'efficiencyuse 16', 'pattern':fr'({regex.search_terms.value}.+{regex.based_terms.value}.+{regex.grading_terms.value}.+{regex.able_terms.value}.+{regex.product_terms.value})'},
         {'type': 'efficiencyuse 17', 'pattern':fr'({regex.product_terms.value}.+{regex.based_terms.value}.+{regex.observe_terms.value}.+{regex.ease_terms.value})'},
         {'type': 'efficiencyuse 18', 'pattern':fr'({regex.code_terms.value}.+{regex.discount_terms.value}.+{regex.buy_terms.value}.+{regex.discount_terms.value})'},
         {'type': 'efficiencyuse 19', 'pattern':fr'({regex.inventory_terms.value}.+{regex.shopping_cart_terms.value}.+{regex.time_terms.value}.+{regex.observe_terms.value}.+{regex.product_terms.value})'},
         {'type': 'efficiencyuse 20', 'pattern':fr'({regex.want_terms.value}.+{regex.invoice_terms.value}.+{regex.buy_terms.value}.+{regex.observe_terms.value}.+{regex.able_terms.value}.+{regex.detail_terms.value}.+{regex.buy_terms.value})'},
         {'type': 'efficiencyuse 21', 'pattern':fr'({regex.want_terms.value}.+({regex.experience_terms.value}|{regex.suggestion_terms.value}).+{regex.buy_terms.value}.+{regex.subscription_terms.value}.+{regex.able_terms.value}.+{regex.learning_terms.value})'},
         {'type': 'efficiencyuse 22', 'pattern':fr'({regex.want_terms.value}.+({regex.experience_terms.value}|{regex.suggestion_terms.value}).+{regex.able_terms.value}.+{regex.experience_terms.value}.+{regex.subscription_terms.value})'},
         {'type': 'efficiencyuse 23', 'pattern':fr'({regex.want_terms.value}.+{regex.submit_terms.value}.+{regex.decision_terms.value}.+{regex.able_terms.value}.+{regex.product_terms.value}.+{regex.time_terms.value}.+{regex.receive_terms.value})'},
         {'type': 'efficiencyuse 24', 'pattern':fr'({regex.want_terms.value}.+{regex.legal_terms.value}.+{regex.fast_terms.value}.+{regex.observe_terms.value}.+{regex.able_terms.value}.+({regex.legal_terms.value}|{regex.task_terms.value}).+{regex.learning_terms.value})'},
         {'type': 'efficiencyuse 25', 'pattern':fr'({regex.want_terms.value}.+{regex.product_terms.value}.+{regex.favourite_terms.value}.+{regex.able_terms.value}.+{regex.ease_terms.value}.+({regex.buy_terms.value}|{regex.access_terms.value}))'},
         {'type': 'efficiencyuse 26', 'pattern':fr'({regex.want_terms.value}.+{regex.notification_terms.value}.+{regex.product_terms.value}.+{regex.able_terms.value}.+{regex.discount_terms.value}.+{regex.buy_terms.value})'},
         {'type': 'efficiencyuse 27', 'pattern':fr'({regex.want_terms.value}.+{regex.product_terms.value}.+{regex.based_terms.value}.+{regex.search_terms.value}.+{regex.able_terms.value}.+{regex.product_terms.value}.+{regex.ease_terms.value}.+{regex.find_terms.value})'},
         {'type': 'efficiencyuse 28', 'pattern':fr'({regex.want_terms.value}.+{regex.content_terms.value}.+{regex.clear_terms.value}.+{regex.able_terms.value}.+{regex.ease_terms.value}.+{regex.use_terms.value})'},
         {'type': 'efficiencyuse 29', 'pattern':fr'({regex.want_terms.value}.+{regex.fast_terms.value}.+{regex.access_terms.value}.+{regex.able_terms.value}.+{regex.time_terms.value}.+{regex.access_terms.value})'},
         {'type': 'efficiencyuse 31', 'pattern':fr'({regex.want_terms.value}.+{regex.content_terms.value}.+{regex.clear_terms.value}.+{regex.able_terms.value}.+{regex.ease_terms.value}.+{regex.use_terms.value})'},
         {'type': 'efficiencyuse 30', 'pattern':fr'({regex.want_terms.value}.+{regex.product_terms.value}.+{regex.based_terms.value}.+{regex.search_terms.value}.+{regex.able_terms.value}.+{regex.product_terms.value}.+{regex.ease_terms.value})'},
         {'type': 'efficiencyuse 32', 'pattern':fr'({regex.want_terms.value}.+{regex.preview_terms.value}.+{regex.Feature_terms.value}.+{regex.able_terms.value}.+{regex.result_terms.value}.+{regex.confident_terms.value})'},
         {'type': 'efficiencyuse 33', 'pattern':fr'({regex.want_terms.value}.+{regex.ui_terms.value}.+({regex.clear_terms.value}|{regex.simple_terms.value}).+{regex.able_terms.value}.+{regex.ease_terms.value}.+{regex.task_terms.value})'},
         {'type': 'efficiencyuse 34', 'pattern':fr'({regex.want_terms.value}.+({regex.search_terms.value}|{regex.filter_terms.value}).+{regex.able_terms.value}.+{regex.result_terms.value}.+{regex.ease_terms.value}.+{regex.find_terms.value})'},
         {'type': 'efficiencyuse 35', 'pattern':fr'({regex.want_terms.value}.+{regex.change_terms.value}.+{regex.terminate_terms.value}.+{regex.able_terms.value}.+{regex.wrong_terms.value}.+{regex.learning_terms.value})'},
         {'type': 'efficiencyuse 36', 'pattern':fr'({regex.want_terms.value}.+{regex.task_terms.value}.+{regex.observe_terms.value}.+{regex.able_terms.value}.+{regex.ease_terms.value}.+{regex.again_terms.value})'},
         {'type': 'efficiencyuse 37', 'pattern':fr'({regex.want_terms.value}.+{regex.task_terms.value}.+{regex.Simultaneously_terms.value}.+{regex.able_terms.value}.+(({regex.fast_terms.value}.+{regex.time_terms.value})|({regex.time_terms.value}.+{regex.fast_terms.value})))'},
        #{'type': 'efficiencyuse 38', 'pattern':fr'({regex.able_terms.value}.+({regex.fast_terms}|{regex.efficiency_terms.value}).+({regex.use_terms.value}|{regex.efficienct_verbs.value}))'}, //bad pattern
         {'type': 'efficiencyuse 39', 'pattern':fr'({regex.want_terms.value}.+{regex.search_terms.value}.+{regex.fast_terms.value}.+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})))'},
         {'type': 'efficiencyuse 40', 'pattern':fr'({regex.want_terms.value}.+{regex.automated_terms.value}.+{regex.save_terms.value}.+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})))'},
         {'type': 'efficiencyuse 41', 'pattern':fr'({regex.want_terms.value}.+{regex.task_terms.value}.+{regex.Simultaneously_terms.value}.+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})))'},
         {'type': 'efficiencyuse 42', 'pattern':fr'({regex.want_terms.value}.+{regex.search_terms.value}.+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})))'},
        #{'type': 'efficiencyuse 43', 'pattern':fr'({regex.want_terms.value}.+{regex.automated_terms.value}.+{regex.able_terms.value}.+({regex.efficiency_terms.value}|{regex.time_terms.value}))'},//bad pattern
         {'type': 'efficiencyuse 44', 'pattern':fr'({regex.want_terms.value}.+{regex.default_terms.value}.+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})))'},
        #{'type': 'efficiencyuse 45', 'pattern':fr'({regex.able_terms.value}.+({regex.efficiency_terms.value}|{regex.time_terms.value}))'} //bad pattern
         {'type': 'efficiencyuse 46', 'pattern':fr'({regex.want_terms.value}.+{regex.click_terms.value}.+{regex.submit_terms.value}.+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})))'},
         {'type': 'efficiencyuse 47', 'pattern':fr'({regex.want_terms.value}.+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})))'},
         {'type': 'efficiencyuse 48', 'pattern':fr'({regex.want_terms.value}.+{regex.shortcut_terms.value}.+{regex.able_terms.value}.+({regex.fast_terms.value}|({regex.time_terms.value}).+{regex.task_terms.value}.+{regex.efficienct_verbs.value}))'},
         {'type': 'efficiencyuse 49', 'pattern':fr'({regex.want_terms.value}.+{regex.event_terms.value}.+({regex.previous_terms.value}|{regex.task_terms.value}).+{regex.observe_terms.value}.+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})|{regex.fast_terms.value}|({regex.ease_terms.value}.+{regex.access_terms.value})))'},
         {'type': 'efficiencyuse 50', 'pattern':fr'({regex.want_terms.value}.+{regex.filter_terms.value}.+{regex.have_terms.value}.+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})|({regex.fast_terms.value}|{regex.use_terms.value})))'},
         {'type': 'efficiencyuse 51', 'pattern':fr'({regex.able_terms.value}.+{regex.task_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})|({regex.fast_terms.value}|{regex.use_terms.value})))'},
         {'type': 'efficiencyuse 52', 'pattern':fr'({regex.want_terms.value}.+(({regex.filter_terms.value}.+{regex.Feature_terms.value})|{regex.search_terms.value}).+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})|({regex.fast_terms.value}|({regex.use_terms.value}|{regex.find_terms.value}))))'},
         {'type': 'efficiencyuse 53', 'pattern':fr'({regex.want_terms.value}.+({regex.ease_terms.value}|{regex.fast_terms.value}|{regex.efficiency_terms}).+{regex.able_terms.value}.+{regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})|({regex.fast_terms.value}|{regex.use_terms.value}))'},
         {'type': 'efficiencyuse 54', 'pattern':fr'({regex.want_terms.value}.+(({regex.ease_terms.value}|{regex.fast_terms.value}|{regex.efficiency_terms})?!.*({regex.learning_terms.value}|{regex.training_terms.value}|{regex.guide_terms.value})).+{regex.able_terms.value}.+({regex.efficiency_terms.value}|({regex.time_terms.value}.+{regex.efficienct_verbs})|({regex.fast_terms.value}|{regex.use_terms.value}))?!.*{regex.learning_terms.value})'},
    ]

    satisfaction_patterns = [
         {'type': 'satisfaction 00', 'pattern':fr'({regex.want_terms.value}.+({regex.review_terms.value}|{regex.grading_terms.value}).+{regex.product_terms.value}.+{regex.able_terms.value}.+{regex.subscription_terms.value})'},
         {'type': 'satisfaction 01', 'pattern':fr'({regex.want_terms.value}.+{regex.support_terms.value}.+{regex.access_terms.value}.+{regex.able_terms.value}.+{regex.experience_terms.value}.+{regex.good_terms.value})'},
         {'type': 'satisfaction 02', 'pattern':fr'({regex.want_terms.value}.+{regex.able_terms.value}.+{regex.satisfaction_terms_pattern.value})'},
    ]

    # lemma_userstory is already a string, no need to join
    
    for p in satisfaction_patterns:
            if re.search(p['pattern'], lemma_userstory):
                arr.append({'type':p['type']})
                print('Nonfunctional user stories are extracted')
                matched = True
                return arr
    if not matched:
        for p in learnability_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append({'type':p['type']})
                print('Nonfunctional user stories are extracted')
                matched = True
                return arr
    if not matched:
        for p in error_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append({'type':p['type']})
                print('Nonfunctional user stories are extracted')
                matched = True
                return arr            
    if not matched:
        for p in efficiencyuse_pattern:
            if re.search(p['pattern'], lemma_userstory):
                arr.append({'type':p['type']})
                print('Nonfunctional user stories are extracted')
                matched = True
                return arr



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

@app.post("/analyze-story", response_model=StoryResponse)
async def analyze_story(story_request: StoryRequest):
    role, capability, objective = userstory_check_first(story_request.story)
    if role and capability and objective:
        role, capability, objective = userstory_check_first(story_request.story)
        informal_normalized_story = informal_normalize(story_request.story)
        normalized_story = normalize(informal_normalized_story)
        tokenized_story = tokenize(normalized_story)
        stopword_story = stopwords(tokenized_story)
        lemmatized_story = lemmatizer(stopword_story)
        nonfunctional_userstory = userstory_nonfunctional(lemmatized_story)
        
        return StoryResponse(
            validity="valid",
            role=role,
            capability=capability,
            goal=objective,
            normalized_story=normalized_story,
            tokenized_story=str(tokenized_story),
            lemmatized_story=lemmatized_story,
            non_functional_requirement=nonfunctional_userstory,
            other_non_functional_requirements="امنیت بالا و رمزنگاری داده‌ها",
        )
    else:
        validity = "invalid"
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
