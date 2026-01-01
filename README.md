# Terminal DeepSearch

> *"Why pay $20/month when I have 32GB of RAM and an RTX 4070 heating up my dorm room?"*

**Terminal DeepSearch** is a free, privacy-focused research assistant that lives in your Linux terminal. It combines the reasoning power of **GPT-OSS (20B)** with real-time web search to replace tools like Perplexity or ChatGPT Plus.

It scrapes the web for the latest docs/news, feeds them into a locally running Mixture-of-Experts model, and outputs a synthesized answer without you ever leaving your command line.

---

## The "Why"
As a Computer Science student, I faced three problems:
1.  **MONEY:** Between Claude and Gemini Pro, I was looking at £50-60 per month, for something I can replicate for free (if a bit worse)
2.  **Hardware Utilization:** I have a powerful machine (i9 + RTX 4070). It seemed wasteful to rent GPUs in the cloud when I have one right here.
3.  **Context Switching:** Alt-tabbing to Chrome to read documentation breaks flow. I wanted answers *inside* my environment.
   
---

## 🛠️ The Stack
* **Engine:** [Ollama](https://ollama.com) (Local Inference)
* **Brain:** `gpt-oss:20b` (A 20B parameter Mixture-of-Experts model)
* **Eyes:** `duckduckgo-search` (Privacy-friendly web scraping)
* **Editor:** **Neovim** (I used Neovim btw)
* **OS:** Ubuntu (Linux)

---

## 🧪 Experimentation Log: Finding the Sweet Spot
This project wasn't just "install and run." I spent hours benchmarking models to find the perfect balance for an **8GB VRAM (GPU) + 32GB RAM (System)** setup.

| Model Tried | Verdict | Result |
| :--- | :--- | :--- |
| **DeepSeek-R1 (8B)** | ❌ Removed | Fast, but hallucinates Chinese language often. Unreliable for English queries. |
| **Llama 3.1 (8B)** | ❌ Removed | Too "safe" and generic. Great speed, but lacked depth for complex CS topics. |
| **Qwen 3 (8B)** | ❌ Removed | Brilliant logic, but occasionally drifted into non-English responses. |
| **GPT-OSS (20B)** | ✅ **Winner** | **The Goldilocks Choice.** It's slower (8-12 t/s) because it spills into system RAM, but the reasoning quality is massively superior. |

---

## 📦 Installation Guide

### 1. Install Ollama
The engine that runs the AI.
```bash
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
```

### 2. Download GPT-OSS:20B (around 14gb)
This is the main model we will be using
```bash
ollama pull gpt-oss:20b
```

### 3. Clone and Environment Set Up
I use a virtual env to not mess with my system python
```bash
# Clone this repo
git clone [https://github.com/SamanAshoori/deepsearch.git](https://github.com/SamanAshoori/deepsearch.git)
cd deepsearch

# Create virtual environment
python3 -m venv .venv

# Install dependencies
.venv/bin/pip install ollama duckduckgo-search colorama
```

### 4. Create ask command
```bash
# Add to your config
echo 'alias ask="~/deepsearch/.venv/bin/python3 ~/deepsearch/terminal_deepsearch.py"' >> ~/.bashrc

# Refresh shell
source ~/.bashrc
```
note you may need to adjust file path if you cloned to a different filepath

## Usage

Just type `ask` followed by your question.

```bash
ask "What are the breaking changes in the latest React 19 release?"
```

### What Happens
- Searching: The script hits DuckDuckGo for the latest articles.
- Thinking: GPT-OSS 20B loads (partially on GPU, partially on CPU) to analyze the results.
- Answer: You get a synthesized, cited summary in your terminal.

## Limitations & Realities
    Speed vs. Smarts: Because gpt-oss:20b is larger than my 8GB VRAM, it offloads layers to system RAM. This means it generates text at ~10 tokens/second. It's not instant, but it's worth the wait for the IQ boost.
    
    Stateless: The ask command is "fire and forget." It doesn't remember your previous question (yet).

    Web Reliance: If DuckDuckGo rate-limits your IP, the script might fail to fetch context.
