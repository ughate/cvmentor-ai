from app.resume_generator import generate_resume_docx


output_file = "test_resume.docx"


generate_resume_docx(
    output_path=output_file,

    name="Umesh Ghate",

    contact="Pune, India | +91 7030493146 | umesh04ghate@gmail.com",

    summary=(
        "Cloud Engineer with 4+ years of experience in AWS cloud "
        "infrastructure, Linux, Python, Terraform, Docker, Kubernetes "
        "and containerized environments."
    ),

    skills={
        "Cloud": "AWS, EC2, S3, VPC, IAM, Lambda, CloudWatch",
        "Infrastructure as Code": "Terraform, CloudFormation",
        "Containers": "Docker, Kubernetes, Amazon EKS",
        "CI/CD": "GitHub Actions, Argo CD",
        "Monitoring": "Prometheus, Grafana, OpenTelemetry",
        "Scripting": "Python, Shell"
    },

    experience=[
        {
            "title": "Cloud Support Engineer I",
            "company": "Amazon Web Services",
            "location": "Pune, India",
            "dates": "Apr 2026 – Present",
            "bullets": [
                "Delivered customer-facing technical support for mission-critical AWS environments.",
                "Automated infrastructure and application operations using Python, Shell, Terraform and GitHub Actions.",
                "Managed containerized workloads using Docker and Amazon EKS.",
                "Implemented monitoring and observability using Prometheus, Grafana and OpenTelemetry."
            ]
        },
        {
            "title": "Systems Engineer",
            "company": "Qualys Inc.",
            "location": "India",
            "dates": "Mar 2022 – Aug 2024",
            "bullets": [
                "Administered and maintained 5,000+ production servers across Linux and Windows environments.",
                "Managed VMware vSphere environments including ESXi, vCenter, HA and DRS.",
                "Performed vulnerability assessments and coordinated remediation across enterprise environments."
            ]
        }
    ],

    certifications=[
        "RHCSA",
        "AWS Certified Solutions Architect – Associate",
        "AWS Certified AI Practitioner"
    ],

    education=[
        "MCA – Master of Computer Applications, 2022"
    ],

    achievements=[
        "Reduced AWS OpenSearch costs by 25% through ISM policy implementation.",
        "Delivered a Terraform-based CloudWatch → Kinesis → Dynatrace integration pattern."
    ]
)

print(f"Resume generated successfully: {output_file}")