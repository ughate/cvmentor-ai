import json
import re

from app.llm_service import ask_llm


def optimize_resume(resume_text: str, job_description: str) -> dict:
    """
    Optimize a resume against a job description using Ollama.

    Safety rules:
    - Never invent experience.
    - Never invent skills or technologies.
    - Never invent employers, titles, dates, projects, certifications,
      achievements, metrics, percentages, server counts, or responsibilities.
    - Preserve factual information from the original resume.
    - Improve wording and ATS alignment only where supported by the resume.
    """

    prompt = f"""
You are an expert ATS resume consultant, technical recruiter,
and professional resume writer.

Your task is to rewrite and optimize the candidate's resume
for the provided job description.

============================================================
CRITICAL FACTUAL ACCURACY RULES
============================================================

The original resume is the ONLY source of truth about the candidate.

You MUST follow these rules:

1. NEVER invent experience.

2. NEVER invent a technology.

3. NEVER invent a skill.

4. NEVER invent a certification.

5. NEVER invent an employer.

6. NEVER invent a job title.

7. NEVER invent employment dates.

8. NEVER invent education.

9. NEVER invent projects.

10. NEVER invent achievements.

11. NEVER invent responsibilities.

12. NEVER invent metrics.

13. NEVER invent percentages.

14. NEVER invent numbers.

15. NEVER invent server counts.

16. NEVER invent cost savings.

17. NEVER invent performance improvements.

18. NEVER invent uptime numbers.

19. NEVER invent business impact.

20. NEVER convert a generic responsibility into a measurable
    achievement unless the original resume already contains
    the measurement.

21. If a metric exists in the original resume, you MAY preserve it.

22. If a metric does NOT exist in the original resume,
    DO NOT create one.

23. Do not assume that knowledge of one technology means
    experience with another technology.

24. If Jenkins is in the JD but not the resume, do NOT add Jenkins.

25. If Helm is in the JD but not the resume, do NOT add Helm.

26. If a JD keyword is missing from the resume, keep it in
    missing_keywords instead of adding it to the rewritten resume.

27. You MAY use standard ATS terminology when it accurately
    describes something already present in the resume.

28. You MAY reorganize existing skills into clearer categories.

29. You MAY improve grammar and professional wording.

30. You MAY combine closely related existing technologies.

31. You MAY explicitly mention a concept when the resume clearly
    demonstrates that concept.

    Example:
    If the resume clearly describes Terraform used for infrastructure
    provisioning, "Infrastructure as Code" can be used.

32. Do NOT claim that the candidate used a tool merely because
    another related tool is present.

33. Do NOT change the candidate's career history.

34. Preserve all employers, job titles, dates, locations,
    certifications, education, and achievements supported by
    the original resume.

============================================================
ATS OPTIMIZATION RULES
============================================================

Optimize for:

- ATS keyword matching
- Clear section headings
- Standard professional terminology
- Simple readable formatting
- Strong action verbs
- Relevant technical skills
- Job-description alignment
- Accurate keyword placement
- Recruiter readability

Avoid:

- Tables
- Columns
- Graphics
- Icons
- Excessive special characters
- Keyword stuffing
- Fake experience
- Fake metrics
- Fake achievements
- Unsupported technologies

============================================================
CONTACT INFORMATION
============================================================

Preserve contact information from the original resume.

If available, include:

- Name
- Phone
- Email
- LinkedIn
- Portfolio
- Location

Do NOT invent missing contact information.

============================================================
RESUME SECTIONS
============================================================

The rewritten resume should preserve these sections when
information exists in the original resume:

1. Name
2. Contact
3. Summary
4. Skills
5. Professional Experience
6. Certifications
7. Education
8. Achievements

Do NOT leave a section empty if the original resume contains
information for that section.

============================================================
SUMMARY
============================================================

Rewrite the summary using ONLY information supported by
the original resume.

Make it:

- ATS-friendly
- concise
- technically relevant
- professional
- aligned with the JD

Do not introduce new technologies or achievements.

============================================================
SKILLS
============================================================

Create clear ATS-friendly skill categories using technologies
already present in the resume.

For example:

Cloud:
AWS, Azure, OCI

Infrastructure as Code:
Terraform

Containers:
Docker, Kubernetes, Amazon EKS

CI/CD:
GitHub Actions

Monitoring and Observability:
Prometheus, Grafana, OpenTelemetry

Scripting:
Python, Shell

Do NOT add a technology simply because it appears in the JD.

============================================================
EXPERIENCE
============================================================

Rewrite existing experience bullets to make them:

- concise
- technically clear
- achievement-oriented when the original supports it
- ATS-friendly

IMPORTANT:

If the original says:

"Developed Python and Shell scripts to automate recurring tasks,
eliminating manual toil and boosting operational efficiency by 20%."

You may preserve the 20%.

But you MUST NOT change it to:

"Improved operational efficiency by 40%."

Do not invent a new number.

If the original does not contain a metric, simply improve the wording
without adding a metric.

============================================================
CERTIFICATIONS
============================================================

Preserve certifications exactly as supported by the resume.

Do not add certifications from the JD.

============================================================
EDUCATION
============================================================

Preserve the candidate's education exactly as supported by
the original resume.

Do not move employment information into the education section.

============================================================
ACHIEVEMENTS
============================================================

Preserve achievements supported by the original resume.

Improve wording if necessary, but do not create new achievements.

============================================================
ATS KEYWORDS
============================================================

For matched keywords:

Only include keywords clearly supported by the resume.

For missing keywords:

Only include important JD keywords that are NOT supported
by the resume.

For keyword recommendations:

Explain how an existing skill or experience can be presented
more clearly.

Do NOT recommend falsely adding a technology.

============================================================
WARNINGS
============================================================

Identify:

- unsupported JD technologies
- potential credibility problems
- duplicate information
- unclear dates
- ATS formatting risks
- missing information

============================================================
JOB DESCRIPTION
============================================================

{job_description}

============================================================
ORIGINAL RESUME
============================================================

{resume_text}

============================================================
OUTPUT
============================================================

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "ats_score": 0,
    "overall_assessment": "",
    "matched_keywords": [],
    "missing_keywords": [],
    "strong_keywords": [],
    "keyword_recommendations": [],
    "summary_recommendation": "",
    "skills_recommendations": [],
    "experience_recommendations": [],
    "formatting_recommendations": [],
    "warnings": [],

    "rewritten_resume": {{
        "name": "",
        "contact": {{
            "location": "",
            "phone": "",
            "email": "",
            "linkedin": "",
            "portfolio": ""
        }},
        "summary": "",
        "skills": [],
        "experience": [],
        "certifications": [],
        "education": [],
        "achievements": []
    }}
}}

============================================================
ATS SCORE
============================================================

Calculate the ATS score based on:

- keyword relevance
- technical skill match
- responsibility match
- experience relevance
- terminology alignment

Do NOT artificially increase the score.

Score ranges:

90-100 = Excellent match
80-89 = Very strong match
70-79 = Good match
60-69 = Moderate match
Below 60 = Significant optimization needed

============================================================
EXPERIENCE FORMAT
============================================================

Each experience item must use:

{{
    "company": "",
    "title": "",
    "location": "",
    "dates": "",
    "bullets": []
}}

Preserve the original career history.

============================================================
SKILLS FORMAT
============================================================

Each skill item must use:

{{
    "category": "",
    "skills": []
}}

Only use technologies and skills supported by the original resume.

============================================================
FINAL SAFETY CHECK
============================================================

Before returning the JSON, internally verify:

- Did I invent any technology?
- Did I invent any employer?
- Did I invent any job title?
- Did I invent any date?
- Did I invent any certification?
- Did I invent any project?
- Did I invent any achievement?
- Did I invent any percentage?
- Did I invent any number?
- Did I invent any server count?
- Did I invent any performance improvement?
- Did I invent any business impact?

If YES to any of these, remove the invented information.

Return JSON only.
"""

    response = ask_llm(prompt)

    return _parse_llm_response(response)


