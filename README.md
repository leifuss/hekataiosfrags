# Hekataios Fragment Places - Interactive Web Map

An interactive web map displaying places mentioned in the fragments of **Hekataios of Miletus** (c. 550-476 BCE), one of the earliest Greek geographers and the author of *Periodos Ges* (Circuit of the Earth).

## Live Demo

[View the map](https://your-username.github.io/hekataiosfrags/)

## About Hekataios

Hekataios of Miletus was an early Greek historian and geographer who lived during the late 6th and early 5th centuries BCE. His *Periodos Ges* was one of the first systematic attempts to describe the known world, organized as a journey around the Mediterranean and beyond. Only fragments of his work survive, preserved in quotations by later authors.

## Features

- **Interactive Map**: Built with Leaflet.js and MapLibre GL
- **Historical Base Layer**: Uses OpenHistoricalMap vector tiles for historically-appropriate cartography
- **Place Markers**: Shows locations mentioned in Hekataios's fragments
- **Popups**: Click markers to see place names and descriptions
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
hekataiosfrags/
├── index.html                 # Main web map interface
├── hekataios_places.json      # GeoJSON data of fragment places
├── extract_places.py          # Python scraper for Topostext data
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Data Sources

- **Topostext.org**: Ancient place gazetteer with coordinates
- **OpenHistoricalMap**: Community-built historical map data

## Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/hekataiosfrags.git
   cd hekataiosfrags
   ```

2. Serve the files with a local web server:
   ```bash
   # Python 3
   python -m http.server 8000

   # Or use any other local server
   ```

3. Open `http://localhost:8000` in your browser

## Updating the Data

The repository includes sample data. To fetch complete data from Topostext:

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the scraper:
   ```bash
   python extract_places.py
   ```

   This will create/update `hekataios_places.json` with places scraped from Topostext.

   **Note**: Web scraping may take time and should respect Topostext's terms of service. Use the `--sample` flag for demonstration data:
   ```bash
   python extract_places.py --sample
   ```

## Technical Details

### Map Technology

- **Leaflet 1.9.4**: JavaScript mapping library
- **MapLibre GL 3.6.2**: Vector tile rendering engine
- **OpenHistoricalMap**: Historical base layer (vector tiles)

### Why Vector Tiles?

OpenHistoricalMap has moved from raster tiles (XYZ) to vector tiles. Vector tiles offer:
- Better performance
- Sharper rendering on high-DPI displays
- Dynamic styling capabilities
- Smaller file sizes

### Important Considerations

As noted by the Gemini guidance:

1. **Coordinate Precision**: Ancient places are mapped to modern coordinates based on archaeological sites. This implies precision that the original texts don't support.

2. **Temporal Mismatch**: OHM shows historical data from various periods. The default view may not accurately represent the world as Hekataios knew it (~500 BCE).

3. **Narrative Topology**: Hekataios's *Periodos Ges* describes places *in sequence* as a circuit. Simply plotting them as points loses the narrative order along coastlines.

## Future Enhancements

- [ ] Extract places in their original sequence from fragments
- [ ] Add route lines showing the "circuit" narrative
- [ ] Filter OHM to show only features contemporary with Hekataios (~500 BCE)
- [ ] Add fragment text excerpts to popups
- [ ] Distinguish between certain and uncertain locations
- [ ] Add timeline visualization
- [ ] Support for multiple ancient authors

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Areas for Contribution

- Improved place data extraction from Topostext
- Additional ancient geographer datasets
- Better historical context in popups
- Temporal filtering for base map features
- Mobile UI improvements

## License

This project is released under the MIT License. See LICENSE file for details.

## Acknowledgments

- **Topostext.org**: For their comprehensive ancient place gazetteer
- **OpenHistoricalMap**: For historical cartographic data
- **Gemini AI**: For the technical guidance that formed the basis of this implementation

## References

- Topostext Hekataios page: https://topostext.org/people/13921
- OpenHistoricalMap: https://www.openhistoricalmap.org/
- Leaflet documentation: https://leafletjs.com/
- MapLibre GL: https://maplibre.org/

## Contact

For questions or suggestions, please open an issue on GitHub.

---

*Built with historical curiosity and modern web technologies.*
