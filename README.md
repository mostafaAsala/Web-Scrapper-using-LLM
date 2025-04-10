# Web Scraper Framework

A configurable and extensible web scraping framework designed to handle multiple websites with different authentication mechanisms and anti-bot protections.

## Features

- **Multiple Connection Methods**: Support for requests, cloudscraper, and Selenium
- **Configurable Search Strategies**: URL-based, form-based, and POST request-based approaches
- **Anti-Bot Bypass**: Integration with undetected_chromedriver to handle sophisticated anti-scraping measures
- **JSON Configuration**: Define site-specific parameters without code changes
- **Comprehensive Logging**: Detailed operation logs for monitoring and debugging

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/web-scraper-framework.git
cd web-scraper-framework

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Configure your scraping targets in `scraper_config.json`:

```json
{
  "sites": [
    {
      "id": "site1_001",
      "name": "site1",
      "connection_type": "url",
      "connection_library": "requests",
      "url_search": {
        "url": "https://www.site1.com/WDA_PARTNUMBER",
        "keyword": "WDA_PARTNUMBER"
      },
      "output": {
        "save_html": true,
        "output_dir": "./scraped_data/site1"
      }
    }
  ]
}
```

2. Run the scraper:

```python
from web_scraper import WebScraper

# Initialize the scraper with your config
scraper = WebScraper("scraper_config.json")

# Search for a part on a specific site
result = scraper.search("site1", "B7106G24EV2E2HR")
```

## Configuration Options

### Connection Types
- `url`: Direct URL access with keyword replacement
- `form`: Form-based search using Selenium
- `post`: POST request with data payload
- `api`: API-based search with parameters

### Connection Libraries
- `requests`: Standard Python requests library
- `cloudscraper`: For bypassing Cloudflare protection
- `selenium`: For browser automation

## Advanced Usage

### Adding a New Site

To add a new site to the scraper, add a new entry to the `sites` array in your configuration file with the appropriate parameters.

### Custom Chrome Options

For Selenium-based scraping, you can configure Chrome options:

```json
"chrome_options": {
  "disable_extensions": true,
  "headless": false,
  "disable_gpu": true,
  "disable_images": true,
  "disable_javascript": true,
  "log_level": 3,
  "driver_type": "undetected_chrome"
}
```

## License

[MIT License](LICENSE)