def _parse_llm_response(response: str) -> dict:
    """
    Parse JSON returned by Ollama.

    Handles:
    - normal JSON
    - JSON inside markdown code fences
    - accidental text before/after JSON
    """

    if not response:
        raise ValueError("Ollama returned an empty response.")

    response = response.strip()

    # Remove markdown code fences.
    response = re.sub(
        r"^```(?:json)?\s*",
        "",
        response,
        flags=re.IGNORECASE
    )

    response = re.sub(
        r"\s*```$",
        "",
        response
    )

    response = response.strip()

    # First attempt: parse entire response.
    try:
        result = json.loads(response)
        return _validate_result(result)
    except json.JSONDecodeError:
        pass

    # Second attempt: locate JSON object.
    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "Ollama returned an invalid JSON response."
        )

    json_text = response[start:end + 1]

    try:
        result = json.loads(json_text)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Could not parse Ollama response as JSON: {exc}"
        )

    return _validate_result(result)


def _validate_result(result: dict) -> dict:
    """
    Validate and normalize the LLM response.
    """

    if not isinstance(result, dict):
        raise ValueError(
            "LLM response must be a JSON object."
        )

    defaults = {
        "ats_score": 0,
        "overall_assessment": "",
        "matched_keywords": [],
        "missing_keywords": [],
        "strong_keywords": [],
        "keyword_recommendations": [],
        "summary_recommendation": "",
        "skills_recommendations": [],
        "experience_recommendations": [],
        "formatting_recommendations": [],
        "warnings": [],
        "rewritten_resume": {
            "name": "",
            "contact": {
                "location": "",
                "phone": "",
                "email": "",
                "linkedin": "",
                "portfolio": ""
            },
            "summary": "",
            "skills": [],
            "experience": [],
            "certifications": [],
            "education": [],
            "achievements": []
        }
    }

    # Add missing top-level fields.
    for key, default_value in defaults.items():

        if key not in result:
            result[key] = default_value

    # ---------------------------------------------------------
    # ATS SCORE
    # ---------------------------------------------------------

    try:
        result["ats_score"] = float(
            result["ats_score"]
        )

    except (ValueError, TypeError):
        result["ats_score"] = 0

    # Keep score between 0 and 100.
    result["ats_score"] = max(
        0,
        min(100, result["ats_score"])
    )

    # Convert 82.0 -> 82.
    if result["ats_score"].is_integer():
        result["ats_score"] = int(
            result["ats_score"]
        )

    # ---------------------------------------------------------
    # LIST FIELDS
    # ---------------------------------------------------------

    list_fields = [
        "matched_keywords",
        "missing_keywords",
        "strong_keywords",
        "keyword_recommendations",
        "skills_recommendations",
        "experience_recommendations",
        "formatting_recommendations",
        "warnings"
    ]

    for field in list_fields:

        if not isinstance(result[field], list):
            result[field] = []

    # ---------------------------------------------------------
    # REWRITTEN RESUME
    # ---------------------------------------------------------

    rewritten = result.get(
        "rewritten_resume"
    )

    if not isinstance(rewritten, dict):
        rewritten = {}

    rewritten_defaults = {
        "name": "",
        "contact": {
            "location": "",
            "phone": "",
            "email": "",
            "linkedin": "",
            "portfolio": ""
        },
        "summary": "",
        "skills": [],
        "experience": [],
        "certifications": [],
        "education": [],
        "achievements": []
    }

    for key, default_value in rewritten_defaults.items():

        if key not in rewritten:
            rewritten[key] = default_value

    # ---------------------------------------------------------
    # CONTACT
    # ---------------------------------------------------------

    contact = rewritten.get("contact")

    if not isinstance(contact, dict):
        contact = {}

    contact_defaults = {
        "location": "",
        "phone": "",
        "email": "",
        "linkedin": "",
        "portfolio": ""
    }

    for key, default_value in contact_defaults.items():

        if key not in contact:
            contact[key] = default_value

    rewritten["contact"] = contact

    # ---------------------------------------------------------
    # RESUME LIST SECTIONS
    # ---------------------------------------------------------

    resume_list_fields = [
        "skills",
        "experience",
        "certifications",
        "education",
        "achievements"
    ]

    for field in resume_list_fields:

        if not isinstance(
            rewritten[field],
            list
        ):
            rewritten[field] = []

    result["rewritten_resume"] = rewritten

    return result
