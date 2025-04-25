**System Architecture:**  
- **Game Loop:** Pygame main loop handles input, updates, and rendering. (Implemented)
- **City Layout:** Cross-shaped road layout (horizontal and vertical roads intersecting at the center), now spanning the full play area, surrounded by sidewalks and buildings. Pattern chosen for easy asset mapping, accessibility, and future expansion. (Implemented)
- **Player/Taxi:** Rat character, controlled via mouse/keyboard. (Implemented)
- **Fares:** Randomly generated pick-up/drop-off points. (Implemented; always constrained to road tiles for accessibility)
- **Currency:** "Cheese" earned per fare, used for upgrades. (Basic cheese loop implemented)
- **Upgrades:** Menu-based system; Engine (speed), Tires (turning), Seats (capacity), Fare (earnings). (Implemented, cheese deduction enforced and test-verified)
- **Subway:** Fast-travel mechanic between city points. (Implemented, tested; E opens menu, S moves car)
- **UI:** Mini-Map and Fare Meter implemented and tested. Upgrade menu now supports tooltips, icons, mouse navigation, and visual feedback (highlight); all related tests pass (TDD).
- **Assets:** SVGs (generate and integrate 16-bit style placeholders for player, customer, subway, props, and environment/city streets; pre-generated and runtime-generated). City grid rendering now uses SVG assets for each tile type (road, sidewalk, building), replacing the PNG tileset. Tile type mapping is critical for future asset integration.

**Design Patterns:**  
- Entity-Component for game objects (taxi, fares, upgrades).
- State machine for game states (menu, gameplay, upgrade screen).
- Modular asset loading for SVGs and PNG tilesets (Cairo/pycairo-based pipeline with fallback handling; PNG for roads).
- City layout pattern: Cross-shaped road with surrounding sidewalks/buildings for clarity and accessibility.
- Fare generation pattern: Only select pickup/drop-off from driveable road tiles to ensure accessibility and prevent unreachable fares.
- TDD-driven UI: All major UI features (upgrade menu, tooltips, icons, navigation, feedback) are test-driven and verified.

**Component Relationships:**  
- Player interacts with city, fares, upgrades, subway, and UI.
- City contains streets, subway, POIs.
- UI overlays game state and player info. 