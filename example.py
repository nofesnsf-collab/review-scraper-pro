#!/usr/bin/env python
"""Example usage of the ReviewScraper"""

from review_scraper import ReviewScraper

# Example 1: Basic usage
if __name__ == "__main__":
    # Initialize scraper
    scraper = ReviewScraper('https://example-ecommerce.com')
    
    # List of pages to scrape
    pages_to_scrape = [
        'https://example-ecommerce.com/product/laptop/reviews?page=1',
        'https://example-ecommerce.com/product/laptop/reviews?page=2',
        'https://example-ecommerce.com/product/laptop/reviews?page=3',
    ]
    
    # Scrape reviews with 2 second delay between requests
    print("Starting web scraping...")
    reviews = scraper.scrape_multiple_pages(pages_to_scrape, delay=2.0)
    
    # Export results
    print(f"\nScraped {len(reviews)} reviews")
    scraper.export_to_csv('reviews_output.csv')
    scraper.export_to_json('reviews_output.json')
    
    # Display statistics
    stats = scraper.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total reviews: {stats['total_reviews']}")
    print(f"  Errors encountered: {stats['total_errors']}")
    print(f"  Scrape date: {stats['scrape_date']}")
    
    if scraper.errors:
        print(f"\nErrors:")
        for error in scraper.errors:
            print(f"  - {error}")
