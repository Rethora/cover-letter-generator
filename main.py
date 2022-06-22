from Driver import Driver, LinkedinDriver
from Job import Job

DEBUG = False

if __name__ == '__main__':
    driver = None
    linkedin_driver = None
    indeed_driver = None

    # TODO: write display messages in terminal for what's happening
    # TODO: ex: make sure the urls in urls.txt are good and resume is in root

    print(
        """
        Starting Cover Letter Writer...\n
        Make sure urls are formatted correctly inside urls.txt\n
        Make sure resume is in root directory with the name resume.pdf\n
        """
    )

    with open('./urls.txt', 'r') as file:
        for line in file.readlines():
            url = line.strip()
            d = None
            if 'linkedin' in url:
                if linkedin_driver is None:
                    print('Detected LinkedIn URL\nNeed to log in browse LinkedIn job postings...')
                    linkedin_driver = LinkedinDriver(debug=DEBUG)
                    linkedin_driver.login()
                d = linkedin_driver
            # elif 'indeed' in url:
            #     if indeed_driver is None:
            #         indeed_driver = IndeedDriver(debug=DEBUG)
            #     d = indeed_driver
            else:
                if driver is None:
                    driver = Driver(debug=DEBUG)
                d = driver
            print(f"\nGathering info for {url}...")
            Job(url, d)

    if driver is not None:
        driver.quit()
    if linkedin_driver is not None:
        linkedin_driver.quit()

    print('\nDone writing cover letters!\nResume with cover letter in /output folder')
