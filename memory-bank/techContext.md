**Technologies Used:**  
- **Language:** Python
- **Game Library:** Pygame
- **Assets:** SVGs (pre-generated and runtime-generated, rendered with Cairo/pycairo); PNG tilesets (for roads, e.g., tileset_ROAD-1.png). City grid uses a cross-shaped road layout for easy asset mapping and accessibility.
- **Input:** Mouse and keyboard

**Development Setup:**  
- Python 3.x environment
- Pygame installed
- SVG asset handling (Cairo/pycairo for rendering; DLLs must be present and on PATH)
- PNG asset handling (Pygame image loading for tilesets)

**Technical Constraints:**  
- No save/load for MVP
- No sound/music for MVP
- Focus on simple, high-res retro visuals
- Tile type mapping (road, sidewalk, building) is critical for future asset integration; sidewalk and building asset mapping is pending.

**Dependencies:**  
- Pygame
- Cairo/pycairo (for SVG rendering; DLL troubleshooting required on Windows)
- (Potentially) svgwrite or similar for SVG generation

**Current Implementation:**
- MVP gameplay loop (city, player, fare, cheese) implemented and playtestable.
- SVG asset pipeline is now functional: Cairo DLL issues resolved, all SVG asset tests pass. Troubleshooting involved updating PATH and verifying DLL presence.
- PNG tileset integrated for road rendering (tileset_ROAD-1.png).
- City grid uses a cross-shaped road layout that now spans the full play area for easy asset mapping and accessibility.
- Cheese deduction on upgrade purchase is enforced and test-verified. Next: upgrades, subway, UI. 