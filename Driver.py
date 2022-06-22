from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import getpass
import settings


class Driver(webdriver.Firefox):
    def __init__(self, debug: bool = True, *args, **kwargs):
        options = Options()
        if debug is False:
            options.headless = True
        service = Service(GeckoDriverManager().install())
        super().__init__(options=options, service=service, *args, **kwargs)
        self.maximize_window()
        self.soup = None
        self.document_text = None

    def initialize(self, url: str):
        """Initialize/reinitialize driver for every job.
        Use soup for extracting text when elements can't be found"""
        self.get(url)

    def get_company_name(self):
        """Returns the name of the hiring company"""
        return None

    def get_recruiter_name(self):
        """Returns the name of the recruiter.
        Defaults to 'Hiring Manager/Recruiter'
        """
        return 'Hiring Manager/Recruiter'

    def find_languages(self):
        """Get the languages that match document and settings.py."""
        return self.get_matches(settings.languages)

    def find_frameworks(self):
        """Return a list of frameworks that match document and settings.py"""
        return self.get_matches(settings.frameworks_and_libraries)

    def find_additional_technologies(self):
        """Return a list of additional technologies that match document and settings.py"""
        return self.get_matches(settings.additional_technologies)

    def find_strengths(self):
        """Return a list of strengths that match document and settings.py"""
        return self.get_matches(settings.strengths)

    def get_matches(self, to_match):
        """Helper to look through lists in settings.py and find matches in document text."""
        res = []
        for item in to_match:
            for line in self.document_text.splitlines():
                if item.lower() in line.lower():
                    if line not in res and len(line) <= 100:
                        res.append(line.replace('•', '').replace('.', '').strip())
        return res


class LinkedinDriver(Driver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logged_in = False
        self.email = None
        self.password = None

    def initialize(self, url: str):
        self.get(url)
        # try to expand job description if on single view page
        try:
            self.find_element(
                by=By.XPATH, value='/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[2]/footer/button').click()
        except NoSuchElementException:
            pass

        try:
            self.find_element(
                by=By.XPATH, value='/html/body/div[6]/aside/div[1]/header/div[3]/button[2]'
            ).click()
        except NoSuchElementException:
            pass

        self.document_text = self.find_element(by=By.CLASS_NAME, value='jobs-description__container').text

    def login(self):
        """Prompts user to log in to their LinkedIn Account so driver is able to access posting url"""
        email = None
        password = None
        self.get('https://www.linkedin.com/login')

        while not self.logged_in:
            email = input('\nEnter your LinkedIn email: ')
            password = getpass.getpass(prompt='Enter your LinkedIn Password: ', stream=None)

            email_input = self.find_element(by=By.XPATH, value='//*[@id="username"]')
            email_input.clear()
            email_input.send_keys(email)

            password_input = self.find_element(by=By.XPATH, value='//*[@id="password"]')
            password_input.clear()
            password_input.send_keys(password)

            self.find_element(by=By.XPATH, value='/html/body/div/main/div[2]/div[1]/form/div[3]/button').click()

            if 'linkedin.com/feed' in self.current_url:
                self.logged_in = True
            else:
                print('\nInvalid Login, Try Again...\n')

        self.email = email
        self.password = password

    def get_recruiter_name(self):
        try:
            return self.find_element(by=By.CLASS_NAME, value='jobs-poster__name').text
        except NoSuchElementException:
            pass
        try:
            for line in self.find_element(by=By.CLASS_NAME,
                                          value='jobs-unified-top-card__content--two-pane').text.splitlines():
                if 'is hiring for this job' in line.lower():
                    return line.split('is')[0].strip()
        except (NoSuchElementException, AttributeError):
            pass
        return 'Hiring Manager/Recruiter'

    def get_company_name(self):
        """Return the name of the company. Returns an empty string if no company name was found."""
        try:
            return self.find_element(
                by=By.XPATH,
                value='/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[2]/div/div[2]/div[1]/div/div['
                      '1]/div/div[2]/div[1]/span[1]/span[1]/a '
            ).text
        except NoSuchElementException:
            pass
        try:
            parent = self.find_element(by=By.CLASS_NAME, value='jobs-unified-top-card__subtitle-primary-grouping')
            return parent.find_element(by=By.TAG_NAME, value='span').text
        except NoSuchElementException:
            pass
        return ''

# Tests
# d = IndeedDriver()
# d.initialize('https://www.indeed.com/viewjob?from=app-tracker-saved-appcard&hl=en&jk=fcb4ae6c369e394d&tk=1g3d2boklr08l800')
# print(d.get_company_name())
# d.quit()
# d = Driver()
# d.initialize('https://www.indeed.com/viewjob?from=app-tracker-saved-appcard&hl=en&jk=2a340961d478975d&tk=1g3d1lmiqr04q800')
# lines = d.get_lines_by_substring('c++')
# # print(f"\n# of lines {len(lines)}\n")
# # for line in lines:
# #     print(line)
# d.quit()
