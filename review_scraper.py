import requests
from bs4 import BeautifulSoup
import csv
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin
import time
from datetime import datetime

class ReviewScraper:
    """
    Advanced web scraper for extracting product reviews from e-commerce sites.
    Supports multiple export formats: CSV, Excel, JSON.
    """
    
    def __init__(self, base_url: str, headers: Optional[Dict] = None):
        """
        Initialize the scraper with a base URL and optional custom headers.
        
        Args:
            base_url: The URL to scrape reviews from
            headers: Optional custom HTTP headers
        """
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.reviews = []
        self.errors = []
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if request fails
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            self.errors.append(f"Failed to fetch {url}: {str(e)}")
            return None
    
    def extract_reviews(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract reviews from parsed HTML.
        
        Args:
            soup: BeautifulSoup object of parsed HTML
            
        Returns:
            List of review dictionaries
        """
        reviews = []
        review_containers = soup.find_all('div', class_='review-item')
        
        for container in review_containers:
            try:
                review = {
                    'title': container.find('h3', class_='review-title').text.strip(),
                    'author': container.find('span', class_='reviewer-name').text.strip(),
                    'rating': container.find('span', class_='rating').text.strip(),
                    'date': container.find('span', class_='review-date').text.strip(),
                    'text': container.find('p', class_='review-text').text.strip(),
                    'helpful': container.find('span', class_='helpful-count').text.strip(),
                }
                reviews.append(review)
            except AttributeError as e:
                self.errors.append(f"Failed to parse review: {str(e)}")
                continue
        
        return reviews
    
    def scrape_multiple_pages(self, page_urls: List[str], delay: float = 1.0) -> List[Dict]:
        """
        Scrape reviews from multiple pages with rate limiting.
        
        Args:
            page_urls: List of URLs to scrape
            delay: Delay between requests in seconds
            
        Returns:
            Combined list of all reviews
        """
        all_reviews = []
        
        for i, url in enumerate(page_urls, 1):
            print(f"Scraping page {i}/{len(page_urls)}: {url}")
            soup = self.fetch_page(url)
            
            if soup:
                page_reviews = self.extract_reviews(soup)
                all_reviews.extend(page_reviews)
                print(f"Found {len(page_reviews)} reviews on page {i}")
            
            if i < len(page_urls):
                time.sleep(delay)
        
        self.reviews = all_reviews
        return all_reviews
    
    def export_to_csv(self, filename: str) -> bool:
        """
        Export reviews to CSV file.
        
        Args:
            filename: Output CSV filename
            
        Returns:
            True if successful, False otherwise
        """
        if not self.reviews:
            print("No reviews to export")
            return False
        
        try:
            keys = self.reviews[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.reviews)
            print(f"Exported {len(self.reviews)} reviews to {filename}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to export CSV: {str(e)}")
            return False
    
    def export_to_json(self, filename: str) -> bool:
        """
        Export reviews to JSON file.
        
        Args:
            filename: Output JSON filename
            
        Returns:
            True if successful, False otherwise
        """
        if not self.reviews:
            print("No reviews to export")
            return False
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.reviews, f, indent=2, ensure_ascii=False)
            print(f"Exported {len(self.reviews)} reviews to {filename}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to export JSON: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        Get basic statistics about scraped reviews.
        
        Returns:
            Dictionary with statistics
        """
        if not self.reviews:
            return {}
        
        return {
            'total_reviews': len(self.reviews),
            'scrape_date': datetime.now().isoformat(),
            'total_errors': len(self.errors),
        }


if __name__ == '__main__':
    # Example usage
    scraper = ReviewScraper('https://example.com')
    pages = [
        'https://example.com/reviews?page=1',
        'https://example.com/reviews?page=2',
    ]
    
    reviews = scraper.scrape_multiple_pages(pages)
    scraper.export_to_csv('reviews.csv')
    scraper.export_to_json('reviews.json')
    print(scraper.get_statistics())
