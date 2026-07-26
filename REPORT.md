# Course-End Project Report

Title: Building a Python Adventure Game with GitHub Copilot

Summary:
This project implements a text-based adventure game in Python where the player explores a forest and a cave to find a legendary treasure. The CLI uses ASCII art, timed text output, and optional sound effects to create a cinematic feel.

How GitHub Copilot assisted:
- Suggested function structures (start_game, forest_path, cave_path) and common patterns for CLI games.
- Helped produce small utility functions (slow_print) and ASCII art ideas.
- Recommended handling for optional dependencies (playsound, colorama) and safe fallbacks.

Key challenges faced:
- Making the CLI feel "cinematic" without heavy multimedia dependencies.
- Deciding how to include sound assets in a lightweight repo — the chosen approach keeps audio optional so the game runs with or without them.

Enhancements made:
- Inventory system (simple set) so keys and items persist between decisions.
- Randomized elements to increase replayability (chance-based outcomes).
- Clear instructions in README and placeholders for sound assets.

How to generate PDF:
- Convert this REPORT.md to PDF using your preferred tool. Example with pandoc:
  pandoc REPORT.md -o REPORT.pdf

