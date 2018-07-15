
import datetime
import os.path
import sys
import uuid
import eventqueue
import PerfStat

from PerfStat import *
from eventqueue import *

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import TimeoutException
#ref: https://stackoverflow.com/questions/26566799/how-to-wait-until-the-page-is-loaded-with-selenium-for-python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#runs the performance test client using the given paramters
class PerfClient:
    def __init__(self, driver_path, root_url, username, password, timeout=30, client=None, headless=False, queue_connection_string=None):        
        self.queue = None
        self.client = client

        if self.client is None:
            self.client = uuid.uuid4()

        if queue_connection_string is not None and len(queue_connection_string) > 0:
            self.queue = EventQueue(queue_connection_string)

        #create the web driver
        options = webdriver.ChromeOptions()
        self.headless = headless
        if self.headless:
            # linux chromium argumets
            options.set_headless(headless=True)
            options.add_argument('--enable-logging')
            options.add_argument('--v=10000')
            options.add_argument('--no-sandbox')
            #options.add_argument('--headless')
            #options.add_argument('--no-sandbox')

        print('Root url: {0}, Chrome Driver: {1}, timeout: {2}'.format(root_url, driver_path, timeout))    
        #service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
        self.driver = webdriver.Chrome(executable_path=driver_path,chrome_options=options)
        #self.driver = webdriver.Chrome(executable_path=driver_path,chrome_options=options)
        self.root_url = root_url

        self.timeout = timeout
        self.driver.implicitly_wait(timeout)
        self.driver.maximize_window()
        self.username = username
        self.password = password

    #navigate to the url
    def navigate(self, url):
        id = uuid.uuid4()
        start = datetime.now()
        self.driver.get(url)

        stat = PerfStat(self.root_url, self.username, 'navigate',OpType.read, start, datetime.now(), self.client, id)
        return stat
    
    def runCommand(self, command, target, value):
        start = datetime.now()
        optype = OpType.read

        #run the requested operation
        if command == 'open':
            #navigate
            url = target
            if target.startswith('/'):
                url = '{0}{1}'.format(self.root_url, target)

            print('Get: {0}'.format(url))
            self.driver.get(url)            
        elif command.startswith('click'):
            action = ActionChains(self.driver)

            el = self.findElement(target)
            #exec the click command
            action.move_to_element(el)
            action.click()
            action.perform()

            if command == 'click':
                optype = OpType.post
            #el.click()
        elif command == 'type':
            el = self.findElement(target)

            if target == 'id=username' or target == 'id=login':
                el.send_keys(self.username)
            elif target == 'id=password' or target == 'id=pass':
                el.send_keys(self.password)
            else:    
                el.send_keys(value)
        elif command == 'mouseOver' and not self.headless:
            action = ActionChains(self.driver)
            
            el = self.findElement(target)
            action.move_to_element(el)
            action.perform()
        elif command == 'mouseOut':
            action = ActionChains(self.driver)
            
            el = self.findElement(target)
            action.move_to_element_with_offset(el, -10,-10)
            action.perform()            
        else:
            #we havent mapped this command yet
            raise Exception('Unknown command: {0}'.format(command))

        #return the status 
        pstat = PerfStat(self.root_url, self.username, command, optype, start, datetime.now(), target, self.client)

        #send the message if needed
        self.send_pstat_msg(pstat)

        return pstat

    #find the DOM element
    def findElement(self, target):
        id = ''
        element = None

        self.waitForElement(target)

        #find the element
        if target.startswith('id='):
            id = target[3:]
            element = self.driver.find_element_by_id(id)
        elif target.startswith('css='):
            id = target[4:]
            element = self.driver.find_element_by_css_selector(id)
        elif target.startswith('//') or target.startswith('./'):
            element = self.driver.find_element_by_xpath(target)
        elif target.startswith("xpath="):
            id = target[6:]
            element = self.driver.find_element_by_xpath(id)
        else:
            raise Exception('Unknown element mapping {0}'.format(target))

        return element

    #wait for the element to appear in the DOM
    def waitForElement(self, target):
        id = ''
        element = None

        #find the element
        if target.startswith('id='):
            id = target[3:]
            element = EC.presence_of_element_located((By.ID, id))
        elif target.startswith('css='):
            id = target[4:]
            element = EC.presence_of_element_located((By.CSS_SELECTOR, id))
        elif target.startswith('//') or target.startswith('./'):
            element = EC.presence_of_element_located((By.XPATH, target))
        elif target.startswith("xpath="):
            id = target[6:]
            element = EC.presence_of_element_located((By.XPATH, id))
        else:
            raise Exception('Unknown element mapping {0}'.format(target))

        # wait for the element to exists
        WebDriverWait(self.driver, self.timeout).until(element)

    def viewSource(self):
        self.driver.page_source

    #sends the message to event hub
    def send_pstat_msg(self, pstat):
        result = ''
        if self.queue is not None:
            result = self.queue.send(pstat.json())

        if len(result) > 0:
            print('message sent: {0}'.format(result))

    def close(self):
        self.driver.close()
