# 🔍 AI Job Fit Evaluator

---

## Introduction

The AI Job Fit Evaluator is a Streamlit application that analyzes resumes against job descriptions to provide insights on job fit, key strengths, potential gaps, and hiring recommendations. This tool leverages the power of Large Language Models (LLMs) to streamline the recruitment process and offer data-driven evaluations.

## Features

- **Job Description Extraction**: Automatically extracts job details from a provided URL.
- **Resume Parsing**: Extracts text from uploaded PDF resumes using PyMuPDF.
- **AI-Powered Analysis**: Utilizes the Groq LLM to analyze the resume against the job description.
- **Comprehensive Evaluation**: Provides a job fit score, key strengths, potential gaps, and a final recommendation.


## Installation

To run this application, you need Python installed on your system. Follow these steps to set up the environment:

1. Clone the repository:

```
git clone https://github.com/yourusername/ai-job-fit-evaluator.git
cd ai-job-fit-evaluator
```

2. Install the required packages:

```
pip install streamlit requests PyMuPDF langchain-groq tiktoken
```

3. Set up your Groq API key as an environment variable:

```
export GROQ_API_KEY=your_api_key_here
```


## Usage

1. Run the Streamlit app:

```
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).
3. Enter a job listing URL and upload a resume PDF.
4. Click "Analyze Resume" to get the evaluation results.

## Dependencies

- streamlit
- requests
- PyMuPDF (fitz)
- langchain-groq
- tiktoken


## Configuration

- The LLM model used is "llama3-8b-8192" from Groq. You can modify this in the `model` initialization if needed.
- The token limit for processing is set to 6000. Adjust the `max_tokens` variable if necessary.


## Limitations

- The application relies on external APIs and services, which may have usage limits or require authentication.
- PDF parsing may not be perfect for all resume formats, especially those with complex layouts or image-based content.


## Contributing

Contributions to improve the AI Job Fit Evaluator are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
