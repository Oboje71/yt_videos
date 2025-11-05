# Australian Electrician Business Contact Scraper

This project contains Python scripts for collecting publicly available business contact information for electricians in Australia.

## Files

1. **scrape_electricians.py** - Full-featured scraper with Yellow Pages integration
2. **scrape_electricians_demo.py** - Demonstration version with both demo and live modes
3. **electrician_contacts.csv** - Output file with collected contacts

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Demo Mode (Recommended for Testing)

Generate sample data with realistic Australian electrician business information:

```bash
python scrape_electricians_demo.py --mode demo
```

This will:
- Generate 10 realistic electrician business contacts
- Save to `electrician_contacts.csv`
- Display formatted table in console

### Live Mode (Real Scraping)

Attempt to scrape real websites (results may vary based on website accessibility):

```bash
python scrape_electricians_demo.py --mode live
```

### Custom Number of Contacts

```bash
python scrape_electricians_demo.py --mode demo --count 20
```

### Full-Featured Scraper

```bash
python scrape_electricians.py
```

## Features

### Data Collected

For each business, the script collects:

1. **Business Name** - Full legal or trading name
2. **Email Address** - Verified business email (not Gmail/Yahoo/etc.)
3. **Business Owner Name** - Owner, Director, or Manager name
4. **Anything Interesting** - Specializations, years in business, certifications, etc.

### Email Validation

- Basic format validation using regex
- Business email filtering (excludes Gmail, Yahoo, Hotmail, etc.)
- Domain verification (checks MX records in full version)

### Data Sources

The scripts can collect data from:

- Yellow Pages Australia (yellowpages.com.au)
- Business websites directly
- Google Maps/Places (with API)
- Other public business directories

### Rate Limiting

- 2-5 second delays between requests
- Respectful of robots.txt
- Random delays to avoid detection

## Output Format

CSV file with columns:

| Business Name | Email Address | Business Owner Name | Anything Interesting |
|---------------|---------------|---------------------|----------------------|
| Sydney Sparks Electrical Pty Ltd | info@sydneysparks.com.au | Michael Thompson | Residential & Commercial \| 15+ years experience |

## Sample Output

```
================================================================================
                    AUSTRALIAN ELECTRICIAN BUSINESS CONTACTS
================================================================================
Business Name                          Email Address                    Business Owner Name    Anything Interesting
Sydney Sparks Electrical Pty Ltd       info@sydneysparks.com.au        Michael Thompson       Residential & Commercial | 15+ years
Melbourne Electrical Services          contact@melbourneelectrical...  Sarah Chen             Solar Installation | 24/7 Emergency
Brisbane Bright Solutions              admin@brisbanebright.com.au     David Wilson           Commercial & Industrial | Est. 2005
...
================================================================================
Total contacts collected: 10
```

## Technical Details

### Libraries Used

- **requests** - HTTP requests
- **beautifulsoup4** - HTML parsing
- **pandas** - Data manipulation and CSV export
- **email-validator** - Email validation
- **dnspython** - DNS/MX record verification
- **lxml** - Fast HTML parsing

### Modular Design

The code is organized into classes:

- `EmailExtractor` - Extract and validate emails from websites
- `BusinessInfoExtractor` - Extract owner names and interesting details
- `YellowPagesScraperAU` - Scrape Yellow Pages Australia listings
- `ElectricianContactScraper` - Main orchestrator class

## Ethical Considerations

This scraper:

- ✓ Only collects publicly available information
- ✓ Respects robots.txt and rate limits
- ✓ Focuses on business contact info (not personal data)
- ✓ Uses appropriate delays between requests
- ✓ Provides user-agent identification

## Troubleshooting

### No Emails Found

Some business websites may not have email addresses displayed in text. Consider:
- Using contact form scraping
- Looking for social media links
- Checking domain WHOIS data

### Website Blocking

If websites block the scraper:
- Increase delays between requests
- Use rotating user agents
- Consider using proxy services
- Use official APIs where available

### Invalid Emails

Email validation may fail if:
- Domain has no MX records (temporarily down)
- Email is obfuscated on website
- Website uses JavaScript to render emails

## Future Enhancements

- [ ] Google Places API integration
- [ ] Multi-threading for faster scraping
- [ ] Email deliverability testing
- [ ] Social media profile linking
- [ ] Phone number extraction
- [ ] ABN (Australian Business Number) lookup
- [ ] Integration with CRM systems

## Legal Notice

This tool is for collecting publicly available business information only. Users must:

- Comply with all applicable laws and regulations
- Respect website terms of service
- Follow data protection and privacy laws
- Use data responsibly and ethically

## License

This project is provided as-is for educational and legitimate business purposes.

## Support

For issues or questions, please refer to the script documentation and error logs.
