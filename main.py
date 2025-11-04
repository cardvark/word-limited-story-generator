from src.import_word_lists import get_db_cursor
from src.compare_text import evaluate_text
from src.constants import OPENROUTER_API_KEY
from src.openrouter import generate_content
from openai import OpenAI


csv_file_path = "./data/character-table.csv"
table_name = 'chinese_word_groups'

test_story = """
有一只小猫。小猫很白，也很可爱。
今天，小猫不在家。它在城市里。

它走啊走，看见一个公园。公园里有树，有花，还有人。
小猫喜欢公园。它在公园里跑，也跳。

然后，小猫看见一家商店。商店不大，但是很好。
商店里有一个女孩。女孩看见小猫，很高兴。

女孩说：“你好！你饿吗？”
小猫“喵喵”叫。女孩给它一些水和一点饭。

小猫吃完了，觉得很好。它对女孩说“谢谢”（用眼睛说的！）。
天黑了，小猫回家。它今天很开心！
"""

# def main():
#     word_groups = get_word_groups_from_csv(csv_file_path)

#     # hsk_1_list = word_groups['HSK 1']
#     # hsk_2_list = word_groups['HSK 2']

#     # print(f"Extracted HSK 1 words.\nNum words: {len(hsk_1_list)}\n\nFull list:\n{hsk_1_list}")
#     # print(f"Extracted HSK 2 words.\nNum words: {len(hsk_2_list)}\n\nFull list:\n{hsk_2_list}")

#     story_groups_dict, group_counts = compare_cn_text(word_groups, test_story)

#     for group, list in story_groups_dict.items():
#         print(group)
#         print(list)

#     for group, count in group_counts.items():
#         print(f"{group}: {count}")

def main():
    db_cursor = get_db_cursor(csv_file_path, table_name)

    story_groups_dict, group_counts = evaluate_text(db_cursor, table_name, test_story)

    for group, list in sorted(story_groups_dict.items()):
        print(group)
        print(list)

    for group, count in sorted(group_counts.items()):
        print(f"{group}: {count}")


def temp_main():
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    system_prompt = """
    
    
    """

    message = "Tell me a joke."

    generate_content(client, message, verbose=True)


if __name__ == "__main__":
    temp_main()
