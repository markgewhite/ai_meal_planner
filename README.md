---
title: AI Meal Planner
emoji: 🍳
colorFrom: orange
colorTo: yellow
sdk: gradio
sdk_version: "6.0.1"
app_file: meal_planner_app.py
pinned: false
license: mit
---

# AI-Powered Meal Planner

An intelligent web application that generates personalised daily meal plans with beautiful food photography using Google's Gemini AI.

**[Live Demo on HuggingFace Spaces](https://huggingface.co/spaces/YOUR_USERNAME/ai-meal-planner)** <!-- Replace with actual URL after deployment -->

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![HuggingFace Spaces](https://img.shields.io/badge/🤗-HuggingFace%20Spaces-yellow.svg)

## 📋 Overview

This application combines **Large Language Models (LLMs)** and **AI image generation** to create complete meal plans tailored to your available ingredients and dietary preferences. It generates:

- 🥗 **Detailed recipes** for breakfast, lunch, and dinner
- 📊 **Nutritional information** including calories and serving sizes
- 🖼️ **Professional food photography** of each meal
- ⚡ **Interactive web interface** for easy customization

## 🎯 Motivation

This project was developed as part of the [Zero To Mastery AI Application Development course](https://zerotomastery.io/courses/ai-application-development), adapting the instructor's OpenAI-based approach to use Google's Gemini AI instead.

**Going Beyond the Course**: This implementation extends the course material by adding:
- A fully interactive web interface with Gradio
- Advanced image generation capabilities
- Multiple customisation options
- Professional-grade code organisation

**Built with Claude Code**: This project was developed with the assistance of [Claude Code](https://claude.ai/code), demonstrating modern AI-assisted development practices and how AI tools can accelerate learning and development. The app was built in half a day.

The goal was to gain hands-on experience with:
- Working with modern AI APIs
- Integrating text and image generation models
- Building interactive web applications
- Understanding prompt engineering techniques
- AI-assisted development workflows

## ✨ Features

- **Smart Meal Planning**: Generate meals based on available ingredients
- **Calorie Control**: Set daily calorie limits (1000-3500 kcal)
- **Dietary Preferences**: Add requirements (high protein, low carb, vegetarian, etc.)
- **Ingredient Flexibility**: Choose to use only provided ingredients or allow substitutions
- **AI-Generated Images**: High-quality food photography for each meal
- **Temperature Control**: Adjust the creativity level of meal suggestions
- **Beautiful UI**: Clean, responsive Gradio interface

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9 or higher**
2. **Google Gemini API Key** - Get one free at [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/markgewhite/ai_meal_planner.git
cd ai_meal_planner
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up your API key**

Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your-api-key-here
```

⚠️ **Important**: Never commit your `.env` file to version control!

### Running the Application

#### Web Interface
```bash
python meal_planner_app.py
```

Then open your browser to `http://127.0.0.1:7860`

#### Jupyter Notebook
```bash
jupyter notebook deal_meal_planner.ipynb
```

## 🎮 How to Use

1. **Enter Ingredients**: List the ingredients you have available
2. **Set Preferences**:
   - Adjust daily calorie limit
   - Set creativity level (temperature)
   - Add dietary requirements
3. **Generate**: Click "🚀 Generate Meal Plan"
4. **View Results**: See your meal images and detailed recipes

## 🏗️ Project Structure

```
ai-meal-planner/
├── meal_planner_app.py        # Standalone web application
├── deal_meal_planner.ipynb    # Jupyter notebook version
├── requirements.txt            # Python dependencies
├── .env                        # API key (not in git)
├── .gitignore                 # Git ignore file
├── README.md                  # This file
├── LEARNINGS.md              # Key learnings from the project
└── CLAUDE.md                 # Development notes
```

## 🔧 Technical Details

### AI Models Used

- **Text Generation**: `gemini-2.5-flash`
  - Fast, cost-effective
  - Excellent for recipe generation
  - ~$0.0013 per meal plan

- **Image Generation**: `gemini-2.5-flash-image`
  - High-quality food photography
  - Reliable and fast
  - ~$0.039 per image

### Core Technologies

- **Google Generative AI**: LLM and image generation
- **Gradio**: Interactive web interface
- **Pillow**: Image processing
- **Python-dotenv**: Environment management

## Deployment

### HuggingFace Spaces

This application is configured for easy deployment to HuggingFace Spaces.

#### Prerequisites

1. A [HuggingFace account](https://huggingface.co/join)
2. A Google Gemini API key

#### Step-by-Step Deployment

1. **Create a new Space on HuggingFace**
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space)
   - Choose a name (e.g., `ai-meal-planner`)
   - Select **Gradio** as the SDK
   - Choose visibility (public or private)
   - Click "Create Space"

2. **Clone your new Space locally**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-meal-planner
   cd ai-meal-planner
   ```

3. **Copy the required files to your Space**
   - `meal_planner_app.py` - Main application file
   - `requirements.txt` - Python dependencies
   - `README.md` - This file (includes HuggingFace Spaces configuration)

4. **Configure your API key as a Space Secret**
   - Go to your Space's Settings page
   - Navigate to "Repository secrets"
   - Add a new secret:
     - Name: `GOOGLE_API_KEY`
     - Value: Your Google Gemini API key
   - This keeps your API key secure and out of version control

5. **Push to HuggingFace**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push
   ```

6. **Wait for the build**
   - HuggingFace will automatically build and deploy your app
   - Check the "Logs" tab if there are any issues
   - Once complete, your app will be live at `https://huggingface.co/spaces/YOUR_USERNAME/ai-meal-planner`

#### Alternative: Push from existing repo

If you already have this repo cloned locally:

```bash
# Add HuggingFace as a remote
git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/ai-meal-planner

# Push to HuggingFace
git push huggingface main
```

#### Troubleshooting

- **API key not found**: Ensure `GOOGLE_API_KEY` is set in Space Secrets
- **Build fails**: Check that `requirements.txt` is present and properly formatted
- **App crashes on startup**: Check the Logs tab for error messages

## Cost

Using this application is extremely affordable:

- **Per meal plan**: ~$0.13 (text + 3 images)
- **750 meal plans**: ~$1.00
- **Free tier**: Google provides generous free quotas

## 🔒 Security

- API keys are stored in `.env` (git-ignored)
- No data is stored or transmitted to third parties
- All processing happens locally or via Google's APIs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Zero To Mastery](https://zerotomastery.io) for the excellent AI development course
- [Claude Code](https://claude.ai/code) by Anthropic for AI-assisted development support
- Google for providing the Gemini API
- The open-source community for the amazing tools and libraries

## 📧 Contact

Questions or feedback? Open an issue or reach out!

---

**Happy meal planning! 🍽️**
