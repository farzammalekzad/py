import React, { useState } from "react";
import StoryForm from "./StoryForm";
import ResponseDisplay from "./ResponseDisplay";
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [responses, setResponses] = useState([]); // ذخیره پاسخ‌های دریافتی از سرور

  // تابع برای اضافه کردن پاسخ جدید به `responses`
  const addResponse = (newResponse) => {
    setResponses([newResponse, ...responses]); // اضافه کردن پاسخ جدید به لیست
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
          <h2>📌 پاسخ‌های دریافتی</h2>
          <ResponseDisplay responses={responses} />
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "1200px",
    margin: "auto",
    padding: "20px",
    direction: "center",
  
  },
  mainContent: {
    display: "flex",
    justifyContent: "space-between",
  },
  rightPanel: {
    width: "50%",
    padding: "20px",
    backgroundColor: "#fff",
    borderRadius: "5px",
    border: "1px solid #ccc",
    order:2,
    textAlign:"right"
  },
  leftPanel: {
    width: "50%",
    padding: "20px",
    backgroundColor: "#f9f9f9",
    borderRadius: "5px",
    border: "1px solid #007bff",
    order:1,
    textAlign:"right",
    direction:"rtl"
  },
  header: {
    backgroundColor: "#007bff",
    color: "white",
    textAlign: "center",
    padding: "15px",
  },
};

export default App;
