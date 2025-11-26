#!/usr/bin/env python3
"""
AI-Powered Meal Planner Web Application

This application generates personalized daily meal plans with food photography
using Google's Gemini AI models.

Usage:
    python meal_planner_app.py

Then open your browser to http://127.0.0.1:7860
"""

import os
import io
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import gradio as gr


# ============================================================================
# CONFIGURATION
# ============================================================================

# Load environment variables
load_dotenv()

# Configure the API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please check your .env file."
    )

genai.configure(api_key=api_key)
print("✓ Google Gemini API configured successfully!")


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def create_meals(ingredients,
                 kcal=2000,
                 exact_ingredients=False,
                 output_format='text',
                 model='gemini-2.5-flash',
                 system_role='You are a skilled chef with expertise in cooking healthy meals.',
                 temperature=1,
                 extra=None):
    """
    Generate a daily meal plan using Google's Gemini AI.

    Parameters:
    - ingredients: List or string of available ingredients
    - kcal: Daily calorie limit (default 2000)
    - exact_ingredients: If True, use only provided ingredients
    - output_format: Format for output (text, markdown, etc.)
    - model: Gemini model to use (default: gemini-2.5-flash)
    - system_role: System instruction for the AI
    - temperature: Creativity level (0-2, default 1)
    - extra: Additional meal requirements

    Returns:
    - Text response with meal plan
    """

    # Construct the prompt
    prompt = f'''
    Create a healthy daily meal plan for breakfast lunch and dinner based on the following ingredients:
    ```{ingredients}```
    Your output should be in the {output_format} format.
    Follow the instructions below carefully.
    ### Instructions:
    1. {'Use ONLY the provided ingredients with salt, pepper and spices.' if exact_ingredients
            else 'Feel free to adjust the provided ingredients as required for the meal.'}
    2. Specify the exact amount of each ingredient.
    3. Ensure the total daily calorie intake is below {kcal}.
    4. For each meal, explain each recipe step-by-step in clear and simple sentences. Use bullet points or numbers as appropriate.
    5. For each meal, specify the total number of calories and the number of servings.
    6. For each meal, provide a concise and descriptive title that summarises the main ingredients and flavours. The title should be sufficiently detailed for image generation to create an attractive image of the meal.
    7. For each recipe, indicate the preparation cooking and total time.
    {'8. If possible, the meals should be: ' + extra if extra else ''}

    Before answering, make sure that you have followed the instructions listed above.
    The last line of your answer should be a string that contains ONLY the titles of the recipes and nothing more with a semi-colon between the main ingredients.
    '''

    # Initialize the Gemini model with system instruction
    gemini_model = genai.GenerativeModel(
        model_name=model,
        system_instruction=system_role
    )

    # Generate content with specified temperature
    response = gemini_model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=temperature,
        )
    )

    # Return the text response
    return response.text


def extract_meal_titles(meal_plan_text):
    """
    Extract individual meal titles from the meal plan response.

    The meal plan text should have the titles on the last line,
    separated by semi-colons as per the prompt instructions.

    Parameters:
    - meal_plan_text: The full text response from create_meals()

    Returns:
    - List of meal titles (typically 3: breakfast, lunch, dinner)
    """
    # Get the last line which contains only the meal titles
    lines = meal_plan_text.strip().split('\n')
    last_line = lines[-1].strip()

    # Split by semi-colon to get individual titles
    titles = [title.strip() for title in last_line.split(';')]

    return titles


def generate_meal_images(meal_titles, model='gemini-2.5-flash-image'):
    """
    Generate images for each meal using Google's image generation models.

    Parameters:
    - meal_titles: List of meal title strings
    - model: Image generation model (default: gemini-2.5-flash-image)
            Options: 'gemini-2.5-flash-image', 'nano-banana-pro-preview'

    Returns:
    - List of PIL Image objects
    """
    images = []

    print(f"Generating images using {model}...")
    print("=" * 60)

    for i, title in enumerate(meal_titles, 1):
        print(f"\nImage {i}/{len(meal_titles)}: {title[:50]}...")

        try:
            # Create a descriptive prompt
            prompt = f"Generate a professional food photography image of: {title}. Make it appetizing, well-plated, high quality, restaurant style."

            # Initialize model and generate
            image_model = genai.GenerativeModel(model_name=model)
            response = image_model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(temperature=0.4),
                request_options={"timeout": 60}
            )

            # Extract images from response parts
            if hasattr(response, 'parts') and response.parts:
                for part_idx, part in enumerate(response.parts):
                    # Check if this part contains image data
                    if hasattr(part, 'inline_data') and part.inline_data:
                        # Get the image bytes
                        image_data = part.inline_data.data
                        mime_type = part.inline_data.mime_type

                        print(f"  Found image data (type: {mime_type}, size: {len(image_data)} bytes)")

                        # Convert to PIL Image
                        pil_image = Image.open(io.BytesIO(image_data))
                        images.append(pil_image)
                        print(f"  ✓ Image {i} generated successfully! ({pil_image.size[0]}x{pil_image.size[1]})")
                        break  # Only take the first image
                    elif hasattr(part, 'text') and part.text:
                        print(f"  Part {part_idx} contains text: {part.text[:100]}...")
            else:
                print(f"  ⚠ No image data in response")

        except Exception as e:
            print(f"  ✗ Error: {type(e).__name__}: {e}")

    print("=" * 60)
    print(f"\n✓ Generated {len(images)} out of {len(meal_titles)} images")

    return images


