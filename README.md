# Research Assistant using Groq + LangChain + Python

This is a terminal-based Research Assistant powered by Groq's ultra-fast LLMs and LangChain. It intelligently interprets user queries, determines whether external tools are needed (like DuckDuckGo or Wikipedia), and returns a clean, structured response in JSON format.

---

## Features

- Uses Groq’s `llama3-8b-8192` for fast, low-latency responses
- Manual tool invocation logic (Groq does not support OpenAI-style tool calling)
- Wikipedia integration for factual queries
- DuckDuckGo Search integration for broader lookups
- Structured output via Pydantic models
- JSON parsing even with mixed or noisy output
- Environment-based API key management with `.env`
- Modular Python design — easy to extend and customize

---

## How It Works

1. You type a natural language research question
2. The model decides whether to answer directly or use a tool
3. If a tool is needed, the appropriate one is called (Wikipedia or DuckDuckGo)
4. The result is sent back to the LLM
5. The final output is formatted as valid JSON and parsed with Pydantic
6. Structured information is printed clearly

---

## Sample Usage
What can I help you research? who is Cristiano Ronaldo

Model response:
{
"topic": "Cristiano Ronaldo",
"summary": "Cristiano Ronaldo is a Portuguese professional footballer...",
"sources": ["Wikipedia", "ESPN"],
"tools_used": ["Wikipedia"]
}

---

## Project Structure

├── Main.py # Core assistant logic
├── Tools.py # DuckDuckGo and Wikipedia tool definitions
├── .env # Stores the Groq API key
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## Requirements

- Python 3.10 or newer

Install dependencies:


pip install -r requirements.txt

sql
Copy
Edit

Create a `.env` file and add your Groq API key:


You can get your API key at: https://console.groq.com/

---

## Tools Used

- **Groq LLMs** (llama3-8b-8192)
- **LangChain** for prompt and tool orchestration
- **DuckDuckGo Search API** via `ddgs`
- **Wikipedia API** for factual research
- **Pydantic v2** for strict output validation

---

## Example Use Cases

- Quick factual lookups for research or writing
- Educational assistant for students or teachers
- LLM pipeline that returns clean JSON for further automation
- Open-source foundation for more advanced AI agents

---

## License

This project is provided for educational purposes. You are free to modify and build upon it.

---

Feel free to fork, use, and contribute!

