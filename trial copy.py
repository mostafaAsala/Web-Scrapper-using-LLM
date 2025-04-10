import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

def get_driver(browser="chrome"):
    if browser.lower() == "chrome":
        # Set Chrome options
        options = webdriver.ChromeOptions()
        
        # Disable browser extensions
        options.add_argument("--disable-extensions")
        
        # Enable headless mode
        #options.add_argument("--headless")
        
        # Disable GPU hardware acceleration
        options.add_argument("--disable-gpu")
        
        # Disable images
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        
        # Disable JavaScript
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
        
        # Disable logging
        options.add_argument("--log-level=3")
        
        # Specify path to chromedriver (change the path if necessary)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    elif browser.lower() == "orig chrome":
        # Set Chrome options
        options = uc.ChromeOptions()
        
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    elif browser.lower() == "undetected_chrome":
         # Set Chrome options
        options = uc.ChromeOptions()
        
        # Disable browser extensions
        options.add_argument("--disable-extensions")
        
        # Enable headless mode
        #options.add_argument("--headless")
        
        # Disable GPU hardware acceleration
        options.add_argument("--disable-gpu")
        
        # Disable images
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        
        # Disable JavaScript
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
        
        # Disable logging
        options.add_argument("--log-level=3")
        
        # Use undetected-chromedriver and ChromeDriverManager to automatically manage and install ChromeDriver
        driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
    elif browser.lower() == "firefox":
        # Set Firefox options
        options = webdriver.FirefoxOptions()
        
        # Disable browser extensions
        options.set_preference("extensions.enabled", False)
        
        # Enable headless mode
        options.add_argument("--headless")
        
        # Disable GPU hardware acceleration
        options.set_preference("layers.acceleration.disabled", True)
        
        # Disable images
        options.set_preference("permissions.default.image", 2)
        
        # Disable JavaScript
        options.set_preference("javascript.enabled", False)
        
        # Disable logging
        options.set_preference("devtools.console.stdout.content", False)
        
        # Specify path to geckodriver (change the path if necessary)
        driver = webdriver.Firefox(service=FirefoxService("/path/to/geckodriver"), options=options)
    
    else:
        raise ValueError("Invalid browser name. Use 'chrome' or 'firefox'.")
    
    return driver


x = datetime.datetime.now()

# Choose the browser ('chrome' or 'firefox')
driver = get_driver(browser="orig chrome")
# Navigate to a webpage
driver.get('https://www.mitaccomputing.com/en/Search')
# Do your actions here...
# Example: print the title of the page
print(driver.title)
print(datetime.datetime.now()-x)
# Close the browser
driver.quit()
