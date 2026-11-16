from app.resume_rewriter import rewrite_resume


resume_text = """
Umesh Ghate

Cloud Engineer with 4+ years of IT experience in VMware, Linux,
Docker, Kubernetes and AWS cloud infrastructure.

Skills:
AWS, Linux, Python, Terraform, Docker, Kubernetes, Amazon EKS,
GitHub Actions, Argo CD, Ansible, Prometheus, Grafana,
OpenTelemetry, Shell, VMware.

Experience:

Cloud Support Engineer I
Amazon Web Services
Pune, India
Apr 2026 - Present

- Delivered customer-facing technical support for mission-critical AWS environments.
- Automated infrastructure using Terraform.
- Managed Docker containers and Amazon EKS workloads.
- Built CI/CD automation using GitHub Actions.
- Implemented monitoring and observability using Prometheus and Grafana.
- Developed Python and Shell scripts for operational automation.

Cloud Support Associate
Amazon Web Services
Hyderabad, India
Aug 2024 - Apr 2026

- Administered AWS infrastructure including EC2, S3, VPC, IAM and Lambda.
- Provisioned infrastructure using Terraform.
- Automated infrastructure lifecycle across environments using Terraform.
- Managed configuration using Ansible.

Systems Engineer
Qualys Inc.
India
Mar 2022 - Aug 2024

- Administered and maintained 5,000+ servers across Linux and Windows.
- Managed VMware vSphere environments including ESXi and vCenter.
- Performed vulnerability assessments and security hardening.
"""


job_description = """
We are looking for an experienced DevOps Engineer.

Requirements:

AWS, Linux, Python, Terraform, Docker, Kubernetes,
Amazon EKS, Helm, Jenkins, GitHub Actions, CI/CD,
Git, Prometheus, Grafana, observability, monitoring,
Infrastructure as Code, DevOps and automation.

Experience with EC2, S3, VPC, IAM, Lambda and CloudWatch
is preferred.

Experience with Argo CD and Ansible is desirable.
"""


ats_analysis = {
    "ats_score": 75,

    "matched_keywords": [
        "AWS",
        "Linux",
        "Python",
        "Terraform",
        "Docker",
        "Kubernetes",
        "Amazon EKS",
        "GitHub Actions",
        "Argo CD",
        "Ansible",
        "Prometheus",
        "Grafana",
        "OpenTelemetry"
    ],

    "missing_keywords": [
        "Jenkins",
        "Helm",
        "Git",
        "CI/CD",
        "Monitoring",
        "Observability",
        "DevOps",
        "Automation"
    ],

    "supported_missing_keywords": [
        "CI/CD",
        "Monitoring",
        "Observability",
        "Infrastructure as Code",
        "Automation",
        "DevOps"
    ],

    "unsupported_keywords": [
        "Jenkins",
        "Helm",
        "Git"
    ]
}


result = rewrite_resume(
    resume_text=resume_text,
    job_description=job_description,
    ats_analysis=ats_analysis
)


print("\n==============================")
print("REWRITTEN RESUME")
print("==============================")

print("\nNAME:")
print(result["name"])

print("\nCONTACT:")
print(result["contact"])

print("\nSUMMARY:")
print(result["summary"])

print("\nSKILLS:")

for category, skills in result["skills"].items():

    if skills:
        print(f"  {category}: {skills}")


print("\nEXPERIENCE:")

for job in result["experience"]:

    print(
        f"\n{job.get('title', '')} | "
        f"{job.get('company', '')}"
    )

    print(
        f"{job.get('location', '')} | "
        f"{job.get('dates', '')}"
    )

    for bullet in job.get("bullets", []):
        print(f"  • {bullet}")


print("\nCERTIFICATIONS:")

for item in result["certifications"]:
    print(f"  • {item}")


print("\nEDUCATION:")

for item in result["education"]:
    print(f"  • {item}")


print("\nACHIEVEMENTS:")

for item in result["achievements"]:
    print(f"  • {item}")


print("\nOPTIMIZATION NOTES:")

for item in result["optimization_notes"]:
    print(f"  • {item}")


print("\nUNSUPPORTED KEYWORDS NOT ADDED:")

for item in result["unsupported_keywords_not_added"]:
    print(f"  ✗ {item}")


print("\n==============================")