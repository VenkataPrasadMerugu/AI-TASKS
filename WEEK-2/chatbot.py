import os
import openai
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

LOG_FILE = "log.txt"

def log_message(role: str, content: str):
    """Append messages to log file with timestamps."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {role.upper()}: {content}\n")

# Initial system prompt
system_prompt = input("Enter a system prompt (): ").strip()
if not system_prompt:
    system_prompt = "You are a helpful assistant."
messages = [{"role": "system", "content": system_prompt}]
log_message("system", system_prompt)

print("\nChatbot is ready! (type 'exit' to quit)")
print("Tip: Type /prompt <new prompt> anytime to change assistant behavior.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Ending chat. Goodbye!")
        break

    # Check for new prompt command
    if user_input.lower().startswith("/prompt"):
        new_prompt = user_input[len("/prompt"):].strip()
        if new_prompt:
            system_prompt = new_prompt
            messages = [{"role": "system", "content": system_prompt}]
            log_message("system", system_prompt)
            print(f"System prompt changed to: {system_prompt}\n")
        else:
            print("Please provide a new system prompt after /prompt")
        continue

    # Normal conversation
    messages.append({"role": "user", "content": user_input})
    log_message("user", user_input)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        print(f"Assistant: {reply}\n")
        messages.append({"role": "assistant", "content": reply})
        log_message("assistant", reply)
    except Exception as e:
        error_msg = f"Error: {e}"
        print(error_msg)
        log_message("error", str(e))
