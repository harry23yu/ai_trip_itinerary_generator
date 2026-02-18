function QuestionRenderer({ question, formData, handleChange }) {
    const value = formData[question.id] || "";
  
    return (
      <div style={{ marginTop: "20px" }}>
        <p>{question.label}</p>
  
        {/* Multiple Choice */}
        {question.type === "mc" && (
          <select
            value={value}
            onChange={(e) =>
              handleChange(question.id, e.target.value)
            }
          >
            <option value="">Select</option>
            {question.options.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        )}
  
        {/* Open Ended */}
        {question.type === "oe" && (
          <input
            type="text"
            value={value}
            onChange={(e) =>
              handleChange(question.id, e.target.value)
            }
            style={{ width: "400px" }}
          />
        )}
  
        {/* Number */}
        {question.type === "num" && (
          <input
            type="number"
            value={value}
            onChange={(e) =>
              handleChange(question.id, e.target.value)
            }
          />
        )}
  
        {/* Check All That Apply */}
        {question.type === "cata" &&
          question.options.map((option) => (
            <div key={option}>
              <label>
                <input
                  type="checkbox"
                  checked={
                    formData[question.id]?.includes(option) || false
                  }
                  onChange={(e) => {
                    const current = formData[question.id] || [];
  
                    if (e.target.checked) {
                      handleChange(question.id, [
                        ...current,
                        option,
                      ]);
                    } else {
                      handleChange(
                        question.id,
                        current.filter((o) => o !== option)
                      );
                    }
                  }}
                />
                {option}
              </label>
            </div>
          ))}
      </div>
    );
  }
  
  export default QuestionRenderer;  