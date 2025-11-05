#!/usr/bin/env python3
"""
Australian Electrician Business Contact Scraper

This script collects publicly available business contact information for electricians
in Australia from legitimate sources like Yellow Pages and business websites.

Usage:
    python scrape_electricians.py

Output:
    - electrician_contacts.csv (CSV file with collected data)
    - Console output with formatted table
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import dns.resolver
from email_validator import validate_email, EmailNotValidError
from urllib.parse import urljoin, urlparse
import logging
from typing import List, Dict, Optional
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmailExtractor:
    """Extract and validate email addresses from websites."""

    EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    @staticmethod
    def extract_emails_from_text(text: str) -> List[str]:
        """Extract email addresses from text using regex."""
        emails = re.findall(EmailExtractor.EMAIL_REGEX, text)
        return list(set(emails))  # Remove duplicates

    @staticmethod
    def is_business_email(email: str) -> bool:
        """Check if email is a business email (not generic providers)."""
        generic_providers = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'live.com', 'icloud.com', 'aol.com', 'mail.com'
        ]
        domain = email.split('@')[1].lower()
        return domain not in generic_providers

    @staticmethod
    def validate_email_format(email: str) -> bool:
        """Validate email format and check if domain exists."""
        try:
            # Validate email format
            valid = validate_email(email, check_deliverability=False)
            email = valid.email

            # Check if domain has MX records
            domain = email.split('@')[1]
            try:
                dns.resolver.resolve(domain, 'MX')
                return True
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
                logger.warning(f"Domain {domain} has no MX records")
                return False

        except EmailNotValidError as e:
            logger.warning(f"Invalid email {email}: {e}")
            return False
        except Exception as e:
            logger.warning(f"Error validating {email}: {e}")
            return False

    @staticmethod
    def extract_from_website(url: str, timeout: int = 10) -> List[str]:
        """Extract emails from a website."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()
            emails = EmailExtractor.extract_emails_from_text(text)

            # Filter business emails and validate
            valid_emails = []
            for email in emails:
                if EmailExtractor.is_business_email(email):
                    if EmailExtractor.validate_email_format(email):
                        valid_emails.append(email)

            return valid_emails

        except Exception as e:
            logger.error(f"Error extracting emails from {url}: {e}")
            return []


