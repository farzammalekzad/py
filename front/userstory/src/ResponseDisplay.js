import React from "react";

function ResponseDisplay({ responses }) {
  return (
    <div>
      <h3>📌 پاسخ‌های دریافتی</h3>
      {responses.length > 0 ? (
        responses.map((response, index) => (
          <div key={index} style={styles.responseCard}>
            <p><strong>✅ صحّت داستان:</strong> {response.validity}</p>
            <p><strong>👤 نقش:</strong> {response.role}</p>
            <p><strong>⚡ قابلیت:</strong> {response.capability}</p>
            <p><strong>🎯 هدف:</strong> {response.goal}</p>
            <p><strong>🛠 الزامات غیرعملکردی:</strong> {response.non_functional_requirement}</p>
            <p><strong>🔍 سایر الزامات:</strong> {response.other_non_functional_requirements}</p>
          </div>
        ))
      ) : (
        <p>⏳ هنوز پاسخی دریافت نشده است.</p>
      )}
    </div>
  );
}

const styles = {
  responseCard: {
    marginBottom: "15px",
    padding: "10px",
    backgroundColor: "#e6f7ff",
    borderRadius: "5px",
    border: "1px solid #007bff",
  },
};

export default ResponseDisplay;
