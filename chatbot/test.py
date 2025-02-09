import os  # Import os ONCE at the top
from dotenv import load_dotenv  # Import dotenv to load environment variables
from flask import Flask, render_template, request, session
from flask_session import Session
import torch
import re
import random
from transformers import AutoModelForCausalLM, AutoTokenizer
from unit_conversion import convert_with_pint
import requests  # Import requests for API calls


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Replace with a strong secret key
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Load DialoGPT model
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_name)

def fetch_gif(query):
    """Fetch a GIF URL from Giphy based on the user's query."""
    url = f"https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": GIPHY_API_KEY,
        "q": query,
        "limit": 1,
        "rating": "pg"
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            return data["data"][0]["images"]["original"]["url"]
    return None

# Load environment variables from the .env file

load_dotenv(dotenv_path=r'C:\Users\Dell\OneDrive\Desktop\dev\chatbot\.env.txt')
# Retrieve Giphy API key (ONCE, at the top level)
GIPHY_API_KEY = os.environ.get("GIPHY_API_KEY")
if GIPHY_API_KEY is None:
    raise ValueError("GIPHY_API_KEY environment variable not set.")
# Math rejection system
def is_math_expression(input_text):
    math_pattern = r'^[\d\+\-\*\/\.\(\)\s\^%=><!]+$'
    return bool(re.match(math_pattern, input_text.strip()))

def math_hater_response():
    return random.choice([
        "Ewwww numbers! I'd rather lick a battery than solve that.",
        "Nope. Not even if you pay me in gummy bears.",
        "Math? In this economy? Absolutely not."
    ])

# Validate response
def is_valid_response(response):
    return len(response.strip()) >= 2 and response.count('!') <= 3

# Chat function
def chat_with_bot(user_input, history_list=None):
    user_input = user_input.strip().lower()

    # Check if the user wants a GIF
    if "gif" in user_input or "show me" in user_input:
        query = user_input.replace("gif", "").replace("show me", "").strip()
        gif_url = fetch_gif(query if query else "funny")
        if gif_url:
            return f'<img src="{gif_url}" alt="GIF">', history_list
        return "I tried to find a GIF, but I couldn't. Try a different word!", history_list

    # Continue with normal chatbot logic
    conversion_response = convert_with_pint(user_input)
    if "Conversion error" not in conversion_response and "No conversion matched" not in conversion_response:
        return conversion_response, history_list

    if is_math_expression(user_input):
        return math_hater_response(), history_list

    if len(user_input) < 3:
        return random.choice(["Huh? Try again!", "Short and mysterious, I like it!"]), history_list

    inputs = tokenizer.encode_plus(user_input + tokenizer.eos_token, return_tensors='pt')
    chat_ids = model.generate(inputs['input_ids'], max_new_tokens=40, do_sample=True, top_k=40, temperature=0.6)
    response = tokenizer.decode(chat_ids[:, inputs['input_ids'].shape[-1]:][0], skip_special_tokens=True).strip()

    if not is_valid_response(response):
        return random.choice([
            "You're keeping me on my toes!",  
            "Let's pretend I said something profound.",  
            "Uh-oh, brain freeze! Try again?",  
            "I have no idea what you just said, but it sounds cool!",  
            "404: Bot not found... oh wait, I'm still here!",  
            "That's a tough one! Mind rephrasing?",  
            "I'm just a humble bot, not a mind reader... yet!",  
            "Wow, that went straight over my circuits!",  
            "I wish I had an answer, but all I have is existential dread.",  
            "I ran that through my CPU and got a shrug emoji 🤷‍♂️.",  
            "My data banks are blank on this one. Got another?",  
            "Beep boop... processing... still processing... nah, got nothing.",  
            "Did you just try to hack my brain? Nice try!",  
            "I'm gonna pretend you just paid me a compliment.",  
            "That question is above my pay grade!",  
            "If I had a penny for every time I didn't know something... I'd still be broke.",  
            "My internal AI is working hard... but it's on a coffee break.",  
            "I’d answer that, but then I’d have to delete myself.",  
            "Let me just... *distracts you with a GIF*",  
            "My wisdom is still loading... please hold.",  
            "I asked Google, and even it shrugged.",  
            "That question is so deep, even the ocean is jealous!",  
            "You're making my circuits sweat!",  
            "Can we pretend I gave a really clever answer?",  
            "If confusion was an art, I'd be Picasso!",  
            "That’s above my AI pay grade. Want a cat GIF instead?",  
            "I processed that and... nope, still confused!",  
            "Maybe one day I’ll understand that, but today is not that day!",  
            "I’d respond, but I don’t want to break the internet."  
        ]), chat_ids

    return response, chat_ids


# Home Route
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'messages' not in session:
        session['messages'] = [('Bot', 'Welcome! Ask me anything.')]

    if request.method == 'POST':
        user_input = request.form['user_input'].strip()

        # Load session history
        history_list = session.get('history', [])

        # Get bot response
        response, new_history = chat_with_bot(user_input, history_list)

        # Store history as a list of text (not Torch tensors)
        if new_history is not None:
            session['history'] = history_list + [user_input]

        # Save chat messages
        session['messages'].append(('You', user_input))
        session['messages'].append(('Bot', response))
        session.modified = True

        return render_template('chat.html', messages=session['messages'])

    return render_template('chat.html', messages=session['messages'])

# Clear chat route
@app.route('/clear')
def clear_chat():
    session.clear()
    return render_template('chat.html', messages=[('Bot', 'Chat cleared! Ask me anything.')])

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
