from app.resume_generator import generate_resume_docx


sample_resume = {
    "name": "Umesh Ghate",

    "contact": {
        "location": "Pune, India",
        "phone": "+91 7030493146",
        "email": "umesh04ghate@gmail.com",
        "linkedin": "https://www.linkedin.com/in/ughate58",
        "portfolio": "https://ughate.github.io/portfolio/"
    },

    "summary": (
        "Cloud Engineer with 4+ years of IT experience specializing "
        "in AWS, Linux, Python, Terraform, Docker, Kubernetes, "
        "Amazon EKS, automation, and cloud infrastructure. "
        "Experienced in CI/CD, infrastructure as code, monitoring, "
        "observability, and production cloud environments."
    ),

    "skills": [
        {
            "category": "Cloud",
            "skills": [
                "AWS",
                "Azure",
                "OCI"
            ]
        },
        {
            "category": "Infrastructure as Code",
            "skills": [
                "Terraform"
            ]
        },
        {
            "category": "Containers",
            "skills": [
                "Docker",
                "Kubernetes",
                "Amazon EKS"
            ]
        },
        {
            "category": "CI/CD",
            "skills": [
                "GitHub Actions",
                "Argo CD"
            ]
        },
        {
            "category": "Monitoring and Observability",
            "skills": [
                "Prometheus",
                "Grafana",
                "OpenTelemetry",
                "Loki"
            ]
        },
        {
            "category": "Automation and Scripting",
            "skills": [
                "Python",
                "Shell",
                "Ansible"
            ]
        },
        {
            "category": "Operating Systems",
            "skills": [
                "Red Hat Linux",
                "OEL",
                "CentOS",
                "Ubuntu",
                "Windows",
                "ESXi"
            ]
        }
    ],

    "experience": [
        {
            "company": "Amazon Web Services",
            "title": "Cloud Support Engineer I",
            "location": "Pune, India",
            "dates": "Apr 2026 - Present",
            "bullets": [
                "Delivered customer-facing technical support for mission-critical AWS environments.",
                "Built and orchestrated Docker containers for 2-tier and 3-tier applications.",
                "Designed and implemented containerized microservices architecture.",
                "Deployed and managed production workloads on Amazon EKS using Argo CD for GitOps-driven cluster management.",
                "Automated infrastructure provisioning and application releases via GitHub Actions.",
                "Built an end-to-end observability stack using Grafana, Prometheus, Loki, Promtail, and OpenTelemetry.",
                "Designed dashboards and alerting rules to monitor system health and performance, reducing incident response time by 25%.",
                "Developed Python and Shell scripts to automate recurring tasks, improving operational efficiency by 20%.",
                "Architected a Terraform-based IaC solution to stream CloudWatch metrics to Dynatrace via Kinesis."
            ]
        },
        {
            "company": "Amazon Web Services",
            "title": "Cloud Support Associate",
            "location": "Hyderabad, India",
            "dates": "Aug 2024 - Apr 2026",
            "bullets": [
                "Administered and optimized AWS cloud infrastructure including EC2, S3, VPC, IAM, Lambda, and CloudFormation.",
                "Provisioned and managed AWS infrastructure using Terraform with remote state backends.",
                "Automated the infrastructure lifecycle from development to production, reducing manual effort by 40%.",
                "Configured and maintained infrastructure using Ansible across AWS cloud and on-premises VMware environments.",
                "Automated software deployment, patching, and service management across hybrid environments."
            ]
        },
        {
            "company": "Qualys Inc.",
            "title": "Systems Engineer",
            "location": "India",
            "dates": "Mar 2022 - Aug 2024",
            "bullets": [
                "Administered and maintained 5,000+ servers across RHEL, Ubuntu, Amazon Linux, Windows Server, and macOS.",
                "Managed patching cycles, performance tuning, user access controls, and CIS security hardening.",
                "Reduced infrastructure downtime by 30% by implementing high-availability strategies and disaster recovery frameworks.",
                "Conducted vulnerability assessments and coordinated cross-functional remediation.",
                "Managed VMware vSphere environments including ESXi, vCenter, HA, DRS, vMotion, and Storage vMotion."
            ]
        }
    ],

    "certifications": [
        "RHCSA - Red Hat Certified Systems Administrator",
        "AWS Certified Solutions Architect Associate",
        "AWS Certified AI Practitioner",
        "AWS Certified DevOps Engineer",
        "Terraform Certified Associate"
    ],

    "education": [
        {
            "degree": "MCA - Master of Computer Applications",
            "institution": "Pune University",
            "details": "8.07 GPA, First Class with Distinction, 2022"
        }
    ],

    "achievements": [
        "Contributed to AWS Kendra official documentation by identifying an outdated API and building a validated POC with the newer approach.",
        "Cut AWS OpenSearch costs by 25% through ISM policy implementation.",
        "Delivered an undocumented Terraform IaC pattern for CloudWatch to Kinesis to Dynatrace integration after building a working POC from scratch."
    ]
}


output = generate_resume_docx(
    sample_resume,
    "output/Umesh_Ghate_DevOps_Resume.docx"
)

print("Resume generated successfully:")
print(output)