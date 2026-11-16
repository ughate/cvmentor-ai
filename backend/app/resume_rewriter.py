import json
import re

from app.llm_service import ask_llm


def rewrite_resume(
    resume_text: str,
    job_description: str,
    ats_analysis: dict
) -> dict:
    """
    Rewrite a resume for a specific job description.

    IMPORTANT:
    - Never invent experience.
    - Never add unsupported technologies.
    - Preserve actual employers and career history.
    - Improve ATS terminology only when supported by the original resume.
    """

    analysis_json = json.dumps(
        ats_analysis,
        indent=2,
        ensure_ascii=False
    )

    prompt = f"""
You are an expert technical resume writer and ATS optimization specialist.

Your task is to rewrite the candidate's resume for the supplied job description.

========================
STRICT ANTI-FABRICATION RULES
========================

NEVER:

- invent skills
- invent technologies
- invent employers
- invent job titles
- invent certifications
- invent projects
- invent responsibilities
- invent achievements
- invent metrics
- invent dates
- invent education
- claim experience with a technology that is not supported by the original resume

The optimized resume MUST remain truthful.

========================
IMPORTANT KEYWORD RULE
========================

You may improve terminology when the original resume already supports it.

Examples:

Terraform
→ Infrastructure as Code

GitHub Actions
→ CI/CD

Prometheus + Grafana + OpenTelemetry
→ Monitoring and Observability

Python + Shell scripts
→ Automation

These are SAFE because the underlying experience already exists.

However:

Jenkins
Helm
or any other technology not supported by the resume

MUST NOT be added.

========================
OPTIMIZATION GOALS
========================

1. Improve ATS keyword alignment.
2. Improve professional wording.
3. Make the professional summary stronger.
4. Make experience bullets clearer and more technically precise. Describe outcomes only when explicitly supported by the original resume.
5. Use standard DevOps/Cloud terminology where supported.
6. Preserve the candidate's actual career history.
7. Keep the resume concise.
8. Remove unnecessary repetition.
9. Make skills easy for ATS systems to identify.
10. Do not keyword-stuff unnaturally.

========================
JOB DESCRIPTION
========================

{job_description}

========================
ATS ANALYSIS
========================

{analysis_json}

========================
ORIGINAL RESUME
========================

{resume_text}

========================
OUTPUT FORMAT
========================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "name": "",
    "contact": "",

    "summary": "",

    "skills": {{
        "Cloud": "",
        "Operating Systems": "",
        "Infrastructure as Code": "",
        "Containers": "",
        "CI/CD": "",
        "Monitoring and Observability": "",
        "Automation and Scripting": "",
        "Configuration Management": "",
        "Version Control": ""
    }},

    "experience": [
        {{
            "title": "",
            "company": "",
            "location": "",
            "dates": "",
            "bullets": []
        }}
    ],

    "certifications": [],

    "education": [],

    "achievements": [],

    "optimization_notes": [],

    "unsupported_keywords_not_added": []
}}

========================
SUMMARY
========================

Write a strong professional summary using ONLY information supported
by the original resume.

Prioritize experience relevant to the job description.

Do not claim missing technologies.

========================
SKILLS
========================

Organize ONLY skills that actually appear in the original resume.

You may use standard terminology.

For example:

Terraform

can be represented as:

"Infrastructure as Code: Terraform"

GitHub Actions

can be represented as:

"CI/CD: GitHub Actions"

Prometheus, Grafana and OpenTelemetry

can be represented as:

"Monitoring and Observability: Prometheus, Grafana, OpenTelemetry"

Do NOT add Jenkins or Helm unless they are supported by the original resume.

If a category has no supported skills, return an empty string.

========================
EXPERIENCE
========================

Rewrite existing experience bullets.

Make them:
- concise
- technically precise
- professional
- ATS-friendly
- easy to understand

STRICT FACTUAL ACCURACY RULES:

1. Preserve the exact meaning of every original responsibility.
2. Do not add business outcomes that are not explicitly stated.
3. Do not claim reduced downtime, improved performance, increased
   productivity, enhanced security, cost savings, or better reliability
   unless the original resume explicitly supports that result.
4. Do not add implied metrics, percentages, quantities, or measurements.
5. Do not describe work as automated unless automation is supported
   by the original resume.
6. Do not claim ownership, leadership, implementation, or architecture
   responsibilities unless the original resume supports them.
7. Do not turn a troubleshooting activity into a claim that a system
   was optimized or business impact was achieved without evidence.
8. You may improve grammar, sentence structure, technical terminology,
   and clarity without changing the underlying meaning.
9. You may combine repetitive bullets only if all original facts remain.
10. If a bullet cannot be improved without adding unsupported claims,
    preserve its original meaning and use simpler wording.

Avoid unsupported phrases such as:
- ensuring minimal downtime
- improving operational efficiency
- enhancing security compliance
- increasing productivity
- optimizing performance
- reducing costs

These phrases may only be used when the original resume explicitly
documents the corresponding outcome.

Preserve exactly:
- company
- title
- dates
- location
- actual responsibilities
- actual metrics

You may use supported terminology such as:
CI/CD, Infrastructure as Code, automation, monitoring, observability,
and DevOps ONLY when supported by the original resume.

Never invent an achievement to make a bullet sound stronger.

========================
CERTIFICATIONS
========================

Copy certifications from the original resume.

Do not invent certifications.

========================
EDUCATION
========================

Copy education from the original resume.

Do not invent education.

========================
ACHIEVEMENTS
========================

Keep genuine achievements from the original resume.

Improve their wording if appropriate.

Do not invent new achievements.

========================
OPTIMIZATION NOTES
========================

Explain what was improved.

Examples:

"Added Infrastructure as Code terminology to describe Terraform experience."

"Associated CI/CD terminology with existing GitHub Actions experience."

"Improved observability terminology around Prometheus and Grafana."

========================
UNSUPPORTED KEYWORDS
========================

List important JD technologies that were intentionally NOT added
because the resume does not support them.

Example:

[
    "Jenkins",
    "Helm"
]

This is important for preventing resume fabrication.

Return JSON ONLY.
"""

    response = ask_llm(prompt)

    return _parse_response(response)


