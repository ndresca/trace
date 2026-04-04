# Trace Architecture

## Overview

Trace should start as a simple monorepo with clear separation between the mobile client, backend API, ranking engine, and static data. The first version should favor readability and low operational complexity over heavy infrastructure.

## Monorepo Structure

- `apps/mobile`  
  Mobile application for the user experience, including the question flow, answer input, guess display, and session history UI.

- `services/api`  
  Backend service responsible for game session orchestration, exposing endpoints for starting a game, submitting answers, retrieving the next question, and making guesses.

- `packages/engine`  
  Shared ranking and question-selection logic. This package should take answers plus candidate data and return updated rankings, confidence, and the next best question.

- `data/questions`  
  Static question bank files. These define the canonical questions the engine can ask.

- `data/seeds`  
  Seed data for famous people and their attributes. This is the base dataset used by the engine.

- `data/eval`  
  Evaluation cases and benchmark scenarios used to measure guess accuracy and question efficiency.

## Responsibilities

- The mobile app handles presentation and user input.
- The API manages sessions and calls the engine.
- The engine remains stateless and reusable.
- Questions, entities, and evaluation data are stored as versioned files in `data`.

## Initial Design Principles

- Keep data formats file-based and easy to inspect.
- Keep the engine independent from UI and transport details.
- Keep the API thin so ranking behavior lives in one place.
- Avoid adding infrastructure or frameworks until the product loop is validated.
