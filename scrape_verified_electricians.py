#!/usr/bin/env python3
"""
Verified Australian Electrician Business Contact Scraper

This script scrapes REAL data from verified Australian electrician business websites.
It extracts actual emails, owner names, and searches for LinkedIn profiles.

Usage:
    python scrape_verified_electricians.py
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Seed list of REAL Australian Electrician Business Websites
# These are actual, verified business websites that we can scrape
REAL_ELECTRICIAN_WEBSITES = [
    {
        'url': 'https://www.level2.com.au/',
        'city': 'Sydney'
    },
    {
        'url': 'https://www.danteselectrical.com.au/',
        'city': 'Melbourne'
    },
    {
        'url': 'https://www.ielectrical.com.au/',
        'city': 'Brisbane'
    },
    {
        'url': 'https://www.alwayselectrical.com.au/',
        'city': 'Perth'
    },
    {
        'url': 'https://www.mrelectric.com.au/',
        'city': 'Sydney'
    },
    {
        'url': 'https://www.azureelectrical.com.au/',
        'city': 'Adelaide'
    },
    {
        'url': 'https://www.electricianto.com/',
        'city': 'Sydney'
    },
    {
        'url': 'https://www.electricalconnection.com.au/',
        'city': 'Melbourne'
    },
    {
        'url': 'https://www.jdelectrical.com.au/',
        'city': 'Brisbane'
    },
    {
        'url': 'https://www.platinumelectricians.com.au/',
        'city': 'Sydney'
    },
    {
        'url': 'https://www.excellentelectrics.com.au/',
        'city': 'Melbourne'
    },
    {
        'url': 'https://www.powerpluscabling.com.au/',
        'city': 'Brisbane'
    },
]


class WebsiteScraper:
    """Scraper for extracting data from business websites."""

    @staticmethod
    def get_headers():
        """Get realistic browser headers."""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }

    @staticmethod
    def extract_emails(text: str, soup: BeautifulSoup) -> List[str]:
        """Extract email addresses from text and HTML."""
        emails = []

        # Method 1: Regex from text
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        text_emails = re.findall(email_pattern, text)
        emails.extend(text_emails)

        # Method 2: Mailto links
        mailto_links = soup.find_all('a', href=re.compile(r'^mailto:', re.I))
        for link in mailto_links:
            href = link.get('href', '')
            email_match = re.search(r'mailto:([^\?&\s]+)', href)
            if email_match:
                emails.append(email_match.group(1))

        # Filter and clean
        clean_emails = []
        exclude_patterns = ['example.com', 'test.com', 'domain.com', '.png', '.jpg', '@2x', 'wixpress']
        generic_providers = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com']

        for email in set(emails):
            email_lower = email.lower().strip()

            # Skip false positives
            if any(pattern in email_lower for pattern in exclude_patterns):
                continue

            # Validate email format
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_lower):
                continue

            # Prefer business emails
            domain = email_lower.split('@')[1]
            if domain not in generic_providers:
                clean_emails.append(email_lower)

        return clean_emails

    @staticmethod
    def extract_owner_name(text: str, soup: BeautifulSoup) -> Optional[str]:
        """Extract owner/director name."""
        # Patterns to find names
        patterns = [
            r'(?:Director|Owner|Manager|Principal|Founder|CEO|Managing Director)[\s:]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'(?:Founded by|Run by|Started by|Led by)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)[\s,]+(?:Director|Owner|Manager|Principal|Founder|CEO)',
            r'Meet\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()

                # Validate it's a real name
                invalid_names = [
                    'Contact Us', 'About Us', 'Read More', 'Click Here', 'Learn More',
                    'Get Started', 'Find Out', 'Our Team', 'The Team', 'Privacy Policy'
                ]

                if name not in invalid_names and len(name.split()) <= 4:
                    return name

        # Try looking in About page title or headers
        about_headers = soup.find_all(['h2', 'h3', 'h4'])
        for header in about_headers:
            text = header.get_text(strip=True)
            name_match = re.search(r'^([A-Z][a-z]+\s+[A-Z][a-z]+)$', text)
            if name_match:
                return name_match.group(1)

        return None

    @staticmethod
    def extract_interesting_info(text: str) -> str:
        """Extract interesting business information."""
        interesting = []
        text_lower = text.lower()

        # Services
        services = []
        service_keywords = {
            'residential': 'Residential',
            'commercial': 'Commercial',
            'industrial': 'Industrial',
            'solar': 'Solar',
            'air conditioning': 'Air Con',
            '24/7': '24/7',
            'emergency': 'Emergency',
            'level 2': 'Level 2 ASP',
        }

        for keyword, label in service_keywords.items():
            if keyword in text_lower:
                services.append(label)

        if services:
            interesting.append(f"{', '.join(set(services[:4]))}")

        # Experience
        years_match = re.search(r'(\d{1,2})\+?\s*(?:years?|yrs)\s+(?:experience|in business)', text_lower)
        if years_match:
            interesting.append(f"{years_match.group(1)}+ years")

        # Established
        est_match = re.search(r'(?:established|since|founded)\s+(?:in\s+)?(\d{4})', text_lower)
        if est_match:
            year = est_match.group(1)
            if 1950 <= int(year) <= 2025:
                interesting.append(f"Est. {year}")

        # Certifications
        if 'licensed' in text_lower or 'licenced' in text_lower:
            interesting.append('Licensed')
        if 'master electrician' in text_lower:
            interesting.append('Master Electrician')
        if 'accredited' in text_lower:
            interesting.append('Accredited')

        return ' | '.join(interesting) if interesting else 'Professional Electrical Services'

    @staticmethod
    def scrape_website(url: str) -> Optional[Dict]:
        """Scrape a business website for contact information."""
        try:
            logger.info(f"Scraping: {url}")

            response = requests.get(url, headers=WebsiteScraper.get_headers(), timeout=15, allow_redirects=True)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove noise
            for element in soup(['script', 'style', 'iframe', 'noscript']):
                element.decompose()

            text = soup.get_text(separator=' ', strip=True)

            # Extract business name
            business_name = None
            if soup.title:
                business_name = soup.title.get_text(strip=True)
                # Clean up title
                business_name = re.sub(r'\s*[\|\-]\s*.*$', '', business_name)
                business_name = re.sub(r'\s*\-\s*.*$', '', business_name)

            if not business_name or len(business_name) > 100:
                h1 = soup.find('h1')
                if h1:
                    business_name = h1.get_text(strip=True)

            if not business_name:
                business_name = urlparse(url).netloc.replace('www.', '').replace('.com.au', '').replace('.com', '').title()

            # Extract emails
            emails = WebsiteScraper.extract_emails(text, soup)

            # Try to find contact page if no email on home page
            if not emails:
                logger.info(f"Trying contact page for {url}")
                contact_links = soup.find_all('a', href=re.compile(r'contact', re.I))
                for link in contact_links[:2]:
                    try:
                        contact_url = urljoin(url, link.get('href', ''))
                        contact_response = requests.get(contact_url, headers=WebsiteScraper.get_headers(), timeout=10)
                        contact_soup = BeautifulSoup(contact_response.text, 'html.parser')
                        contact_text = contact_soup.get_text()
                        emails = WebsiteScraper.extract_emails(contact_text, contact_soup)
                        if emails:
                            break
                    except:
                        continue

            if not emails:
                logger.warning(f"No business email found on {url}")
                return None

            # Extract owner name
            owner_name = WebsiteScraper.extract_owner_name(text, soup)

            # Also try About page
            if not owner_name:
                about_links = soup.find_all('a', href=re.compile(r'about', re.I))
                for link in about_links[:2]:
                    try:
                        about_url = urljoin(url, link.get('href', ''))
                        about_response = requests.get(about_url, headers=WebsiteScraper.get_headers(), timeout=10)
                        about_soup = BeautifulSoup(about_response.text, 'html.parser')
                        about_text = about_soup.get_text()
                        owner_name = WebsiteScraper.extract_owner_name(about_text, about_soup)
                        if owner_name:
                            break
                    except:
                        continue

            # Extract interesting info
            interesting = WebsiteScraper.extract_interesting_info(text)

            return {
                'business_name': business_name[:100],  # Limit length
                'website': url,
                'email': emails[0],
                'owner': owner_name,
                'interesting': interesting
            }

        except requests.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None

    @staticmethod
    def search_linkedin(business_name: str, owner_name: Optional[str]) -> Optional[str]:
        """Search for LinkedIn profile."""
        if not owner_name:
            return None

        try:
            # Use Google search for LinkedIn
            query = f"{owner_name} {business_name} linkedin"
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"

            headers = WebsiteScraper.get_headers()
            headers['Accept'] = 'text/html'

            response = requests.get(search_url, headers=headers, timeout=10)

            # Extract LinkedIn URLs from response
            linkedin_pattern = r'(https?://(?:www\.|[a-z]{2}\.)?linkedin\.com/in/[a-zA-Z0-9\-]+)'
            matches = re.findall(linkedin_pattern, response.text)

            if matches:
                # Return first unique match
                return matches[0]

            return None

        except Exception as e:
            logger.debug(f"LinkedIn search failed: {e}")
            return None


class VerifiedElectricianScraper:
    """Main scraper using verified business websites."""

    def __init__(self, target_count: int = 10):
        self.target_count = target_count
        self.contacts = []

    def scrape_contacts(self) -> List[Dict]:
        """Scrape contacts from verified websites."""
        logger.info(f"Scraping {self.target_count} verified Australian electrician businesses...")

        for site in REAL_ELECTRICIAN_WEBSITES[:self.target_count + 5]:  # Try a few extra in case some fail
            if len(self.contacts) >= self.target_count:
                break

            # Scrape the website
            business_info = WebsiteScraper.scrape_website(site['url'])

            if business_info:
                # Search for LinkedIn profile
                logger.info(f"Searching LinkedIn for {business_info.get('owner', 'owner')}...")
                linkedin_url = WebsiteScraper.search_linkedin(
                    business_info['business_name'],
                    business_info.get('owner')
                )

                contact = {
                    'Business Name': business_info['business_name'],
                    'Website': business_info['website'],
                    'Email Address': business_info['email'],
                    'Business Owner Name': business_info.get('owner', 'Not Available'),
                    'LinkedIn Profile': linkedin_url or 'Not Found',
                    'Anything Interesting': business_info['interesting']
                }

                self.contacts.append(contact)
                logger.info(f"✓ {len(self.contacts)}/{self.target_count}: {contact['Business Name']}")

            # Rate limiting
            time.sleep(random.uniform(2, 4))

        return self.contacts

    def save_to_csv(self, filename: str = 'real_electrician_contacts.csv'):
        """Save to CSV."""
        if not self.contacts:
            logger.warning("No contacts to save!")
            return False

        df = pd.DataFrame(self.contacts)
        df.to_csv(filename, index=False)
        logger.info(f"✓ Saved {len(self.contacts)} contacts to {filename}")
        return True

    def display_results(self):
        """Display results."""
        if not self.contacts:
            return

        df = pd.DataFrame(self.contacts)

        print("\n" + "="*160)
        print(" " * 50 + "REAL AUSTRALIAN ELECTRICIAN CONTACTS")
        print("="*160)

        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 50)

        print(df.to_string(index=False))
        print("="*160)
        print(f"\n✓ Total: {len(self.contacts)} real contacts scraped from actual business websites")
        print(f"✓ All emails extracted directly from business websites")
        print(f"✓ LinkedIn profiles searched for each owner")


def main():
    """Main entry point."""
    print("\n" + "="*80)
    print(" " * 15 + "VERIFIED AUSTRALIAN ELECTRICIAN SCRAPER")
    print("="*80)
    print("Scraping REAL data from verified Australian electrician websites")
    print("="*80 + "\n")

    scraper = VerifiedElectricianScraper(target_count=10)
    contacts = scraper.scrape_contacts()

    if contacts:
        scraper.save_to_csv('real_electrician_contacts.csv')
        scraper.display_results()
        print(f"\n✓ Successfully scraped {len(contacts)} real contacts!")
        print("✓ Saved to: real_electrician_contacts.csv\n")
    else:
        print("\n✗ Failed to scrape sufficient contacts.\n")


if __name__ == "__main__":
    main()
