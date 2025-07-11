# Research Assistant using Groq + LangChain + Streamlit + Python

This is a terminal and GUI-based Research Assistant powered by Groq's ultra-fast LLMs and LangChain. It intelligently interprets user queries, determines whether external tools are needed (like DuckDuckGo or Wikipedia), and returns a clean, structured response in JSON format — viewable in both the terminal and browser-based UI via Streamlit.

---

## Features

- Uses Groq’s `llama3-8b-8192` for fast, low-latency responses
- Intelligent tool usage detection and response formatting
- Wikipedia and DuckDuckGo integration for live research
- Pydantic for strict structured response validation
- Dual interface: terminal-based and web GUI (Streamlit)
- JSON parsing and cleanup logic to handle messy LLM output
- .env support for secure API key loading
- Modular code and tool definitions

---

## How It Works

1. Ask a question via terminal or GUI
2. Model decides if a tool is needed (`search:` or `wiki:`)
3. Python invokes the relevant tool if required
4. Tool result is fed back into the model
5. Final answer is returned in clean JSON format
6. Result is displayed in the terminal or Streamlit UI

---

## Sample Terminal Output

