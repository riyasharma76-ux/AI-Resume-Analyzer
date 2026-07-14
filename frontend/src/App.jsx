import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!file) {
      alert("Please select a PDF resume.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze",
        formData
      );

      setResult(response.data);

    } catch (error) {
      console.log(error);
      alert("Something went wrong!");
    }

    setLoading(false);
  };

  return (
    <div className="container">

      <h1>AI Resume Analyzer</h1>

      <p>Upload your resume and get AI analysis.</p>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={analyzeResume}>
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {result && (
        <div className="result">

          <h2>ATS Score</h2>
          <p>{result.analysis.ats_score}</p>

          <h2>Strengths</h2>
          <ul>
            {result.analysis.strengths.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h2>Weaknesses</h2>
          <ul>
            {result.analysis.weaknesses.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h2>Missing Skills</h2>
          <ul>
            {result.analysis.missing_skills.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h2>Suggestions</h2>
          <ul>
            {result.analysis.suggestions.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h2>Recommended Job Roles</h2>
          <ul>
            {result.analysis.job_roles.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>


        </div>
      )}

    </div>
  );
}

export default App;