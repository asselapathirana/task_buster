# -*- coding: utf-8 -*-
from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip
import re


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
    
    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)    

    
    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn("TaskBuster", self.browser.title)
        
    
    def test_h1_css(self):
            self.browser.get(self.get_full_url("home"))
            h1 = self.browser.find_element_by_tag_name("h1")
            self.assertEqual(h1.value_of_css_property("color"),
                             "rgba(200, 50, 255, 1)")
           
    def test_home_files(self):
        self.browser.get(self.live_server_url + "/robots.txt")
        self.assertNotIn("Not Found", self.browser.title)
        self.assertEqual("",self.browser.title)
        self.browser.get(self.live_server_url + "/humans.txt")
        self.assertNotIn("Not Found", self.browser.title) 
        self.assertEqual("",self.browser.title)
    
    def test_favicon(self):
        self.browser.get(self.get_full_url("home"))
        links=self.browser.find_elements_by_xpath("//head/link")
        p=re.compile('.+favicon.ico$')
        link=[x for x in links if p.match(x.get_attribute(name='href'))][0]
        self.assertEqual(link.get_attribute(name='rel'),"shortcut icon")
        a=link.get_attribute(name='href')
        self.browser.get(a)
        self.assertIn("favicon.ico",self.browser.title)
        self.assertNotIn("Not Found", self.browser.title)         


 
  
# DO not use direct calling to run these. The main below is only for exploratory coding.   
if __name__=="__main__":
    print ("WARNING: This is not the way to run tests!! (use ./manage.py test ..)")
    nw=NewVisitorTest()
    nw.setUp()
    nw.browser.get("http://localhost:8000/")
    links=nw.browser.find_elements_by_xpath("//head/link")
    p=re.compile('.+favicon.ico$')
    link=[x for x in links if p.match(x.get_attribute(name='href'))][0]
    nw.assertRegex(link.get_attribute(name='rel'),"shortcut icon")    
    response=nw.client.get(link.get_attribute(name='href'))
    nw.assertContains(response,None,status_code=200)    
    nw.tearDown()
    
    

        
