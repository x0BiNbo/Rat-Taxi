# Rat Taxi

A cozy, retro-style simulation/tycoon game where you play as a rat taxi driver navigating a city, picking up and dropping off customers, earning cheese, and upgrading your taxi. Built with Python and Pygame, with a robust SVG asset pipeline and strict test-driven development (TDD).

## Features
- Play as a rat taxi driver in a city with streets and subway lines
- Pick up and drop off fares to earn cheese (currency)
- Spend cheese on upgrades: Engine (speed), Tires (turning), Seats (capacity), Fare (earnings)
- Navigate a cross-shaped city grid with roads, sidewalks, buildings, and props
- Subway system for fast travel between city edges
- Health mechanic with hazards and pickups
- Mini-map, fare meter, and upgrade menu UI
- Retro, high-res 16-bit look using SVG assets (with PNG fallback for roads)
- Accessibility: icon contrast, minimap clarity, colorblind-friendly, font scaling
- All features are TDD-verified with comprehensive tests

## Installation & Setup
1. **Requirements:**
   - Python 3.x
   - Pygame
   - Cairo/pycairo (for SVG rendering; ensure DLLs are present and on PATH for Windows)
   - (Optional) svgwrite or similar for SVG generation
2. **Install dependencies:**
   ```sh
   pip install pygame cairosvg
   ```
3. **Run the game:**
   ```sh
   python src/main.py
   ```

## Controls
- Arrow keys / WASD: Move taxi
- E: Open subway menu at stations
- S: Move car down
- TAB: Show fare menu
- Enter: Select/confirm (upgrade, fare, subway)
- Up/Down: Navigate menus

## Development & TDD
- All features are developed using strict TDD: failing tests are written first, then minimal code to pass, then refactor and document.
- Tests cover UI, asset loading, player movement, upgrades, fares, city generation, and accessibility (contrast, minimap markers, feedback).
- See the `tests/` directory for all test cases.

## Asset Pipeline
- SVG assets are used for all city tiles, props, UI, player, subway, fares, and health.
- PNG tileset is used for roads as a fallback.
- Asset mapping is robust and TDD-verified; fallback logic for missing/corrupt SVGs is implemented and tested.

## Testing
- Run all tests with:
   ```sh
   pytest
   ```
- All tests must pass before new features are merged.

## Roadmap / Next Steps
- Continue UI/UX and accessibility improvements (icon contrast, minimap clarity, player feedback, UI layout, colorblind support, font scaling)
- Additional polish and bug fixes
- Expand asset mapping as new assets become available
- Maintain TDD and update documentation after each milestone

## Contributing
- Please follow TDD and update tests/documentation for any new features or changes.
- See the `memory-bank/` directory for project context and development history.

## License
MIT License (see LICENSE file if present)
