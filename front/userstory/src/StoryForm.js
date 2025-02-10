import React, { useState } from "react";

function StoryForm() {
  const [story, setStory] = useState(""); // داستان کاربری
  const [file, setFile] = useState(null); // فایل انتخاب شده
  const [loading, setLoading] = useState(false); // وضعیت بارگذاری
  const [error, setError] = useState(""); // مدیریت خطا
  const [responses, setResponses] = useState([]); // ذخیره پاسخ‌های دریافتی

  // مدیریت تغییرات در فیلد ورودی داستان
  const handleStoryChange = (event) => {
    setStory(event.target.value);
  };

  // مدیریت تغییرات در فیلد انتخاب فایل
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // ارسال داستان
  const handleSubmitStory = (event) => {
    event.preventDefault();

    // بررسی که فقط داستان وارد شده باشد
    if (!story.trim()) {
      setError("لطفاً یک داستان وارد کنید.");
      return;
    }

    setError(""); // پاک کردن خطای قبلی
    setLoading(true); // شروع بارگذاری

    // شبیه‌سازی ارسال به سرور
    setTimeout(() => {
      const fakeResponse = {
        id: Date.now(),
        validity: "صحیح",
        role: "مدیر محصول",
        capability: "ثبت مشخصات محصول",
        goal: "بهبود روند ثبت محصولات",
        normalizedStory: "داستان کاربری نرمالیزه شده",
        tokenizedStory: "داستان توکن شده",
        lemmatizedStory: "داستان لمتایز شده",
        nonFunctionalRequirement: "الزامات غیرعملکردی: سرعت بارگذاری صفحه",
        otherNonFunctionalRequirements: "الزامات امنیتی: رمزنگاری داده‌ها",
      };

      // اضافه کردن پاسخ به لیست پاسخ‌ها
      setResponses([fakeResponse, ...responses]);
      setLoading(false); // پایان بارگذاری
      setStory(""); // پاک کردن ورودی داستان
    }, 2000); // شبیه‌سازی تاخیر 2 ثانیه‌ای
  };

  // ارسال فایل
  const handleSubmitFile = (event) => {
    event.preventDefault();

    // بررسی که فقط فایل انتخاب شده باشد
    if (!file) {
      setError("لطفاً یک فایل انتخاب کنید.");
      return;
    }

    setError(""); // پاک کردن خطای قبلی
    setLoading(true); // شروع بارگذاری

    // شبیه‌سازی ارسال به سرور
    setTimeout(() => {
      const fakeResponse = {
        id: Date.now(),
        validity: "صحیح",
        role: "مدیر محصول",
        capability: "بارگذاری فایل",
        goal: "مدیریت فایل‌ها",
        normalizedStory: "فایل نرمالیزه شده",
        tokenizedStory: "فایل توکن شده",
        lemmatizedStory: "فایل لمتایز شده",
        nonFunctionalRequirement: "الزامات غیرعملکردی: حجم فایل",
        otherNonFunctionalRequirements: "الزامات امنیتی: رمزنگاری فایل",
      };

      // اضافه کردن پاسخ به لیست پاسخ‌ها
      setResponses([fakeResponse, ...responses]);
      setLoading(false); // پایان بارگذاری
      setFile(null); // پاک کردن فایل انتخاب شده
    }, 2000); // شبیه‌سازی تاخیر 2 ثانیه‌ای
  };

  return (
    <div>
      <form style={styles.form}>
        {/* بخش ارسال داستان */}
        <div style={styles.storySection}>
          <h3>ارسال داستان کاربری</h3>
          <textarea
            value={story}
            onChange={handleStoryChange}
            placeholder="داستان کاربری خود را بنویسید..."
            rows="5"
            style={styles.textarea}
          />
          <button
            type="button"
            onClick={handleSubmitStory}
            style={styles.button}
          >
            ارسال داستان
          </button>
        </div>

        {/* بخش ارسال فایل */}
        <div style={styles.fileSection}>
          <h3>ارسال فایل</h3>
          <p style={styles.instructions}>
            لطفاً فایل خود را انتخاب کرده و ارسال کنید. فقط فایل‌های متنی یا تصویری قابل قبول هستند.
          </p>
          <input
            type="file"
            onChange={handleFileChange}
            style={styles.input}
          />
          <button
            type="button"
            onClick={handleSubmitFile}
            style={styles.button}
          >
            ارسال فایل
          </button>
        </div>

        {/* نمایش خطا */}
        {error && <div style={styles.error}>{error}</div>}

        {/* نمایش اسپینر در هنگام بارگذاری */}
        {loading && (
          <div style={styles.spinner}>
            <div className="spinner-border" role="status">
              <span className="sr-only">در حال بارگذاری...</span>
            </div>
          </div>
        )}
      </form>

      {/* نمایش پاسخ‌های دریافتی از سرور */}
      <div style={styles.responses}>
        {responses.length > 0 && (
          <div style={styles.responseSection}>
            <h3>پاسخ‌های دریافتی</h3>
            {responses.map((response) => (
              <div key={response.id} style={styles.responseCard}>
                <p><strong>صحّت داستان:</strong> {response.validity}</p>
                <p><strong>نقش:</strong> {response.role}</p>
                <p><strong>قابلیت:</strong> {response.capability}</p>
                <p><strong>هدف:</strong> {response.goal}</p>
                <p><strong>داستان کاربری نرمالیزه:</strong> {response.normalizedStory}</p>
                <p><strong>داستان کاربری توکن شده:</strong> {response.tokenizedStory}</p>
                <p><strong>داستان کاربری لمتایز شده:</strong> {response.lemmatizedStory}</p>
                <p><strong>الزامات غیرعملکردی مرتبط:</strong> {response.nonFunctionalRequirement}</p>
                <p><strong>سایر الزامات غیرعملکردی مرتبط:</strong> {response.otherNonFunctionalRequirements}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// استایل‌های کامپوننت
const styles = {
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
    padding: "20px",
  },
  storySection: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  fileSection: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  textarea: {
    width: "100%",
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    fontSize: "16px",
  },
  input: {
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ccc",
  },
  button: {
    backgroundColor: "blue",
    color: "white",
    padding: "10px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  instructions: {
    fontSize: "14px",
    color: "#555",
  },
  error: {
    color: "red",
    fontSize: "14px",
    marginTop: "10px",
  },
  spinner: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    marginTop: "10px",
  },
  responses: {
    marginTop: "30px",
  },
  responseSection: {
    backgroundColor: "#f9f9f9",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
  },
  responseCard: {
    marginBottom: "15px",
    fontSize: "16px",
  },
};

export default StoryForm;
