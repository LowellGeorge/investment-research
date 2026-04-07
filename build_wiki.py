#!/usr/bin/env python3
"""
build_wiki.py — Parse raw analysis .md files and generate wiki/_index.md
Also outputs company_metadata.json for downstream wiki generation.
"""

import os
import re
import json
from pathlib import Path

REPO = Path(__file__).parent
RAW_DIR = REPO
WIKI_DIR = REPO / "wiki"

# Map of company name -> preferred file (qanalysis > analysis)
def get_company_files():
    """Scan raw .md files, deduplicate (prefer qanalysis), return sorted list.
    Case-insensitive deduplication: if both 'mediatek-analysis.md' and 'Mediatek-qanalysis.md'
    exist, keep the qanalysis version with the cased name from that file.
    """
    files = {}
    # Track by lowercase key for dedup
    seen_lower = {}
    for f in sorted(RAW_DIR.glob("*.md")):
        name = f.name
        if name.endswith("-qanalysis.md"):
            company = name.replace("-qanalysis.md", "")
            key = company.lower()
            seen_lower[key] = company
            files[company] = {"file": name, "type": "qanalysis"}
            # Remove any case-variant analysis entry
            for existing in list(files.keys()):
                if existing.lower() == key and existing != company:
                    del files[existing]
        elif name.endswith("-analysis.md"):
            company = name.replace("-analysis.md", "")
            key = company.lower()
            # Only add if no qanalysis exists (case-insensitive)
            if key not in seen_lower:
                files[company] = {"file": name, "type": "analysis"}
                seen_lower[key] = company
    return files


def parse_metadata(filepath):
    """Extract metadata from first 15 lines of an analysis file."""
    meta = {
        "ticker": "",
        "country": "",
        "sector": "",
        "market_cap": "",
        "date": "",
        "title": "",
    }

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()[:20]

    header_text = "".join(lines)

    # Title from first line
    if lines and lines[0].startswith("#"):
        meta["title"] = lines[0].strip("# \n")

    # Date
    date_match = re.search(r"\*\*Date:\*\*\s*(.+?)(?:\n|\*\*)", header_text)
    if date_match:
        meta["date"] = date_match.group(1).strip()

    # Ticker - various formats
    ticker_match = re.search(r"\*\*Ticker:\*\*\s*([^\n|*]+)", header_text)
    if ticker_match:
        meta["ticker"] = ticker_match.group(1).strip().split("|")[0].strip()
    else:
        # Try extracting from title: "Company (TICKER)"
        title_ticker = re.search(r"\(([A-Z0-9.:]+(?:\s*/\s*[A-Z0-9.:]+)?)\)", meta["title"])
        if title_ticker:
            meta["ticker"] = title_ticker.group(1).strip()

    # Market Cap
    mcap_match = re.search(r"\*\*Market\s*Cap:\*\*\s*([^\n|*]+)", header_text)
    if mcap_match:
        meta["market_cap"] = mcap_match.group(1).strip()

    # Sector
    sector_match = re.search(r"\*\*(?:Sector|GICS):\*\*\s*([^\n|*]+)", header_text)
    if sector_match:
        meta["sector"] = sector_match.group(1).strip()

    # Country
    country_match = re.search(r"\*\*Country:\*\*\s*([^\n|*]+)", header_text)
    if country_match:
        meta["country"] = country_match.group(1).strip()
    elif "Headquarters:" in header_text:
        hq_match = re.search(r"\*\*Headquarters:\*\*\s*([^\n|*]+)", header_text)
        if hq_match:
            meta["country"] = hq_match.group(1).strip()

    return meta


def slug(name):
    """Convert company name to a wiki-safe slug."""
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


# Country inference for files that don't explicitly state it
COUNTRY_MAP = {
    "AIA": "Hong Kong",
    "Alibaba": "China",
    "Anta Sports Products": "China",
    "China Mengniu Dairy": "China",
    "China resources beer": "China",
    "Full Truck Alliance": "China",
    "Hongfa Technology": "China",
    "Huazhu Group": "China",
    "LG Corp": "South Korea",
    "Midea Group": "China",
    "Netease": "China",
    "PDD Holdings": "China",
    "Prosus": "Netherlands",
    "Samsung Electronics": "South Korea",
    "Shenzhen Mindray": "China",
    "Sony": "Japan",
    "Tencent": "China",
    "Trip.com": "China",
    "Zhejiang Chint Electrics": "China",
    "Airtac International": "Taiwan",
    "TSMC": "Taiwan",
    "Mediatek": "Taiwan",
    "mediatek": "Taiwan",
    "Silergy": "Taiwan",
    "Quanta Computer": "Taiwan",
    "HCL Technologies": "India",
    "HDFC Bank": "India",
    "ICICI Bank": "India",
    "ICICI Lombard": "India",
    "Kotak Mahindra Bank": "India",
    "Mahindra & Mahaindra": "India",
    "Computer Age Management Services": "India",
    "United Breweries Limited": "India",
    "DBS Group": "Singapore",
    "Sea Ltd": "Singapore",
    "Jardine Matheson Holdings": "Singapore",
    "PT Bank Central Asia": "Indonesia",
    "Bank of the Philippine Islands": "Philippines",
    "FPT Corp": "Vietnam",
    "Fisher & Paykel": "New Zealand",
    "CSL Holdings": "Australia",
    "Resmed": "Australia",
    "Techtronic": "Hong Kong",
    "SK Hynix": "South Korea",
    "KB Financial Group": "South Korea",
    "Nintendo": "Japan",
    "Microsoft": "United States",
    "POOL Corp": "United States",
    "Nu Holdings": "Brazil",
    "TOTVS": "Brazil",
    "Credicorp": "Peru",
    "Regional S.A.B.": "Mexico",
    "Alsea S.A.B.": "Mexico",
    "Qualitas Controladora": "Mexico",
    "Wal Mart de Mexico SAB": "Mexico",
    "Dino Polska": "Poland",
    "Capitec Bank": "South Africa",
}

