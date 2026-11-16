import { useState, useEffect } from "react";
import Auth from "./Auth";
import { supabase } from "./lib/supabase";
import "./App.css";

const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

function App() {
  const [session, setSession] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [file, setFile] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");

  const [uploading, setUploading] = useState(false);
  const [optimizing, setOptimizing] = useState(false);

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
    supabase.auth.getSession().then(({ data, error }) => {
      if (error) console.error("Session check failed:", error.message);
      setSession(data?.session ?? null);
      setAuthLoading(false);
    });
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, newSession) => {
      setSession(newSession);
      setAuthLoading(false);
    });
    return () => subscription.unsubscribe();
  }, []);

  // =====================================================
  // FILE SELECTION
  // =====================================================

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) return;

    const extension = selectedFile.name
      .split(".")
      .pop()
      .toLowerCase();

    if (!["pdf", "docx"].includes(extension)) {
      setError("Please upload a PDF or DOCX resume.");
      return;
    }

    setFile(selectedFile);
    setError("");
    setResult(null);
  };

  // =====================================================
  // UPLOAD RESUME
  // =====================================================

  const handleUpload = async () => {
    if (!file) {
      setError("Please select your resume first.");
      return;
    }

    setUploading(true);
    setError("");

    try {
      const formData = new FormData();

      formData.append("file", file);

      const response = await fetch(
        `${API_URL}/upload-resume`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${session.access_token}`,
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Resume upload failed."
        );
      }

      setResumeText(data.resume_text || "");

    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  // =====================================================
  // OPTIMIZE RESUME
  // =====================================================

  const handleOptimize = async () => {
    if (!resumeText) {
      setError("Please upload your resume first.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please paste the job description.");
      return;
    }

    setOptimizing(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `${API_URL}/optimize-resume`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${session.access_token}`,
          },
          body: JSON.stringify({
            resume_text: resumeText,
            job_description: jobDescription,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Resume optimization failed."
        );
      }

      setResult(data);

    } catch (err) {
      setError(err.message);
    } finally {
      setOptimizing(false);
    }
  };

  const handleDownload = async () => {
    if (!result?.download_url || !session?.access_token) {
      setError("Please sign in again before downloading.");
      return;
    }

    try {
      setError("");

      const response = await fetch(
        `${API_URL}${result.download_url}`,
        {
          headers: {
            Authorization: `Bearer ${session.access_token}`,
          },
        }
      );

      if (!response.ok) {
        let message = "Resume download failed.";

        try {
          const data = await response.json();
          message = data.detail || message;
        } catch {
          // Keep the default error message.
        }

        throw new Error(message);
      }

      const blob = await response.blob();

      if (!blob.size) {
        throw new Error("The generated resume file is empty.");
      }

      const objectUrl = URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = objectUrl;
      link.download = "optimized_resume.docx";

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.setTimeout(() => {
        URL.revokeObjectURL(objectUrl);
      }, 1000);

    } catch (err) {
      setError(err.message);
    }
  };
  // =====================================================
  // RESET
  // =====================================================

  const handleReset = () => {
    setFile(null);
    setResumeText("");
    setJobDescription("");
    setResult(null);
    setError("");
  };

  // =====================================================
  // RESULT DATA
  // =====================================================

  const score = Math.round(
    result?.ats_score ?? 0
  );

  const analysis = result?.analysis || {};

  const matchedKeywords =
    analysis.matched_keywords || [];

  const missingKeywords =
    analysis.missing_keywords || [];

  const warnings =
    analysis.warnings || [];

  const rewrittenResume =
    result?.rewritten_resume || {};

  const scoreClass =
    score >= 80
      ? "excellent"
      : score >= 60
        ? "good"
        : "needs-work";

  // =====================================================
  // RENDER
  // =====================================================

  if (authLoading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        Checking your session...
      </div>
    );
  }

  if (!session) {
    return <Auth />;
  }

  return (
    <div className="app">

      {/* Animated background */}

      <div className="background-glow glow-one" />
      <div className="background-glow glow-two" />
      <div className="background-grid" />

      {/* =================================================
          HEADER
      ================================================= */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            AI
          </div>

          <div>
            <div className="logo">
              Resume<span>AI</span>
            </div>

            <div className="brand-subtitle">
              ATS Resume Optimizer
            </div>
          </div>

        </div>

        <div className="header-status">
          <span className="status-dot" />
          AI Engine Online
        </div>

      </header>


      {/* =================================================
          MAIN
      ================================================= */}

      <main className="container">

        {/* =================================================
            HERO
        ================================================= */}

        <section className="hero">

          <div className="hero-badge">
            <span>âœ¦</span>
            AI-POWERED CAREER OPTIMIZATION
          </div>

          <h1>
            Turn Your Resume Into
            <br />

            <span className="gradient-text">
              Your Interview Machine.
            </span>
          </h1>

          <p>
            Upload your resume, add the target job
            description, and let AI analyze and
            optimize your resume for ATS systems.
          </p>

          <div className="hero-features">

            <span>âœ“ ATS Analysis</span>
            <span>âœ“ Keyword Matching</span>
            <span>âœ“ AI Optimization</span>
            <span>âœ“ DOCX Download</span>

          </div>

        </section>


        {/* =================================================
            ERROR
        ================================================= */}

        {error && (

          <div className="error-box">

            <span className="error-icon">
              !
            </span>

            <span>
              {error}
            </span>

            <button
              onClick={() => setError("")}
            >
              Ã—
            </button>

          </div>

        )}


        {/* =================================================
            INPUT SECTION
        ================================================= */}

        <section className="workspace">

          {/* RESUME */}

          <div className="glass-card">

            <div className="card-header">

              <div className="step-number">
                01
              </div>

              <div>
                <h2>
                  Upload Resume
                </h2>

                <p>
                  Your current resume
                </p>
              </div>

            </div>


            <label
              className={`drop-zone ${
                file ? "has-file" : ""
              }`}
            >

              <input
                type="file"
                accept=".pdf,.docx"
                onChange={handleFileChange}
              />

              <div className="upload-icon">
                {file ? "âœ“" : "â†‘"}
              </div>

              {!file ? (
                <>
                  <strong>
                    Drop your resume here
                  </strong>

                  <span>
                    or click to browse
                  </span>

                  <small>
                    PDF or DOCX â€¢ Maximum 10 MB
                  </small>
                </>
              ) : (
                <>
                  <strong>
                    {file.name}
                  </strong>

                  <span>
                    {(file.size / 1024 / 1024).toFixed(2)}
                    {" "}MB
                  </span>
                </>
              )}

            </label>


            <button
              className="secondary-button"
              onClick={handleUpload}
              disabled={!file || uploading}
            >

              {uploading ? (
                <>
                  <span className="spinner" />
                  Extracting Resume...
                </>
              ) : (
                <>
                  Extract Resume
                  <span>â†’</span>
                </>
              )}

            </button>


            {resumeText && (

              <div className="success-box">

                <div className="success-check">
                  âœ“
                </div>

                <div>
                  <strong>
                    Resume Ready
                  </strong>

                  <span>
                    {resumeText.length.toLocaleString()}
                    {" "}characters extracted
                  </span>
                </div>

              </div>

            )}

          </div>


          {/* JOB DESCRIPTION */}

          <div className="glass-card">

            <div className="card-header">

              <div className="step-number">
                02
              </div>

              <div>
                <h2>
                  Target Job
                </h2>

                <p>
                  Job description
                </p>
              </div>

            </div>


            <div className="textarea-wrapper">

              <textarea
                className="jd-input"
                placeholder={
                  "Paste the complete job description here...\n\n" +
                  "Example:\n" +
                  "We are looking for a DevOps Engineer..."
                }
                value={jobDescription}
                onChange={(event) =>
                  setJobDescription(
                    event.target.value
                  )
                }
              />

              <div className="textarea-footer">

                <span>
                  AI will identify relevant keywords
                </span>

                <span>
                  {jobDescription.length.toLocaleString()}
                  {" "}characters
                </span>

              </div>

            </div>

          </div>

        </section>


        {/* =================================================
            OPTIMIZE BUTTON
        ================================================= */}

        <section className="action-section">

          <div className="action-line" />

          <button
            className="optimize-button"
            onClick={handleOptimize}
            disabled={
              optimizing ||
              !resumeText ||
              !jobDescription.trim()
            }
          >

            {optimizing ? (
              <>
                <span className="button-spinner" />

                <span>
                  AI IS ANALYZING YOUR RESUME...
                </span>
              </>
            ) : (
              <>
                <span className="sparkle">
                  âœ¦
                </span>

                <span>
                  OPTIMIZE MY RESUME
                </span>

                <span className="button-arrow">
                  â†’
                </span>
              </>
            )}

          </button>

          <div className="action-line" />

        </section>


        {/* =================================================
            PROCESSING
        ================================================= */}

        {optimizing && (

          <div className="processing-card">

            <div className="processing-orb">
              <div />
            </div>

            <div>

              <strong>
                AI is working on your resume
              </strong>

              <p>
                Analyzing keywords, matching skills,
                and generating an optimized version.
              </p>

            </div>

          </div>

        )}


        {/* =================================================
            RESULTS
        ================================================= */}

        {result && (

          <section className="results">

            <div className="results-heading">

              <div>
                <div className="hero-badge">
                  âœ¦ ANALYSIS COMPLETE
                </div>

                <h2>
                  Your Resume
                  <span className="gradient-text">
                    {" "}Scorecard
                  </span>
                </h2>

                <p>
                  Here's how well your resume matches
                  the target job.
                </p>
              </div>

              {result.download_url && (

                <button
                  type="button"
                  className="download-button"
                  onClick={handleDownload}
                >
                  <span>↓</span>
                  Download Optimized Resume
                </button>

              )}

            </div>


            {/* SCORE */}

            <div className="score-dashboard">

              <div className="score-panel">

                <div className="score-ring">

                  <svg
                    viewBox="0 0 160 160"
                  >

                    <circle
                      className="score-track"
                      cx="80"
                      cy="80"
                      r="68"
                    />

                    <circle
                      className={`score-progress ${scoreClass}`}
                      cx="80"
                      cy="80"
                      r="68"
                      style={{
                        strokeDashoffset:
                          427 -
                          (427 * score) / 100,
                      }}
                    />

                  </svg>

                  <div className="score-center">

                    <strong>
                      {score}
                    </strong>

                    <span>
                      / 100
                    </span>

                  </div>

                </div>

                <div className="score-title">
                  ATS Compatibility
                </div>

                <div className={`score-status ${scoreClass}`}>
                  {score >= 80
                    ? "Excellent Match"
                    : score >= 60
                      ? "Good Match"
                      : "Needs Improvement"}
                </div>

              </div>


              <div className="score-details">

                <div className="metric">

                  <div className="metric-icon">
                    âœ“
                  </div>

                  <div>
                    <span>
                      Matched Keywords
                    </span>

                    <strong>
                      {matchedKeywords.length}
                    </strong>
                  </div>

                </div>


                <div className="metric">

                  <div className="metric-icon warning">
                    !
                  </div>

                  <div>
                    <span>
                      Missing Keywords
                    </span>

                    <strong>
                      {missingKeywords.length}
                    </strong>
                  </div>

                </div>


                <div className="metric">

                  <div className="metric-icon purple">
                    AI
                  </div>

                  <div>
                    <span>
                      Optimization
                    </span>

                    <strong>
                      Complete
                    </strong>
                  </div>

                </div>

              </div>

            </div>


            {/* KEYWORDS */}

            <div className="analysis-grid">

              <div className="result-card">

                <div className="result-card-title">

                  <div className="result-icon matched-icon">
                    âœ“
                  </div>

                  <div>
                    <h3>
                      Matched Keywords
                    </h3>

                    <p>
                      Skills already present in your resume
                    </p>
                  </div>

                </div>


                <div className="keyword-list">

                  {matchedKeywords.length > 0 ? (
                    matchedKeywords.map(
                      (keyword, index) => (

                        <span
                          className="keyword matched-keyword"
                          key={`${keyword}-${index}`}
                        >
                          âœ“ {keyword}
                        </span>

                      )
                    )
                  ) : (
                    <span className="empty-state">
                      No matched keywords found.
                    </span>
                  )}

                </div>

              </div>


              <div className="result-card">

                <div className="result-card-title">

                  <div className="result-icon missing-icon">
                    !
                  </div>

                  <div>
                    <h3>
                      Missing Keywords
                    </h3>

                    <p>
                      Important terms missing from your resume
                    </p>
                  </div>

                </div>


                <div className="keyword-list">

                  {missingKeywords.length > 0 ? (
                    missingKeywords.map(
                      (keyword, index) => (

                        <span
                          className="keyword missing-keyword"
                          key={`${keyword}-${index}`}
                        >
                          + {keyword}
                        </span>

                      )
                    )
                  ) : (
                    <span className="empty-state">
                      No missing keywords found.
                    </span>
                  )}

                </div>

              </div>

            </div>


            {/* ASSESSMENT */}

            {analysis.overall_assessment && (

              <div className="assessment-card">

                <div className="assessment-icon">
                  âœ¦
                </div>

                <div>

                  <div className="section-label">
                    AI ASSESSMENT
                  </div>

                  <p>
                    {analysis.overall_assessment}
                  </p>

                </div>

              </div>

            )}


            {/* WARNINGS */}

            {warnings.length > 0 && (

              <div className="warnings-card">

                <div className="section-label">
                  âš  WARNINGS
                </div>

                {warnings.map(
                  (warning, index) => (

                    <div
                      className="warning-item"
                      key={index}
                    >
                      <span>!</span>
                      {warning}
                    </div>

                  )
                )}

              </div>

            )}


            {/* OPTIMIZED RESUME */}

            <div className="resume-preview">

              <div className="preview-header">

                <div>

                  <div className="section-label">
                    AI OPTIMIZED RESUME
                  </div>

                  <h2>
                    Optimized Resume Preview
                  </h2>

                </div>

                {result.download_url && (

                  <button
                    type="button"
                    className="small-download"
                    onClick={handleDownload}
                  >
                    ↓ Download DOCX
                  </button>

                )}

              </div>


              <div className="resume-document">

                {rewrittenResume.name && (
                  <h1>
                    {rewrittenResume.name}
                  </h1>
                )}

                {rewrittenResume.contact && (

                  <div className="resume-contact">

                    {Object.values(
                      rewrittenResume.contact
                    )
                      .filter(Boolean)
                      .join(" â€¢ ")}

                  </div>

                )}


                {rewrittenResume.summary && (

                  <ResumeSection
                    title="Summary"
                  >
                    <p>
                      {rewrittenResume.summary}
                    </p>
                  </ResumeSection>

                )}


                {Array.isArray(
                  rewrittenResume.skills
                ) && rewrittenResume.skills.length > 0 && (

                  <ResumeSection title="Skills">

                    {rewrittenResume.skills.map(
                      (group, index) => (

                        <div
                          className="resume-skill-group"
                          key={index}
                        >

                          <strong>
                            {group.category}
                          </strong>

                          <span>
                            {Array.isArray(group.skills)
                              ? group.skills.join(", ")
                              : ""}
                          </span>

                        </div>

                      )
                    )}

                  </ResumeSection>

                )}


                {Array.isArray(
                  rewrittenResume.experience
                ) &&
                  rewrittenResume.experience.length > 0 && (

                  <ResumeSection title="Professional Experience">

                    {rewrittenResume.experience.map(
                      (job, index) => (

                        <div
                          className="resume-job"
                          key={index}
                        >

                          <div className="resume-job-header">

                            <strong>
                              {job.title}
                            </strong>

                            <span>
                              {job.company}
                            </span>

                          </div>

                          <div className="resume-meta">
                            {job.location}
                            {job.location && job.dates
                              ? " â€¢ "
                              : ""}
                            {job.dates}
                          </div>

                          {Array.isArray(job.bullets) && (

                            <ul>

                              {job.bullets.map(
                                (bullet, bulletIndex) => (

                                  <li
                                    key={bulletIndex}
                                  >
                                    {bullet}
                                  </li>

                                )
                              )}

                            </ul>

                          )}

                        </div>

                      )
                    )}

                  </ResumeSection>

                )}


                {Array.isArray(
                  rewrittenResume.certifications
                ) &&
                  rewrittenResume.certifications.length > 0 && (

                  <ResumeSection title="Certifications">

                    <ul>

                      {rewrittenResume.certifications.map(
                        (item, index) => (
                          <li key={index}>
                            {item}
                          </li>
                        )
                      )}

                    </ul>

                  </ResumeSection>

                )}


                {Array.isArray(
                  rewrittenResume.education
                ) &&
                  rewrittenResume.education.length > 0 && (

                  <ResumeSection title="Education">

                    <ul>

                      {rewrittenResume.education.map(
                        (item, index) => (

                          <li key={index}>

                            {typeof item === "string"
                              ? item
                              : `${item.degree || ""}${
                                  item.institution
                                    ? ` â€¢ ${item.institution}`
                                    : ""
                                }${
                                  item.details
                                    ? ` â€¢ ${item.details}`
                                    : ""
                                }`}

                          </li>

                        )
                      )}

                    </ul>

                  </ResumeSection>

                )}

              </div>

            </div>


            <button
              className="reset-button"
              onClick={handleReset}
            >
              â† Analyze Another Resume
            </button>

          </section>

        )}

      </main>


      {/* =================================================
          FOOTER
      ================================================= */}

      <footer>

        <div className="footer-logo">
          Resume<span>AI</span>
        </div>

        <p>
          AI-powered resume optimization for
          modern job seekers.
        </p>

        <span>
          Built for better career opportunities.
        </span>

      </footer>

    </div>
  );
}


// =========================================================
// RESUME SECTION COMPONENT
// =========================================================

function ResumeSection({ title, children }) {
  return (
    <section className="resume-section">

      <h3>
        {title}
      </h3>

      {children}

    </section>
  );
}


export default App;








