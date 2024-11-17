# Smart Shopper Agents

A multi-agent system that simulates shopping behavior using autonomous agents.

## Description

This project implements a virtual marketplace where multiple AI agents interact to simulate shopping behavior. Each agent has different roles, preferences, and decision-making capabilities.

## Features

- **Price Search Agent**: Searches and compares prices across major South African retailers including:
  - Makro
  - Checkers
  - Shoprite
  - Woolworths
  - Pick n Pay

- **Price Analysis Agent**: 
  - Compares unit prices across stores
  - Identifies best deals and savings
  - Analyzes loyalty program benefits
  - Calculates potential savings

- **Shopping Recommendation Agent**:
  - Creates optimized shopping plans
  - Considers store proximity and delivery options
  - Factors in loyalty programs (Smart Shopper, Xtra Savings, WRewards)
  - Provides regional-specific recommendations

- **User Interface**:
  - Interactive shopping list management
  - Region selection for accurate pricing
  - Detailed price analysis views
  - Shopping plan recommendations
  - Loyalty program benefit summaries

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/smart-shopper-agents.git
   ```
2. Navigate to the project directory:
   ```sh
   cd smart-shopper-agents
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Pull and Run Llama 3.2 using Ollama:

```bash
# Pull the model
ollama pull llama3.2

# Verify installation
ollama list
```

5. Create a .env file with your configurations:
```bash
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=api-key 
```
6. Run the Streamlit app
```bash
streamlit run smart_shopper_agent.py
```

## smart_shopper_agent.py

The `smart_shopper_agent.py` script is the main entry point for running the Smart Shopper Agents application. It initializes the Streamlit app, sets up the agent environment, and handles user interactions. The script allows users to simulate shopping scenarios, analyze agent behavior, and visualize the results.
