import json
import os
import requests
import cloudscraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import time
import logging

class WebScraper:
    def __init__(self, config_path):
        self.all_configs = self._load_config(config_path)
        self.logger = self._setup_logger()
        
    def _load_config(self, config_path):
        """Load the scraper configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load configuration: {str(e)}")
    
    def _setup_logger(self):
        """Setup logging for the scraper."""
        logger = logging.getLogger("web_scraper")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def get_site_config(self, site_name):
        """Get configuration for a specific site by name."""
        for site_config in self.all_configs.get('sites', []):
            if site_config.get('name') == site_name:
                return site_config
        return None
    
    def _get_chrome_driver(self, chrome_options_config):
        """Configure and return a Chrome driver based on options."""
        options = webdriver.ChromeOptions()
        
        if chrome_options_config.get('disable_extensions', False):
            options.add_argument("--disable-extensions")
        
        if chrome_options_config.get('headless', False):
            options.add_argument("--headless")
        
        if chrome_options_config.get('disable_gpu', False):
            options.add_argument("--disable-gpu")
        
        if chrome_options_config.get('log_level', None):
            options.add_argument(f"--log-level={chrome_options_config.get('log_level')}")
        
        prefs = {}
        if chrome_options_config.get('disable_images', False):
            prefs["profile.managed_default_content_settings.images"] = 2
        
        if chrome_options_config.get('disable_javascript', False):
            prefs["profile.managed_default_content_settings.javascript"] = 2
        
        if prefs:
            options.add_experimental_option("prefs", prefs)
        
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    def _get_undetected_chrome_driver(self, chrome_options_config):
        """Configure and return an undetected Chrome driver based on options."""
        options = uc.ChromeOptions()
        
        if chrome_options_config.get('disable_extensions', False):
            options.add_argument("--disable-extensions")
        
        if chrome_options_config.get('headless', False):
            options.add_argument("--headless")
        
        if chrome_options_config.get('disable_gpu', False):
            options.add_argument("--disable-gpu")
        
        if chrome_options_config.get('log_level', None):
            options.add_argument(f"--log-level={chrome_options_config.get('log_level')}")
        
        prefs = {}
        if chrome_options_config.get('disable_images', False):
            prefs["profile.managed_default_content_settings.images"] = 2
        
        if chrome_options_config.get('disable_javascript', False):
            prefs["profile.managed_default_content_settings.javascript"] = 2
        
        if prefs:
            options.add_experimental_option("prefs", prefs)
        
        return uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    def search_by_url(self, site_config, part_number):
        """Search by replacing keywords in URL."""
        if 'url_search' not in site_config:
            self.logger.error(f"URL search configuration not found for site {site_config.get('name')}")
            return None
            
        url_config = site_config['url_search']
        url = url_config['url']
        keyword = url_config.get('keyword', 'WDA_PARTNUMBER')
        
        # Replace the keyword with the part number
        search_url = url.replace(keyword, part_number)
        self.logger.info(f"Searching URL: {search_url}")
        
        connection_library = site_config.get('connection_library', 'requests').lower()
        
        try:
            if connection_library == 'requests':
                response = requests.get(search_url)
                content = response.text
            elif connection_library == 'cloudscraper':
                scraper = cloudscraper.create_scraper()
                response = scraper.get(search_url)
                content = response.text
            elif connection_library == 'selenium':
                chrome_options = site_config.get('chrome_options', {})
                driver_type = chrome_options.get('driver_type', 'chrome')
                
                if driver_type == 'undetected_chrome':
                    driver = self._get_undetected_chrome_driver(chrome_options)
                else:
                    driver = self._get_chrome_driver(chrome_options)
                
                try:
                    driver.get(search_url)
                    time.sleep(2)  # Wait for page to load
                    content = driver.page_source
                finally:
                    driver.quit()
            else:
                self.logger.error(f"Unknown connection library: {connection_library}")
                return None
            
            # Save the result if configured
            if site_config.get('output', {}).get('save_html', False):
                self._save_result(site_config, part_number, content)
            
            return content
        except Exception as e:
            self.logger.error(f"Error during URL search: {str(e)}")
            return None
    
    def search_by_form(self, site_config, search_term):
        """Search using a form on the website."""
        if 'form_search' not in site_config:
            self.logger.error(f"Form search configuration not found for site {site_config.get('name')}")
            return None
            
        form_config = site_config['form_search']
        url = form_config['url']
        search_input_xpath = form_config.get('search_input_xpath')
        submit_button_xpath = form_config.get('submit_button_xpath')
        
        if not search_input_xpath or not submit_button_xpath:
            self.logger.error("Missing XPath configuration for form search")
            return None
        
        # Get Chrome options from config
        chrome_options_config = form_config.get('chrome_options', {})
        driver_type = chrome_options_config.get('driver_type', 'chrome')
        
        if driver_type == 'undetected_chrome':
            driver = self._get_undetected_chrome_driver(chrome_options_config)
        else:
            driver = self._get_chrome_driver(chrome_options_config)
        
        try:
            # Navigate to the page
            driver.get(url)
            time.sleep(2)  # Wait for page to load
            
            # Find and fill the search input
            search_input = driver.find_element(By.XPATH, search_input_xpath)
            search_input.clear()
            search_input.send_keys(search_term)
            
            # Find and click the submit button
            submit_button = driver.find_element(By.XPATH, submit_button_xpath)
            submit_button.click()
            
            # Wait for results page to load
            time.sleep(3)
            
            # Get the page content
            page_content = driver.page_source
            
            # Save the result if configured
            if site_config.get('output', {}).get('save_html', False):
                self._save_result(site_config, search_term, page_content)
                
            return page_content
            
        except Exception as e:
            self.logger.error(f"Error during form search: {str(e)}")
            return None
        finally:
            driver.quit()

    def search_by_post(self, site_config, part_number):
        """Search using POST request with data payload."""
        if 'post_search' not in site_config:
            self.logger.error(f"POST search configuration not found for site {site_config.get('name')}")
            return None
        
        post_config = site_config['post_search']
        url = post_config['url']
        data_field = post_config.get('data_field', 'search')
        headers = post_config.get('headers', {})
        
        # Create data payload
        data = {
            data_field: part_number
        }
        
        self.logger.info(f"Performing POST search to {url} with data: {data}")
        
        connection_library = site_config.get('connection_library', 'requests').lower()
        
        try:
            if connection_library == 'requests':
                response = requests.post(url, headers=headers, data=data)
                content = response.text
            elif connection_library == 'cloudscraper':
                scraper = cloudscraper.create_scraper()
                response = scraper.post(url, headers=headers, data=data)
                content = response.text
            elif connection_library == 'selenium':
                chrome_options_config = site_config.get('chrome_options', {})
                driver_type = chrome_options_config.get('driver_type', 'chrome')
                
                if driver_type == 'undetected_chrome':
                    driver = self._get_undetected_chrome_driver(chrome_options_config)
                else:
                    driver = self._get_chrome_driver(chrome_options_config)
                
                try:
                    driver.get(url)
                    time.sleep(2)  # Wait for page to load
                    
                    # Find and fill the form field
                    form_field = driver.find_element(By.NAME, data_field)
                    form_field.clear()
                    form_field.send_keys(part_number)
                    
                    # Submit the form
                    form_field.submit()
                    
                    time.sleep(3)  # Wait for results
                    content = driver.page_source
                finally:
                    driver.quit()
            else:
                self.logger.error(f"Unknown connection library: {connection_library}")
                return None
            
            # Save the result if configured
            if site_config.get('output', {}).get('save_html', False):
                self._save_result(site_config, part_number, content)
            
            return content
        except Exception as e:
            self.logger.error(f"Error during POST search: {str(e)}")
            return None

    def search_by_api(self, site_config, part_number):
        """Search using direct API call."""
        if 'api_search' not in site_config:
            self.logger.error(f"API search configuration not found for site {site_config.get('name')}")
            return None
        
        api_config = site_config['api_search']
        url = api_config['url']
        method = api_config.get('method', 'GET').upper()
        params = api_config.get('params', {})
        headers = api_config.get('headers', {})
        data = api_config.get('data', {})
        json_data = api_config.get('json', {})
        
        # Replace placeholders in parameters, data, and JSON
        search_param = api_config.get('search_param_name', 'q')
        
        if method == 'GET':
            params[search_param] = part_number
        elif method in ['POST', 'PUT']:
            if json_data:
                json_data[search_param] = part_number
            else:
                data[search_param] = part_number
        
        self.logger.info(f"Performing API {method} request to {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif method == 'POST':
                response = requests.post(url, params=params, headers=headers, 
                                        data=data if not json_data else None, 
                                        json=json_data if json_data else None)
            elif method == 'PUT':
                response = requests.put(url, params=params, headers=headers, 
                                       data=data if not json_data else None, 
                                       json=json_data if json_data else None)
            else:
                self.logger.error(f"Unsupported HTTP method: {method}")
                return None
            
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Check if response is JSON or HTML
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                content = json.dumps(response.json(), indent=2)
            else:
                content = response.text
            
            # Save the result if configured
            if site_config.get('output', {}).get('save_html', False):
                self._save_result(site_config, part_number, content)
            
            return content
        except Exception as e:
            self.logger.error(f"Error during API search: {str(e)}")
            return None

    def _save_result(self, site_config, part_number, content):
        """Save the search result to a file."""
        output_dir = site_config.get('output', {}).get('output_dir', './scraped_data')
        site_name = site_config.get('name', 'unknown')
        
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the content to a file
        filename = f"{output_dir}/{site_name}_{part_number}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        self.logger.info(f"Saved result to {filename}")

    def search(self, site_name, part_number):
        """Search for a part number on a specific site."""
        site_config = self.get_site_config(site_name)
        if not site_config:
            self.logger.error(f"Configuration for site '{site_name}' not found")
            return None
        
        connection_type = site_config.get('connection_type', 'url')
        
        if connection_type.lower() == 'url':
            self.logger.info(f"Using URL-based search for {part_number} on {site_name}")
            return self.search_by_url(site_config, part_number)
        elif connection_type.lower() == 'form':
            self.logger.info(f"Using form-based search for {part_number} on {site_name}")
            return self.search_by_form(site_config, part_number)
        elif connection_type.lower() == 'post':
            self.logger.info(f"Using POST-based search for {part_number} on {site_name}")
            return self.search_by_post(site_config, part_number)
        elif connection_type.lower() == 'api':
            self.logger.info(f"Using API-based search for {part_number} on {site_name}")
            return self.search_by_api(site_config, part_number)
        else:
            self.logger.error(f"Unknown connection type: {connection_type}")
            return None

# Example usage
if __name__ == "__main__":
    scraper = WebScraper("scraper_config.json")
    
    # Search for a part on different sites
    part_number = "B7106G24EV2E2HR"
    
    # Search on mitac (POST-based with cloudscraper)
    result = scraper.search("mitac", part_number)
    if result:
        print(f"Search successful on mitac for {part_number}")
        # Save the result to a file
        with open("mitac_search.html", "w", encoding="utf-8") as file:
            file.write(result)






