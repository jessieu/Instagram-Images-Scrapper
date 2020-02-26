# - *- coding: utf- 8 - *-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os # check path existence
from bs4 import BeautifulSoup
import requests
import shutil
from xlsxwriter import Workbook
import argparse

class App:
    def __init__(self, username, password, target_username, path):
        self.username = username
        self.password = password
        self.target_username = target_username
        self.path = path
        self.error = False
        self.all_images = []
        # self.driver = webdriver.Edge()
        # self.driver = webdriver.Chrome('D:/chromedriver.exe')
        self.driver = webdriver.Chrome('/home/weilan/Documents/jessieu/instagram-scrapper/chromedriver')
        self.main_url = 'https://www.instagram.com'
        self.driver.get(self.main_url)
        sleep(3)

        # login function
        self.log_in()

        sleep(2)

        # search target
        if self.error is False:
            self.open_target_profile()
        if self.error is False:
            self.scroll_down()
        if self.error is False:
            # check file existence - if not exists, make one
            if not os.path.exists(path):
                os.mkdir(path)
                self.downloading_images()
                self.downloading_captions()

        sleep(10)
        self.driver.close()


    def write_caption_to_excel_file(self, caption_path):
        workbook = Workbook(os.path.join(caption_path, 'captions.xlsx'))
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row, 0, 'Image Name') # row number , column number, value
        worksheet.write(row, 1, 'Caption')
        row += 1
        for index, image in enumerate(self.all_images):
            filename = 'image_' + str(index) + '.jpg'
            try:
                caption = image['alt']
            except KeyError:
                caption = 'No caption exists'
            worksheet.write(row, 0, filename)
            worksheet.write(row, 1, caption)
            row += 1
        workbook.close()

    def downloading_captions(self):
        caption_folder_path = os.path.join(self.path, 'captions')
        if not os.path.exists(caption_folder_path):
            os.mkdir(caption_folder_path)
        self.write_caption_to_excel_file(caption_folder_path)
        # for index, image in enumerate(self.all_images):
        #     try:
        #         caption = image['alt']
        #     except KeyError:
        #         caption = 'No caption exists for this image'
        #     file_name = 'caption_' + str(index) + '.txt'
        #     file_path = os.path.join(caption_folder_path, file_name)
        #     link = image['src']
        #     with open(file_path, 'wb') as file:
        #         file.write(str('link: ' + str(link) + '\n' + 'caption: ' + caption).encode())


    def downloading_images(self):
        print("Length of all images: {}".format(len(self.all_images)))
        for index, image in enumerate(self.all_images):
            filename = 'image_' + str(index) + '.jpg'
            # full path of image
            image_path = os.path.join(self.path, filename)
            link = image['src']

            # grap the link and store to hard disk
            response = requests.get(link, stream=True)

            try:
                with open(image_path, 'wb') as file:
                    shutil.copyfileobj(response.raw, file)

            except Exception as e:
                print(e)
                print("Could not download image number ", index)
                print("Image link ---->", link)

    def scroll_down(self):
        try:
            # Whether it can scrape all images or not really depends on the network speed
            SCROLL_PAUSE_TIME = 2

            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while True:
                # soup = BeautifulSoup(self.driver.page_source, 'lxml')
                for image in soup.find_all('img'):
                    self.all_images.append(image)
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

        except Exception as e:
            print(e)
            print("Could not find the post")
            self.error = True

    def open_target_profile (self):
        try:
            # short hint that describes the expected value of a search field - it's reliable than using class or id
            search_bar = self.driver.find_element_by_xpath("//input[@placeholder='Search']")
            search_bar.send_keys(self.target_username)
            # can be improved by clicking the search results
            target_profile_url = self.main_url + '/' + self.target_username + '/'
            self.driver.get(target_profile_url)
            sleep(3)
        except Exception as e:
            self.error = True
            print(e)
            print("Cannot open user profile")

    def log_in(self):
        try:
            # go to the login page
            login_button = self.driver.find_element_by_xpath('//p[@class="izU2O"]/a')
            login_button.click()

            sleep(2)

            try:
                # username input
                user_name_input = self.driver.find_element_by_xpath("//input[@name='username']")
                user_name_input.send_keys(self.username)

                sleep(2)
                # password input
                user_password_input = self.driver.find_element_by_xpath("//input[@name='password']")
                user_password_input.send_keys(self.password)

                # click the login button - can also use user_password_input
                user_name_input.submit()
                # alternative in case of suspicious activities detected by Chrome
                # submit = self.driver.find_element_by_tag_name('form')
                # submit.submit()
            except Exception as e:
                print(e)
                print("Error occurred in finding the field of username/password")
        except Exception as e:
            self.error = True
            print(e)
            print("Unable to find login buttons")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Take instagram account username, password and target username")

    parser.add_argument("username", help="Account username", action="store")
    parser.add_argument("password", help="Account password", action="store")
    parser.add_argument("target_username", help="Searching target username", action="store")
    parser.add_argument("path", help="Path to store the image", action="store")
    args = parser.parse_args()

    app = App(args.username, args.password, args.target_username, args.path)