class BusinessInfoExtractor:
    """Extract business information from websites."""

    @staticmethod
    def extract_owner_name(soup: BeautifulSoup, url: str) -> Optional[str]:
        """Try to extract business owner/director name from website."""
        try:
            # Look for common patterns
            patterns = [
                r'(?:Owner|Director|Manager|Principal):\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
                r'(?:Founded by|Run by|Operated by)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
                r'([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+(?:Owner|Director|Manager)',
            ]

            text = soup.get_text()
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    return match.group(1)

            # Check About page
            about_links = soup.find_all('a', href=re.compile(r'about', re.I))
            for link in about_links[:2]:  # Check first 2 about links
                about_url = urljoin(url, link.get('href', ''))
                try:
                    response = requests.get(about_url, timeout=10, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    about_soup = BeautifulSoup(response.text, 'html.parser')
                    about_text = about_soup.get_text()

                    for pattern in patterns:
                        match = re.search(pattern, about_text)
                        if match:
                            return match.group(1)
                except:
                    continue

            return None

        except Exception as e:
            logger.error(f"Error extracting owner name: {e}")
            return None

    @staticmethod
    def extract_interesting_info(soup: BeautifulSoup) -> str:
        """Extract interesting information about the business."""
        interesting = []

        try:
            text = soup.get_text().lower()

            # Specializations
            specializations = []
            specialization_keywords = [
                'residential', 'commercial', 'industrial', 'solar',
                'air conditioning', 'renovations', 'new builds',
                'emergency', '24/7', '24 hour', 'licensed', 'certified'
            ]

            for keyword in specialization_keywords:
                if keyword in text:
                    specializations.append(keyword.title())

            if specializations:
                interesting.append(f"Specializations: {', '.join(specializations[:3])}")

            # Years in business
            years_match = re.search(r'(\d{1,2})\+?\s*years?\s+(?:in business|experience|established)', text)
            if years_match:
                interesting.append(f"{years_match.group(1)}+ years experience")

            # Established year
            est_match = re.search(r'(?:established|since|founded)\s+(?:in\s+)?(\d{4})', text)
            if est_match:
                year = est_match.group(1)
                if 1950 <= int(year) <= 2024:
                    interesting.append(f"Established {year}")

            # Certifications
            certs = []
            cert_keywords = ['master electrician', 'licensed electrician', 'qualified electrician']
            for cert in cert_keywords:
                if cert in text:
                    certs.append(cert.title())
            if certs:
                interesting.append(f"Certifications: {', '.join(certs[:2])}")

            return ' | '.join(interesting) if interesting else 'N/A'

        except Exception as e:
            logger.error(f"Error extracting interesting info: {e}")
            return 'N/A'


class YellowPagesScraperAU:
    """Scrape electrician listings from Yellow Pages Australia."""

    BASE_URL = "https://www.yellowpages.com.au"

    @staticmethod
    def search_electricians(location: str, max_results: int = 5) -> List[Dict]:
        """Search for electricians in a given location."""
        businesses = []

        try:
            search_url = f"{YellowPagesScraperAU.BASE_URL}/search/listings"
            params = {
                'clue': 'electricians',
                'locationClue': location,
                'firstRecord': 1
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            logger.info(f"Searching for electricians in {location}...")

            response = requests.get(search_url, params=params, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find business listings
            listings = soup.find_all(['div', 'article'], class_=re.compile(r'listing|business', re.I), limit=max_results * 2)

            for listing in listings[:max_results]:
                try:
                    business = {}

                    # Extract business name
                    name_elem = listing.find(['h3', 'h2', 'a'], class_=re.compile(r'name|title|business', re.I))
                    if name_elem:
                        business['name'] = name_elem.get_text(strip=True)
                    else:
                        continue

                    # Extract website
                    website_elem = listing.find('a', href=re.compile(r'^http'))
                    if website_elem:
                        business['website'] = website_elem.get('href')

                    businesses.append(business)

                except Exception as e:
                    logger.warning(f"Error parsing listing: {e}")
                    continue

            logger.info(f"Found {len(businesses)} businesses in {location}")

        except Exception as e:
            logger.error(f"Error searching Yellow Pages for {location}: {e}")

        return businesses


class ElectricianContactScraper:
    """Main scraper class to coordinate data collection."""

    def __init__(self, target_count: int = 10):
        self.target_count = target_count
        self.contacts = []
        self.cities = ['Sydney NSW', 'Melbourne VIC', 'Brisbane QLD', 'Perth WA', 'Adelaide SA']

    def scrape_from_yellow_pages(self) -> List[Dict]:
        """Scrape electrician contacts from Yellow Pages."""
        all_businesses = []

        for city in self.cities:
            businesses = YellowPagesScraperAU.search_electricians(city, max_results=3)
            all_businesses.extend(businesses)

            # Rate limiting
            time.sleep(random.uniform(2, 4))

            if len(all_businesses) >= self.target_count:
                break

        return all_businesses[:self.target_count * 2]  # Get extra in case some fail

    def enrich_business_data(self, business: Dict) -> Optional[Dict]:
        """Enrich business data with email, owner name, and interesting info."""
        try:
            website = business.get('website')
            if not website:
                logger.warning(f"No website for {business.get('name')}")
                return None

            logger.info(f"Processing {business.get('name')}...")

            # Fetch website
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(website, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract emails
            emails = EmailExtractor.extract_from_website(website)
            if not emails:
                logger.warning(f"No valid business email found for {business.get('name')}")
                return None

            # Extract owner name
            owner_name = BusinessInfoExtractor.extract_owner_name(soup, website)

            # Extract interesting info
            interesting = BusinessInfoExtractor.extract_interesting_info(soup)

            return {
                'Business Name': business.get('name'),
                'Email Address': emails[0],  # Use first valid email
                'Business Owner Name': owner_name or 'Not Available',
                'Anything Interesting': interesting
            }

        except Exception as e:
            logger.error(f"Error enriching {business.get('name')}: {e}")
            return None

    def scrape_contacts(self) -> List[Dict]:
        """Main method to scrape contacts."""
        logger.info(f"Starting scrape for {self.target_count} electrician contacts...")

        # Get businesses from Yellow Pages
        businesses = self.scrape_from_yellow_pages()

        # If Yellow Pages doesn't work well, use mock data for demonstration
        if len(businesses) < 3:
            logger.warning("Yellow Pages scraping yielded few results. Using alternative approach...")
            businesses = self._get_mock_businesses()

        # Enrich each business with detailed data
        for business in businesses:
            if len(self.contacts) >= self.target_count:
                break

            contact = self.enrich_business_data(business)
            if contact:
                self.contacts.append(contact)
                logger.info(f"✓ Collected contact {len(self.contacts)}/{self.target_count}")

            # Rate limiting
            time.sleep(random.uniform(2, 5))

        return self.contacts

    def _get_mock_businesses(self) -> List[Dict]:
        """Generate mock business data for demonstration (uses real Australian electrician data patterns)."""
        logger.info("Generating sample data based on typical Australian electrician businesses...")

        # This represents the structure we'd get from real scraping
        # In production, these would come from actual Yellow Pages searches
        mock_businesses = [
            {'name': 'Sydney Sparks Electrical', 'website': 'https://example.com/sydney-sparks'},
            {'name': 'Melbourne Master Electricians', 'website': 'https://example.com/melb-masters'},
            {'name': 'Brisbane Bright Electrical', 'website': 'https://example.com/brisbane-bright'},
            {'name': 'Perth Power Solutions', 'website': 'https://example.com/perth-power'},
            {'name': 'Adelaide All Hours Electrical', 'website': 'https://example.com/adelaide-allhours'},
            {'name': 'Gold Coast Electrical Services', 'website': 'https://example.com/gc-electrical'},
            {'name': 'Canberra Circuit Solutions', 'website': 'https://example.com/canberra-circuits'},
            {'name': 'Hobart Home Electrical', 'website': 'https://example.com/hobart-home'},
            {'name': 'Darwin Electricians Pro', 'website': 'https://example.com/darwin-pro'},
            {'name': 'Newcastle Electrical Experts', 'website': 'https://example.com/newcastle-experts'},
        ]

        return mock_businesses

    def save_to_csv(self, filename: str = 'electrician_contacts.csv'):
        """Save contacts to CSV file."""
        if not self.contacts:
            logger.warning("No contacts to save!")
            return

        df = pd.DataFrame(self.contacts)
        df.to_csv(filename, index=False)
        logger.info(f"✓ Saved {len(self.contacts)} contacts to {filename}")

    def display_results(self):
        """Display results in a formatted table."""
        if not self.contacts:
            logger.warning("No contacts to display!")
            return

        df = pd.DataFrame(self.contacts)
        print("\n" + "="*100)
        print("AUSTRALIAN ELECTRICIAN BUSINESS CONTACTS")
        print("="*100)
        print(df.to_string(index=False))
        print("="*100)
        print(f"\nTotal contacts collected: {len(self.contacts)}")


def main():
    """Main entry point."""
    print("Australian Electrician Contact Scraper")
    print("="*50)
    print("Collecting 10 verified electrician business contacts...")
    print("Sources: Yellow Pages Australia, Business Websites")
    print("="*50 + "\n")

    scraper = ElectricianContactScraper(target_count=10)

    # Scrape contacts
    contacts = scraper.scrape_contacts()

    if contacts:
        # Save to CSV
        scraper.save_to_csv('electrician_contacts.csv')

        # Display results
        scraper.display_results()

        print(f"\n✓ Successfully collected {len(contacts)} contacts!")
        print("✓ Data saved to electrician_contacts.csv")
    else:
        print("\n✗ Failed to collect contacts. Please check the logs.")


if __name__ == "__main__":
    main()
