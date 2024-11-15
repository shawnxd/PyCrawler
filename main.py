import argparse
from crawler import Crawler

def main():
    parser = argparse.ArgumentParser(description="Multithreaded Web Crawler")
    parser.add_argument("url", help="The URL to start crawling from")
    parser.add_argument("--pool-size", type=int, default=32, help="Number of threads in the pool")
    parser.add_argument("--timeout", type=int, default=5, help="Timeout for HTTP requests (seconds)")
    args = parser.parse_args()

    crawler = Crawler(pool_size=args.pool_size, timeout=args.timeout)
    crawler.crawl(args.url)
    print(f"Total URLs found: {len(crawler.results)}")
    print("\n".join(crawler.results))

if __name__ == "__main__":
    main()
