import { useState } from "react";
import { supabase } from "./lib/supabase";

export default function Auth() {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setMessage("");
    setError("");

    try {
      if (mode === "signup") {
        const { data, error: authError } = await supabase.auth.signUp({
          email: email.trim(),
          password,
          options: {
            emailRedirectTo: window.location.origin,
          },
        });

        if (authError) throw authError;

        if (data.session) {
          setMessage("Account created successfully. You are signed in.");
        } else {
          setMessage(
            "Account created. Please check your email and click the verification link before signing in."
          );
        }
      } else {
        const { error: authError } =
          await supabase.auth.signInWithPassword({
            email: email.trim(),
            password,
          });

        if (authError) throw authError;
      }
    } catch (err) {
      setError(err.message || "Authentication failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const switchMode = () => {
    setMode((current) => current === "login" ? "signup" : "login");
    setMessage("");
    setError("");
  };

  return (
    <main style={styles.page}>
      <section style={styles.card}>
        <div style={styles.logo}>CV<span>Mentor</span></div>
        <p style={styles.eyebrow}>AI-POWERED CAREER TOOLS</p>

        <h1 style={styles.heading}>
          {mode === "login" ? "Welcome back" : "Create your account"}
        </h1>

        <p style={styles.subtitle}>
          {mode === "login"
            ? "Sign in to continue optimizing your resume."
            : "Create an account to get started with CV Mentor."}
        </p>

        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label} htmlFor="auth-email">Email address</label>
          <input
            id="auth-email"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@example.com"
            style={styles.input}
          />

          <label style={styles.label} htmlFor="auth-password">Password</label>
          <input
            id="auth-password"
            type="password"
            autoComplete={mode === "login" ? "current-password" : "new-password"}
            minLength={6}
            required
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="At least 6 characters"
            style={styles.input}
          />

          {error && <p role="alert" style={styles.error}>{error}</p>}
          {message && <p role="status" style={styles.message}>{message}</p>}

          <button type="submit" disabled={loading} style={styles.button}>
            {loading
              ? "Please wait..."
              : mode === "login" ? "Sign in" : "Create account"}
          </button>
        </form>

        <p style={styles.switchText}>
          {mode === "login" ? "New to CV Mentor?" : "Already have an account?"}
          {" "}
          <button type="button" onClick={switchMode} style={styles.switchButton}>
            {mode === "login" ? "Create account" : "Sign in"}
          </button>
        </p>

        <p style={styles.footer}>
          Your account is secured by Supabase Authentication.
        </p>
      </section>
    </main>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "grid",
    placeItems: "center",
    padding: "24px",
    background: "radial-gradient(circle at top, #25345b 0%, #101525 48%, #090d17 100%)",
    color: "#f8fafc",
    fontFamily: "Inter, Arial, sans-serif",
  },
  card: {
    width: "100%",
    maxWidth: "440px",
    padding: "38px",
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: "20px",
    background: "rgba(19,27,46,0.94)",
    boxShadow: "0 24px 80px rgba(0,0,0,0.35)",
  },
  logo: {
    fontSize: "27px",
    fontWeight: 800,
    letterSpacing: "-1px",
  },
  eyebrow: {
    marginTop: "9px",
    color: "#8fa8ff",
    fontSize: "11px",
    fontWeight: 700,
    letterSpacing: "2px",
  },
  heading: {
    margin: "30px 0 8px",
    fontSize: "29px",
  },
  subtitle: {
    color: "#aab4c8",
    lineHeight: 1.6,
    marginBottom: "26px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "11px",
  },
  label: {
    color: "#dce4f4",
    fontSize: "13px",
    fontWeight: 600,
    marginTop: "7px",
  },
  input: {
    width: "100%",
    boxSizing: "border-box",
    padding: "14px",
    borderRadius: "9px",
    border: "1px solid #35415b",
    background: "#10182a",
    color: "#ffffff",
    fontSize: "15px",
    outline: "none",
  },
  button: {
    marginTop: "12px",
    padding: "15px",
    border: 0,
    borderRadius: "9px",
    background: "linear-gradient(100deg, #647cff, #8b5cf6)",
    color: "#ffffff",
    fontSize: "15px",
    fontWeight: 700,
    cursor: "pointer",
  },
  error: {
    color: "#ff9c9c",
    background: "rgba(220,38,38,0.12)",
    padding: "10px",
    borderRadius: "8px",
    fontSize: "13px",
  },
  message: {
    color: "#9ee6bd",
    background: "rgba(34,197,94,0.12)",
    padding: "10px",
    borderRadius: "8px",
    fontSize: "13px",
    lineHeight: 1.5,
  },
  switchText: {
    marginTop: "24px",
    color: "#aab4c8",
    textAlign: "center",
    fontSize: "14px",
  },
  switchButton: {
    border: 0,
    background: "none",
    color: "#a5b4fc",
    fontWeight: 700,
    cursor: "pointer",
  },
  footer: {
    marginTop: "28px",
    color: "#77839b",
    fontSize: "11px",
    textAlign: "center",
  },
};
