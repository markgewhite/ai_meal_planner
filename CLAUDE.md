# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jupyter notebook project for a training course that creates daily meal plans using Google's Gemini API. The project generates:
1. Text-based meal plans (breakfast, lunch, dinner) using Gemini text models
2. Images of the meals using Google's Imagen (Nano Banana Pro) model

The instructor is using OpenAI, but this implementation adapts the approach to use Google's APIs instead.

## Development Setup

This project uses a Python virtual environment:
- Activate the environment: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
- Install dependencies: `pip install google-generativeai` (and other packages as needed)
- Run Jupyter: `jupyter notebook` or `jupyter lab`

## API Configuration

The project requires a Google API key to access Gemini models:
- Get an API key from Google AI Studio: https://aistudio.google.com/app/apikey
- Store the key securely (use environment variables, not hardcoded in the notebook)
- Initialize the Gemini client with: `genai.configure(api_key=YOUR_API_KEY)`

## Notebook Architecture

**Main notebook**: `deal_meal_planner.ipynb`

The core function is `create_meals()` which:
- Takes ingredients, calorie limits, and formatting preferences as parameters
- Constructs a detailed prompt for meal plan generation
- Calls the Gemini text model to generate recipes with nutritional info
- Returns meal titles for subsequent image generation
- Will be extended to call Imagen for generating meal images

Key parameters:
- `ingredients`: List or string of available ingredients
- `kcal`: Daily calorie limit (default 2000)
- `exact_ingredients`: Boolean to restrict to only provided ingredients
- `output_format`: Format for the response (text, markdown, etc.)
- `model`: The Gemini model to use (e.g., 'gemini-1.5-flash', 'gemini-1.5-pro')
- `temperature`: Controls response creativity (0-2)
- `extra`: Additional constraints or preferences

## Google Gemini API Notes

- Use `google.generativeai` library (imported as `genai`)
- Text generation: `genai.GenerativeModel(model_name).generate_content(prompt)`
- Image generation: Use Imagen API (separate from text models)
- The prompt includes specific instructions for structured output with meal titles on the last line
