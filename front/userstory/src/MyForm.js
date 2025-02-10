import React, { useState } from "react";

function MyForm() {
  // مدیریت داده‌های ورودی با useState
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });

  // تابع تغییر مقدار ورودی‌ها
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  // تابع ارسال فرم
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("اطلاعات ارسال شد:", formData);
    alert("فرم با موفقیت ارسال شد!");
  };

  return (
    <div style={{ maxWidth: "400px", margin: "20px auto", textAlign: "center" }}>
      <h2>فرم تماس</h2>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        <input
          type="text"
          name="name"
          placeholder="نام"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="ایمیل"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <textarea
          name="message"
          placeholder="پیام شما..."
          value={formData.message}
          onChange={handleChange}
          required
        />
        <button type="submit" style={{ backgroundColor: "blue", color: "white", padding: "10px", border: "none" }}>
          ارسال
        </button>
      </form>
    </div>
  );
}

export default MyForm;
