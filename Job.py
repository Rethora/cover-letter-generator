from PDF import CoverLetter
from PyPDF2 import PdfFileMerger, PdfFileReader
from urllib.parse import urlparse
import settings


class Job:
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver

        self.company_name = None
        self.recruiter_name = None
        self.languages = None
        self.frameworks = None
        self.additional_technologies = None
        self.strengths = None

        self.initialize()
        self.write_cover_letter()
        self.attach_cover_letter()

    # wrap call in try catch block in main.py
    def initialize(self):
        """
        Initializes class with all info about job

        :return: None
        """
        self.driver.initialize(self.url)
        self.company_name = self.driver.get_company_name()
        self.recruiter_name = self.driver.get_recruiter_name()
        self.languages = self.driver.find_languages()
        self.frameworks = self.driver.find_frameworks()
        self.additional_technologies = self.driver.find_additional_technologies()
        self.strengths = sorted(set(self.driver.find_strengths()))

    # TODO: make method that filters any possible duplicate findings

    def write_cover_letter(self):
        """
        Write the cover letter for the job description.
        :return: None
        """
        letter = CoverLetter()
        letter.write_name(settings.name)
        letter.write_sub_header(settings.location, settings.phone_number, settings.email)
        letter.write_date()
        letter.write_greeting(self.recruiter_name)
        letter.write_first_paragraph(self.get_domain(), strengths=self.stringify_skills(self.strengths),
                                     position=settings.position)
        letter.write_second_paragraph()
        letter.write_third_paragraph()
        letter.write_list(sorted(set(self.languages + self.frameworks + self.additional_technologies)))
        letter.write_fourth_paragraph(settings.phone_number, position=settings.position, email=settings.email)
        letter.write_outro()
        letter.sign_bottom(settings.name)
        letter.output('./tmp/cover-letter.pdf')

    def attach_cover_letter(self):
        """Takes the resume located at ./resume.pdf and attaches the newly created cover letter.
        Saves to ./output folder"""
        merger = PdfFileMerger()

        merger.append(PdfFileReader(open('./resume.pdf', 'rb')))
        merger.append(PdfFileReader(open('./tmp/cover-letter.pdf', 'rb')))

        merger.write(f"./output/{(settings.name + '_' + self.company_name).replace(' ', '_')}_Resume.pdf")

    @staticmethod
    def stringify_skills(match_list):
        """
        Converts list of skills and languages to usable string for cover letter

        :returns: String of skills appended together by commas and 'and'. If length of list is 0 returns None
        """
        if len(match_list) == 0:
            return None
        res = ''
        if len(match_list) == 1:
            res += match_list[0].lower()
        elif len(match_list) == 2:
            res += f"{match_list[0].lower()} and {match_list[1].lower()}"
        elif len(match_list) > 2:
            for i, item in enumerate(match_list):
                if i < len(match_list) - 1:
                    res += item.lower() + ', '
                else:
                    res += 'and ' + item.lower()
        return res

    def get_domain(self):
        """Get the domain of the url from the job posting."""
        return urlparse(self.url).netloc
