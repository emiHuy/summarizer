from dotenv import load_dotenv
import os
import cohere
from bs4 import BeautifulSoup
import requests

def get_client():
    load_dotenv()
    return cohere.ClientV2(os.getenv("API_KEY"))


def summarize_url(type,url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        return summarize(type,soup.get_text())
    except: 
        return "Url does not exist."


def summarize_file(type, file_path):
    try:
        with open(file_path, "r") as file:
            text = file.read()
    except: 
        return "File not found or file cannot be read."
    return summarize(type,text)
        

def summarize(type, text):
    # Choose system message based on the requested summary type
    match type:
        case "Bullet points":
            system_message = (
                "Format your response like html formatting."
                "Write the text in a shorter way and in bullet points. Avoid unnecessary details. Categories for bullet points do not have to be in bullet points." 
                "Make the language simple and easy to understand when possible."
            )
        case "Notes":
            system_message = {
                "Format your response like html formatting."
                "Your response should be like study notes, in a concise and organized manner. " 
                "Use bullet points or numbered lists when necessary. Include headings for different topics and sections." 
                "Use simple, easy-to-understand language when possible, however, do not change key terms."
            }
        case "TL;DR":
            system_message = "Write the text in a shorter way using a maximum of two sentences. Format your response like html formatting."
        case _: 
            system_message = "Format your response like html formatting. Write the text in a shorter way. Make the language simple and easy to understand when possible."

    # Construct messages for AI model
    messages = [{'role': 'system', 'content': system_message}, {'role': 'user', 'content': text}]

    # Generate responses using the AI model   
    response = generate_response(get_client(), messages)
    response = response.split("\n")[1:-1]
    return "\n".join(response)
        

def generate_response(co, messages, temperature=0.3):
    response = co.chat(model="command-a-03-2025", messages=messages, temperature = 0.3)
    return response.message.content[0].text


def write_to_file(file_path, summarized_text, mode):
    try:
        with open(file_path, mode) as file:
            if mode == "w":
                file.write(summarized_text)
            else:
                file.write("\n\n"+summarized_text)
        return "Sucess!"
    except:
        return "Unable to write to file."