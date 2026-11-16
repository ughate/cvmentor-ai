from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def generate_resume_docx(
    rewritten_resume: dict,
    output_path: str = "generated_resume.docx"
) -> str:
    """
    Generate an ATS-friendly DOCX resume from rewritten_resume JSON.

    The function only uses information provided in rewritten_resume.
    """

    document = Document()

    # ---------------------------------------------------------
    # PAGE SETUP
    # ---------------------------------------------------------

    section = document.sections[0]

    section.top_margin = Pt(36)
    section.bottom_margin = Pt(36)
    section.left_margin = Pt(45)
    section.right_margin = Pt(45)

    # ---------------------------------------------------------
    # DEFAULT FONT
    # ---------------------------------------------------------

    styles = document.styles

    normal_style = styles["Normal"]
    normal_style.font.name = "Arial"
    normal_style.font.size = Pt(10)

    # ---------------------------------------------------------
    # HELPER FUNCTIONS
    # ---------------------------------------------------------

    def remove_table_borders(table):
        """
        Keep tables out of the resume.
        This helper is intentionally unused but kept here
        if the generator is extended later.
        """
        tbl = table._tbl
        tblPr = tbl.tblPr

        borders = tblPr.first_child_found_in("w:tblBorders")

        if borders is None:
            borders = OxmlElement("w:tblBorders")
            tblPr.append(borders)

        for edge in (
            "top",
            "left",
            "bottom",
            "right",
            "insideH",
            "insideV"
        ):
            tag = "w:" + edge
            element = borders.find(qn(tag))

            if element is None:
                element = OxmlElement(tag)
                borders.append(element)

            element.set(qn("w:val"), "nil")

    def add_heading(text):
        if not text:
            return

        paragraph = document.add_paragraph()

        paragraph.paragraph_format.space_before = Pt(10)
        paragraph.paragraph_format.space_after = Pt(4)

        run = paragraph.add_run(text.upper())

        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(11)

        # Bottom border for section heading
        p = paragraph._p
        pPr = p.get_or_add_pPr()

        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")

        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "1")

        pBdr.append(bottom)
        pPr.append(pBdr)

    def add_bullet(text):
        if not text:
            return

        paragraph = document.add_paragraph()

        paragraph.style = document.styles["Normal"]

        paragraph.paragraph_format.left_indent = Pt(12)
        paragraph.paragraph_format.first_line_indent = Pt(-8)
        paragraph.paragraph_format.space_after = Pt(2)

        run = paragraph.add_run("• " + str(text))

        run.font.name = "Arial"
        run.font.size = Pt(9.5)

    def add_normal(text):
        if not text:
            return

        paragraph = document.add_paragraph()

        paragraph.paragraph_format.space_after = Pt(4)

        run = paragraph.add_run(str(text))

        run.font.name = "Arial"
        run.font.size = Pt(10)

    # ---------------------------------------------------------
    # NAME
    # ---------------------------------------------------------

    name = rewritten_resume.get("name", "").strip()

    if name:
        paragraph = document.add_paragraph()

        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        paragraph.paragraph_format.space_after = Pt(4)

        run = paragraph.add_run(name)

        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(18)

    # ---------------------------------------------------------
    # CONTACT
    # ---------------------------------------------------------

    contact = rewritten_resume.get("contact", {})

    if isinstance(contact, dict):

        contact_parts = []

        location = contact.get("location", "").strip()
        phone = contact.get("phone", "").strip()
        email = contact.get("email", "").strip()
        linkedin = contact.get("linkedin", "").strip()
        portfolio = contact.get("portfolio", "").strip()

        if location:
            contact_parts.append(location)

        if phone:
            contact_parts.append(phone)

        if email:
            contact_parts.append(email)

        if linkedin:
            contact_parts.append(linkedin)

        if portfolio:
            contact_parts.append(portfolio)

        if contact_parts:

            paragraph = document.add_paragraph()

            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

            paragraph.paragraph_format.space_after = Pt(8)

            run = paragraph.add_run(
                " | ".join(contact_parts)
            )

            run.font.name = "Arial"
            run.font.size = Pt(8.5)

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    summary = rewritten_resume.get("summary", "")

    if summary:
        add_heading("Summary")
        add_normal(summary)

    # ---------------------------------------------------------
    # SKILLS
    # ---------------------------------------------------------

    skills = rewritten_resume.get("skills", [])

    if skills:
        add_heading("Skills")

        for skill_group in skills:

            if not isinstance(skill_group, dict):
                continue

            category = skill_group.get("category", "")
            skill_list = skill_group.get("skills", [])

            if not isinstance(skill_list, list):
                continue

            skill_values = [
                str(skill).strip()
                for skill in skill_list
                if str(skill).strip()
            ]

            if not skill_values:
                continue

            paragraph = document.add_paragraph()

            paragraph.paragraph_format.space_after = Pt(3)

            if category:
                category_run = paragraph.add_run(
                    f"{category}: "
                )

                category_run.bold = True
                category_run.font.name = "Arial"
                category_run.font.size = Pt(9.5)

            skills_run = paragraph.add_run(
                ", ".join(skill_values)
            )

            skills_run.font.name = "Arial"
            skills_run.font.size = Pt(9.5)

    # ---------------------------------------------------------
    # EXPERIENCE
    # ---------------------------------------------------------

    experience = rewritten_resume.get("experience", [])

    if experience:
        add_heading("Professional Experience")

        for job in experience:

            if not isinstance(job, dict):
                continue

            company = job.get("company", "")
            title = job.get("title", "")
            location = job.get("location", "")
            dates = job.get("dates", "")

            # Job header
            paragraph = document.add_paragraph()

            paragraph.paragraph_format.space_before = Pt(5)
            paragraph.paragraph_format.space_after = Pt(1)

            if title:
                title_run = paragraph.add_run(title)

                title_run.bold = True
                title_run.font.name = "Arial"
                title_run.font.size = Pt(10.5)

            if company:
                company_run = paragraph.add_run(
                    f" | {company}"
                )

                company_run.bold = True
                company_run.font.name = "Arial"
                company_run.font.size = Pt(10.5)

            # Location / dates
            metadata = []

            if location:
                metadata.append(location)

            if dates:
                metadata.append(dates)

            if metadata:

                paragraph = document.add_paragraph()

                paragraph.paragraph_format.space_after = Pt(3)

                run = paragraph.add_run(
                    " | ".join(metadata)
                )

                run.italic = True
                run.font.name = "Arial"
                run.font.size = Pt(8.5)

            # Job bullets
            bullets = job.get("bullets", [])

            if isinstance(bullets, list):

                for bullet in bullets:
                    add_bullet(bullet)

    # ---------------------------------------------------------
    # CERTIFICATIONS
    # ---------------------------------------------------------

    certifications = rewritten_resume.get(
        "certifications",
        []
    )

    if certifications:
        add_heading("Certifications")

        if isinstance(certifications, list):

            for certification in certifications:
                add_bullet(certification)

    # ---------------------------------------------------------
    # EDUCATION
    # ---------------------------------------------------------

    education = rewritten_resume.get(
        "education",
        []
    )

    if education:
        add_heading("Education")

        if isinstance(education, list):

            for education_item in education:

                if isinstance(education_item, dict):

                    degree = education_item.get(
                        "degree",
                        ""
                    )

                    institution = education_item.get(
                        "institution",
                        ""
                    )

                    details = education_item.get(
                        "details",
                        ""
                    )

                    text_parts = []

                    if degree:
                        text_parts.append(degree)

                    if institution:
                        text_parts.append(institution)

                    if details:
                        text_parts.append(details)

                    if text_parts:
                        add_bullet(
                            " | ".join(text_parts)
                        )

                else:
                    add_bullet(education_item)

    # ---------------------------------------------------------
    # ACHIEVEMENTS
    # ---------------------------------------------------------

    achievements = rewritten_resume.get(
        "achievements",
        []
    )

    if achievements:
        add_heading("Achievements")

        if isinstance(achievements, list):

            for achievement in achievements:
                add_bullet(achievement)

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    output_file = Path(output_path)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    document.save(output_file)

    return str(output_file.resolve())