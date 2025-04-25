Rat Taxi (MVP) — Project Brief

**Core Problem/Concept:**  
Create a simple, retro-style game where the player acts as a rat taxi driver navigating a city to pick up and drop off customers.

**Goals:**  
- Develop a functional game using Python and Pygame.
- Deliver a cozy, slightly challenging player experience.
- Implement core mechanics: earning currency, upgrading the taxi.
- Scope for indie/casual players who enjoy light simulation/tycoon elements.

**Audience:**  
- Indie gamers.
- Fans of casual simulation/tycoon games.
- Broad age range, not just children.

**Core Features:**  
- Player controls a rat driving a taxi.
- Navigate a city (streets and subway lines).
- Gameplay loop: accept fares, drive, drop off, earn "cheese" currency.
- Use cheese to buy upgrades (Engine, Tires, Seats, Fare).
- Retro, high-res 16-bit look using SVG placeholders (SVG asset pipeline now robust, rendered with Cairo/pycairo, with fallback for missing/corrupt SVGs; all related tests pass, TDD).
- Upgrade menu UI supports tooltips, icons, mouse navigation, and visual feedback (highlight); all related tests pass (TDD).
- City grid cross-shaped road layout now spans the full play area, ensuring all fares are reachable and gameplay is accessible.
- City grid rendering now uses SVG assets for each tile type (road, sidewalk, building), replacing the PNG tileset and enabling flexible asset mapping.
- Cheese is properly deducted when upgrades are purchased, and this is verified by tests.

**MVP Scope (IN):**  
- Two gameplay areas: street and subway line.
- Core pick-up, navigation, and drop-off system.
- Cheese currency tied to fare completion.
- Four upgrade types: Engine (max speed), Tires (turning speed), Seats (passenger capacity), Fare (earnings).
- UI: Fare Meter, Mini-Map (shows player, direction, city layout, POIs).
- Artwork: SVG placeholders (some pre-generated, some runtime-generated).

**MVP Scope (OUT):**  
- More than two city sections.
- Complex NPCs, more upgrades, narrative, side quests, advanced physics, final artwork, sound/music.

**Technical Leanings:**  
- Python, Pygame.
- SVG assets (mix of pre-generated and runtime-generated, rendered with Cairo/pycairo; DLL troubleshooting required for Windows; robust fallback for missing/corrupt SVGs).
- Mouse and keyboard controls.
- TDD-driven UI: All major UI features (upgrade menu, tooltips, icons, navigation, feedback) are test-driven and verified.
- No save/load for MVP. 