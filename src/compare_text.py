import jieba
import re
import src.agent_messaging as am
import src.import_word_lists as iwl
import src.db_manager as dbm


def extract_story_from_response(story_text: str) -> str:
    pattern = rf"{am.STORY_DELIMITER}([\s\S]*?){am.STORY_DELIMITER}"

    match = re.search(pattern, story_text)

    if match:
        return match.group(1).strip()


def add_word_to_story_groups(word, group, story_groups_dict):
    # TODO: Test to switch to list; calculate unique sets later. Enables total count of words in each 
    if group in story_groups_dict:
        story_groups_dict[group].add(word)
    else:
        story_groups_dict[group] = {word}


def find_group_from_exact_word(db_cursor, table_name, word):
    db_cursor.execute(f"""
    select Character, WordGroup
    from {table_name}
    where Character = '{word}'
    limit 1
    ;
    """)

    result = db_cursor.fetchall()
    word_and_group = result[0] if result else None
    # print(word_and_group)

    return word_and_group

    
def find_group_from_partial_match(db_cursor, table_name, word):
    # print(f"Executing partial match for: {word}")
    db_cursor.execute(f"""
    select Character, WordGroup
    from {table_name}
    where Character like '%{word}%'
    limit 1
    ;
    """)

    result = db_cursor.fetchall()
    word_and_group = result[0] if result else None
    # print(word_and_group)

    return word_and_group


def get_word_and_group(db_cursor, table_name, word):
    word_and_group = find_group_from_exact_word(db_cursor, table_name, word)

    if not word_and_group:
        word_and_group = find_group_from_partial_match(db_cursor, table_name, word)
    
    return word_and_group


def submit_word(word, word_and_group, story_groups_dict):
    add_word_to_story_groups(word, word_and_group[1], story_groups_dict)
    
    if word != word_and_group[0]:
        partial_string = f"{word} matched {word_and_group[0]} of {word_and_group[1]}"
        add_word_to_story_groups(partial_string,'partial_match',story_groups_dict)
    

def get_segmented_chinese_words_only(story_text: str) -> list[str]:
    raw_segmented_words = jieba.cut(story_text, cut_all=False)
    segmented_clean = []
    chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')

    for word in raw_segmented_words:
        if re.match(chinese_char_pattern, word):
            segmented_clean.append(word)

    return segmented_clean


# TODO rework this to return also a count of each word used.
# The data structure is getting a little unwieldy, though. Would be a list of lists? or a list of dicts?
def get_story_groups_dict(story_text: str) -> dict[str, list[str]]:
    cursor = dbm.get_db_cursor()
    table_name = dbm.table_name
    segmented_words = get_segmented_chinese_words_only(story_text)
    story_groups_dict = {}

    for word in segmented_words:
        word_and_group = find_group_from_exact_word(cursor, table_name, word)
        if word_and_group:
            submit_word(word, word_and_group, story_groups_dict)
            continue
        
        # searching for matches by char
        if len(word) > 1:
            found_list = []

            for char in word:
                word_and_group = get_word_and_group(cursor, table_name, char)
                if not word_and_group:
                    break

                found_word, group = word_and_group
                found_list.append((char, word_and_group))

            for word_tup in found_list:
                submit_word(word_tup[0], word_tup[1], story_groups_dict)
            continue
        
        # trying partial match.
        word_and_group = find_group_from_partial_match(cursor, table_name, word)
        if word_and_group:
            submit_word(word, word_and_group, story_groups_dict)
            continue

        # no matches found.        
        add_word_to_story_groups(word, "not_found", story_groups_dict)

    return story_groups_dict


def get_required_words_count(
        story_text: str, 
        required_words: list[str],
        ) -> dict[str, int]:
    
    count_dict = {}
    for word in required_words:
        word_count = story_text.count(word)
        count_dict[word] = word_count

    return count_dict


def check_required_words_missing(
        required_words_count_dict: dict[str, int],
        ) -> list[str]:
    missing_words = []
    
    for word, count in required_words_count_dict.items():
        if count == 0:
            missing_words.append(word)

    return missing_words


def get_group_counts(
        story_groups_dict: dict[str, str],
        required_words: list[str],
        ) -> dict[str, int]:
    
    group_counts = {}
    
    for group, word_list in story_groups_dict.items():
        word_count = 0
        for word in word_list:
            if word in required_words:
                continue
            word_count += 1
        group_counts[group] = word_count
    
    return group_counts


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


def hsk_level_violations_checker(
        group_counts_dict: dict[str, int], 
        hsk_level: int) -> float:
    # returns value 0-1 that exceed the allowed HSK level, or are not found.
    # hsk_string = str(hsk_level)

    total_unique_words = 0
    total_violations = 0

    for group_name, count in sorted(group_counts_dict.items()):
        if "partial_match" in group_name:
            continue
        
        total_unique_words += count
        if "HSK" in group_name:
            if int(group_name[-1]) <= hsk_level:
                continue
        total_violations += count

    return total_violations / total_unique_words