# ============================================================================
# GRADIO INTERFACE
# ============================================================================

def generate_meal_plan_with_images(ingredients, kcal, exact_ingredients, output_format, temperature, extra_requirements):
    """
    Wrapper function for Gradio that generates meal plan and images.
    """
    try:
        # Generate the meal plan
        print("Generating meal plan...")
        meal_plan = create_meals(
            ingredients=ingredients,
            kcal=kcal,
            exact_ingredients=exact_ingredients,
            output_format=output_format,
            temperature=temperature,
            extra=extra_requirements if extra_requirements else None
        )

        # Extract meal titles
        print("Extracting meal titles...")
        titles = extract_meal_titles(meal_plan)

        # Generate images
        print("Generating images...")
        images = generate_meal_images(titles, model='gemini-2.5-flash-image')

        return images, meal_plan

    except Exception as e:
        error_msg = f"Error: {type(e).__name__}: {str(e)}"
        print(error_msg)
        return [], error_msg


def create_interface():
    """Create and configure the Gradio interface."""

    demo = gr.Blocks(title="AI Meal Planner")

    with demo:
        gr.Markdown("# 🍳 AI-Powered Meal Planner")
        gr.Markdown("Generate personalized daily meal plans with beautiful food photography using Google Gemini AI")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Inputs")

                ingredients_input = gr.Textbox(
                    label="Available Ingredients",
                    placeholder="Enter your ingredients, one per line:\n- Chicken breast\n- Broccoli\n- Rice\n- Eggs",
                    lines=8,
                    value="- Chicken breast\n- Broccoli\n- Rice\n- Eggs\n- Tomatoes\n- Onions\n- Garlic\n- Olive oil"
                )

                with gr.Row():
                    kcal_input = gr.Slider(
                        minimum=1000,
                        maximum=3500,
                        value=2000,
                        step=100,
                        label="Daily Calorie Limit"
                    )

                    temperature_input = gr.Slider(
                        minimum=0,
                        maximum=2,
                        value=0.8,
                        step=0.1,
                        label="Creativity (Temperature)"
                    )

                exact_ingredients_input = gr.Checkbox(
                    label="Use ONLY provided ingredients (no substitutions)",
                    value=False
                )

                output_format_input = gr.Dropdown(
                    choices=["text", "markdown"],
                    value="markdown",
                    label="Output Format"
                )

                extra_input = gr.Textbox(
                    label="Additional Requirements (optional)",
                    placeholder="e.g., high in protein, low carb, vegetarian",
                    lines=2
                )

                generate_btn = gr.Button("🚀 Generate Meal Plan", variant="primary")

            with gr.Column(scale=2):
                gr.Markdown("### Results")

                images_output = gr.Gallery(
                    label="Meal Images",
                    columns=3
                )

                with gr.Accordion("📄 Meal Plan Details", open=True):
                    meal_plan_output = gr.Markdown(
                        value="*Click 'Generate Meal Plan' to start...*"
                    )

        # Connect the button to the function
        generate_btn.click(
            fn=generate_meal_plan_with_images,
            inputs=[
                ingredients_input,
                kcal_input,
                exact_ingredients_input,
                output_format_input,
                temperature_input,
                extra_input
            ],
            outputs=[images_output, meal_plan_output]
        )

        gr.Markdown("""
        ---
        **Tips:**
        - Higher temperature = more creative/varied meals
        - Lower temperature = more predictable/consistent meals
        - Enable "exact ingredients" to avoid adding extras
        - The model generates breakfast, lunch, and dinner
        """)

    return demo


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("Starting AI Meal Planner...")
    print("=" * 60)

    # Create and launch the interface
    demo = create_interface()
    demo.launch(share=False)
