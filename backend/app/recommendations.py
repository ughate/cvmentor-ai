from typing import List, Dict


def generate_recommendations(
    matched_skills: List[str],
    missing_skills: List[str],
    resume_text: str,
    job_description: str,
) -> List[Dict]:

    recommendations = []

    resume_lower = resume_text.lower()

    # --------------------------------------------------
    # Missing skills
    # --------------------------------------------------

    for skill in missing_skills:

        recommendations.append({
            "type": "missing_skill",
            "skill": skill,
            "priority": "high",
            "message": (
                f"The job description mentions '{skill}', "
                "but we could not find clear evidence of it "
                "in the resume."
            ),
            "action": (
                f"Add '{skill}' only if you genuinely have "
                "experience with it."
            )
        })

    # --------------------------------------------------
    # CI/CD
    # --------------------------------------------------

    if "github actions" in resume_lower or "argo cd" in resume_lower:

        if "ci/cd" in missing_skills:

            recommendations.append({
                "type": "keyword",
                "skill": "ci/cd",
                "priority": "medium",
                "message": (
                    "Your resume describes GitHub Actions "
                    "and/or Argo CD, which are commonly used "
                    "for CI/CD."
                ),
                "action": (
                    "If accurate, explicitly use the term "
                    "'CI/CD' in the relevant experience bullet."
                )
            })

    # --------------------------------------------------
    # Infrastructure as Code
    # --------------------------------------------------

    if "terraform" in resume_lower:

        if "infrastructure as code" in missing_skills:

            recommendations.append({
                "type": "keyword",
                "skill": "infrastructure as code",
                "priority": "medium",
                "message": (
                    "Your resume mentions Terraform, but the "
                    "phrase 'Infrastructure as Code' may not "
                    "be explicitly visible."
                ),
                "action": (
                    "If accurate, describe Terraform work as "
                    "'Infrastructure as Code (IaC)'."
                )
            })

    # --------------------------------------------------
    # Monitoring
    # --------------------------------------------------

    monitoring_tools = [
        "prometheus",
        "grafana",
        "cloudwatch",
        "loki",
        "opentelemetry",
    ]

    has_monitoring = any(
        tool in resume_lower
        for tool in monitoring_tools
    )

    if has_monitoring and "monitoring" in missing_skills:

        recommendations.append({
            "type": "keyword",
            "skill": "monitoring",
            "priority": "medium",
            "message": (
                "Your resume contains monitoring-related "
                "technologies."
            ),
            "action": (
                "Explicitly mention 'monitoring' where "
                "accurate, especially in experience bullets."
            )
        })

    # --------------------------------------------------
    # Observability
    # --------------------------------------------------

    if any(
        tool in resume_lower
        for tool in [
            "prometheus",
            "grafana",
            "loki",
            "opentelemetry",
            "open telemetry",
        ]
    ):

        if "observability" in missing_skills:

            recommendations.append({
                "type": "keyword",
                "skill": "observability",
                "priority": "medium",
                "message": (
                    "Your resume contains tools commonly "
                    "associated with observability."
                ),
                "action": (
                    "If accurate, explicitly describe this "
                    "experience as 'observability'."
                )
            })

    # --------------------------------------------------
    # Automation
    # --------------------------------------------------

    automation_tools = [
        "python",
        "shell",
        "terraform",
        "ansible",
        "github actions",
    ]

    has_automation = any(
        tool in resume_lower
        for tool in automation_tools
    )

    if has_automation and "automation" in missing_skills:

        recommendations.append({
            "type": "keyword",
            "skill": "automation",
            "priority": "medium",
            "message": (
                "Your resume contains scripting and "
                "automation technologies."
            ),
            "action": (
                "Use the word 'automation' where it accurately "
                "describes your existing work."
            )
        })

    # --------------------------------------------------
    # DevOps
    # --------------------------------------------------

    devops_tools = [
        "terraform",
        "kubernetes",
        "docker",
        "github actions",
        "argo cd",
        "ansible",
    ]

    has_devops = any(
        tool in resume_lower
        for tool in devops_tools
    )

    if has_devops and "devops" in missing_skills:

        recommendations.append({
            "type": "keyword",
            "skill": "devops",
            "priority": "medium",
            "message": (
                "Your resume contains several DevOps-related "
                "technologies."
            ),
            "action": (
                "If accurate, explicitly describe relevant "
                "experience using DevOps terminology."
            )
        })

    return recommendations