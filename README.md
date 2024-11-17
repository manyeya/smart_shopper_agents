# Smart Shopper Agents

A multi-agent system that simulates shopping behavior using autonomous agents.

## Description

This project implements a virtual marketplace where multiple AI agents interact to simulate shopping behavior. Each agent has different roles, preferences, and decision-making capabilities.

## Features

- Multiple agent types (Shoppers, Store managers, Inventory managers)
- Price comparison and negotiation capabilities
- Dynamic inventory management
- Shopping behavior analysis

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
