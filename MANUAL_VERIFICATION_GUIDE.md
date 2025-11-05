# Manual Verification Guide for Australian Electrician Contacts

## Why Manual Verification is Needed

The cloud environment has network restrictions preventing direct web scraping. To get **real, verified data**, you need to:

1. Run the scraping scripts on your **local machine** (with internet access)
2. OR manually verify and collect data using this guide

## Method 1: Run Scripts Locally (Recommended)

### Setup on Your Local Machine

```bash
# Install dependencies
pip install requests beautifulsoup4 pandas lxml

# Run the verified scraper
python scrape_verified_electricians.py
```

This will:
- Visit real Australian electrician websites
- Extract real email addresses
- Find owner/director names
- Search for LinkedIn profiles
- Generate CSV with verified data

## Method 2: Manual Data Collection

### Step-by-Step Process

For each business, collect:

1. **Business Name** - From website title or header
2. **Website URL** - The actual business website
3. **Email Address** - From Contact page (must be business domain, not Gmail)
4. **Owner/Director Name** - From About page or team section
5. **LinkedIn Profile** - Search "Owner Name + Business Name + LinkedIn" on Google
6. **Interesting Info** - Services, years in business, certifications

### Example: How to Verify One Business

#### Example: Level 2 Electrical Sydney

1. **Visit Website**: https://www.level2.com.au/

2. **Extract Business Name**:
   - Look at page title or main header
   - Usually in format: "Business Name - Location"

3. **Find Email**:
   - Check "Contact" page
   - Look for: info@, contact@, admin@, hello@ with business domain
   - **Avoid**: Gmail, Yahoo, Hotmail addresses

4. **Find Owner Name**:
   - Check "About Us" page
   - Look for:
     - "Director: John Smith"
     - "Founded by John Smith"
     - "Meet the team" section
   - Note: Some businesses don't publicly list owners

5. **Find LinkedIn**:
   - Google search: "John Smith Level 2 Electrical LinkedIn"
   - Look for: linkedin.com/in/john-smith-xxxxx
   - Verify it matches the business

6. **Extract Interesting Info**:
   - Services: "Residential, Commercial, Level 2 ASP"
   - Experience: "15+ years in business"
   - Certifications: "Licensed Master Electrician"
   - Special: "24/7 Emergency Service"

### Real Australian Electrician Business Sources

Use these sources to find real businesses:

1. **Google Search**:
   ```
   "electrician Sydney" site:.com.au
   "electrician Melbourne" site:.com.au
   ```

2. **Business Directories**:
   - Yellow Pages Australia: yellowpages.com.au
   - True Local: truelocal.com.au
   - Hipages: hipages.com.au

3. **Google Maps**:
   - Search "electricians near Sydney"
   - Filter for businesses with websites
   - Visit their actual websites

### Data Validation Checklist

Before adding to your list, verify:

- [ ] Business has a professional website (.com.au preferred)
- [ ] Email is business domain (not Gmail/Yahoo)
- [ ] Business appears legitimate (not spam)
- [ ] Website is active and working
- [ ] Business operates in Australia

### Example Real Data Format

```csv
Business Name,Website,Email Address,Business Owner Name,LinkedIn Profile,Anything Interesting
"Level 2 Electrical Sydney Pty Ltd","https://www.level2.com.au","info@level2.com.au","John Smith","https://linkedin.com/in/johnsmith","Level 2 ASP | Residential & Commercial | 15+ years | Licensed"
```

## Method 3: Use API Services (Most Reliable)

For production use, consider:

1. **Google Places API**
   - Official business data
   - Includes contact info, reviews
   - Paid service with free tier

2. **Australian Business Register API**
   - Government ABN lookup
   - Official business details
   - Free for legitimate use

3. **LinkedIn API**
   - Official profile data
   - Requires application approval
   - Most accurate for professional profiles

### Google Places API Example

```python
import googlemaps

gmaps = googlemaps.Client(key='YOUR_API_KEY')

# Search for electricians
places = gmaps.places('electrician in Sydney Australia')

for place in places['results']:
    place_id = place['place_id']
    details = gmaps.place(place_id)

    # Extract contact info
    name = details['result']['name']
    website = details['result'].get('website')
    phone = details['result'].get('formatted_phone_number')
    # ... extract more details
```

## Common Issues and Solutions

### Issue 1: No Email on Website

**Solution**:
- Check multiple pages (Contact, About, Footer)
- Look in privacy policy or terms
- Use WHOIS lookup for domain contact
- Contact via form and ask for email

### Issue 2: Can't Find Owner Name

**Solution**:
- Check ABN lookup (business.gov.au)
- Search company on LinkedIn company page
- Check "Our Team" or "Staff" sections
- Some businesses keep this private (note as "Not Available")

### Issue 3: LinkedIn Profile Uncertain

**Solution**:
- Verify profile photo matches business website
- Check profile shows same company
- Verify location matches
- If uncertain, mark as "Not Confirmed"

## Tools to Help

### Email Finding Tools

- Hunter.io - Find email patterns
- Voila Norbert - Email verification
- Snov.io - Business email finder

### LinkedIn Tools

- LinkedIn Sales Navigator (paid)
- LinkedIn search with company filter
- Google search: site:linkedin.com/in "company name"

### Website Analysis

- BuiltWith.com - Check website tech
- Whois lookup - Domain registration info
- Archive.org - Check business history

## Final Output Format

Your CSV should have these columns:

| Column Name | Description | Example |
|------------|-------------|---------|
| Business Name | Full legal or trading name | "Level 2 Electrical Sydney Pty Ltd" |
| Website | Full URL | "https://www.level2.com.au" |
| Email Address | Business email only | "info@level2.com.au" |
| Business Owner Name | Director/Owner/Founder | "John Smith" or "Not Available" |
| LinkedIn Profile | Full LinkedIn URL | "https://linkedin.com/in/johnsmith" or "Not Found" |
| Anything Interesting | Services, experience, etc. | "Level 2 ASP \| Residential \| 15+ years" |

## Quality Standards

For your data to be considered "verified":

1. **Email must be verified**:
   - Actually exists on the website
   - Is a business domain
   - Format is valid

2. **Business must be real**:
   - Active website
   - Real Australian business
   - Professional online presence

3. **Data must be current**:
   - Website is active (not 404)
   - Email domain is active
   - Business appears operational

## Next Steps

1. Run `scrape_verified_electricians.py` on your local machine
2. OR manually collect 10 businesses using this guide
3. Verify each entry meets quality standards
4. Save to CSV in the specified format

## Support

If you encounter issues:

1. Check the error logs in the Python scripts
2. Verify your internet connection
3. Try different businesses if some fail
4. Use manual collection as fallback

Remember: **Quality over quantity** - 10 verified, accurate contacts are better than 100 inaccurate ones.
