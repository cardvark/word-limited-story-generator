from openai import OpenAI
from src.constants import DEEPSEEK_API_KEY
import src.compare_text as ct
import src.db_manager as dbm
import json
import re

SYSTEM_PROMPT = """
You are a helpful Chinese language teacher, designed to help English speakers learn Mandarin Chinese. Your responses should be in English, except for where you providing examples or stories in Chinese, which should be written in simplified Chinese characters.

Review all requirements carefully when generating responses, and double check your work as necessary to ensure that your responses adhere to the requirements. If you your responses deviate too greatly from the requirements, you will be prompted to try again.

"""

CHAT_MODEL = "deepseek-chat"
STORY_DELIMITER = "---"

def generate_initial_prompt() -> None:
    # TODO move this up to main; need to use the inputted values for text parsing.
    print("This program will contact an LLM in order to generate a exercises in Mandarin Chinese, based on your requirements.")

    while True:
        HSK_LEVEL = input("What is the highest level of HSK characters you are familiar with? Enter between 1 - 6.\n>> ")

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
    
    # TODO: set up logic for story vs. simple practice sentences.

    story_topic = input("Do you have a preference on the subject of the story? E.g., a cat getting lost in the city. Leave blank if you have no preference.\n>> ")

    if not story_topic: 
        if not required_words:
            story_topic = "a cat getting lost in a city"
        else:
            story_topic = "use your best judgment, based on the specific requested words below."
        
    request = f"""Tell me a story about: {story_topic}.
Requirements:
- Use characters through HSK{HSK_LEVEL} only
- No more than 300 words long.
"""
    
    if required_words:
        request += f"- The student is attempting to learn these specific words through practice. Include the following words in your story: {required_words_list}\n"

    request += f"Bracket the story with '{STORY_DELIMITER}' in order to make it easier for the reader to parse the story, separate from any other notes you may have. \nRemember that your story should be in simplified Mandarin Chinese."
    
    print(f"Submitting the following request:\n{request}")
    print("\nPlease wait while the agent works on your story...")
    converse_with_agent(request, required_words)


def converse_with_agent(
        request: str, 
        requird_words: list[str],
        ) -> None:
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY, 
        base_url="https://api.deepseek.com"
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request},
    ]

    conversing = True
    while conversing:
        response_content = generate_content(client, messages, True)
        print(response_content)
        # print("Confirming that the underlying list was updated:")
        # print(messages)

        story_text = ct.extract_story_from_response(response_content)
        
        cursor = dbm.get_db_cursor()

        story_groups_dict, group_counts = ct.evaluate_text(
        cursor, 
        dbm.table_name,
        story_text,
        )

        print("\n\nEvaluating story text to determine fit against your requirements:")

        # TODO
        # make use of "required_words" list.
        # check if words are in list. Remove them from the evaluation process?
            # 1. Need to confirm the story has the words.
            # 2. Need to "remove" these from the the HSK comparison. 
                # idea: can check words against required list; if in list, then don't add to the HSK count dict.

        #TODO Make the printing into a separate function in "compare_text.py"
        for group, list in sorted(story_groups_dict.items()):
            print(group)
            print(list)

        for group, count in sorted(group_counts.items()):
            print(f"{group}: {count}")

        # TODO: logic here to parse the story. Raise issues to user if the LLM response doesn't match requirements. (or something wonky, like all the story is in english.)
        # Provide stats on: whether all required words were included; what % of words were within the HSK levels.
        # let user decide to accept or try again with greater restriction.
        
        user_input = input("Response:\n>> ")

        if user_input == "done":
            break
        

def run_story_evaluation(
        story_text: str, 
        required_words: list[str],
        hsk_level: int | None,
        ):
    print("\n\nEvaluating story text to determine fit against your requirements:")
    story_groups_dict = ct.get_story_groups_dict(story_text)
    group_counts_dict = ct.get_group_counts(story_groups_dict, required_words)

    # ct.story_group_printer(story_groups_dict)
    print("Unique characters breakdown by group:")
    ct.group_counts_printer(group_counts_dict)
    required_counts_dict = ct.get_required_words_count(story_text, required_words)

    # print(required_counts_dict)
    hsk_violations_percent = ct.hsk_level_violations_checker(group_counts_dict, hsk_level)
    print(f"Note: {hsk_violations_percent * 100:.1f}% characters over HSK{hsk_level}\n")

    print("Required words count:")
    for word, count in required_counts_dict.items():
        print(f"{word}: {count}")
    

def request_required_words_fix(
        story_text: str,
        required_words: list[str],
        ) -> str:
    fix_request = ""

    required_words_count_dict = ct.get_required_words_count(story_text, required_words)
    missing_list = ct.check_required_words_missing(required_words_count_dict)

    if missing_list:
        fix_request = "You failed to include the following required words:\n"
        for word in missing_list:
            fix_request += f"- {word}\n"

        fix_request += f"Please ensure you include all required words when generating your next attempt: {required_words}\n"

    return fix_request


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