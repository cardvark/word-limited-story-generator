import jieba
import re
import src.db_manager as dbm


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
    conn = dbm.get_db_conn()
    cursor = conn.cursor()
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

    conn.close()
    return story_groups_dict


def get_words_by_group(
        group_name: str, 
        ) -> list[str]:
    
    conn = dbm.get_db_conn()
    cursor = conn.cursor()
    
    cursor.execute(f"""
    select Character 
    from {dbm.table_name}
    where WordGroup = '{group_name}'
    ;
    """)

    result = cursor.fetchall()

    words_list = [row[0] for row in result ]
    # print(words_list)

    conn.close()
    return words_list