# Sector inference for files that don't have it in headers
SECTOR_MAP = {
    "AIA": "Insurance",
    "Microsoft": "Software",
    "Netease": "Interactive Media and Services",
    "Nintendo": "Interactive Home Entertainment",
    "POOL Corp": "Distributors",
    "Silergy": "Semiconductors",
    "SK Hynix": "Semiconductors",
    "TSMC": "Semiconductors",
    "mediatek": "Semiconductors",
    "Tencent": "Interactive Media and Services",
    "Sea Ltd": "Broadline Retail",
    "HDFC Bank": "Diversified Banks",
    "LG Corp": "Industrial Conglomerates",
    "HCL Technologies": "IT Consulting and Other Services",
    "Mahindra & Mahaindra": "Automobile Manufacturers",
}

# Ticker overrides for files where parsing fails
TICKER_MAP = {
    "AIA": "1299.HK",
    "Alsea S.A.B.": "ALSEA (BMV)",
    "Capitec Bank": "CPI (JSE)",
    "China Mengniu Dairy": "2319.HK",
    "CSL Holdings": "CSL (ASX)",
    "Dino Polska": "DNP (WSE)",
    "FPT Corp": "FPT (HOSE)",
    "KB Financial Group": "A105560 (KRX)",
    "LG Corp": "003550 (KRX)",
    "Netease": "NTES / 9999.HK",
    "Nintendo": "7974.T / NTDOY",
    "POOL Corp": "POOL (NASDAQ)",
    "Silergy": "6415.TW",
    "SK Hynix": "000660 (KRX)",
}

# Market cap overrides
MCAP_MAP = {
    "AIA": "~$85B USD",
    "Netease": "~$63B USD",
    "Nintendo": "~$85B USD",
    "POOL Corp": "~$14B USD",
    "Silergy": "~$6B USD",
}

# Country cleanup — normalize parsed values
COUNTRY_CLEANUP = {
    "Hangzhou, China": "China",
    "Lima, Peru (incorporated in Bermuda)": "Peru",
}


def normalize_sector(sector_raw):
    """Group detailed GICS sectors into broader categories."""
    s = sector_raw.lower()
    if any(k in s for k in ["bank", "financial"]):
        return "Banking & Financial Services"
    if any(k in s for k in ["semiconductor", "semis"]):
        return "Semiconductors"
    if any(k in s for k in ["software", "systems software", "it consulting", "data processing"]):
        return "Technology & Software"
    if any(k in s for k in ["broadline retail", "e-commerce"]):
        return "Internet & E-Commerce"
    if any(k in s for k in ["interactive media", "interactive home"]):
        return "Internet & Gaming"
    if any(k in s for k in ["insurance"]):
        return "Insurance"
    if any(k in s for k in ["health care", "biotech"]):
        return "Healthcare"
    if any(k in s for k in ["food", "brewer", "packaged food", "dairy", "consumer staples", "merchandise retail"]):
        return "Consumer Staples"
    if any(k in s for k in ["apparel", "hotel", "restaurant", "consumer"]):
        return "Consumer Discretionary"
    if any(k in s for k in ["automobile"]):
        return "Industrials"
    if any(k in s for k in ["industrial", "machinery", "electrical", "cargo", "appliance", "conglomerate"]):
        return "Industrials"
    if any(k in s for k in ["technology hardware", "electronic"]):
        return "Technology Hardware"
    if any(k in s for k in ["distributor"]):
        return "Distributors"
    if any(k in s for k in ["property", "casualty"]):
        return "Insurance"
    return sector_raw


