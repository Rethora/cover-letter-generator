from fpdf import FPDF
from datetime import datetime


class CoverLetter(FPDF):
    """CoverLetter Generation Class"""

    def __init__(self):
        super().__init__()
        self.page_size = 190
        self.page_margin = 20
        self.width = self.page_size - self.page_margin
        self.cl_fonts = {
            'heading': 'Arial',
            'subheading': 'Arial',
            'text': 'Times',
            'signature': 'Arial'
        }
        self.set_top_margin(self.page_margin)
        self.set_left_margin(self.page_margin)
        self.add_font("Arial", "", "arial.ttf", uni=True)
        self.set_font('Arial', size=12)
        self.add_page()

    def write_name(self, name: str):
        """
        Writes the name centered on the cover letter at the top.

        :param name: The name of the applicant
        :return: None
        """
        self.set_font('', size=16)
        self.cell(self.width, 5, txt=name, ln=1, align='C')

    def write_sub_header(self, location: str, phone: str, email: str):
        """
        Writes the location, phone number and email of the applicant under their name.

        :param location: The location of where the applicant lives
        :param phone: The contact phone number of the applicant
        :param email: The contact email of the applicant
        :return: None
        """
        formatted_text = f"{location} · {phone} · {email}"
        self.set_font('', size=8)
        self.cell(self.width, 10, txt=formatted_text, ln=1, align='C')

    def write_date(self):
        """
        Writes the current date on the cover letter.

        :return: None
        """
        self.set_font('', size=10)
        date = datetime.now()
        formatted_date = date.strftime('%b %d, %Y')
        self.cell(self.width, 15, txt=formatted_date, ln=1, align='L')

    def write_greeting(self, recruiter_name: str):
        """
        Writes the greeting to whoever is reading the cover letter.

        :param recruiter_name: The name of the recruiter to greet
        :return: None
        """
        greeting = f"Dear {recruiter_name},"
        self.cell(self.width, 10, txt=greeting, ln=1, align='L')

    def write_first_paragraph(self, domain: str,  strengths: str, position: str = 'Software Developer'):
        """
        Writes the first paragraph of the cover letter.

        :param domain: The name of the domain where the job posting was listed
        :param position: The title of the position that the applicant is applying for
        :param strengths: The skills that match the job description and settings.py
        :return: None
        """
        self.ln()
        interest_sent = f"This letter is to express my interest in your posting on {domain} for an experienced {position}. "
        if strengths is None:
            strengths_sent = ''
        else:
            strengths_sent = f"I have {strengths}. "
        closing_sent = "I am confident I can be an asset to your organization. "

        paragraph = interest_sent + strengths_sent + closing_sent
        self.multi_cell(self.width, 7, txt=paragraph)

    def write_second_paragraph(self):
        """Writes the second paragraph of the cover letter."""
        self.ln()
        sent = 'I enjoy being challenged and engaging with projects that require me to work outside my comfort and ' \
               'knowledge set, as continuing to learn new languages and development techniques are important to me ' \
               'and the success of your organization. '
        paragraph = sent
        # self.set_font(self.cl_fonts['text'], size=12)
        self.multi_cell(self.width, 7, txt=paragraph)

    def write_third_paragraph(self):
        """Writes the third paragraph of the cover letter."""
        # TODO: List could potentially be empty.
        # TODO: Combine this method and the one below to make a bullshit list if it is empty
        self.ln()
        sent = 'Your listed requirements closely match my background and skills. A few I would like to highlight that ' \
               'would enable me to contribute to your bottom line are: '
        paragraph = sent
        self.multi_cell(self.width, 7, txt=paragraph)

    def write_list(self, skills: list):
        """
        Writes a bulleted list of from list

        :param skills: the list of items to write to the cover letter
        """
        self.ln()
        for item in skills:
            self.multi_cell(self.width, 7, txt=' ' * 8 + '· ' + item)

    def write_fourth_paragraph(self, phone: str, email: str, position: str = 'Software Developer'):
        """
        Writes the fourth paragraph to the cover letter.

        :param email: The email of the applicant
        :param phone: The phone number of the applicant
        :param position: The position that the applicant is applying for. Defaults to Software Developer
        :return: None
        """
        self.ln()
        first_sent = f"I've attached a copy of my resume that details my projects and experience as a {position}. "
        second_sent = f"I can be reached anytime via my cell phone, {phone} or via email at {email}."
        paragraph = first_sent + second_sent
        self.multi_cell(self.width, 7, txt=paragraph)

    def write_outro(self):
        """Write the cover letter outro"""
        self.ln()
        sent = 'Thank you for your time and consideration. I look forward to speaking with you about this opportunity.'
        paragraph = sent
        self.multi_cell(self.width, 7, txt=paragraph)

    def sign_bottom(self, name: str):
        """
        Signs the bottom of the cover letter with the name of the applicant.

        :param name: The name of the applicant
        """
        self.ln()
        """Sign the bottom of the cover letter with applicant's name.

        :param name: The name of the applicant
        :return: None
        """
        self.cell(self.width, 7, ln=1, txt='Sincerely,')
        self.cell(self.width, 7, ln=1, txt=name)

# Tests
# pn = '012-345-6789'
# e = 'person@email.com'
# test = CoverLetter()
# test.write_name('Billy Bob')
# test.write_sub_header('San Diego, CA', pn, e)
# test.write_date()
# test.write_greeting('Joe Mama')
# test.write_first_paragraph('Linkedin', 'Software Engineer', 'React, TypeScript, Ruby and Ruby on Rails', 3)
# test.write_second_paragraph()
# test.write_third_paragraph()
# test.write_list(['One', 'Two', 'Three'])
# test.write_fourth_paragraph(pn, e, 'Software Engineer')
# test.write_outro()
# test.sign_bottom('Billy Bob')
# test.output('./tmp/tmp-cover-letter.pdf')
