# Trace MVP

## Product

Trace is a mobile app where a user thinks of a famous person and the app tries to guess who it is by asking a short sequence of yes-or-no style questions. The goal of the MVP is to make the experience feel fast, playful, and surprisingly accurate with a focused set of well-known public figures.

## Core Loop

1. The user thinks of a famous person.
2. The app asks one question at a time.
3. The user answers with one of five choices: `yes`, `probably_yes`, `i_dont_know`, `probably_no`, or `no`.
4. The app updates its ranking after each answer.
5. The app makes a guess when confidence is high enough, or after a limited number of questions.
6. The user confirms whether the guess was correct.

## Monetization

The MVP should use a simple freemium model:

- Free users can play the core guessing game.
- A paid tier can remove ads and unlock extras such as deeper stats, unlimited sessions, or themed packs.
- Ads, if added, should appear between rounds rather than during active questioning.
