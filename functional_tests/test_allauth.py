# -*- coding: utf-8 -*-

import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate


class TestGoogleLogin(StaticLiveServerTestCase):
    
    fixtures = ['allauth_fixture']

    def setUp(self):
        username=os.getenv("SAUCE_USERNAME","NONE")
        if (username!="NONE"): # travis-ci with saucelabs
            accesskey=os.getenv("SAUCE_ACCESS_KEY","NONE")
            sauce_url = "http://"+username+":"+accesskey+"@ondemand.saucelabs.com:80/wd/hub"
            
            desired_capabilities = {
                'platform': "Mac OS X 10.9", # 
                'browserName': "chrome",
                'version': "31",  
                'tunnel-identifier': os.environ['TRAVIS_JOB_NUMBER'], # important!!
            }
            self.browser= webdriver.Remote(desired_capabilities=desired_capabilities,
                                      command_executor=sauce_url)            
        else:
            self.browser = webdriver.Firefox()
            
        self.browser.implicitly_wait(3)
        self.browser.wait = WebDriverWait(self.browser, 10)
        activate('en')

    def tearDown(self):
        self.browser.quit()

    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
            (By.ID, element_id)))

    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
            (By.ID, element_id)))

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)
    
    def user_login(self):
        import json
        with open("taskbuster/fixtures/google_user.json") as f:
            credentials = json.loads(f.read())
        for key, value in credentials.items():
            self.get_element_by_id(key).send_keys(value)
        for btn in ["signIn", "submit_approve_access"]:
            self.get_button_by_id(btn).click()
        return    

    def test_google_login(self):
        self.browser.get(self.get_full_url("home"))
        google_login = self.get_element_by_id("google_login")
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(
            google_login.get_attribute("href"),
            self.live_server_url + "/accounts/google/login")
        
        google_login.click()
        # do not continue beyond this point in Travis. Google does not like it. 
        if (os.getenv('TRAVIS_JOB_NUMBER','NONE')!='NONE'):
            return 
        self.user_login()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
        google_logout = self.get_element_by_id("logout")
        google_logout.click()
        confirm= self.browser.find_element_by_xpath("//body/form/button") #fix me later: too non-specific
        confirm.click()
        google_login = self.get_element_by_id("google_login")