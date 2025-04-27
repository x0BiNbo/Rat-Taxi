# Active Context

## Current Work Focus
- Core gameplay loop is now complete: player can move, pick up and complete fares, earn cheese, buy upgrades, use the subway, and experience a full game over and upgrade loop with persistent upgrades.
- Game over state, score tracking, and roguelike upgrade system are now implemented, tested, and working as intended.
- Game over screen displays score and cheese, allows spending cheese on upgrades, and restarts run with upgrades persisting.
- All tests pass, confirming TDD compliance.
- Implementing a prioritized, test-driven plan for gameplay and UI/UX improvements, including:
  1. Icon contrast (accessibility, now improved and tested with WCAG 4.5:1 ratio, outlines, and lighter tints)
  2. Minimap clarity (now improved: all markers have outlines and accessible colors, and pass the WCAG 4.5:1 contrast ratio test)
  3. Player feedback (visual/audio, now visually clear: player icon flashes green for pickups, red for hazards, blue for fare completion; tested and passes TDD)
  4. UI layout polish (multi-resolution)
  5. Accessibility enhancements (colorblind, font scaling)
  6. Upgrade persistence bug fixed: upgrades purchased in the upgrade menu now persist and affect gameplay after a reset. The fix sets the new Player's upgrade levels from the persistent UpgradeManager on reset. This is now tested and verified in-game.
- All improvements will follow TDD: failing tests first, then minimal code to pass, then documentation.

## Recent Changes
- Implemented game over state and UI.
- Added score tracking and display on game over.
- Added roguelike upgrade system: cheese can be spent on upgrades after game over, upgrades persist between runs.
- Updated progress.md and other memory bank files to reflect new features.
- **Standardized all core/corner road and sidewalk SVGs to 40x40 pixels, fixing grid seams and alignment issues.**
- **Tested updated SVGs in-game; grid and tile seams are resolved, and all tiles align perfectly.**
- Plan for UI/UX and gameplay improvements approved and documented.
- Memory Bank updated to reflect new improvement cycle.

## Next Steps
- Continue asset mapping for sidewalk and building tiles as new assets become available.
- Additional polish and bug fixes.
- Maintain TDD workflow and keep memory bank up to date.
- **Focus on UI/UX and gameplay improvements: icon contrast, mini-map clarity, player feedback, new mechanics.**
- Write failing tests for each improvement area.
- Implement minimal code to pass tests, one area at a time.
- Run and verify tests after each change.
- Update documentation and .cursorrules as needed.

## Rationale
- Improvements are based on best practices for retro/sim games, accessibility, and user feedback.
- TDD ensures all changes are robust and verifiable.
- Memory Bank and documentation are kept current for agentic AI handoff and future development.

## Active Decisions and Considerations
- All gameplay loops (currency, upgrades, fares, health, pickups, hazards, subway, game over, score) are test-verified and robust.
- Memory bank is current and accurately reflects project state.

**Current Focus:**  
- City grid now features multiple vertical and horizontal roads, with intersections, for a more interesting and traversable map. Sidewalks and buildings fill the rest of the grid.
- Building tiles now use a variety of retro/pixel-art SVGs for visual diversity, assigned statically per tile.
- Environmental props (trees, benches, streetlights, trashcans, mailboxes, cones, cars, fire hydrants) are now placed and rendered on sidewalk tiles for added city life.
- Player and subway stations always spawn on valid, accessible road tiles.
- Player movement is now smooth and supports map wrapping (toroidal movement).
- Subway menu logic fixed: player can select and move to any other station, menu closes after travel.
- SVG rendering is now cached for performance; lag is reduced.
- Subway and player icons are visually distinct and retro-styled.
- Fare (pickup/drop-off) generation is constrained to road tiles only.
- Cheese is now properly deducted when upgrades are purchased, fixing the progression loop.
- All TDD tests now reflect real game logic and pass.
- Ground tiles (grass, dirt) now fill non-road/building/sidewalk spaces, with contextual sidewalk placement along roads/buildings.
- Health mechanic added: player has hearts, loses half a heart on non-road collision, UI displays hearts.
- **Health pickups (cheese wedge) and hazards (pothole, puddle, rat) are now randomly placed on sidewalk/ground tiles.**
- **New grass/dirt tile variants and new prop (fire hydrant) added for visual variety.**
- **Multiple fares and special fares are now supported, with a fare selection menu and special fare bonuses.**
- **Subway system now has a cooldown and simple animation/transition when traveling.**
- **Game over state, score tracking, and roguelike upgrade system implemented. Player sees a game over screen with score and cheese, can spend cheese on upgrades, and restart with upgrades persisting between runs.**

