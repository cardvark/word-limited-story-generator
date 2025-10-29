import jieba
import re


def add_word_to_story_groups(word, group, story_groups_dict):
    # TODO: test to ensure this updates the mutable dicts in place.
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
    
    

def evaluate_text(db_cursor, table_name, output_text):
    segmented_words = jieba.cut(output_text, cut_all=False)

    chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')
    story_groups_dict = {}
    group_counts = {}

    for word in segmented_words:
        if not re.match(chinese_char_pattern, word):
            # print(f"Non-chinese char found: '{repr(word)}'; skipping to next word.")
            continue


        word_and_group = get_word_and_group(db_cursor, table_name, word)
        if word_and_group:
            # print(word_and_group)
            submit_word(word, word_and_group, story_groups_dict)
            continue


        # triggers if no partial match found, either.
        if len(word) > 1:
            found_list = []

            for char in word:
                word_and_group = get_word_and_group(db_cursor, table_name, char)
                if not word_and_group:
                    break

                found_word, group = word_and_group
                found_list.append((char, word_and_group))

            for word_tup in found_list:
                submit_word(word_tup[0], word_tup[1], story_groups_dict)

            continue
        
        add_word_to_story_groups(word, "not_found", story_groups_dict)

    for group, word_list in story_groups_dict.items():
        group_counts[group] = len(word_list)

    return story_groups_dict, group_counts
