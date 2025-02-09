# InsightURL Chatbot

A web-based Q&A tool that allows users to ask questions about content from specified URLs. The application uses LangChain, Together AI's Llama-3.3-70B-Instruct-Turbo model, and BGE embeddings to create an intelligent chat interface for querying webpage content.

## Features

- Load and analyze content from multiple URLs
- Interactive chat interface for asking questions
- Real-time streaming responses
- Persistent storage of processed content
- URL validation and error handling
- Support for multiple simultaneous URLs
- State-of-the-art LLM (Llama-3.3-70B-Instruct-Turbo)
- High-quality embeddings (BGE-M3)

## Prerequisites

Before running the application, make sure you have:

- Python 3.8 or higher
- Poetry (Python package manager)
- Together AI API key(for llm)
- Hugging Face API token(for embeddings)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sathvika-891/InsightURL.git
cd InsightURL
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file in the project root with your API keys:
```env
TOGETHER_API_KEY=your_together_api_key
HUGGINGFACE_ACCESS_TOKEN=your_huggingface_token
```

## Running the Application

1. Start the Streamlit application:
```bash
poetry run streamlit run streamlit.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

## Using the Application

1. Enter URLs:
   - In the sidebar, paste one or more URLs (one per line)
   - Click "Load URLs" to process the content
   - **Important**: Initial loading may take 1-2 minutes per URL as the system:
     - Downloads and processes webpage content
     - Generates embeddings using BGE-M3 model
     - Creates and stores vector representations
   - Wait for the confirmation message before proceeding

2. Ask Questions:
   - Type your question in the chat input at the bottom
   - The response will stream in real-time using Llama-3.3-70B-Instruct-Turbo
   - Previous messages are maintained in the chat history

⚠️ **Important Notes:**
- If you need to analyze new URLs, please refresh the page at http://localhost:8501 before loading them
- The application validates URLs before processing them
- Invalid URLs will be reported in the sidebar
- Responses are generated based only on the content from the provided URLs
- First-time URL loading is slower due to embedding generation
- Subsequent queries to the same URLs will be faster due to persistent storage

## Technical Stack

- **Language Model**: Llama-3.3-70B-Instruct-Turbo (via Together AI)
  - High-performance instruction-tuned model
  - Optimized for detailed, accurate responses
  - Real-time response streaming

- **Embeddings**: BGE-M3 (BAAI)
  - State-of-the-art text embeddings
  - Optimized for semantic search
  - Multilingual support

## Project Structure

```
project/
├── pyproject.toml    # Poetry dependencies and project metadata
├── README.md         # This documentation
├── chatbot.py        # Core chatbot functionality
├── streamlit.py      # Streamlit web interface
├── prompt.py         # LLM prompting configuration
└── .env              # Mandatory API keys
```

## Dependencies

Key dependencies include:
- `langchain-together`: For LLM integration with Llama-3.3
- `langchain-huggingface`: For BGE-M3 embeddings
- `streamlit`: For the web interface
- `chromadb`: For vector storage
- `python-dotenv`: For environment variable management

## Troubleshooting

1. **URL Loading Issues:**
   - Ensure URLs are complete (including http:// or https://)
   - Check if websites are accessible
   - Verify your internet connection
   - Be patient during initial loading (1-2 minutes per URL is normal)

2. **API Key Issues:**
   - Verify your API keys in the `.env` file
   - Ensure both Together AI and Hugging Face tokens are valid
   - Check API usage limits

3. **Performance Issues:**
   - Try loading fewer URLs at once (3-5 URLs recommended)
   - Ensure you have sufficient disk space for vector storage
   - Check your internet connection speed
   - Consider closing other resource-intensive applications

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
