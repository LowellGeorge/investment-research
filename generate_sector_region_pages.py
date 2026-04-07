#!/usr/bin/env python3
"""
generate_sector_region_pages.py — Generate sector and region wiki pages
from company_metadata.json
"""

import json
import re
from pathlib import Path

REPO = Path(__file__).parent
WIKI = REPO / "wiki"

def slug(name):
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def load_metadata():
    with open(WIKI / "company_metadata.json") as f:
        return json.load(f)

def generate_sector_pages(data):
    sectors = {}
    for e in data:
        sb = e["sector_broad"]
        if sb not in sectors:
            sectors[sb] = []
        sectors[sb].append(e)

    # Sector index
    lines = [
        "# Sector Overview",
        "",
        "Investment research organized by sector.",
        "",
        "| Sector | Companies | Regions |",
        "|--------|-----------|---------|",
    ]
    for sector in sorted(sectors):
        s = slug(sector)
        entries = sectors[sector]
        region_set = sorted(set(e["region"] for e in entries))
        region_links = ", ".join(f"[[wiki/regions/{slug(r)}|{r}]]" for r in region_set)
        lines.append(f"| [[wiki/sectors/{s}|{sector}]] | {len(entries)} | {region_links} |")

    with open(WIKI / "sectors" / "_index.md", "w") as f:
        f.write("\n".join(lines))

    # Individual sector pages
    for sector, entries in sorted(sectors.items()):
        s = slug(sector)
        entries_sorted = sorted(entries, key=lambda x: x["company"])

        page = [
            f"---",
            f"sector: \"{sector}\"",
            f"companies: {len(entries)}",
            f"last_updated: 2026-04-07",
            f"---",
            f"",
            f"# {sector}",
            f"",
            f"Sector overview covering {len(entries)} companies across the investment research wiki.",
            f"",
            f"## Companies",
            f"",
            f"| Company | Ticker | Country | Market Cap |",
            f"|---------|--------|---------|------------|",
        ]

        for e in entries_sorted:
            page.append(f"| [[wiki/companies/{e['wiki_slug']}|{e['company']}]] | {e['ticker']} | {e['country']} | {e['market_cap']} |")

        # Geographic distribution
        region_groups = {}
        for e in entries:
            r = e["region"]
            if r not in region_groups:
                region_groups[r] = []
            region_groups[r].append(e)

        page.extend([
            "",
            "## Geographic Distribution",
            "",
        ])
        for region in sorted(region_groups):
            companies = sorted(region_groups[region], key=lambda x: x["company"])
            links = ", ".join(f"[[wiki/companies/{e['wiki_slug']}|{e['company']}]]" for e in companies)
            page.append(f"- **[[wiki/regions/{slug(region)}|{region}]]**: {links}")

        # Cross-sector themes
        page.extend([
            "",
            "## Key Themes",
            "",
        ])

        if sector == "Banking & Financial Services":
            page.extend([
                "- **Digital transformation**: Several banks are leading digital banking innovation, from [[wiki/companies/dbs-group|DBS Group]]'s tech-first strategy to [[wiki/companies/nu-holdings|Nu Holdings]]' mobile-only model",
                "- **Emerging market growth**: Banks in India, Indonesia, and Latin America benefit from low financial penetration and rising middle classes",
                "- **Capital allocation discipline**: Focus on ROE optimization, dividend growth, and selective M&A",
                "- **Regulatory navigation**: Operating across diverse regulatory regimes requires adaptability",
            ])
        elif sector == "Semiconductors":
            page.extend([
                "- **AI-driven demand**: Unprecedented demand for advanced chips and packaging driven by AI training and inference",
                "- **Geopolitical risk**: Taiwan concentration risk, US-China tensions, and supply chain diversification",
                "- **Capital intensity**: Multi-billion dollar fab investments create natural oligopoly dynamics",
                "- **Technology leadership**: Process node advancement as the primary competitive differentiator",
            ])
        elif sector == "Internet & E-Commerce":
            page.extend([
                "- **Platform economics**: Network effects and marketplace dynamics driving scale advantages",
                "- **Regulatory environment**: Varying degrees of regulatory scrutiny across jurisdictions",
                "- **Cross-border expansion**: Companies like [[wiki/companies/sea-ltd|Sea Ltd]] and [[wiki/companies/pdd-holdings|PDD Holdings]] expanding internationally",
                "- **Monetization evolution**: Shift from GMV growth to profitability and shareholder returns",
            ])
        elif sector == "Internet & Gaming":
            page.extend([
                "- **IP ownership**: Proprietary game franchises and content as durable moats",
                "- **Platform diversification**: Expansion beyond core gaming into cloud, payments, and social media",
                "- **China regulatory cycle**: Navigating game approvals and content restrictions",
                "- **Global distribution**: Leveraging digital platforms for worldwide reach",
            ])
        elif sector == "Industrials":
            page.extend([
                "- **Manufacturing excellence**: Companies leveraging scale and process know-how",
                "- **China exposure**: Several companies tied to Chinese manufacturing and infrastructure",
                "- **Energy transition**: Beneficiaries of electrification and renewable energy trends",
                "- **Global supply chains**: Serving multinational customers across geographies",
            ])
        elif sector == "Healthcare":
            page.extend([
                "- **Aging demographics**: Growing healthcare demand from aging populations globally",
                "- **Innovation-driven moats**: R&D investment creating sustainable competitive advantages",
                "- **Regulatory barriers**: FDA/CE approvals as meaningful entry barriers",
                "- **Geographic expansion**: Emerging market growth as developed markets mature",
            ])
        elif sector == "Consumer Discretionary":
            page.extend([
                "- **Brand building**: Companies investing in brand equity for pricing power",
                "- **Asia consumption growth**: Rising middle class driving demand for discretionary goods",
                "- **Multi-brand strategies**: Portfolio approaches to capture different consumer segments",
                "- **Digital channels**: E-commerce and DTC as growth accelerators",
            ])
        elif sector == "Consumer Staples":
            page.extend([
                "- **Defensive characteristics**: Resilient demand through economic cycles",
                "- **Market penetration**: Growth through geographic expansion and store rollouts",
                "- **Brand loyalty**: Consumer habits creating switching costs",
                "- **Input cost management**: Navigating commodity and labor inflation",
            ])
        elif sector == "Insurance":
            page.extend([
                "- **Underpenetration**: Low insurance penetration in emerging markets offers growth runway",
                "- **Underwriting discipline**: Consistent combined ratios as competitive differentiator",
                "- **Distribution advantages**: Agency networks and distribution partnerships",
                "- **Investment income**: Float management as secondary income driver",
            ])
        elif sector == "Technology & Software":
            page.extend([
                "- **Digital transformation**: Secular demand for IT services and software",
                "- **Recurring revenue**: SaaS and subscription models providing visibility",
                "- **Talent arbitrage**: Leveraging cost-competitive engineering talent pools",
                "- **AI integration**: Opportunity and disruption from AI adoption",
            ])
        elif sector == "Technology Hardware":
            page.extend([
                "- **AI infrastructure buildout**: Servers and hardware demand driven by AI investment cycle",
                "- **Vertical integration**: Manufacturing capabilities as competitive advantage",
                "- **Cyclical dynamics**: Technology investment cycles affecting demand patterns",
            ])
        elif sector == "Distributors":
            page.extend([
                "- **Scale advantages**: Distribution network density creating barriers to entry",
                "- **Recurring demand**: Essential products driving repeat purchase patterns",
                "- **Consolidation opportunity**: Fragmented markets enabling M&A-driven growth",
            ])

        # Comparisons link
        page.extend([
            "",
            "## Related",
            "",
            "- [[wiki/_index|Back to Index]]",
        ])

        with open(WIKI / "sectors" / f"{s}.md", "w") as f:
            f.write("\n".join(page))

    print(f"Generated {len(sectors)} sector pages + index")


