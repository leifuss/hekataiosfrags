# Hekataios Fragment Places - Interactive Web Map

An interactive web map displaying places mentioned in the fragments of **Hekataios of Miletus** (c. 550-476 BCE), one of the earliest Greek geographers and the author of *Periodos Ges* (Circuit of the Earth).

## Live Demo

[View the map](https://your-username.github.io/hekataiosfrags/)

## About Hekataios

Hekataios of Miletus was an early Greek historian and geographer who lived during the late 6th and early 5th centuries BCE. His *Periodos Ges* was one of the first systematic attempts to describe the known world, organized as a journey around the Mediterranean and beyond. Only fragments of his work survive, preserved in quotations by later authors.

## Features

- **Interactive Map**: Built with Leaflet.js
- **Historical Base Layer**: Uses AWMC/CAWM raster tiles optimized for ancient world mapping
- **71 Places Mapped**: Comprehensive coverage of Hekataios's geographic knowledge
- **Place Type Differentiation**:
  - Cities: Orange circular markers
  - Regions: Purple markers with permanent labels (Lydia, Scythia, etc.)
  - Islands: Blue markers (Sicily, Crete, Cyprus, etc.)
  - Rivers: Cyan markers (Nile, Istros/Danube, Phasis)
  - Seas/Straits: Dark blue markers
  - Sanctuaries: Gold markers (Olympia, Delphi)
- **Fragment Links**: Each popup links directly to the relevant Topostext fragments
- **Rich Metadata**: View which fragments mention each place
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

- **Topostext.org**: Ancient place gazetteer with coordinates and fragment texts
- **AWMC/CAWM Tiles**: Ancient World Mapping Center base map tiles hosted by the University of Iowa

## Dataset Statistics

- **71 total places** from Hekataios fragments:
  - 37 cities (Athens, Sparta, Rome, Babylon, etc.)
  - 25 regions (Scythia, Egypt, Persia, Germania, etc.)
  - 7 islands (Sicily, Crete, Cyprus, Rhodes, etc.)
  - 3 rivers (Nile, Istros/Danube, Phasis)
  - 1 sea (Pontus Euxinus/Black Sea)
  - 1 strait (Hellespont)
  - 1 sanctuary (Olympia)
- Geographic coverage from **Iberia to India**, **Scythia to Ethiopia**

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
- **AWMC/CAWM Tiles**: Raster XYZ tiles optimized for ancient geography
  - URL: `https://cawm.lib.uiowa.edu/tiles/{z}/{x}/{y}.png`
  - Hosted by University of Iowa Digital Scholarship and Publishing Studio
  - CC BY 4.0 License

### Why CAWM Tiles?

The Ancient World Mapping Center (AWMC) tiles are specifically designed for mapping ancient places:
- Cartography optimized for classical geography
- Labels and features appropriate for the ancient world
- No anachronistic modern features
- Professional scholarly resource

### Important Considerations

1. **Coordinate Precision**: Ancient places are mapped to modern coordinates based on archaeological sites. This implies precision that the original texts don't support. The AWMC tiles use fuzzy markers and uncertainty indicators where appropriate.

2. **Fragment Preservation**: Only fragments of Hekataios's work survive through later citations. The places shown represent those mentioned in surviving fragments, not the complete original text.

3. **Narrative Topology**: Hekataios's *Periodos Ges* describes places *in sequence* as a circuit around the Mediterranean. Simply plotting them as points loses the narrative order along coastlines.

4. **Scholarly Uncertainty**: Some place identifications in Topostext are more certain than others. The map shows the scholarly consensus but should not be taken as definitive.

## Future Enhancements

- [ ] Extract places in their original sequence from fragments
- [ ] Add route lines showing the "circuit" narrative structure of *Periodos Ges*
- [ ] Add fragment text excerpts to popups
- [ ] Distinguish between certain and uncertain locations (confidence levels)
- [ ] Add timeline visualization showing Hekataios in context
- [ ] Support for multiple ancient authors (Herodotus, Strabo, etc.)
- [ ] Scrape live data from Topostext (currently using curated dataset)
- [ ] Add search/filter functionality for places and fragments

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

- **Topostext.org**: For their comprehensive ancient place gazetteer and fragment database
- **Ancient World Mapping Center (AWMC)**: For the historical base map tiles
- **University of Iowa Libraries**: For hosting the CAWM tile server
- **Gemini AI**: For the technical guidance that formed the basis of this implementation

## References

- Topostext Hekataios page: https://topostext.org/people/13921
- AWMC/CAWM Tiles: https://cawm.lib.uiowa.edu/
- Ancient World Mapping Center: https://awmc.unc.edu/
- Leaflet documentation: https://leafletjs.com/
- Digital Classicist Wiki (AWMC Tiles): https://wiki.digitalclassicist.org/AWMC_Map_Tiles

## Contact

For questions or suggestions, please open an issue on GitHub.

---

*Built with historical curiosity and modern web technologies.*
