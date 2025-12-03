import src.compare_text as ct
from src.config import *
import re


def extract_story_from_response(story_text: str) -> str:
    pattern = rf"{STORY_DELIMITER}([\s\S]*?){STORY_DELIMITER}"

    match = re.search(pattern, story_text)

    if match:
        return match.group(1).strip()


def run_story_evaluation(
        story_text: str, 
        required_words: list[str],
        hsk_level: int | None,
        ) -> str:
    print("\n\nEvaluating story text to determine fit against your requirements:")
    story_groups_dict = ct.get_story_groups_dict(story_text)
    group_counts_dict = ct.get_group_counts(story_groups_dict, required_words)
    required_counts_dict = ct.get_required_words_count(story_text, required_words)

    run_evaluation_printer(story_groups_dict, group_counts_dict, required_counts_dict, hsk_level)

    while True:
        prompt = "Select from the following options:\n[1] See detailed Character group and list breakdown.\n[2] Request the agent to fix requirements issues with the story. \n[3] Accept story as is.\n>> "
        user_choice = input(prompt)

        try: 
            choice = int(user_choice)
            if choice < 1 or choice > 3: raise ValueError
        except ValueError:
            print("Invalid input. Please enter a digit for one of the options.")

        match choice:
            case 1:
                story_group_printer(story_groups_dict)
            case 2:
                return generate_fix_prompt(story_groups_dict, group_counts_dict, required_counts_dict, hsk_level)
            case 3:
                print("Enjoy!")
                return ""
            

def generate_fix_prompt(
        story_groups_dict: dict[str, list[str]], 
        group_counts_dict: dict[str, int],
        required_counts_dict: dict[str, int],
        hsk_level: int | None,
        ) -> None:
    # TODO: Get user input on what specific elements to address, and to what constraints.
    # Function to send agent list of words that violate HSK levels. 
        # Provide guidance on % deviation from HSK requirements?
    # Hook in the required words fix function.
    # return to agent. 
    # also print this text for the user so they know what they're prompting.
    return "Your story included several words that were outside of the requested HSK limit. Please review your text and try again."


def run_evaluation_printer(
        story_groups_dict: dict[str, list[str]], 
        group_counts_dict: dict[str, int],
        required_counts_dict: dict[str, int],
        hsk_level: int | None,
        ) -> None:
    print("\nUnique characters breakdown by group:")
    group_counts_printer(group_counts_dict)
    hsk_violations_percent = ct.hsk_level_violations_checker(group_counts_dict, hsk_level)
    print(f"Note: {hsk_violations_percent * 100:.1f}% characters over HSK{hsk_level}\n")

    print("Required words count:")
    for word, count in required_counts_dict.items():
        print(f"{word}: {count}")


def generate_required_words_fix_prompt(
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


def story_group_printer(story_groups_dict):
    for group, list in sorted(story_groups_dict.items()):
        print(group)
        print(list)


def group_counts_printer(group_counts):
    total_unique_words = 0

    for group, count in group_counts.items():
        if "partial_match" in group:
            continue
        total_unique_words += count

    for group, count in sorted(group_counts.items()):
        if count == 0:
            continue
        if "partial_match" in group:
            continue

        percent = count / total_unique_words * 100
        print(f"{group}: {count} ({percent: .2f}%)")


def raw_to_chars_list(raw_input: str) -> list[str]:
    split_pattern = r"[，、,]"
    words_list = re.split(split_pattern, raw_input)
    words_list = [item.strip() for item in words_list if item.strip()]
    return words_list


def check_if_chinese_chars(words_list: list[str]) -> bool:
    all_chinese = True       
    chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')
    for word in words_list:
        for char in word:
            if not re.match(chinese_char_pattern, char):
                all_chinese = False
                break
            
    return all_chinese