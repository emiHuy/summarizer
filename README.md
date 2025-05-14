# Summarizer

## Description
A simple summarizer tool that condenses information from bodies of text, webpages (url), and files. This tool provides a summary of the original content in various formats.

## Project Metadata
**Author:** Emily  
**Date Created:** May 12, 2025  
**Last Updated:** May 15, 2025  

## Features
- Summarize text from body of text, url, and/or file path
- Summarize text into one of the following formats: bullet points, notes, TL;DR, sentences
- Copy summarized text or save summarized text to a file

## Requirements 
- Python 3.12.5
- Install the necessary dependancies using the `requirements.txt` file

## File Information
- `.env`: contains your Cohere API Key ('API_KEY')
- `.gitignore`: specifies untracked files to ignore in Git
- `main.py`: entry point
- `README.md`: project overeview and documentation
- `requirements.txt`: necessary packages and dependencies
- `summarizer_controller.py`: event handling and user interaction
- `summarizer_tool.py`: business logic, interacts with the Cohere API
- `summarizer_view.py`: GUI (with PySide6)

## Setup
1. Create a `.env` file in the root directory
2. Add your Cohere API key to the `.env` file:
```env
API_KEY = your_cohere_api_key_here
```
3. Install dependencies using `requirements.txt`:
```bash
pip install -r requirements.txt
```