**Recent Changes:**  
- Refactored city grid logic to generate multiple vertical and horizontal roads, with intersections, for a more interesting city layout.
- Added multiple building SVGs and updated rendering logic to use static building variety per tile.
- Added environmental prop SVGs and logic to place and render props on sidewalk tiles.
- Improved building SVGs for better retro/pixel-art style and variety.
- Player and subway station spawn logic ensures valid, accessible road tiles.
- Player movement is now smooth and supports map wrapping.
- Subway menu logic fixed: player can select and move to any other station, menu closes after travel.
- SVG rendering is now cached for performance; lag is reduced.
- Improved subway and player SVG icons for clarity and style.
- City grid rendering now selects the correct SVG for each tile type.
- Fixed upgrade purchase logic so cheese is deducted from the player when upgrades are bought.
- Updated/implemented tests for cheese currency, upgrade purchase, player movement, subway travel, prop rendering, and UI rendering. Removed placeholder tests.
- Test suite now fully passes, confirming TDD compliance.
- Added contextual ground tile system (grass, dirt) and improved sidewalk placement.
- Implemented health mechanic with heart icons and impact damage.
- **Integrated health pickups and hazards into gameplay. Added new tile/prop variants.**
- **Implemented multiple/special fares, fare selection menu, subway cooldown, and subway animation.**
- **Implemented game over state, score tracking, and roguelike upgrade system. Game over screen now displays score and cheese, allows spending cheese on upgrades, and restarts run with upgrades persisting.**
- Game over UI now has a left-aligned info panel and a right-aligned upgrade menu panel, with clear spacing and no overlap.
- Upgrade menu navigation (up/down/enter) is always active during game over, allowing cheese spending and upgrade persistence.
- Tests added for upgrade menu navigation and persistence during game over.
- The score is now always drawn below the last row of hearts, regardless of health value, preventing overlap. A test was added to verify this UI behavior.

**Next Steps:**  
- Continue polish and bug fixes.
- Maintain TDD and memory bank updates after each milestone.
- **Enhance fare and subway systems (multiple fares, special fares, subway cooldown/animation).**
- **Polish and expand visual assets (tiles, props, buildings, UI).**

**Active Decisions:**  
- Use a multi-road layout for MVP and asset mapping.
- Use SVG assets for all city grid tile types and props for flexibility and clarity.
- TDD and memory bank updates after each milestone.
- Ensure all gameplay loops (currency, upgrades, fares, health, pickups, hazards, subway, game over, score) are test-verified and robust.
- Added a new test (test_city_tile_asset_mapping) to verify that all city grid tile types (sidewalk and building variants) are mapped to the correct SVG asset and render without error. This ensures asset mapping robustness and further strengthens TDD compliance for the visual pipeline.
- Health UI now wraps hearts to new rows to prevent overlap, ensuring clarity for all health values.
- Roguelike game over is now triggered on health depletion, allowing the player to spend cheese on upgrades and restart with persistent upgrades.
- New SVGs for fare pickup and dropoff are created and integrated for better visibility and clarity.
- Tests added/updated for health UI wrapping, game over on health depletion, and SVG asset loading for new fare icons.

## Prioritized Next Steps for UI/UX and Gameplay Improvements
1. **Improve Icon Contrast**
   - Test: All icons (stars, cones, etc.) pass accessibility contrast checks and are clearly visible on all backgrounds.
2. **Refine Mini-Map Visuals**
   - Test: Mini-map is readable at all times, with clear player, fare, and station indicators.
3. **Enhance Player Feedback**
   - Test: Player receives clear visual/audio feedback for pickups, hazards, and fare completion.
4. **Add/Refine Gameplay Mechanics**
   - Test: New mechanics (e.g., special fares, hazards) are test-verified for correct integration and player experience.
5. **Polish UI Layout and Clarity**
   - Test: All UI elements (score, hearts, fare meter, upgrade menu) are non-overlapping, readable, and visually consistent at all resolutions.

- Icon contrast improvements implemented: all major icons now have outlines and lighter tints, and pass the WCAG 4.5:1 contrast ratio test for accessibility.
- Minimap clarity and accessibility improved: all markers now have outlines and accessible colors, and pass the WCAG 4.5:1 contrast ratio test.
- Player feedback is now visually clear: player icon flashes green for pickups, red for hazards, and blue for fare completion. This is tested and passes TDD.
- Upgrade persistence bug fixed: upgrades purchased in the upgrade menu now persist and affect gameplay after a reset. The fix sets the new Player's upgrade levels from the persistent UpgradeManager on reset. This is now tested and verified in-game. 