from openai import OpenAI
from src.constants import DEEPSEEK_API_KEY
import json
import re

SYSTEM_PROMPT = """
You are a helpful Chinese language teacher, designed to help English speakers learn Mandarin Chinese. Your responses should be in English, except for where you providing examples or stories in Chinese, which should be written in simplified Chinese characters.

Review all requirements carefully when generating responses, and double check your work as necessary to ensure that your responses adhere to the requirements. If you your responses deviate too greatly from the requirements, you will be prompted to try again.

"""

CHAT_MODEL = "deepseek-chat"

def generate_initial_prompt():
    print("This program will contact an LLM in order to generate a story in Mandarin Chinese, based on your requirements.")

    while True:
        HSK_LEVEL = input("What is the highest level of HSK characters you want for your story? Enter between 1 - 6.\n>> ")

        try:
            int_check = int(HSK_LEVEL)
        except:
            continue

        if int_check > 0 and int_check < 7:
            break

    while True:
        required_words = input("Do you have any specific Chinese words you wish to see included? List up to ten (10) words or phrases in Simplified Chinese, separated by commas.\n Leave blank if not.\n>> ")

        # print(required_words)

        if not required_words:
            break
        
        split_pattern = r"[，、,]"
        required_words_list = re.split(split_pattern, required_words)
        required_words_list = [item.strip() for item in required_words_list if item.strip()]

        all_chinese = True       
        chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')
        for word in required_words_list:
            for char in word:
                if not re.match(chinese_char_pattern, char):
                    print("Please ensure all words are simplified Chinese characters.")
                    all_chinese = False
                    break

        if not all_chinese:
            continue
        break

    story_topic = input("Do you have a preference on the subject of the story? E.g., a cat getting lost in the city. Leave blank if you have no preference.\n>> ")

    if not story_topic:
        story_topic = "a cat getting lost in a city"
        
    request = f"""Tell me a story about: {story_topic}.
Requirements:
- Use characters through HSK{HSK_LEVEL} only
- No more than 300 words long.
"""
    
    if required_words:
        request += f"- The student is attempting to learn these specific words through practice. Include the following words in your story: {required_words_list}"
    
    print(f"Submitting the following request:\n{request}")
    converse_with_agent(request)


def converse_with_agent(request: str):
    conversing = True

    client = OpenAI(
        api_key=DEEPSEEK_API_KEY, 
        base_url="https://api.deepseek.com"
    )


    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request},
    ]

    while conversing:
        response_content = generate_content(client, messages, True)
        print(response_content)
        print("Confirming that the underlying list was updated:")
        print(messages)
        
        user_input = input("Response:")

        if user_input == "done":
            break


def generate_content(
        client: OpenAI, 
        messages: list[dict[str, str]], 
        verbose: bool | None = False 
        ) -> str:
    
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        stream=False,
    )
    
    response_message = response.choices[0].message

    messages.append(response_message)
    response_content = response_message.content

    return response_content