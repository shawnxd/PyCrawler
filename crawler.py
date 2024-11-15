import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import threading

class Crawler:
    """
    A multithreaded web crawler to extract and traverse links on a website.
    """
    def __init__(self, pool_size=32, timeout=5):
        """
        Initialize the Crawler.

        Args:
            pool_size (int): Number of threads for the thread pool.
            timeout (int): Timeout for HTTP requests in seconds.
        """
        self.pool_size = pool_size
        self.timeout = timeout
        self.results = set()
        self.lock = threading.Lock()

    def get_page_links(self, url):
        """
        Get all links from a given webpage.

        Args:
            url (str): URL to fetch links from.

        Returns:
            list: A list of absolute URLs found on the page.
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all("a", href=True)
            page_links = [urljoin(url, link['href']) for link in links]
            return page_links
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            return []

    def crawl(self, url):
        """
        Start the crawling process for a given URL.

        Args:
            url (str): The starting URL to crawl.
        """
        hostname = self.get_hostname(url)
        with ThreadPoolExecutor(max_workers=self.pool_size) as executor:
            executor.submit(self._crawl, url, hostname)

    def _crawl(self, url, hostname):
        """
        Recursively crawl a given URL.

        Args:
            url (str): The URL to crawl.
            hostname (str): The base hostname to restrict crawling to.
        """
        sanitized_url = self.sanitize(url)
        with self.lock:
            if sanitized_url in self.results:
                return
            if self.get_hostname(sanitized_url) != hostname:
                return
            self.results.add(sanitized_url)

        sub_urls = self.get_page_links(sanitized_url)
        with ThreadPoolExecutor(max_workers=self.pool_size) as executor:
            futures = [executor.submit(self._crawl, sub_url, hostname) for sub_url in sub_urls]
            for future in futures:
                future.result()

    def get_hostname(self, url):
        """
        Extract the hostname from a URL.

        Args:
            url (str): The URL to extract the hostname from.

        Returns:
            str: The hostname.
        """
        return urlparse(url).hostname

    def sanitize(self, url):
        """
        Sanitize a URL by removing fragments.

        Args:
            url (str): The URL to sanitize.

        Returns:
            str: The sanitized URL.
        """
        return url.split('#')[0]