def generate_region_pages(data):
    regions = {}
    for e in data:
        r = e["region"]
        if r not in regions:
            regions[r] = []
        regions[r].append(e)

    # Region index
    lines = [
        "# Regional Overview",
        "",
        "Investment research organized by geography.",
        "",
        "| Region | Companies | Sectors |",
        "|--------|-----------|---------|",
    ]
    for region in sorted(regions):
        r = slug(region)
        entries = regions[region]
        sector_set = sorted(set(e["sector_broad"] for e in entries))
        sector_links = ", ".join(f"[[wiki/sectors/{slug(s)}|{s}]]" for s in sector_set)
        lines.append(f"| [[wiki/regions/{r}|{region}]] | {len(entries)} | {sector_links} |")

    with open(WIKI / "regions" / "_index.md", "w") as f:
        f.write("\n".join(lines))

    # Individual region pages
    for region, entries in sorted(regions.items()):
        r = slug(region)
        entries_sorted = sorted(entries, key=lambda x: x["company"])

        page = [
            f"---",
            f"region: \"{region}\"",
            f"companies: {len(entries)}",
            f"last_updated: 2026-04-07",
            f"---",
            f"",
            f"# {region}",
            f"",
            f"Regional overview covering {len(entries)} companies in the investment research wiki.",
            f"",
            f"## Companies",
            f"",
            f"| Company | Ticker | Sector | Market Cap |",
            f"|---------|--------|--------|------------|",
        ]

        for e in entries_sorted:
            page.append(f"| [[wiki/companies/{e['wiki_slug']}|{e['company']}]] | {e['ticker']} | {e['sector_broad']} | {e['market_cap']} |")

        # Sector distribution
        sector_groups = {}
        for e in entries:
            sb = e["sector_broad"]
            if sb not in sector_groups:
                sector_groups[sb] = []
            sector_groups[sb].append(e)

        page.extend([
            "",
            "## By Sector",
            "",
        ])
        for sector in sorted(sector_groups):
            companies = sorted(sector_groups[sector], key=lambda x: x["company"])
            links = ", ".join(f"[[wiki/companies/{e['wiki_slug']}|{e['company']}]]" for e in companies)
            page.append(f"- **[[wiki/sectors/{slug(sector)}|{sector}]]**: {links}")

        # Regional themes
        page.extend([
            "",
            "## Regional Themes",
            "",
        ])

        if region == "China":
            page.extend([
                "- **Regulatory environment**: Navigating evolving regulatory landscape post-2021 crackdown",
                "- **Consumer upgrading**: Rising middle class driving premiumization across categories",
                "- **Technology self-sufficiency**: Government push for domestic technology capabilities",
                "- **Geopolitical tensions**: US-China friction affecting cross-border investment and supply chains",
                "- **VIE structure risk**: Offshore listing structures creating governance complexity",
            ])
        elif region == "India":
            page.extend([
                "- **Demographic dividend**: Young population driving consumption and financial inclusion",
                "- **Digital infrastructure**: UPI, Aadhaar, and GST creating platform for financial services growth",
                "- **Banking underpenetration**: Low credit-to-GDP ratio offering multi-decade growth runway",
                "- **Reform momentum**: Government policy supporting infrastructure and manufacturing investment",
                "- **Valuation premium**: Quality Indian companies consistently trade at premium multiples",
            ])
        elif region == "Southeast Asia":
            page.extend([
                "- **Young demographics**: Fast-growing populations with rising incomes",
                "- **Digital adoption**: Rapid smartphone and internet penetration driving fintech and e-commerce",
                "- **China+1**: Manufacturing diversification benefiting regional economies",
                "- **Banking dominance**: Well-run banks capturing disproportionate share of economic growth",
            ])
        elif region == "Taiwan & Korea":
            page.extend([
                "- **Semiconductor leadership**: Global dominance in chip manufacturing and memory",
                "- **Chaebol/conglomerate structures**: Complex holding structures affecting governance",
                "- **Shareholder value reform**: Korea's Corporate Value-up program improving capital returns",
                "- **Geopolitical exposure**: Cross-strait tensions and Korean peninsula risk",
                "- **Technology innovation**: Deep engineering talent pools driving competitive advantage",
            ])
        elif region == "Latin America":
            page.extend([
                "- **Fintech disruption**: Digital banking and payments transforming financial services",
                "- **Consumer market depth**: Large populations with growing middle classes",
                "- **Currency and macro risk**: Exposure to commodity cycles and political volatility",
                "- **Nearshoring opportunity**: Manufacturing investment shifting closer to US",
                "- **Remittance economy**: Cross-border flows as a growth driver for financial services",
            ])
        elif region == "Japan":
            page.extend([
                "- **Corporate governance reform**: Tokyo Stock Exchange reforms driving shareholder value",
                "- **IP-rich businesses**: Globally recognized brands and content franchises",
                "- **Currency dynamics**: Yen weakness affecting translated earnings and competitiveness",
                "- **Aging demographics**: Both challenge and opportunity for different sectors",
            ])
        elif region == "ANZ":
            page.extend([
                "- **Healthcare innovation**: Strong medtech and biotech ecosystem",
                "- **Developed market stability**: Mature regulatory and governance frameworks",
                "- **Asia-Pacific proximity**: Positioned to serve growing Asian healthcare demand",
            ])
        elif region == "Greater China":
            page.extend([
                "- **Hong Kong as gateway**: Companies leveraging HK as bridge between East and West",
                "- **Pan-Asian reach**: Businesses with footprints spanning Greater China and Southeast Asia",
                "- **Global brands**: Companies with operations extending well beyond the region",
            ])
        elif region == "Europe":
            page.extend([
                "- **Diverse business models**: From consumer retail to tech investment holding companies",
                "- **Regulatory maturity**: Operating within well-established governance frameworks",
                "- **Emerging market exposure**: European-listed companies with EM growth profiles",
            ])
        elif region == "Africa":
            page.extend([
                "- **Financial inclusion**: Massive unbanked population creating growth opportunity",
                "- **Technology-led disruption**: Leapfrogging traditional banking infrastructure",
                "- **Regulatory environment**: Navigating complex and evolving financial regulation",
            ])
        elif region == "United States":
            page.extend([
                "- **Technology leadership**: Global technology and innovation hub",
                "- **Deep capital markets**: Access to the world's most liquid equity and debt markets",
                "- **Mature competitive dynamics**: Established market positions with high barriers to entry",
            ])

        page.extend([
            "",
            "## Related",
            "",
            "- [[wiki/_index|Back to Index]]",
        ])

        with open(WIKI / "regions" / f"{r}.md", "w") as f:
            f.write("\n".join(page))

    print(f"Generated {len(regions)} region pages + index")


if __name__ == "__main__":
    data = load_metadata()
    generate_sector_pages(data)
    generate_region_pages(data)
