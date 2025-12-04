import src.utils as ct
import src.config as cfg
import re


def extract_story_from_response(story_text: str) -> str:
    pattern = rf"{cfg.STORY_DELIMITER}([\s\S]*?){cfg.STORY_DELIMITER}"

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

    run_evaluation_printer(group_counts_dict, required_counts_dict, hsk_level)

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
                return generate_fix_prompt(story_groups_dict, required_words, required_counts_dict, hsk_level)
            case 3:
                print("Enjoy!")
                return ""
            

# TODO Evaluate parameters to see what I should convert into a class or classes.
def generate_fix_prompt(
        story_groups_dict: dict[str, list[str]], 
        required_words: list[str],
        required_counts_dict: dict[str, int],
        hsk_level: int | None,
        ) -> str:
    # TODO: Get user input on what specific elements to address, and to what constraints.
    # Function to send agent list of words that violate HSK levels. 
        # Provide guidance on % deviation from HSK requirements?
    # Hook in the required words fix function.
    # return to agent. 
    # also print this text for the user so they know what they're prompting.

    # 1. Check if they want stricter adherence to HSK standards
    # 2. Confirm to demand required words are included.

    hsk_limit = "HSK " + str(hsk_level)

    request_prompt = "Your story deviated from the original requirements. Please make another attempt, adhering more closely to the requested requirements.\n"

    while True:
        missing_list = ct.check_required_words_missing(required_counts_dict)
        
        if not missing_list: 
            break

        prompt = f"Several required words were missing from the origiinally requested required words: {missing_list} out of {required_words}.\n\n Would you like to request that the agent try again and include all required words?\n[1] Yes\n[2] No\n>> "
        
        user_choice = input(prompt)

        try: 
            choice = int(user_choice)
            if choice < 1 or choice > 2: raise ValueError
        except ValueError:
            print("Invalid input. Please enter a digit for one of the options.")
        
        match user_choice:
            case "1":
                request_prompt += f"You failed to include the following required words in your story: {missing_list}.\nPlease be sure to include all required words in your next attempt: {required_words}.\n"
                break
            case "2":
                break

    while True:
        prompt = f"Would you like to strictly enforce the HSK level restriction ({hsk_limit}) you originally requested?\n[1] Yes\n[2] No\n>> "
        user_choice = input(prompt)

        try: 
            choice = int(user_choice)
            if choice < 1 or choice > 2: raise ValueError
        except ValueError:
            print("Invalid input. Please enter a digit for one of the options.")
        
        match user_choice:
            case "1":
                # Get list of words that exceeded HSK requirements.
                # Get % of violation compared to all words used.
                # Share list of actually allowed HSK words.
                request_prompt += f"Your story included several words that exceeded the original request of {hsk_limit}. \n"
                fix_request = generate_HSK_fix_prompt(story_groups_dict, hsk_level)
                request_prompt += fix_request
                break # temp
            case "2":
                break

    return request_prompt


def generate_HSK_fix_prompt(
        story_groups_dict: dict[str, list[str]], 
        hsk_level: int | None,
        ) -> str:
    hsk_limit = "HSK " + str(hsk_level)

    fix_request = f"Note the following words in your story exceeded the originally requested HSK limit ({hsk_limit}):\n"

    HSK_violations_dict = ct.get_HSK_violations_dict(story_groups_dict, hsk_level)

    for group, list in sorted(HSK_violations_dict.items()):
        fix_request += f"{group}: {list}\n"
    
    fix_request += f"Please ensure that all words used are only up to {hsk_limit}. As a reference, the below are comprehensive HSK word lists up to {hsk_limit}:\n"

    for i in range(1, hsk_level + 1):
        hsk_lookup = f"HSK {i}"
        hsk_list = ct.get_words_by_group(hsk_lookup)
        fix_request += f"{hsk_lookup}: {hsk_list}\n"
    
    fix_request += "Please refer back to the provided HSK word list(s) when generating your response."

    return fix_request
    

def run_evaluation_printer(
        group_counts_dict: dict[str, int],
        required_counts_dict: dict[str, int],
        hsk_level: int | None,
        ) -> None:
    print("\nUnique characters breakdown by group:")
    group_counts_printer(group_counts_dict)
    hsk_violations_percent = ct.hsk_level_violations_checker(group_counts_dict, hsk_level)
    print(f"Note: {hsk_violations_percent * 100:.1f}% characters over HSK{hsk_level}\n")

    if required_counts_dict:
        print("Required words count:")
    for word, count in required_counts_dict.items():
        print(f"{word}: {count}")

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