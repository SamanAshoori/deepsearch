# Terminal DeepSearch

> "Why pay subscriptions when I have 32GB of RAM and an RTX 4070 heating up my dorm room?"

**Terminal DeepSearch** is a privacy-first research assistant that lives in your Linux terminal. It combines the reasoning power of **GPT-OSS (20B)** with the **Brave Search API** to replace tools like Perplexity or ChatGPT Plus.

It retrieves the latest documentation and news via Brave, feeds them into a locally running Mixture-of-Experts model, and outputs a synthesised answer without you ever leaving your command line.

---

## The "Why"
As a Computer Science student, I faced three problems:
1.  **Subscription Fatigue:** Between GitHub Copilot, Claude, and ChatGPT, costs were adding up.
2.  **Hardware Utilisation:** I have a powerful machine (i9 + RTX 4070). It seemed wasteful to rent GPUs in the cloud when I have one right here.
3.  **Context Switching:** Alt-tabbing to Chrome to read documentation breaks flow. I wanted answers *inside* my environment.

---

## The Stack
* **Engine:** [Ollama](https://ollama.com) (Local Inference)
* **Brain:** `gpt-oss:20b` (A 20B parameter Mixture-of-Experts model)
* **Eyes:** Brave Search API (High-quality, developer-friendly search index)
* **Glue:** Python + `requests`
* **Editor:** Neovim (I use Neovim btw)
* **OS:** Ubuntu (Linux)

---

## Experimentation Log: Finding the Sweet Spot
This project was not just "install and run." I spent hours benchmarking models to find the perfect balance for an **8GB VRAM (GPU) + 32GB RAM (System)** setup.

| Model Tried | Verdict | Result |
| :--- | :--- | :--- |
| **DeepSeek-R1 (8B)** | Removed | Fast, but often hallucinated Chinese language. Unreliable for English queries. |
| **Llama 3.1 (8B)** | Removed | Too "safe" and generic. Great speed, but lacked depth for complex CS topics. |
| **Qwen 3 (8B)** | Removed | Brilliant logic, but occasionally drifted into non-English responses. |
| **GPT-OSS (20B)** | **Winner** | **The Goldilocks Choice.** It is slower (8-12 t/s) because it spills into system RAM, but the reasoning quality is significantly superior. |

---

## Installation Guide

### 1. Install Ollama
The engine that runs the AI.
```bash
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
```

### 2. Download the Model
We use `gpt-oss:20b`. It is a large download (~14GB).
```bash
ollama pull gpt-oss:20b
```

### 3. Get a Brave Search API Key
1.  Go to [Brave Search API](https://brave.com/search/api/).
2.  Sign up for the Free Tier (allows 2,000 queries per month).
3.  Copy your API Key.
4.  Paste it into `terminal_deepsearch.py` where it says `BRAVE_API_KEY`.

### 4. Clone & Environment Setup
Use a virtual environment to manage dependencies.

```bash
# Clone this repo
git clone [https://github.com/SamanAshoori/deepsearch.git](https://github.com/SamanAshoori/deepsearch.git)
cd deepsearch

# Create virtual environment
python3 -m venv .venv

# Install dependencies (We now use 'requests' instead of 'duckduckgo-search')
.venv/bin/pip install ollama colorama requests
```

### 5. Create the "Ask" Command
Add this alias to your `.bashrc` (or `.zshrc`) to make the tool accessible from anywhere.

```bash
# Add to your config
echo 'alias ask="~/deepsearch/.venv/bin/python3 ~/deepsearch/terminal_deepsearch.py"' >> ~/.bashrc

# Refresh shell
source ~/.bashrc
```
*(Note: Adjust paths if you cloned the repo elsewhere).*

---

## Usage

Just type `ask` followed by your question.

```bash
ask "What is the difference between C++17 and C++20?"
```

**What happens:**
1.  **Searching:** The script queries the Brave API for high-relevance results.
2.  **Thinking:** GPT-OSS 20B loads (partially on GPU, partially on CPU) to analyse the results.
3.  **Answer:** You get a synthesised, cited summary in your terminal.
   
<img width="2293" height="1016" alt="image" src="https://github.com/user-attachments/assets/2ed509e4-6966-4eba-a17b-16dcbc1c516c" />


---

## Limitations & Realities

* **Speed vs. Smarts:** Because `gpt-oss:20b` is larger than my 8GB VRAM, it offloads layers to system RAM. This means it generates text at **~10 tokens/second**. It is not instant, but the quality is worth the wait.
* **Stateless:** The `ask` command is "fire and forget." It does not remember your previous question.
* **API Limits:** The free Brave API tier has a monthly limit. If you hit it, the script will error out (or you can pay for a tier).