def _parse_response(response: str) -> dict:
    """
    Parse JSON returned by Ollama.
    """

    response = response.strip()

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

    try:
        result = json.loads(response)

    except json.JSONDecodeError:

        start = response.find("{")
        end = response.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "Ollama returned invalid JSON."
            )

        json_text = response[start:end + 1]

        try:
            result = json.loads(json_text)

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Could not parse Ollama JSON response: {exc}"
            )

    return _validate_response(result)


def _validate_response(result: dict) -> dict:
    """
    Validate and normalize the rewritten resume.
    """

    if not isinstance(result, dict):
        raise ValueError(
            "Resume rewrite response must be a JSON object."
        )

    defaults = {
        "name": "",
        "contact": "",
        "summary": "",
        "skills": {},
        "experience": [],
        "certifications": [],
        "education": [],
        "achievements": [],
        "optimization_notes": [],
        "unsupported_keywords_not_added": []
    }

    for key, value in defaults.items():

        if key not in result:
            result[key] = value

    if not isinstance(result["skills"], dict):
        result["skills"] = {}

    if not isinstance(result["experience"], list):
        result["experience"] = []

    if not isinstance(result["certifications"], list):
        result["certifications"] = []

    if not isinstance(result["education"], list):
        result["education"] = []

    if not isinstance(result["achievements"], list):
        result["achievements"] = []

    if not isinstance(result["optimization_notes"], list):
        result["optimization_notes"] = []

    if not isinstance(
        result["unsupported_keywords_not_added"],
        list
    ):
        result["unsupported_keywords_not_added"] = []

    return result