import sys
from src.import_word_lists import get_db_cursor
from src.compare_text import evaluate_text
from src.constants import OPENROUTER_API_KEY
from src.openrouter import generate_content
from openai import OpenAI
import src.agent_messaging as am

# TODO
# Allow command prompt input for: 
# - selecting HSK limits
# - requesting specific words / phrases to be used (up to 10?)
# - providing guidance for the type of story to be told
# - small / medium / large story lengts (150 / 300 / 500 words?)
# logic for:
# - taking command inputs and updating the prompt.
# - logic to check if the story included the required words.
# - providing "feedback" to the agent on adherence to guidelines.
# - running the request again, and comparing the second output.
# prompt engineering:
# - try various means of ensuring the first story is as close to the requirements as possible.


csv_file_path = "./data/character-table.csv"
db_file = "./data/characters_database.db"
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

test_story2 = """
小猫在公园玩耍。它看到很多鸟，就追过去。突然，它找不到回家的路。

小猫走啊走，来到大街道。有很多车，很多行人。它害怕，躲在树后面。

一个小孩看到小猫，叫："妈妈！有只小猫！" 妈妈说："我们帮它找家吧。"

他们带着小猫走，看到警察叔叔。警察叔叔问："你从哪里来？" 小猫不会说话。

警察叔叔把小猫带到动物中心。那里有很多动物，有狗，有兔子。

第二天，小猫的主人来找它。主人是女的，穿红色衣服。她看到小猫，大哭："我的宝宝！"

警察叔叔说："你来得正好，小猫在这里。" 主人抱起小猫，说："以后别跑远了。"

小猫回家，看到自己的小窝。它舔舔爪子，心想："以后要小心。"

城市很大，小猫学会认路。它看到红绿灯，知道什么时候走。它学会找家，不再害怕。
"""

test_story3 = """
一只小猫在街上走。它迷路了。城市很大，有很多房子和车。小猫害怕，找不到回家的路。

小猫看到很多行人，但没人注意它。它饿了，想找点食物。它走到一个公园，看到一些小朋友在玩。小猫悄悄走过去，想吃点东西。

一个女孩看到小猫，叫她的妈妈。妈妈给小猫一点食物。小猫吃了，不那么害怕了。妈妈说：“这只猫好可怜，我们帮它找家吧。”

她们带小猫回家，给它水和食物。小猫很感激。妈妈给它一个纸箱，让它睡觉。小猫在箱子里很安全。

第二天，妈妈在门口贴一张纸，上面写着猫的图片和电话号码。她说：“有人看到这只猫，请打电话。”

几天后，一个男人打电话来说：“我看到这只猫，它是我家的猫。”妈妈很高兴，带小猫回家。

小猫终于回家了。它和主人抱在一起。主人说：“你跑哪里去了？我们好担心。”

小猫喵喵叫，好像在说：“对不起，我以后不会再跑远了。”
"""

test_story4 = """
小明和小红是一对夫妻。这个星期五，他们想出去吃饭。但是，他们遇到了一个麻烦。

小红说：“我们去中国饭店吧。我喜欢吃中国菜。”
小明说：“不，我们去美国饭店。美国菜很好吃。”
小红不高兴了。她说：“你总是想去美国饭店！”
小明也不高兴了。他说：“你也总是想去中国饭店！”

他们开始吵架。小红很生气，小明也很生气。

后来，小红说：“你不要生气。我们可以猜一下去哪里。”
小明说：“好。你猜我想去哪里？”
小红说：“我猜你想去美国饭店。”
小明说：“对！你猜对了。现在，我猜你想去中国饭店。”
小红笑了：“你也猜对了！”

他们体会到，吵架很不好。他们决定去一个日本饭店。日本菜他们都很喜欢。

现在，他们不吵架了。他们很开心。
"""

test_story5 = """
小明的猫不见了。他出去找猫，在公园里**遇到**了他的朋友小红。  
小红说：“我听见那边有两个人**吵架**，不知道是不是因为猫？”  
小明说：“我**猜**我的猫可能在那里。”  
他们走过去，看见两个人正在大声说话。  
小明**体会**到他们很生气。  
他说：“对不起，我的猫不见了，你们看见一只白猫吗？”  
那两个人不**吵架**了。一个人说：“我看见了！它在树上。”  
小明很高兴，但是猫在很高的地方，有点儿**麻烦**。  
小红说：“我们可以帮你。”  
最后，他们一起让猫下来了。小明说：“谢谢你们！今天我真**体会**到了朋友很重要。”  
"""

def text_parser(text):
    # TODO:
    # Take user's inputted characters, add to the table as requested.

    db_cursor = get_db_cursor(csv_file_path, table_name)

    story_groups_dict, group_counts = evaluate_text(
        db_cursor, 
        table_name,
        text,
    )

    for group, list in sorted(story_groups_dict.items()):
        print(group)
        print(list)

    for group, count in sorted(group_counts.items()):
        print(f"{group}: {count}")


def agent_messenger():
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    message = "Tell me a story about a cat who gets lost in a city, using only words in HSK1 and HSK2. Simplified Chinese. No more than 300 words long. Before responding, double check to ensure all words fall within the previous restrictions. /no_think"

    messages = [
                {
                    "role": "user",
                    "content": message,
                }
    ]

    first_draft = generate_content(client, messages, verbose=True)

    print(messages)

    text_parser(first_draft)


def main():
    mode = "parser"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    
    if mode == "parser":
        text_parser(test_story5)

    elif mode == "agent":
        # agent_messenger()
        am.generate_initial_prompt()



if __name__ == "__main__":
    main()
