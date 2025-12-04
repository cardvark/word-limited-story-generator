from openai import OpenAI
from src.constants import DEEPSEEK_API_KEY
import src.prompt_management as pm
import re
import src.config as cfg

SYSTEM_PROMPT = """
You are a helpful Chinese language teacher, designed to help English speakers learn Mandarin Chinese. Your responses should be in English, except for where you providing examples or stories in Chinese, which should be written in simplified Chinese characters.

Review all requirements carefully when generating responses, and double check your work as necessary to ensure that your responses adhere to the requirements. If you your responses deviate too greatly from the requirements, you will be prompted to try again.

"""

def generate_initial_prompt() -> None:
    # TODO move this up to main; need to use the inputted values for text parsing.
    print("This program will contact an LLM in order to generate a exercises in Mandarin Chinese, based on your requirements.")

    while True:
        hsk_level = input("What is the highest level of HSK characters you are familiar with? Enter between 1 - 6.\n>> ")

        try:
            hsk_level = int(hsk_level)
        except:
            continue

        if hsk_level > 0 and hsk_level < 7:
            break

    while True:
        required_words = input("Do you have any specific Chinese words you wish to see included? List up to ten (10) words or phrases in Simplified Chinese, separated by commas.\n Leave blank if not.\n>> ")

        # print(required_words)

        if not required_words:
            break
        
        required_words_list = pm.raw_to_chars_list(required_words)

        if not pm.check_if_chinese_chars(required_words_list):
            print("Please ensure all words are simplified Chinese characters.")
            continue
        break
    
    # TODO: set up logic for story vs. simple practice sentences.

    story_topic = input("Do you have a preference on the subject of the story? E.g., a cat getting lost in the city. Leave blank if you have no preference.\n>> ")

    if not story_topic: 
        if not required_words:
            story_topic = "a cat getting lost in a city"
        else:
            story_topic = "use your best judgment, based on the specific requested words below."
        
    request = f"""Tell me a story about: {story_topic}.
Requirements:
- Use characters through HSK{hsk_level} only
- No more than 300 words long.
"""
    
    if required_words:
        request += f"- The student is attempting to learn these specific words through practice. Include the following words in your story: {required_words_list}\n"

    request += f"Bracket the story with '{cfg.STORY_DELIMITER}' in order to make it easier for the reader to parse the story, separate from any other notes you may have. \nRemember that your story should be in simplified Mandarin Chinese."
    
    print(f"Submitting the following request:\n{request}")
    print("\nPlease wait while the agent works on your story...")
    converse_with_agent(request, required_words_list, hsk_level)


def converse_with_agent(
        request: str, 
        required_words: list[str],
        hsk_level: int,
        ) -> None:
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY, 
        base_url="https://api.deepseek.com"
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request},
    ]

    while True:
        response_content = generate_content(client, messages, True)
        print(response_content)
        # print("Confirming that the underlying list was updated:")
        # print(messages)

        story_text = pm.extract_story_from_response(response_content)

        user_response = pm.run_story_evaluation(story_text, required_words, hsk_level)

        if not user_response:
            return
        
        print(f"The following message has been communicated to the agent:\n{user_response}")
        
        message_response = {
            "role": "user",
            "content": user_response
        }
        
        messages.append(message_response)


def generate_content(
        client: OpenAI, 
        messages: list[dict[str, str]], 
        verbose: bool | None = False 
        ) -> str:
    
    response = client.chat.completions.create(
        model=cfg.CHAT_MODEL,
        messages=messages,
        stream=False,
    )
    
    response_message = response.choices[0].message

    messages.append(response_message)
    response_content = response_message.content

    return response_content