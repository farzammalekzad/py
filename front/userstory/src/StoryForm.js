import React, { useState } from "react";
import "./StoryForm.css";


function StoryForm({ addResponse }) {
  const [story, setStory] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (event) => {
    setStory(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!story.trim()) {
      setError("⚠ لطفاً یک داستان وارد کنید.");
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze-story", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ story }),
      });

      if (!response.ok) {
        throw new Error("❌ مشکلی در دریافت پاسخ از سرور رخ داده است.");
      }

      const data = await response.json();
      addResponse(data); // ✅ ارسال پاسخ به `App.js`
      setStory(""); // پاک کردن فیلد پس از ارسال موفقیت‌آمیز
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h3>📩 ارسال داستان کاربری</h3>
      <form onSubmit={handleSubmit} style={styles.form}>
        <textarea
          value={story}
          onChange={handleChange}
          placeholder="✍ لطفاً داستان کاربری خود را اینجا بنویسید..."
          rows="5"
          style={styles.textarea}
        />
        <button type="submit" style={styles.button} disabled={loading}>
          {loading ? "⏳ در حال ارسال..." : "🚀 ارسال"}
        </button>
      </form>

      {/* نمایش پیام خطا در صورت وجود */}
      {error && <p style={styles.error}>{error}</p>}
    </div>
  );
}

// 📌 استایل‌های جذاب برای فرم
const styles = {
  container: {
    width: "100%",
    maxWidth: "500px",
    padding: "20px",
    backgroundColor: "#ffffff",
    borderRadius: "10px",
    border: "1px solid #ddd",
    boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
    textAlign: "center",
    transition: "all 0.3s ease-in-out",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  textarea: {
    width: "100%",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #ccc",
    fontSize: "16px",
    transition: "border 0.3s ease-in-out",
    outline: "none",
    resize: "none",
  },
  button: {
    backgroundColor: "#007bff",
    color: "white",
    padding: "12px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "16px",
    fontWeight: "bold",
    transition: "background 0.3s ease-in-out",
  },
  buttonHover: {
    backgroundColor: "#0056b3",
  },
  error: {
    color: "red",
    fontSize: "14px",
    marginTop: "10px",
  },
};

export default StoryForm;
