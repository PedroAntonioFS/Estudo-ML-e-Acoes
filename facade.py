from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class SeleniumFacade:
    @staticmethod
    def open_with_firefox(driver_path='C:\Windows'):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=r'{}\geckodriver.exe'.format(driver_path), options=firefox_options)

        return driver
    
    @staticmethod
    def get(driver, url):
        driver.get(url)

    @staticmethod
    def close(driver):
        driver.close()

    @staticmethod
    def click_button(section, xpath):
        elem = LocatingFacade.find_element(section, xpath)
        elem.click()

class WebDriverWaitFacade:
    @staticmethod
    def setup(driver, time):
        return WebDriverWait(driver, time)

    @staticmethod
    def wait_until_clickable(wait, xpath):
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    @staticmethod
    def wait_until_visible(wait, xpath):
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

class DriverFacade:

    @staticmethod
    def switch_to_frame(driver, xpath):
        frame = driver.find_element(By.XPATH, xpath)
        driver.switch_to.frame(frame)

    @staticmethod
    def switch_to_parent(driver):
        driver.switch_to.parent_frame()

class LocatingFacade:
    @staticmethod
    def find_element(section, xpath):
        return section.find_element(By.XPATH, xpath)
    
    @staticmethod   
    def get_children(section):
        return section.find_elements(By.XPATH, "*")

class ExceptionsFacade:
    @staticmethod
    def get_NoSuchElementException():
        return NoSuchElementException

    @staticmethod
    def get_TimeoutException():
        return TimeoutException