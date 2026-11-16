import re

from app.recommendations import generate_recommendations


# ============================================================
# SKILL / KEYWORD ALIASES
# ============================================================

SKILL_ALIASES = {

    # -------------------------
    # Cloud
    # -------------------------

    "aws": [
        "aws",
        "amazon web services",
    ],

    "azure": [
        "azure",
        "microsoft azure",
    ],

    "oci": [
        "oci",
        "oracle cloud",
        "oracle cloud infrastructure",
    ],

    "gcp": [
        "gcp",
        "google cloud",
        "google cloud platform",
    ],

    # -------------------------
    # Operating Systems
    # -------------------------

    "linux": [
        "linux",
        "rhel",
        "red hat",
        "redhat",
        "ubuntu",
        "centos",
        "amazon linux",
        "oracle enterprise linux",
        "oel",
    ],

    "windows server": [
        "windows server",
        "windows",
    ],

    # -------------------------
    # Programming / Scripting
    # -------------------------

    "python": [
        "python",
        "python scripting",
        "python script",
    ],

    "shell scripting": [
        "shell",
        "shell scripting",
        "bash",
        "bash scripting",
        "shell script",
    ],

    "powershell": [
        "powershell",
        "power shell",
    ],

    # -------------------------
    # Infrastructure as Code
    # -------------------------

    "terraform": [
        "terraform",
    ],

    "infrastructure as code": [
        "infrastructure as code",
        "iac",
        "terraform",
        "cloudformation",
    ],

    "cloudformation": [
        "cloudformation",
        "aws cloudformation",
    ],

    # -------------------------
    # Configuration Management
    # -------------------------

    "ansible": [
        "ansible",
        "ansible automation",
    ],

    # -------------------------
    # Containers
    # -------------------------

    "docker": [
        "docker",
        "docker container",
        "docker containers",
        "containerized",
        "containerization",
        "containers",
    ],

    "kubernetes": [
        "kubernetes",
        "k8s",
        "kube",
    ],

    "amazon eks": [
        "eks",
        "amazon eks",
        "aws eks",
        "elastic kubernetes service",
    ],

    "azure aks": [
        "aks",
        "azure aks",
        "azure kubernetes service",
    ],

    "helm": [
        "helm",
        "helm charts",
        "helm chart",
    ],

    # -------------------------
    # CI/CD
    # -------------------------

    "ci/cd": [
        "ci/cd",
        "ci cd",
        "cicd",
        "continuous integration",
        "continuous deployment",
        "continuous delivery",
        "github actions",
        "jenkins",
        "gitlab ci",
        "gitlab ci/cd",
        "argo cd",
        "argocd",
    ],

    "github actions": [
        "github actions",
        "github action",
    ],

    "jenkins": [
        "jenkins",
    ],

    "gitlab ci": [
        "gitlab ci",
        "gitlab-ci",
        "gitlab cicd",
        "gitlab ci/cd",
    ],

    "argocd": [
        "argo cd",
        "argocd",
        "argo-cd",
    ],

    # -------------------------
    # Version Control
    # -------------------------

    "git": [
        "git",
        "github",
        "gitlab",
        "bitbucket",
    ],

    # -------------------------
    # Monitoring / Observability
    # -------------------------

    "prometheus": [
        "prometheus",
    ],

    "grafana": [
        "grafana",
    ],

    "loki": [
        "loki",
    ],

    "opentelemetry": [
        "open telemetry",
        "opentelemetry",
        "otel",
    ],

    "observability": [
        "observability",
        "open telemetry",
        "opentelemetry",
        "otel",
        "prometheus",
        "grafana",
        "loki",
        "metrics",
        "logs",
        "traces",
        "distributed tracing",
        "alerting",
    ],

    "monitoring": [
        "monitoring",
        "monitor",
        "monitored",
        "prometheus",
        "grafana",
        "cloudwatch",
        "metrics",
        "logs",
        "alerting",
        "dashboards",
    ],

    "logging": [
        "logging",
        "logs",
        "log management",
        "loki",
        "cloudwatch logs",
        "elasticsearch",
        "opensearch",
    ],

    # -------------------------
    # Networking
    # -------------------------

    "networking": [
        "networking",
        "network",
        "tcp/ip",
        "tcp",
        "udp",
        "dns",
        "http",
        "https",
        "load balancer",
        "load balancing",
        "vpc",
        "subnet",
        "routing",
        "firewall",
    ],

    "vpc": [
        "vpc",
        "aws vpc",
        "amazon vpc",
        "virtual private cloud",
    ],

    "dns": [
        "dns",
        "route 53",
        "route53",
    ],

    "load balancing": [
        "load balancer",
        "load balancing",
        "alb",
        "application load balancer",
        "nlb",
        "network load balancer",
    ],

    # -------------------------
    # AWS Services
    # -------------------------

    "ec2": [
        "ec2",
        "amazon ec2",
    ],

    "s3": [
        "s3",
        "amazon s3",
    ],

    "iam": [
        "iam",
        "aws iam",
        "identity and access management",
    ],

    "lambda": [
        "lambda",
        "aws lambda",
        "amazon lambda",
    ],

    "rds": [
        "rds",
        "amazon rds",
    ],

    "sqs": [
        "sqs",
        "amazon sqs",
    ],

    "sns": [
        "sns",
        "amazon sns",
    ],

    "kinesis": [
        "kinesis",
        "amazon kinesis",
        "kinesis data streams",
    ],

    "eventbridge": [
        "eventbridge",
        "amazon eventbridge",
        "aws eventbridge",
    ],

    # -------------------------
    # Databases / Search
    # -------------------------

    "opensearch": [
        "opensearch",
        "amazon opensearch",
        "aws opensearch",
    ],

    "elasticsearch": [
        "elasticsearch",
        "elastic search",
    ],

    # -------------------------
    # VMware
    # -------------------------

    "vmware": [
        "vmware",
        "vmware vsphere",
        "vsphere",
        "esxi",
        "vcenter",
    ],

    "esxi": [
        "esxi",
        "vmware esxi",
    ],

    "vcenter": [
        "vcenter",
        "vmware vcenter",
    ],

    # -------------------------
    # DevOps / Engineering
    # -------------------------

    "devops": [
        "devops",
        "dev ops",
        "devsecops",
    ],

    "automation": [
        "automation",
        "automate",
        "automated",
        "automating",
        "scripting",
        "python",
        "shell",
        "bash",
        "terraform",
        "ansible",
        "github actions",
    ],

    "microservices": [
        "microservices",
        "microservice",
        "micro-services",
    ],

    "high availability": [
        "high availability",
        "highly available",
        "fault tolerant",
        "fault tolerance",
    ],

    "disaster recovery": [
        "disaster recovery",
        "business continuity",
        "backup and recovery",
    ],

    # -------------------------
    # Security
    # -------------------------

    "security": [
        "security",
        "cybersecurity",
        "information security",
        "cloud security",
    ],

    "vulnerability management": [
        "vulnerability management",
        "vulnerability assessment",
        "vulnerability scanning",
        "cve",
        "qualys",
    ],

    "iam security": [
        "iam",
        "identity and access management",
        "access control",
        "permissions",
        "least privilege",
    ],

    # -------------------------
    # Production / SRE
    # -------------------------

    "incident management": [
        "incident management",
        "incident response",
        "incident triage",
        "production incident",
        "troubleshooting",
    ],

    "troubleshooting": [
        "troubleshooting",
        "debugging",
        "root cause analysis",
        "rca",
        "problem solving",
    ],

    "sre": [
        "sre",
        "site reliability engineering",
        "site reliability engineer",
    ],

    "sla": [
        "sla",
        "service level agreement",
        "service-level agreement",
    ],

    "slo": [
        "slo",
        "service level objective",
        "service-level objective",
    ],
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize text before keyword matching.
    """

    if not text:
        return ""

    text = text.lower()

    # Normalize unicode dashes
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Normalize arrows
    text = text.replace("→", " ")

    # Normalize bullet characters
    text = text.replace("•", " ")

    # Normalize CI/CD variations
    text = text.replace("ci / cd", "ci/cd")
    text = text.replace("ci-cd", "ci/cd")

    # Keep letters, numbers, spaces, slash, plus, hash,
    # dot and hyphen.
    text = re.sub(
        r"[^a-z0-9/\s+#.-]",
        " ",
        text
    )

    # Multiple spaces -> single space
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# SAFE ALIAS MATCHING
# ============================================================

def contains_alias(
    text: str,
    alias: str
) -> bool:
    """
    Safely determine whether an alias exists in text.

    Example:

        git

    should match:

        GitHub

    but we don't want arbitrary partial-word matches.
    """

    alias = normalize_text(alias)

    if not alias:
        return False

    escaped_alias = re.escape(alias)

    pattern = (
        rf"(?<![a-z0-9])"
        rf"{escaped_alias}"
        rf"(?![a-z0-9])"
    )

    return re.search(
        pattern,
        text
    ) is not None


# ============================================================
# FIND REQUIRED SKILLS FROM JD
# ============================================================

def find_required_skills(
    job_description: str
) -> list:
    """
    Identify skills mentioned in the Job Description.
    """

    normalized_jd = normalize_text(
        job_description
    )

    required_skills = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if contains_alias(
                normalized_jd,
                alias
            ):

                required_skills.append(
                    skill
                )

                break

    return required_skills


# ============================================================
# FIND MATCHING SKILLS
# ============================================================

def find_matching_skills(
    resume_text: str,
    job_description: str,
) -> dict:
    """
    Compare resume against JD-required skills.
    """

    normalized_resume = normalize_text(
        resume_text
    )

    required_skills = find_required_skills(
        job_description
    )

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        aliases = SKILL_ALIASES.get(
            skill,
            [skill]
        )

        found = False

        for alias in aliases:

            if contains_alias(
                normalized_resume,
                alias
            ):

                found = True
                break

        if found:
            matched_skills.append(
                skill
            )
        else:
            missing_skills.append(
                skill
            )

    total = len(required_skills)

    if total > 0:

        match_percentage = round(
            len(matched_skills)
            / total
            * 100,
            2
        )

    else:

        match_percentage = 0.0

    return {
        "total_required_skills": total,

        "matched_skills_count": len(
            matched_skills
        ),

        "missing_skills_count": len(
            missing_skills
        ),

        "match_percentage": match_percentage,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,
    }


# ============================================================
# KEYWORD ANALYSIS
# ============================================================

def analyze_keywords(
    resume_text: str,
    job_description: str,
) -> dict:
    """
    Backward-compatible keyword analysis.
    """

    result = find_matching_skills(
        resume_text,
        job_description
    )

    return {
        "total_keywords": result[
            "total_required_skills"
        ],

        "matched_count": result[
            "matched_skills_count"
        ],

        "missing_count": result[
            "missing_skills_count"
        ],

        "match_percentage": result[
            "match_percentage"
        ],

        "matched_keywords": result[
            "matched_skills"
        ],

        "missing_keywords": result[
            "missing_skills"
        ],
    }


# ============================================================
# ATS SCORE
# ============================================================

def calculate_ats_score(
    skill_match_percentage: float
) -> float:
    """
    Current ATS score.

    At this stage only skill matching contributes
    to the score.

    Future components will include:

        Experience Match
        Job Title Match
        Education Match
        Resume Structure
        Section Quality
    """

    score = (
        skill_match_percentage
        * 0.70
    )

    return round(
        score,
        2
    )


# ============================================================
# MAIN ANALYZER
# ============================================================

def analyze_job_description(
    resume_text: str,
    job_description: str,
) -> dict:
    """
    Main ATS analysis function.
    """

    if not resume_text:
        raise ValueError(
            "Resume text cannot be empty."
        )

    if not job_description:
        raise ValueError(
            "Job description cannot be empty."
        )

    # ----------------------------------------
    # Skill analysis
    # ----------------------------------------

    skill_analysis = find_matching_skills(
        resume_text,
        job_description
    )

    skill_match_percentage = (
        skill_analysis[
            "match_percentage"
        ]
    )

    # ----------------------------------------
    # ATS score
    # ----------------------------------------

    ats_score = calculate_ats_score(
        skill_match_percentage
    )

    # ----------------------------------------
    # Recommendations
    # ----------------------------------------

    recommendations = (
        generate_recommendations(
            matched_skills=skill_analysis[
                "matched_skills"
            ],

            missing_skills=skill_analysis[
                "missing_skills"
            ],

            resume_text=resume_text,

            job_description=job_description,
        )
    )

    # ----------------------------------------
    # Final response
    # ----------------------------------------

    return {

        "ats_score": ats_score,

        "score_breakdown": {

            "skill_match": (
                skill_match_percentage
            ),

            "skill_weight": 70,

            "experience_match": 0,

            "experience_weight": 10,

            "resume_structure": 0,

            "structure_weight": 10,

            "education_match": 0,

            "education_weight": 5,

            "job_title_match": 0,

            "job_title_weight": 5,
        },

        "skill_analysis": skill_analysis,

        # Keep this for compatibility
        # with the current API/frontend.
        "keyword_analysis": (
            analyze_keywords(
                resume_text,
                job_description
            )
        ),

        "recommendations": recommendations,
    }


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    sample_resume = """
    Cloud Engineer with 4+ years of experience
    in AWS, Linux, Python, Terraform, Docker,
    Kubernetes, Amazon EKS, GitHub Actions,
    Argo CD, Prometheus, Grafana,
    OpenTelemetry and automation.
    """

    sample_jd = """
    We are looking for a DevOps Engineer with
    AWS, Linux, Terraform, Kubernetes, Docker,
    Jenkins, Helm, GitHub Actions, CI/CD,
    Prometheus, Grafana, observability,
    monitoring and Infrastructure as Code.
    """

    result = analyze_job_description(
        sample_resume,
        sample_jd
    )

    import json

    print(
        json.dumps(
            result,
            indent=2
        )
    )