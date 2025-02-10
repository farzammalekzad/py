import React from "react";

function ResponseDisplay({ responses }) {
  return (
    <div style={styles.container}>
      {responses.length === 0 ? (
        <p style={styles.noResponse}>هیچ پاسخی دریافت نشده است.</p>
      ) : (
        responses.map((response) => (
          <div key={response.id} style={styles.responseItem}>
            {response.text}
          </div>
        ))
      )}
    </div>
  );
}

// استایل‌های کامپوننت
const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  responseItem: {
    backgroundColor: "#e3f2fd",
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #90caf9",
  },
  noResponse: {
    color: "#777",
    fontStyle: "italic",
  },
};

export default ResponseDisplay;
