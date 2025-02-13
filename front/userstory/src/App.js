import React, { useState } from "react";
import StoryForm from "./StoryForm";
import ResponseDisplay from "./ResponseDisplay";

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
        <p>این نرم‌افزار با هدف تحلیل و بررسی داستان‌های کاربری به زبان فارسی طراحی و پیاده‌سازی شده است...</p>
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
    width: "45%",
    padding: "20px",
    backgroundColor: "#fff",
    borderRadius: "5px",
    border: "1px solid #ccc",
    order:2,
    textAlign:"right"
  },
  leftPanel: {
    width: "45%",
    padding: "20px",
    backgroundColor: "#f9f9f9",
    borderRadius: "5px",
    border: "1px solid #007bff",
    order:1,
    textAlign:"right"
  },
  header: {
    marginBottom: "20px",
    padding: "20px",
    backgroundColor: "#007bff",
    borderRadius: "5px",
    color: "#fff",
    textAlign: "center",
  },
};

export default App;
