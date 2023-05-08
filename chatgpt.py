import openai
import argparse

# Set up the OpenAI API credentials
openai.api_key = "<YOUR_API_KEY>"

# Define a function to interact with me
def chat_with_me(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

# Parse command line arguments
parser = argparse.ArgumentParser(description="Chat with ChatGPT via command line")
parser.add_argument("prompt", type=str, help="The prompt to send to ChatGPT")

# Process the command line arguments and chat with me
args = parser.parse_args()
response = chat_with_me(args.prompt)
print(response)


# you need to have an OpenAI API key to use this script. You can sign up for an API key at the OpenAI website.
