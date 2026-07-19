---
name: assistant-overlay-options
description: 'Use when you need to replace an open assistant overlay with a clearer assistant experience that offers three options: strategy planning, trade recording for buy/sell/hold, and a personalized chat bot.'
argument-hint: 'Describe the current overlay, target app, and the three assistant actions'
user-invocable: true
---

# Assistant Overlay Options

## When to Use
- An assistant overlay is open and should be removed or replaced.
- You want a cleaner entry point with three focused assistant actions.
- The app needs a strategy planner, trade journal helper, and personalized chat experience.

## Goal
Create an assistant experience with three main options:
1. Strategy planning
2. Trade recording (buy, sell, hold)
3. Personalized chat bot

## Procedure
1. Remove or hide the existing assistant overlay so it no longer blocks the main view.
2. Identify the main UI surface that should host the new assistant experience.
3. Add three clearly labeled options:
   - Strategy planning: collect goals, horizon, risk tolerance, and decision thresholds.
   - Trade recording: let the user log a buy, sell, or hold action with symbol, quantity, price, and notes.
   - Personalized chat bot: use saved preferences and current market context to answer questions.
4. Keep the UI consistent with the existing dashboard theme and avoid overwhelming the user with too many controls.
5. Verify that:
   - the old overlay is gone or replaced,
   - each option is visible and clickable,
   - each action routes to the correct state or backend behavior,
   - the chat experience responds with context-aware guidance.

## Implementation Notes
- Reuse existing market context, forecasts, and journal data whenever possible.
- Keep trade recording lightweight and structured so it works well for quick logging.
- For personalization, store simple preferences such as risk tolerance, preferred symbols, or communication style.
- Present the assistant as decision support rather than financial advice.

## Example Prompts
- "Remove the current assistant overlay and replace it with three options for strategy planning, trade logging, and a personalized chat bot."
- "Add a buy/sell/hold recorder to the assistant panel."
- "Make the assistant chat remember my preferences and current strategy."