def normalize_region(country):
    """Map country to region."""
    regions = {
        "India": "India",
        "China": "China",
        "Taiwan": "Taiwan & Korea",
        "South Korea": "Taiwan & Korea",
        "Japan": "Japan",
        "Singapore": "Southeast Asia",
        "Indonesia": "Southeast Asia",
        "Philippines": "Southeast Asia",
        "Vietnam": "Southeast Asia",
        "Hong Kong": "Greater China",
        "Brazil": "Latin America",
        "Peru": "Latin America",
        "Mexico": "Latin America",
        "Poland": "Europe",
        "Netherlands": "Europe",
        "South Africa": "Africa",
        "Australia": "ANZ",
        "New Zealand": "ANZ",
        "United States": "United States",
    }
    return regions.get(country, "Other")


def main():
    companies = get_company_files()
    metadata = []

    for company, info in sorted(companies.items()):
        filepath = RAW_DIR / info["file"]
        meta = parse_metadata(filepath)

        # Fill in missing country/sector from maps
        if not meta["country"] and company in COUNTRY_MAP:
            meta["country"] = COUNTRY_MAP[company]
        if not meta["sector"] and company in SECTOR_MAP:
            meta["sector"] = SECTOR_MAP[company]
        if not meta["ticker"] and company in TICKER_MAP:
            meta["ticker"] = TICKER_MAP[company]
        if not meta["market_cap"] and company in MCAP_MAP:
            meta["market_cap"] = MCAP_MAP[company]
        # Clean up country values
        if meta["country"] in COUNTRY_CLEANUP:
            meta["country"] = COUNTRY_CLEANUP[meta["country"]]

        wiki_slug = slug(company)
        sector_broad = normalize_sector(meta["sector"]) if meta["sector"] else "Unknown"
        region = normalize_region(meta["country"]) if meta["country"] else "Unknown"

        entry = {
            "company": company,
            "wiki_slug": wiki_slug,
            "raw_file": info["file"],
            "analysis_type": info["type"],
            "ticker": meta["ticker"],
            "country": meta["country"],
            "sector": meta["sector"],
            "sector_broad": sector_broad,
            "region": region,
            "market_cap": meta["market_cap"],
            "date": meta["date"],
            "title": meta["title"],
        }
        metadata.append(entry)

    # Save metadata
    with open(WIKI_DIR / "company_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    # Generate _index.md
    generate_index(metadata)

    print(f"Processed {len(metadata)} companies")
    print(f"Metadata saved to wiki/company_metadata.json")
    print(f"Index saved to wiki/_index.md")


def generate_index(metadata):
    """Generate wiki/_index.md master table."""
    lines = [
        "# Investment Research Wiki",
        "",
        "Auto-generated knowledge base covering {} companies across {} sectors and {} regions.".format(
            len(metadata),
            len(set(e["sector_broad"] for e in metadata)),
            len(set(e["region"] for e in metadata)),
        ),
        "",
        "## Quick Links",
        "",
        "- [[wiki/sectors/_index|Sectors Overview]]",
        "- [[wiki/regions/_index|Regions Overview]]",
        "- [[wiki/concepts/_index|Investment Concepts]]",
        "- [[wiki/comparisons/_index|Peer Comparisons]]",
        "",
        "---",
        "",
        "## All Companies",
        "",
        "| Company | Ticker | Sector | Country | Market Cap | Wiki | Raw |",
        "|---------|--------|--------|---------|------------|------|-----|",
    ]

    for e in sorted(metadata, key=lambda x: x["company"]):
        wiki_link = f"[[{e['wiki_slug']}|{e['company']}]]"
        raw_link = f"[raw](/{e['raw_file']})"
        lines.append(
            f"| {wiki_link} | {e['ticker']} | {e['sector_broad']} | {e['country']} | {e['market_cap']} | [[wiki/companies/{e['wiki_slug']}|page]] | {raw_link} |"
        )

    # Sector summary
    lines.extend([
        "",
        "---",
        "",
        "## By Sector",
        "",
    ])

    sectors = {}
    for e in metadata:
        sb = e["sector_broad"]
        if sb not in sectors:
            sectors[sb] = []
        sectors[sb].append(e)

    for sector in sorted(sectors.keys()):
        sector_slug = slug(sector)
        entries = sectors[sector]
        company_links = ", ".join(f"[[wiki/companies/{e['wiki_slug']}|{e['company']}]]" for e in sorted(entries, key=lambda x: x["company"]))
        lines.append(f"### [[wiki/sectors/{sector_slug}|{sector}]] ({len(entries)})")
        lines.append(f"{company_links}")
        lines.append("")

    # Region summary
    lines.extend([
        "---",
        "",
        "## By Region",
        "",
    ])

    regions = {}
    for e in metadata:
        r = e["region"]
        if r not in regions:
            regions[r] = []
        regions[r].append(e)

    for region in sorted(regions.keys()):
        region_slug = slug(region)
        entries = regions[region]
        company_links = ", ".join(f"[[wiki/companies/{e['wiki_slug']}|{e['company']}]]" for e in sorted(entries, key=lambda x: x["company"]))
        lines.append(f"### [[wiki/regions/{region_slug}|{region}]] ({len(entries)})")
        lines.append(f"{company_links}")
        lines.append("")

    with open(WIKI_DIR / "_index.md", "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
