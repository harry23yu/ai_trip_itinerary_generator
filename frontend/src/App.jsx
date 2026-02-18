import { useState } from "react";

function App() {
  const [step, setStep] = useState("mode");
  const [mode, setMode] = useState(null);
  const [formData, setFormData] = useState({});

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h1>AI Trip Itinerary Generator</h1>

      {/* ===================== */}
      {/* STEP 1 — MODE SELECT  */}
      {/* ===================== */}
      {step === "mode" && (
        <div style={{ marginTop: "30px" }}>
          <h2>How would you like to plan your trip?</h2>

          <div style={{ marginTop: "20px" }}>
            <button
              style={{ marginRight: "20px", padding: "10px 20px" }}
              onClick={() => {
                setMode("A");
                setStep("required");
              }}
            >
              Option A — I don't know where I want to go
            </button>

            <button
              style={{ padding: "10px 20px" }}
              onClick={() => {
                setMode("B");
                setStep("required");
              }}
            >
              Option B — I already know my destination
            </button>
          </div>
        </div>
      )}

      {/* ===================== */}
      {/* STEP 2 — REQUIRED     */}
      {/* ===================== */}
      {step === "required" && (
        <div style={{ marginTop: "40px" }}>
          <h2>Required Questions (Option {mode})</h2>

          {/* ===== OPTION A REQUIRED SAMPLE ===== */}
          {mode === "A" && (
            <>
              <div style={{ marginTop: "20px" }}>
                <p>How many people are planning to go?</p>
                <select
                  onChange={(e) =>
                    handleChange("people", e.target.value)
                  }
                >
                  <option value="">Select</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3-4">3-4</option>
                  <option value="5-6">5-6</option>
                </select>
              </div>

              <div style={{ marginTop: "20px" }}>
                <p>Where are you currently?</p>
                <input
                  type="text"
                  placeholder="City, Country"
                  onChange={(e) =>
                    handleChange("origin_location", e.target.value)
                  }
                />
              </div>
            </>
          )}

          {/* ===== OPTION B REQUIRED SAMPLE ===== */}
          {mode === "B" && (
            <>
              <div style={{ marginTop: "20px" }}>
                <p>Where is your trip?</p>
                <input
                  type="text"
                  placeholder="City or area"
                  onChange={(e) =>
                    handleChange("destination", e.target.value)
                  }
                />
              </div>

              <div style={{ marginTop: "20px" }}>
                <p>How many people are going?</p>
                <select
                  onChange={(e) =>
                    handleChange("people_b", e.target.value)
                  }
                >
                  <option value="">Select</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3-4">3-4</option>
                  <option value="5-6">5-6</option>
                </select>
              </div>
            </>
          )}

          <div style={{ marginTop: "40px" }}>
            <button
              onClick={() => {
                console.log("Form Data:", formData);
                setStep("optional");
              }}
              style={{ padding: "10px 20px" }}
            >
              Continue to Optional Questions
            </button>
          </div>
        </div>
      )}

      {/* TEMP OPTIONAL SCREEN */}
      {step === "optional" && (
        <div style={{ marginTop: "40px" }}>
          <h2>Optional Questions Coming Next</h2>
        </div>
      )}
    </div>
  );
}

export default App;