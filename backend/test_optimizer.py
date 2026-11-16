from app.resume_optimizer import optimize_resume


resume_text = """
Umesh Ghate

Cloud Engineer with 4+ years of IT experience.

Skills:
AWS, Linux, Python, Terraform, Docker, Kubernetes,
Amazon EKS, GitHub Actions, Argo CD, Ansible,
Prometheus, Grafana, OpenTelemetry, VMware

Experience:

Cloud Support Engineer I - Amazon Web Services
- Supported mission-critical AWS environments.
- Managed AWS infrastructure including EC2, S3, VPC, IAM and Lambda.
- Automated infrastructure using Terraform.
- Managed containerized workloads using Docker and Amazon EKS.
- Built CI/CD automation using GitHub Actions.
- Implemented monitoring and observability using Prometheus and Grafana.
- Developed Python and Shell scripts for operational automation.

Systems Engineer - Qualys
- Administered 5,000+ servers across Linux and Windows.
- Managed VMware vSphere environments including ESXi and vCenter.
- Performed vulnerability assessments and security hardening.
"""


job_description = """
We are looking for an experienced DevOps Engineer.

Requirements:

- AWS
- Linux
- Python
- Terraform
- Docker
- Kubernetes
- Amazon EKS
- Helm
- Jenkins
- GitHub Actions
- CI/CD
- Git
- Prometheus
- Grafana
- Observability
- Monitoring
- Infrastructure as Code
- DevOps
- Automation

Experience with EC2, S3, VPC, IAM, Lambda and CloudWatch is preferred.
Experience with Argo CD and Ansible is desirable.
The candidate should have strong troubleshooting and production experience.
"""


result = optimize_resume(
    resume_text=resume_text,
    job_description=job_description
)


print("\n==============================")
print("ATS OPTIMIZATION RESULT")
print("==============================\n")

print(f"ATS Score: {result['ats_score']}")

print("\nOverall Assessment:")
print(result["overall_assessment"])

print("\nMatched Keywords:")
for keyword in result["matched_keywords"]:
    print(f"  ✓ {keyword}")

print("\nMissing Keywords:")
for keyword in result["missing_keywords"]:
    print(f"  ✗ {keyword}")

print("\nStrong Keywords:")
for keyword in result["strong_keywords"]:
    print(f"  ✓ {keyword}")

print("\nSummary Recommendation:")
print(result["summary_recommendation"])

print("\nExperience Recommendations:")
for item in result["experience_recommendations"]:
    print(f"  - {item}")

print("\nSkills Recommendations:")
for item in result["skills_recommendations"]:
    print(f"  - {item}")

print("\nFormatting Recommendations:")
for item in result["formatting_recommendations"]:
    print(f"  - {item}")

print("\nWarnings:")
for item in result["warnings"]:
    print(f"  ! {item}")

print("\n==============================")