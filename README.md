## Instagram Images Scrapper

### Overview

This project scrapes images from target Instagram user (Need to have an Instagram account beforehand)

Technologies used:

- Python
- Selenium WebDriver
- BeautifulSoup

### Challenges

- Cannot scroll down 
  - The tutorial is to find the total number of images by searching the `post` element and pre-calculate the number of iterations we need to scroll down the page => It doesn't work for me

  - Stack overflow solution for indefinite scroll down works half way down
    - I extend the pause time for loading page
    - And...It really depends on the network speed. Once the loading takes more than the pause time I set, the scroll down will stop and scraper would start to fetch current image and process next steps.
- Chrome and Safari do not work well...Maybe is the problem of setting
  - Chrome keep reporting that current action as suspicious and asking me to verify my action for each time I automate the web browser opening and Instagram login
  - And it also runs really fast, it simply skips the username input and jumps to the password directly -- I have to let it sleep for a few second after clicking the login button
  - Safari is similar. It does not click on the login button and what's weird is it jumps to a signup page.
- Edge had some problems, but in general, it is okay with repeatedly testing.

### Further Improvement

- *Add a logout function before close the webdriver.* Since the code testing includes login function, each time before I run the program,  I have to manually logout.
- *Identify the current state, login already or not.*  It is an alternative for the previous situation. No need to logout each time, instead, detect the current state. If user login already, do the search directly and skip the login.
- Accept user-defined limit of images.
- Use fake_agent to test such that user's personal information would not be leaked. 