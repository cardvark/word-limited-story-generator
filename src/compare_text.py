import jieba
import re


def compare_cn_text(word_groups, output_text):
    segmented_words = jieba.cut(output_text, cut_all=False)

    chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')
    story_groups_dict = {}
    group_counts = {}

    for word in segmented_words:
        # this step skips past non-chinese chars. (punctuation, whitespace, etc.)
        if not re.match(chinese_char_pattern, word):
            print(f"Non-chinese char found: '{repr(word)}'; skipping to next word.")
            continue

        group = find_word_group(word, word_groups)
        
        if group:
            add_word_to_story_groups(word, group, story_groups_dict)
            continue

        # TODO: Check if word is a sub-string of an HSK word.

        # only triggers if word not found in any of the provided groups.
        if len(word) > 1:
            group = False
            found_list = []

            for char in word:
                group = find_word_group(char, word_groups)
                if not group:
                    break
                found_list.append((char, group))
            
            # triggers only if *all* words were found in the provided groups.
            if group:
                add_word_to_story_groups(word, "compound_words", story_groups_dict)
                for word_tup in found_list:
                    add_word_to_story_groups(word_tup[0], word_tup[1], story_groups_dict)
                continue
        
        # triggers if:
            # word not found in group
            # and it isn't a compound word with sub-chars found in groups.
        add_word_to_story_groups(word, "not_found", story_groups_dict)

    for group, word_list in story_groups_dict.items():
        group_counts[group] = len(word_list)

    return story_groups_dict, group_counts

def add_word_to_story_groups(word, group, story_groups_dict):
    # TODO: test to ensure this updates the mutable dicts in place.
    if group in story_groups_dict:
        story_groups_dict[group].add(word)
    else:
        story_groups_dict[group] = {word}

def find_word_group(word, word_groups):
    for group, word_list in word_groups.items():
        if word in word_list:
            return group
    
    return None