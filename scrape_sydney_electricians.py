#!/usr/bin/env python3
"""
Sydney Electrician Business Owner & LinkedIn Scraper

Scrapes the provided list of Sydney electrician websites to extract:
- Business Name
- Website URL
- Email Address
- Business Owner/Director Name
- LinkedIn Profile
- Interesting Information

Usage:
    python scrape_sydney_electricians.py
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import logging
from typing import List, Dict, Optional
import random
from urllib.parse import quote_plus, urljoin, urlparse
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# List of Sydney electrician websites to scrape
ELECTRICIAN_WEBSITES = [
    {"name": "Sydney Electrical Service", "url": "https://sydneyelectricalservice.com.au/"},
    {"name": "The Local Electrician Sydney Level 2 & Emergency Specialists", "url": "https://www.thelocalelectrician.com.au/"},
    {"name": "Just Electrical Sydney Pty Ltd", "url": "https://www.justelectricalsydney.com.au/"},
    {"name": "360 Degrees Sydney Electrical", "url": "http://www.360sydneyelectrical.com.au/"},
    {"name": "24/7 Local Electrician", "url": "https://247localelectrician.com.au/"},
    {"name": "High Demand Electrical", "url": "https://www.hdlevel2electriciansydney.com.au/"},
    {"name": "Captain Cook Electrical Sydney", "url": "https://www.captaincookelectrical.com.au/"},
    {"name": "Surry Hills Electrical", "url": "https://www.surryhillselectrical.com/"},
    {"name": "Everything Electrical Sydney", "url": "https://www.everythingelectricalsydney.com.au/"},
    {"name": "Hello Electrical | Electrician Sydney", "url": "https://www.helloelectrical.com.au/"},
    {"name": "Down To Earth Electrical", "url": "https://www.downtoearthelectrical.com.au/"},
    {"name": "Sparky Nearby", "url": "https://sparkynearby.com.au/"},
    {"name": "Back's Electrical Sydney & Blue Mountains", "url": "https://backselectrical.com.au/"},
    {"name": "Electrician To The Rescue", "url": "http://www.electriciantotherescue.com.au/"},
    {"name": "Sydney Electrical Contractors", "url": "https://www.sec24hour.com.au/"},
    {"name": "J&J Electrical Solutions Pty Ltd", "url": "https://jjelectrical.localchoice.com.au/"},
    {"name": "Level 2 Electrician Sydney", "url": "http://www.level2electriciansydney.com.au/"},
    {"name": "Aussie Electrical And Plumbing Services Sydney", "url": "https://www.aussieelectricalandplumbing.com.au/"},
    {"name": "Kmelectric", "url": "https://kmelectric.com.au/"},
    {"name": "AB Electrical & Communications", "url": "http://www.abelectricians.com.au/"},
    {"name": "Montgomery Electrical", "url": "http://montgomeryelectrical.com.au/"},
    {"name": "The Sydney Electrical Company Pty Ltd", "url": "https://www.sydneyelectricalcompany.com.au/"},
    {"name": "ADS Electrical Contracting Pty Ltd", "url": "https://www.adselectrical.com.au/"},
    {"name": "North Sydney electrical", "url": "http://northsydneyelectrical.com.au/"},
    {"name": "Lightning Electrical Group", "url": "https://lightninggroup.com.au/"},
    {"name": "BF Electrical North Sydney", "url": "https://bfelectricalnorthsydney.com.au/"},
    {"name": "Scott Electrics The Switched On Electricians", "url": "https://scottelectrics.com.au/"},
]


class WebsiteScraper:
    """Scraper for extracting business information."""

    @staticmethod
    def get_headers():
        """Get browser headers."""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        ]
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    @staticmethod
    def extract_emails(text: str, soup: BeautifulSoup) -> List[str]:
        """Extract email addresses."""
        emails = []

        # Method 1: Regex from text
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        text_emails = re.findall(email_pattern, text)
        emails.extend(text_emails)

        # Method 2: Mailto links
        for link in soup.find_all('a', href=re.compile(r'^mailto:', re.I)):
            href = link.get('href', '')
            match = re.search(r'mailto:([^\?&\s]+)', href)
            if match:
                emails.append(match.group(1))

        # Clean and filter
        clean_emails = []
        exclude = ['example.com', 'test.com', 'domain.com', '.png', '.jpg', '@2x', 'wixpress', 'sentry']
        generic = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com']

        for email in set(emails):
            email = email.lower().strip()
            if any(ex in email for ex in exclude):
                continue
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                continue

            # Prefer business emails
            domain = email.split('@')[1]
            if domain not in generic:
                clean_emails.append(email)

        # If no business emails, return any valid email
        if not clean_emails:
            for email in set(emails):
                email = email.lower().strip()
                if any(ex in email for ex in exclude):
                    continue
                if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    clean_emails.append(email)

        return clean_emails[:3]  # Return up to 3 emails

    @staticmethod
    def extract_owner_name(text: str, soup: BeautifulSoup, business_name: str) -> Optional[str]:
        """Extract owner/director/founder name."""

        # Patterns to find names
        patterns = [
            # "Director: John Smith" or "Owner: John Smith"
            r'(?:Director|Owner|Manager|Principal|Founder|CEO|Managing Director|Proprietor)[\s:]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            # "Founded by John Smith" or "Run by John Smith"
            r'(?:Founded by|Run by|Started by|Led by|Managed by)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            # "John Smith, Director" or "John Smith - Owner"
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)[\s,\-]+(?:Director|Owner|Manager|Principal|Founder|CEO)',
            # "Meet John Smith" or "About John Smith"
            r'(?:Meet|About)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            # Just a name before a title in a heading
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*[\-\|]\s*(?:Director|Owner|Manager|Founder)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()

                # Filter out false positives
                invalid = [
                    'Contact Us', 'About Us', 'Read More', 'Click Here', 'Learn More',
                    'Get Started', 'Find Out', 'Our Team', 'The Team', 'Privacy Policy',
                    'Terms And', 'Conditions Apply', 'Level Up', 'Call Us', 'Email Us',
                    'Book Now', 'Get Quote', 'Free Quote', 'Service Area', business_name
                ]

                if name not in invalid and len(name.split()) >= 2 and len(name.split()) <= 4:
                    # Additional validation: check if it looks like a real name
                    words = name.split()
                    if all(word[0].isupper() and word[1:].islower() for word in words if len(word) > 1):
                        return name

        # Try to find name in structured data (JSON-LD)
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    if 'founder' in data:
                        if isinstance(data['founder'], dict) and 'name' in data['founder']:
                            return data['founder']['name']
                        elif isinstance(data['founder'], str):
                            return data['founder']
            except:
                continue

        return None

    @staticmethod
    def extract_interesting_info(text: str, soup: BeautifulSoup) -> str:
        """Extract interesting business information."""
        interesting = []
        text_lower = text.lower()

        # Services
        services = []
        service_keywords = {
            'level 2': 'Level 2 ASP',
            'emergency': 'Emergency',
            '24/7': '24/7',
            'residential': 'Residential',
            'commercial': 'Commercial',
            'industrial': 'Industrial',
            'solar': 'Solar',
        }

        for keyword, label in service_keywords.items():
            if keyword in text_lower:
                services.append(label)

        if services:
            interesting.append(', '.join(list(dict.fromkeys(services))[:4]))

        # Experience
        years_match = re.search(r'(\d{1,2})\+?\s*(?:years?|yrs)\s+(?:experience|in business)', text_lower)
        if years_match:
            interesting.append(f"{years_match.group(1)}+ years")

        # Established year
        est_match = re.search(r'(?:established|since|founded)\s+(?:in\s+)?(\d{4})', text_lower)
        if est_match:
            year = est_match.group(1)
            if 1950 <= int(year) <= 2025:
                interesting.append(f"Est. {year}")

        # Licensed
        if 'licensed' in text_lower or 'licenced' in text_lower:
            interesting.append('Licensed')

        return ' | '.join(interesting) if interesting else 'Electrical Services'

    @staticmethod
    def scrape_website(url: str, business_name: str) -> Optional[Dict]:
        """Scrape a business website."""
        try:
            logger.info(f"Scraping: {business_name}")
            logger.info(f"  URL: {url}")

            # Clean URL
            url = url.split('?')[0]  # Remove query parameters

            response = requests.get(url, headers=WebsiteScraper.get_headers(), timeout=20, allow_redirects=True)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove noise
            for element in soup(['script', 'style', 'iframe', 'noscript']):
                element.decompose()

            text = soup.get_text(separator=' ', strip=True)

            # Extract emails from home page
            emails = WebsiteScraper.extract_emails(text, soup)

            # If no email, try contact page
            if not emails:
                contact_links = soup.find_all('a', href=re.compile(r'contact|about', re.I))
                for link in contact_links[:3]:
                    try:
                        contact_url = urljoin(url, link.get('href', ''))
                        if contact_url == url:
                            continue
                        logger.info(f"  Trying: {contact_url}")
                        contact_response = requests.get(contact_url, headers=WebsiteScraper.get_headers(), timeout=15)
                        contact_soup = BeautifulSoup(contact_response.text, 'html.parser')
                        contact_text = contact_soup.get_text()
                        emails = WebsiteScraper.extract_emails(contact_text, contact_soup)
                        if emails:
                            break
                        time.sleep(1)
                    except:
                        continue

            # Extract owner name from home page
            owner_name = WebsiteScraper.extract_owner_name(text, soup, business_name)

            # If no owner, try about page
            if not owner_name:
                about_links = soup.find_all('a', href=re.compile(r'about|team|our-story', re.I))
                for link in about_links[:3]:
                    try:
                        about_url = urljoin(url, link.get('href', ''))
                        if about_url == url:
                            continue
                        logger.info(f"  Trying About: {about_url}")
                        about_response = requests.get(about_url, headers=WebsiteScraper.get_headers(), timeout=15)
                        about_soup = BeautifulSoup(about_response.text, 'html.parser')
                        about_text = about_soup.get_text()
                        owner_name = WebsiteScraper.extract_owner_name(about_text, about_soup, business_name)
                        if owner_name:
                            break
                        time.sleep(1)
                    except:
                        continue

            # Extract interesting info
            interesting = WebsiteScraper.extract_interesting_info(text, soup)

            logger.info(f"  ✓ Email: {emails[0] if emails else 'Not found'}")
            logger.info(f"  ✓ Owner: {owner_name or 'Not found'}")

            return {
                'business_name': business_name,
                'website': url,
                'email': emails[0] if emails else 'Not Found',
                'owner': owner_name,
                'interesting': interesting
            }

        except requests.Timeout:
            logger.error(f"  ✗ Timeout for {url}")
            return None
        except requests.RequestException as e:
            logger.error(f"  ✗ Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
            return None

    @staticmethod
    def search_linkedin(business_name: str, owner_name: Optional[str]) -> Optional[str]:
        """Search for LinkedIn profile using Google."""
        if not owner_name:
            return None

        try:
            logger.info(f"  Searching LinkedIn for: {owner_name}")

            # Try Google search
            query = f'"{owner_name}" "{business_name}" site:linkedin.com/in'
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"

            response = requests.get(search_url, headers=WebsiteScraper.get_headers(), timeout=10)

            # Extract LinkedIn URLs
            linkedin_pattern = r'(https?://(?:www\.|au\.|[a-z]{2}\.)?linkedin\.com/in/[a-zA-Z0-9\-]+)'
            matches = re.findall(linkedin_pattern, response.text)

            if matches:
                # Clean and deduplicate
                clean_urls = []
                for url in matches:
                    url = url.replace('www.', '').replace('au.', '')
                    if url not in clean_urls:
                        clean_urls.append(url)

                if clean_urls:
                    logger.info(f"  ✓ LinkedIn: {clean_urls[0]}")
                    return clean_urls[0]

            logger.info(f"  ✗ LinkedIn: Not found")
            return None

        except Exception as e:
            logger.debug(f"  LinkedIn search error: {e}")
            return None


def scrape_all_electricians():
    """Scrape all electrician websites."""
    results = []
    total = len(ELECTRICIAN_WEBSITES)

    print("\n" + "="*80)
    print(" " * 15 + "SYDNEY ELECTRICIAN BUSINESS OWNER SCRAPER")
    print("="*80)
    print(f"Scraping {total} Sydney electrician websites...")
    print("Extracting: Business Owner Names & LinkedIn Profiles")
    print("="*80 + "\n")

    for i, site in enumerate(ELECTRICIAN_WEBSITES, 1):
        print(f"\n[{i}/{total}] Processing: {site['name']}")
        print("-" * 80)

        # Scrape website
        info = WebsiteScraper.scrape_website(site['url'], site['name'])

        if info:
            # Search for LinkedIn profile
            linkedin = WebsiteScraper.search_linkedin(info['business_name'], info.get('owner'))

            result = {
                'Business Name': info['business_name'],
                'Website': info['website'],
                'Email Address': info['email'],
                'Business Owner Name': info.get('owner', 'Not Available'),
                'LinkedIn Profile': linkedin or 'Not Found',
                'Anything Interesting': info['interesting']
            }

            results.append(result)
            print(f"✓ SUCCESS - Added to results")

        else:
            # Add entry even if scraping failed
            result = {
                'Business Name': site['name'],
                'Website': site['url'].split('?')[0],
                'Email Address': 'Not Found',
                'Business Owner Name': 'Not Available',
                'LinkedIn Profile': 'Not Found',
                'Anything Interesting': 'Could not scrape website'
            }
            results.append(result)
            print(f"✗ FAILED - Added with limited info")

        # Rate limiting
        time.sleep(random.uniform(3, 6))

    return results


def save_results(results: List[Dict], filename: str = 'sydney_electricians_with_owners.csv'):
    """Save results to CSV."""
    if not results:
        logger.error("No results to save!")
        return False

    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)

    print("\n" + "="*80)
    print(" " * 25 + "RESULTS SUMMARY")
    print("="*80)
    print(f"Total businesses scraped: {len(results)}")
    print(f"Emails found: {len([r for r in results if r['Email Address'] != 'Not Found'])}")
    print(f"Owners found: {len([r for r in results if r['Business Owner Name'] != 'Not Available'])}")
    print(f"LinkedIn profiles found: {len([r for r in results if r['LinkedIn Profile'] != 'Not Found'])}")
    print("="*80)

    # Display table
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)

    print("\n" + df.to_string(index=False))
    print("\n" + "="*80)
    print(f"✓ Results saved to: {filename}")
    print("="*80 + "\n")

    return True


def main():
    """Main entry point."""
    results = scrape_all_electricians()

    if results:
        save_results(results, 'sydney_electricians_with_owners.csv')
        print("\n✓ Scraping complete!\n")
    else:
        print("\n✗ Scraping failed - no results collected\n")


if __name__ == "__main__":
    main()
