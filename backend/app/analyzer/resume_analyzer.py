import re


def clean_text(text: str) -> str:
    """Clean extracted resume text while preserving sections."""

    text = text.replace("\r", "")
    text = text.replace("\t", " ")

    # Remove excessive spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_email(text: str) -> str | None:
    """Extract email address."""

    match = re.search(
        r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    """Extract phone number."""

    match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    return match.group(0) if match else None


def extract_name(text: str) -> str | None:
    """Extract candidate name from the first meaningful line."""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    return lines[0]


def find_heading_index(lines: list[str], headings: list[str]) -> int | None:
    """
    Find a section heading using exact matching.

    This prevents words such as 'experience' appearing inside
    normal sentences from being treated as headings.
    """

    normalized_headings = {
        heading.strip().lower()
        for heading in headings
    }

    for index, line in enumerate(lines):

        normalized_line = line.strip().lower()

        if normalized_line in normalized_headings:
            return index

    return None


def extract_section(
    text: str,
    start_headings: list[str],
    end_headings: list[str],
) -> str:

    lines = text.splitlines()

    start_index = find_heading_index(
        lines,
        start_headings
    )

    if start_index is None:
        return ""

    content = []

    for line in lines[start_index + 1:]:

        normalized_line = line.strip().lower()

        # Stop only when we find an exact section heading
        if normalized_line in {
            heading.lower()
            for heading in end_headings
        }:
            break

        if line.strip():
            content.append(line.strip())

    return "\n".join(content).strip()


def analyze_resume(text: str) -> dict:

    text = clean_text(text)

    lines = text.splitlines()

    email = extract_email(text)
    phone = extract_phone(text)
    name = extract_name(text)

    summary = extract_section(
        text,
        [
            "PROFILE SUMMARY",
            "PROFESSIONAL SUMMARY",
            "SUMMARY",
        ],
        [
            "CONTACT",
            "CERTIFICATIONS",
            "ACTIVITIES AND INTERESTS",
            "LANGUAGES",
            "EDUCATION",
            "EDUCATION:",
            "EXPERIENCE",
            "WORK EXPERIENCE",
            "ACHIEVEMENTS",
        ],
    )

    certifications = extract_section(
        text,
        [
            "CERTIFICATIONS",
            "CERTIFICATION",
        ],
        [
            "ACTIVITIES AND INTERESTS",
            "LANGUAGES",
            "EDUCATION",
            "EDUCATION:",
            "EXPERIENCE",
            "WORK EXPERIENCE",
            "ACHIEVEMENTS",
        ],
    )

    education = extract_section(
        text,
        [
            "EDUCATION",
            "EDUCATION:",
        ],
        [
            "EXPERIENCE",
            "WORK EXPERIENCE",
            "ACHIEVEMENTS",
        ],
    )

    achievements = extract_section(
        text,
        [
            "ACHIEVEMENTS",
            "ACHIEVEMENT",
        ],
        [],
    )

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "summary": summary,
        "certifications": certifications,
        "education": education,
        "achievements": achievements,
        "raw_text": text,
    }