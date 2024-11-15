# Multithreaded Web Crawler

This is a Python-based multithreaded web crawler that extracts and visits links from a given website.

## Features
- Multithreaded for faster crawling
- Respects the same-host constraint
- Configurable thread pool size and timeout

## Installation
1. Clone the repository:

   `git clone https://github.com/shawnxd/PyCrawler.git`

2. Install dependencies:

    `pip install -r requirements.txt`

## Usage
Run the crawler with:
    `python main.py <url> --pool-size <threads> --timeout <seconds>`

Example:
    `python main.py https://andyljones.com --pool-size 5 --timeout 10`

