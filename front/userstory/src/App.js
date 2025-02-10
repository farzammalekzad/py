import React, { useState } from "react";
import StoryForm from "./StoryForm"; // فرم ورود داستان
import ResponseDisplay from "./ResponseDisplay"; // نمایش پاسخ‌ها



function App() {
  const [responses, setResponses] = useState([]); // ذخیره پاسخ‌های دریافتی

  // تابعی که پاسخ جدید را دریافت کرده و به لیست اضافه می‌کند
  const addResponse = (response) => {
    setResponses([...responses, response]);
  };

  return (
    <div style={styles.container}>
      {/* 🔹 اضافه کردن هدر در بالای صفحه */}
      <header style={styles.header}>
        <h1>نرم‌افزار تحلیل داستان کاربری</h1>
        <p>این نرم‌افزار با هدف تحلیل و بررسی داستان‌های کاربری به زبان فارسی طراحی و پیاده‌سازی شده است. نرم‌افزار از کاربر خواسته تا داستان‌های کاربری خود را وارد کند و سپس با پردازش این داده‌ها، اطلاعات مفیدی در مورد بخش‌های مختلف داستان کاربری و الزامات غیرعملکردی آن به کاربر ارائه می‌دهد.

در این نرم‌افزار، برای تحلیل متن علاوه بر استفاده از تکنیک‌های پردازش زبان طبیعی (NLP)، از عبارات منظم (Regular Expressions) نیز بهره گرفته شده است. این تکنیک‌ها به شناسایی الگوهای خاص در متن، استخراج اطلاعات دقیق‌تر و پردازش بهتر داده‌ها کمک می‌کنند. با استفاده از ترکیب این دو روش، نرم‌افزار قادر است به‌طور مؤثری بخش‌های مختلف داستان کاربری را شناسایی کرده و پیشنهاداتی برای بهبود و تکمیل آن‌ها ارائه دهد.

این پروژه مربوط به پایان‌نامه مقطع کارشناسی ارشد اینجانب بوده و هدف آن ارتقاء فرآیند تحلیل و تدوین داستان‌های کاربری در زبان فارسی است. امیدواریم این نرم‌افزار بتواند به توسعه و بهبود کیفیت نرم‌افزارها و سیستم‌های مبتنی بر نیازهای کاربران کمک شایانی نماید.</p>
      </header>

      <div style={styles.mainContent}>
        {/* 🔹 بخش ورود داستان - سمت راست */}
        <div style={styles.rightPanel}>
          <h2>ورود داستان کاربری</h2>
          <StoryForm addResponse={addResponse} />
        </div>

        {/* 🔹 بخش نمایش پاسخ‌ها - سمت چپ */}
        <div style={styles.leftPanel}>
          <h2>پاسخ‌های دریافتی</h2>
          <ResponseDisplay responses={responses} />
        </div>
      </div>
    </div>
  );
}

// استایل‌ها
const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    height: "100vh",
    direction: "rtl", // راست‌چین کردن کل صفحه
  },
  header: {
    backgroundColor: "#007bff",
    color: "white",
    textAlign: "center",
    padding: "15px",
  },
  mainContent: {
    display: "flex",
    flex: 1,
  },
  rightPanel: { // حالا فرم ورود در سمت راست است
    width: "50%",
    padding: "20px",
    backgroundColor: "#f8f9fa",
    textAlign: "right",
    borderLeft: "2px solid #ddd",
  },
  leftPanel: { // حالا پاسخ‌ها در سمت چپ هستند
    width: "50%",
    padding: "20px",
    backgroundColor: "#e3f2fd",
    overflowY: "auto",
    textAlign: "right",
  },
};

export default App;
