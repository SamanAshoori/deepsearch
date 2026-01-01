#!/usr/bin/env python3
import sys
import warnings
import ollama
from duckduckgo_search import DDGS
from colorama import Fore, Style, init

# Silence warnings
warnings.filterwarnings("ignore")

#init colours
init(autoreset=True)

MODEL_NAME = "gpt-oss:20b"

def search_web(query):
    print(f"{Fore.GREEN}Searching the web for: '{query}'...{Style.RESET_ALL}")
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No results found."
        context = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        return context
    except Exception as e:
        return f"Search failed: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: ask 'your question here'")
        sys.exit(1)

    user_query = " ".join(sys.argv[1:])
    
    #step 1 of search - get context
    context = search_web(user_query)
    
    # step 2 - strucutre prompt
    full_prompt = f"""
    Context from web search:
    {context}

    User Question: {user_query}

    Instructions:
    - You are an intelligent research assistant.
    - Synthesize the search results to answer the user's question accurately.
    - If the search results are conflicting, explain the conflict.
    - Provide a concise, high-quality answer in English.
    """

    print(f"{Fore.RED}GPT-OSS 20B is thinking... (This may take a moment){Style.RESET_ALL}\n")

    # stream response to terminal in a try except block
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
