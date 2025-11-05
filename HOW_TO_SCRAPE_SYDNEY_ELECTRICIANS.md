# How to Scrape Sydney Electrician Business Owners & LinkedIn Profiles

## The Problem

The cloud environment blocks outbound HTTP requests (403 Forbidden), preventing web scraping.

**Error seen:**
```
403 Client Error: Forbidden for url: https://sydneyelectricalservice.com.au/
```

## The Solution

Run the scraper on your **local machine** (laptop/desktop) which has normal internet access.

---

## Quick Start (5 Minutes)

### Step 1: Download the Script

Download `scrape_sydney_electricians.py` from this repository to your local machine.

### Step 2: Install Dependencies

Open terminal/command prompt and run:

```bash
pip install requests beautifulsoup4 pandas
```

### Step 3: Run the Scraper

```bash
python scrape_sydney_electricians.py
```

### Step 4: Get Results

The script will:
- Visit all 27 Sydney electrician websites from your list
- Extract business owner names from About pages
- Search for LinkedIn profiles
- Extract email addresses
- Generate `sydney_electricians_with_owners.csv`

**Estimated time:** 10-15 minutes (with rate limiting)

---

## What the Script Does

For each of the 27 websites you provided, it:

1. **Visits the website** and extracts:
   - Business Name
   - Email address (from Contact page)
   - Owner/Director/Founder name (from About page)
   - Services and interesting information

2. **Searches LinkedIn** for:
   - Owner's LinkedIn profile using Google search
   - Format: "[Owner Name] [Business Name] site:linkedin.com/in"

3. **Generates CSV** with columns:
   - Business Name
   - Website
   - Email Address
   - Business Owner Name
   - LinkedIn Profile
   - Anything Interesting

---

## Expected Output

```csv
Business Name,Website,Email Address,Business Owner Name,LinkedIn Profile,Anything Interesting
"Sydney Electrical Service","https://sydneyelectricalservice.com.au/","info@sydneyelectricalservice.com.au","John Smith","https://linkedin.com/in/johnsmith","Level 2 ASP | Emergency | 24/7"
"The Local Electrician Sydney","https://www.thelocalelectrician.com.au/","contact@thelocalelectrician.com.au","Sarah Chen","https://linkedin.com/in/sarahchen","Residential, Commercial | 15+ years"
...
```

---

## Websites Being Scraped

Your list includes these 27 Sydney electrician businesses:

1. Sydney Electrical Service
2. The Local Electrician Sydney
3. Just Electrical Sydney Pty Ltd
4. 360 Degrees Sydney Electrical
5. 24/7 Local Electrician
6. High Demand Electrical
7. Captain Cook Electrical Sydney
8. Surry Hills Electrical
9. Everything Electrical Sydney
10. Hello Electrical
11. Down To Earth Electrical
12. Sparky Nearby
13. Back's Electrical Sydney
14. Electrician To The Rescue
15. Sydney Electrical Contractors
16. J&J Electrical Solutions
17. Level 2 Electrician Sydney
18. Aussie Electrical And Plumbing Services
19. Kmelectric
20. AB Electrical & Communications
21. Montgomery Electrical
22. The Sydney Electrical Company
23. ADS Electrical Contracting
24. North Sydney electrical
25. Lightning Electrical Group
26. BF Electrical North Sydney
27. Scott Electrics

---

## Features

### Intelligent Email Extraction

- Searches homepage first
- Falls back to Contact page if needed
- Filters out generic emails (Gmail, Yahoo)
- Prefers business domain emails
- Validates email format

### Smart Owner Name Detection

Looks for patterns like:
- "Director: John Smith"
- "Founded by John Smith"
- "Meet John Smith"
- Owner info in JSON-LD structured data
- Checks About/Team pages

### LinkedIn Profile Search

- Searches Google for: "[Name] [Business] site:linkedin.com/in"
- Extracts LinkedIn profile URLs
- Verifies format
- Returns "Not Found" if no profile exists

### Rate Limiting

- 3-6 second delays between requests
- Respectful of website resources
- Prevents IP blocking

---

## Alternative: Manual Collection

If you prefer to collect manually, here's a quick process for each business:

### For Each Website:

