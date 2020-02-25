## Web Scraping with Python

#### Projects

- Project1 - scrape a product list and links from consumer report website  

- Project2 - scrape all Java coding problem statements and example from coding bat

- Project3 - scrape images from target Instagram user (Need to use your own Instagram account)
  - Some problems I got in project3:
    - Cannot scroll down 
      - The tutorial is to find the total number of images by searching the `post` element and pre-calculate the number of iterations we need to scroll down the page => It doesn't work for me

      - Stack overflow solution for indefinite scroll down works half way down
        - I extend the pause time for loading page
        - And...It really depends on the network speed. Once the loading takes more than the pause time I set, the scroll down will stop and scraper would start to fetch current image and process next steps.
    - Chrome and Safari do not work well...Maybe is the problem of setting
      - Chrome keep reporting that my action as suspicious and asking me to verify my action - super annoying
        - And it also runs really fast, it simply skips the username input and jumps to the password directly -- I have to let it sleep for a few second after clicking the login button
      - Safari is similar. It does not click on the login button and what's weird is it jumps to a signup page.
    - Edge is not perfect, as well.

  - What I want to improve:
    - Add a logout function before close the webdriver so that I don't have to manually logout each time.
    - Wait for the server response so that all images can be loaded even if the network connection is poor
    - Use fake_agent so that I don't have to use my own account. 
