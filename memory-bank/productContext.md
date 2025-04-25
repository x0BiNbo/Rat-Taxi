**Why This Project Exists:**  
To provide a cozy, accessible, and slightly challenging simulation/tycoon experience in a unique, whimsical setting (a rat taxi driver in a city).

**Problems Solved:**  
- Fills a niche for light, retro-style simulation games.
- Offers a manageable, indie-friendly project scope.
- Provides a fun, replayable gameplay loop with simple upgrade mechanics.

**User Experience Goals:**  
- Cozy, inviting atmosphere with retro visuals (achieved using a functional SVG asset pipeline rendered with Cairo/pycairo, and PNG tilesets for roads).
- City grid uses a cross-shaped road layout that now spans the full play area for easy asset mapping, accessibility, and future expansion, supporting agentic AI handoff.
- Simple controls (mouse/keyboard).
- Clear progression via upgrades and currency, with cheese deduction on upgrade purchase enforced and test-verified.
- Easy to pick up, with enough challenge to stay engaging.
- MVP gameplay loop (city, player, fare, cheese) is now implemented and playtestable.

**Technical Note:**
- SVG asset pipeline is functional and uses Cairo/pycairo for rendering; DLL troubleshooting was required for Windows.
- PNG tileset (tileset_ROAD-1.png) now used for road visuals, supporting the cozy, retro aesthetic.
- City grid layout and documentation are designed for agentic AI handoff and future expansion. 