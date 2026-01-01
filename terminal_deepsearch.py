#!/usr/bin/env python3
import sys
import warnings
import requests  # Changed from duckduckgo_search
import ollama
from colorama import Fore, Style, init

# Silence warnings
warnings.filterwarnings("ignore")

# Init colours
init(autoreset=True)

MODEL_NAME = "gpt-oss:20b"
# Get your free key from https://brave.com/search/api/
BRAVE_API_KEY = "YOUR_BRAVE_API_KEY_HERE" 

def search_web(query):
    print(f"{Fore.GREEN}Searching Brave for: '{query}'...{Style.RESET_ALL}")
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    params = {"q": query, "count": 5}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return f"Error: Brave API returned {response.status_code}"
        
        data = response.json()
        results = data.get('web', {}).get('results', [])
        
        if not results:
            return "No results found."
        
        # Format the results
        context = "\n".join([f"- {r['title']}: {r['description']}" for r in results])
        return context
        
    except Exception as e:
        return f"Search failed: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: ask 'your question here'")
        sys.exit(1)

    user_query = " ".join(sys.argv[1:])
    
    # Step 1: Search
    context = search_web(user_query)
    
    # Step 2 - Structure prompt
    full_prompt = f"""
    ### CONTEXT FROM SEARCH
    {context}

    ### USER QUESTION
    {user_query}

    ### SYSTEM INSTRUCTIONS
    You are a CLI-based research assistant designed for high-density information retrieval.
    
    1. **Directness:** Answer immediately. Do NOT use introductory filler (e.g., "Based on the search results...").
    2. **Formatting:** Use Markdown heavily. 
       - Use `## Headers` for sections.
       - Use `- Bullet points` for lists (easier to read in terminal).
       - Use `**Bold**` for key terms or metrics.
       - Use `Code Blocks` for technical commands or code.
    3. **Citations:** When stating a fact, briefly reference the source title in brackets, e.g., [Source Name].
    4. **Synthesis:** If sources conflict, create a specific section titled "Conflicts" and summarize the difference.
    5. **Honesty:** If the provided context does not answer the question, state: "Insufficient data in search results."
    6. **Technical Detail:** If the query is technical, prioritize syntax-correct code blocks and CLI commands over prose descriptions.
    """

    print(f"{Fore.RED}GPT-OSS 20B is thinking... (This may take a moment){Style.RESET_ALL}\n")

    # Step 3: Stream response
    try:
        stream = ollama.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': full_prompt}],
            stream=True,
        )

        for chunk in stream:
            content = chunk['message']['content']
            print(content, end='', flush=True)

        print("\n")
        
    except ollama.ResponseError as e:
        print(f"{Fore.RED}Error: Could not connect to Ollama. Did you run 'ollama pull {MODEL_NAME}'?{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