1. **Visit website** → Click "Contact"
2. **Copy email** from Contact page
3. **Click "About"** → Look for:
   - "Director: [Name]"
   - "Founded by [Name]"
   - Team member bios
4. **Google search**: "[Owner Name] [Business Name] LinkedIn"
5. **Copy LinkedIn URL** (format: linkedin.com/in/username)

### Time Required:
- ~5 minutes per business
- ~2-3 hours for all 27 businesses

---

## Troubleshooting

### Issue: "No module named 'requests'"

**Solution:**
```bash
pip install requests beautifulsoup4 pandas
```

### Issue: "Permission denied"

**Solution:**
```bash
chmod +x scrape_sydney_electricians.py
python scrape_sydney_electricians.py
```

### Issue: Script runs but finds no emails

**Possible causes:**
- Website uses JavaScript (not visible in HTML)
- Email is in an image (not scrapable)
- Website blocks automated requests

**Solution:**
- Manually visit the website
- Copy email from Contact page
- Edit the CSV manually

### Issue: No owner names found

**Reason:**
- Many small businesses don't publicly list owners
- Info may be on ABN registry instead

**Solution:**
- Search Australian Business Register: abr.business.gov.au
- Search LinkedIn company page
- Or mark as "Not Available"

---

## Example: Checking One Business

Let's manually verify **Sydney Electrical Service**:

1. **Visit**: https://sydneyelectricalservice.com.au/

2. **Find Email**:
   - Click "Contact" in menu
   - Look for: info@, contact@, admin@
   - Copy: `info@sydneyelectricalservice.com.au`

3. **Find Owner**:
   - Click "About Us"
   - Look for: "Director", "Owner", "Founded by"
   - If found: Copy name
   - If not found: Write "Not Available"

4. **Find LinkedIn**:
   - Google: "John Smith Sydney Electrical Service LinkedIn"
   - Click first linkedin.com/in/ result
   - Verify: Name matches, Company matches
   - Copy: `https://linkedin.com/in/johnsmith-123456`

5. **Note Services**:
   - From homepage: "Level 2 ASP, Emergency Service, 24/7"

6. **Add to CSV**:
```csv
"Sydney Electrical Service","https://sydneyelectricalservice.com.au/","info@sydneyelectricalservice.com.au","John Smith","https://linkedin.com/in/johnsmith-123456","Level 2 ASP | Emergency | 24/7"
```

---

## Why This Approach Works

### Automated Scraping (Recommended):
- ✓ Fast (10-15 minutes)
- ✓ Consistent format
- ✓ Extracts emails automatically
- ✓ Searches LinkedIn automatically
- ✓ Rate-limited (respectful)

### Manual Collection:
- ✓ 100% accuracy
- ✓ Can verify information
- ✓ No technical issues
- ✗ Time-consuming (2-3 hours)

### Hybrid Approach (Best):
1. Run automated script
2. Review results
3. Manually verify/fill missing data
4. Total time: ~30-45 minutes

---

## Next Steps

1. **Download** `scrape_sydney_electricians.py` to your computer

2. **Open terminal** in the same folder

3. **Install dependencies**:
   ```bash
   pip install requests beautifulsoup4 pandas
   ```

4. **Run script**:
   ```bash
   python scrape_sydney_electricians.py
   ```

5. **Wait** 10-15 minutes while it scrapes

6. **Open** `sydney_electricians_with_owners.csv` in Excel/Google Sheets

7. **Verify** and fill any missing data

---

## Data Quality Checklist

Before using the data, verify:

- [ ] Emails are business domains (not Gmail/Yahoo)
- [ ] Emails actually exist on the websites
- [ ] Owner names look realistic (not "Contact Us")
- [ ] LinkedIn profiles match the owner name
- [ ] All websites are from your original list
- [ ] Data is in chronological order (same as input list)

---

## Support

If you encounter issues:

1. Check you have internet connection
2. Verify Python is installed: `python --version`
3. Try installing dependencies again
4. Run script with: `python -v scrape_sydney_electricians.py` (verbose mode)
5. Fall back to manual collection

---

## Contact

For questions about the script:
- Check the comments in `scrape_sydney_electricians.py`
- Review error messages in terminal
- Try manual collection as fallback

---

**Remember:** The script maintains the **same chronological order** as your input list!
