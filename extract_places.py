#!/usr/bin/env python3
"""
Extract Hekataios places from Topostext and generate GeoJSON.

This script scrapes the Topostext database to extract places mentioned in
Hekataios of Miletus's fragments and creates a GeoJSON file for mapping.

Usage:
    python extract_places.py [--output OUTPUT_FILE]

Notes:
- Hekataios of Miletus ID on Topostext: 13921
- This scrapes the web frontend, so may break if DOM structure changes
- Respects rate limiting to avoid overwhelming the server
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import argparse
import re
from urllib.parse import urljoin
from collections import defaultdict

# Configuration
TOPOSTEXT_BASE = "https://topostext.org"
HEKATAIOS_ID = "13921"
HEKATAIOS_URL = f"{TOPOSTEXT_BASE}/people/{HEKATAIOS_ID}"
HEADERS = {'User-Agent': 'Academic-Research-Hekataios-Mapping/1.0'}
RATE_LIMIT_DELAY = 1.5  # seconds between requests


def extract_coordinates_from_page(place_url):
    """
    Extract lat/lon coordinates from a Topostext place page.

    Args:
        place_url: Full URL to the place page

    Returns:
        tuple: (latitude, longitude) or None if not found
    """
    try:
        time.sleep(RATE_LIMIT_DELAY)
        response = requests.get(place_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Method 1: Look for coordinates in the page source
        text = response.text

        # Pattern like: "coordinates":[27.27,37.53] or [lon, lat]
        coord_match = re.search(r'"coordinates":\s*\[([+-]?\d+\.?\d*),\s*([+-]?\d+\.?\d*)\]', text)
        if coord_match:
            lon, lat = float(coord_match.group(1)), float(coord_match.group(2))
            return (lat, lon)

        # Pattern like: geo:37.53,27.27
        geo_match = re.search(r'geo:([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)', text)
        if geo_match:
            lat, lon = float(geo_match.group(1)), float(geo_match.group(2))
            return (lat, lon)

        # Look in JavaScript variables
        coord_var = re.search(r'var\s+coordinates\s*=\s*\[([+-]?\d+\.?\d*),\s*([+-]?\d+\.?\d*)\]', text)
        if coord_var:
            lon, lat = float(coord_var.group(1)), float(coord_var.group(2))
            return (lat, lon)

        # Look for data attributes in HTML
        for tag in soup.find_all(attrs={'data-lat': True}):
            lat = float(tag['data-lat'])
            lon = float(tag.get('data-lon', tag.get('data-lng', 0)))
            if lat and lon:
                return (lat, lon)

        # Look for meta tags with coordinates
        for meta in soup.find_all('meta'):
            if 'geo.position' in str(meta.get('name', '')):
                content = meta.get('content', '')
                parts = content.split(';')
                if len(parts) >= 2:
                    lat, lon = float(parts[0]), float(parts[1])
                    return (lat, lon)

        return None

    except Exception as e:
        print(f"  Warning: Could not extract coordinates from {place_url}: {e}")
        return None


def extract_fragment_links(soup):
    """
    Extract fragment links from the Hekataios page.

    Args:
        soup: BeautifulSoup object of the Hekataios page

    Returns:
        list: List of fragment URLs
    """
    fragment_links = []

    # Look for links to /work/ pages (fragments/testimonia)
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/work/' in href:
            full_url = urljoin(TOPOSTEXT_BASE, href)
            if full_url not in fragment_links:
                fragment_links.append(full_url)

    return fragment_links


def extract_places_from_fragment(fragment_url):
    """
    Extract places mentioned in a specific fragment.

    Args:
        fragment_url: URL of the fragment page

    Returns:
        dict: Mapping of place_id -> {name, url, fragment_url, fragment_title}
    """
    print(f"  Fetching fragment: {fragment_url}")
    time.sleep(RATE_LIMIT_DELAY)

    try:
        response = requests.get(fragment_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to get fragment title/reference
        fragment_title = soup.find('title')
        if fragment_title:
            fragment_title = fragment_title.text.strip()
        else:
            fragment_title = fragment_url.split('/')[-1]

        places = {}

        # Extract all place links from the fragment
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/place/' in href:
                place_id = href.split('/place/')[-1].split('?')[0].split('#')[0]
                place_name = link.text.strip()

                if place_id and place_name:
                    places[place_id] = {
                        "name": place_name,
                        "id": place_id,
                        "url": urljoin(TOPOSTEXT_BASE, href),
                        "fragment_url": fragment_url,
                        "fragment_title": fragment_title
                    }

        print(f"    Found {len(places)} place(s)")
        return places

    except Exception as e:
        print(f"    Error fetching fragment: {e}")
        return {}


def get_hekataios_places():
    """
    Scrape Topostext for places mentioned in Hekataios fragments.

    Returns:
        dict: GeoJSON FeatureCollection
    """
    print(f"Fetching Hekataios data from {HEKATAIOS_URL}...")

    try:
        response = requests.get(HEKATAIOS_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching Hekataios page: {e}")
        return create_empty_geojson()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract fragment links
    fragment_links = extract_fragment_links(soup)
    print(f"Found {len(fragment_links)} fragment link(s)")

    # If no fragments found, fall back to direct place extraction
    if not fragment_links:
        print("No fragments found, extracting places directly from author page...")
        return extract_places_directly(soup)

    # Extract places from each fragment
    # Use a dict to track all fragments where each place appears
    place_fragments = defaultdict(list)
    place_data = {}

    for fragment_url in fragment_links[:20]:  # Limit to first 20 to avoid overwhelming the server
        fragment_places = extract_places_from_fragment(fragment_url)

        for place_id, data in fragment_places.items():
            if place_id not in place_data:
                place_data[place_id] = {
                    "name": data["name"],
                    "url": data["url"]
                }

            place_fragments[place_id].append({
                "url": data["fragment_url"],
                "title": data["fragment_title"]
            })

    print(f"\nFound {len(place_data)} unique place(s) across fragments")

    if not place_data:
        print("No places found in fragments. Using sample data.")
        return create_sample_geojson()

    print("Resolving coordinates (this may take a while)...")

    geo_features = []
    successful = 0

    for idx, (place_id, data) in enumerate(place_data.items(), 1):
        print(f"  [{idx}/{len(place_data)}] Processing {data['name']}...")

        coords = extract_coordinates_from_page(data['url'])

        if coords:
            lat, lon = coords
            successful += 1

            # Build fragment links for popup
            fragment_links_html = []
            for frag in place_fragments[place_id]:
                frag_title = frag["title"].replace("Topostext", "").strip()
                if len(frag_title) > 50:
                    frag_title = frag_title[:47] + "..."
                fragment_links_html.append(
                    f'<a href="{frag["url"]}" target="_blank">{frag_title}</a>'
                )

            fragments_section = "<br>".join(fragment_links_html[:3])  # Limit to first 3
            if len(fragment_links_html) > 3:
                fragments_section += f"<br><em>...and {len(fragment_links_html) - 3} more</em>"

            geo_features.append({
                "type": "Feature",
                "properties": {
                    "name": data['name'],
                    "topostext_id": place_id,
                    "place_url": data['url'],
                    "fragment_count": len(place_fragments[place_id]),
                    "fragments": [f["url"] for f in place_fragments[place_id]],
                    "popupContent": f"<b>{data['name']}</b><br><br>"
                                   f"Mentioned in {len(place_fragments[place_id])} fragment(s):<br>"
                                   f"{fragments_section}<br><br>"
                                   f"<a href='{data['url']}' target='_blank'>View place on Topostext</a>"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
            })
        else:
            print(f"    Skipping (no coordinates found)")

    print(f"\nSuccessfully geolocated {successful}/{len(place_data)} places.")

    if not geo_features:
        print("Warning: No coordinates found. Creating sample data.")
        return create_sample_geojson()

    return {
        "type": "FeatureCollection",
        "features": geo_features,
        "metadata": {
            "source": "Topostext.org",
            "author": "Hekataios of Miletus",
            "topostext_id": HEKATAIOS_ID,
            "total_places": len(geo_features),
            "total_fragments": len(fragment_links),
            "generated": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }
    }


def extract_places_directly(soup):
    """
    Fallback: Extract places directly from the author page.

    Args:
        soup: BeautifulSoup object of the author page

    Returns:
        dict: GeoJSON FeatureCollection
    """
    unique_places = {}

    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/place/' in href:
            place_id = href.split('/place/')[-1].split('?')[0].split('#')[0]
            place_name = link.text.strip()

            if place_id and place_name and place_id not in unique_places:
                unique_places[place_id] = {
                    "name": place_name,
                    "id": place_id,
                    "url": urljoin(TOPOSTEXT_BASE, href)
                }

    print(f"Found {len(unique_places)} unique place references.")

    if not unique_places:
        return create_sample_geojson()

    print("Resolving coordinates (this may take a while)...")

    geo_features = []
    successful = 0

    for idx, (place_id, data) in enumerate(unique_places.items(), 1):
        print(f"  [{idx}/{len(unique_places)}] Processing {data['name']}...")

        coords = extract_coordinates_from_page(data['url'])

        if coords:
            lat, lon = coords
            successful += 1

            geo_features.append({
                "type": "Feature",
                "properties": {
                    "name": data['name'],
                    "topostext_id": place_id,
                    "place_url": data['url'],
                    "popupContent": f"<b>{data['name']}</b><br><br>"
                                   f"Mentioned by Hekataios of Miletus<br><br>"
                                   f"<a href='{data['url']}' target='_blank'>View on Topostext</a>"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
            })
        else:
            print(f"    Skipping (no coordinates found)")

    print(f"\nSuccessfully geolocated {successful}/{len(unique_places)} places.")

    if not geo_features:
        return create_sample_geojson()

    return {
        "type": "FeatureCollection",
        "features": geo_features,
        "metadata": {
            "source": "Topostext.org",
            "author": "Hekataios of Miletus",
            "topostext_id": HEKATAIOS_ID,
            "total_places": len(geo_features),
            "generated": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }
    }


def create_empty_geojson():
    """Create an empty GeoJSON structure."""
    return {
        "type": "FeatureCollection",
        "features": [],
        "metadata": {
            "error": "Failed to fetch data from Topostext"
        }
    }


def create_sample_geojson():
    """
    Create sample GeoJSON with known Hekataios places for demonstration.
    This is used as fallback when scraping fails.
    """
    sample_places = [
        {"name": "Miletus", "lat": 37.5333, "lon": 27.2733, "desc": "Hekataios's birthplace"},
        {"name": "Ephesus", "lat": 37.9500, "lon": 27.3667, "desc": "Major Ionian city"},
        {"name": "Samos", "lat": 37.7500, "lon": 26.9833, "desc": "Island of Samos"},
        {"name": "Athens", "lat": 37.9838, "lon": 23.7275, "desc": "Athens"},
        {"name": "Sparta", "lat": 37.0817, "lon": 22.4228, "desc": "Sparta"},
        {"name": "Delphi", "lat": 38.4825, "lon": 22.5011, "desc": "Delphi"},
        {"name": "Olympia", "lat": 37.6379, "lon": 21.6300, "desc": "Olympia"},
        {"name": "Troy", "lat": 39.9575, "lon": 26.2392, "desc": "Troy/Ilion"},
        {"name": "Byzantium", "lat": 41.0082, "lon": 28.9784, "desc": "Later Constantinople"},
        {"name": "Massalia", "lat": 43.2965, "lon": 5.3698, "desc": "Modern Marseille"},
    ]

    features = []
    for place in sample_places:
        features.append({
            "type": "Feature",
            "properties": {
                "name": place["name"],
                "source": "Hekataios of Miletus (sample data)",
                "popupContent": f"<b>{place['name']}</b><br>{place['desc']}<br><em>Sample data - run scraper for complete dataset</em>"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [place["lon"], place["lat"]]
            }
        })

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "note": "Sample data for demonstration. Run the scraper to fetch real data.",
            "generated": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='Extract Hekataios places from Topostext and generate GeoJSON'
    )
    parser.add_argument(
        '--output', '-o',
        default='hekataios_places.json',
        help='Output GeoJSON file (default: hekataios_places.json)'
    )
    parser.add_argument(
        '--sample',
        action='store_true',
        help='Generate sample data without scraping'
    )

    args = parser.parse_args()

    if args.sample:
        print("Generating sample data...")
        geojson_data = create_sample_geojson()
    else:
        geojson_data = get_hekataios_places()

    # Save to file
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(geojson_data['features'])} places to {args.output}")

    if 'metadata' in geojson_data:
        print("\nMetadata:")
        for key, value in geojson_data['metadata'].items():
            print(f"  {key}: {value}")


if __name__ == '__main__':
    main()
