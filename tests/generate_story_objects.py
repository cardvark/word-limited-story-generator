from src.story_object import Story
import src.prompt_management as pm

def generate_missing_words_story() -> Story:
    required_words1 = ['吵架', '遇到', '难道']
    test_hsk_int = 2
    test_story_missing1 = """
---
小明和小红是好朋友。一天，他们在公园玩。突然，他们看到两个人很大声地吵架。一个人说：“这是我的！”另一个人说：“不，这是我的！”

小红问小明：“他们为什么吵架？”小明说：“我不知道。我们走吧，我不想看他们吵架。”

小明说：“对！朋友不应该一起开心地玩吗？吵架不好。”

他们和小狗玩了一会儿。天晚了，他们回家了。今天，他们明白了朋友不要吵架。
---

**Notes for the learner:**
*   **吵架 (chǎo jià):** to quarrel / to have an argument. In the story, two people are **吵架** in the park.
*   **遇到 (yù dào):** to meet / to encounter (by chance). The friends **遇到** a cute dog.
*   **难道 (nán dào):** used to turn a statement into a rhetorical question, implying the answer is "yes" or "obviously". **难道** friends shouldn't play happily together? (The implied answer is: "Of course they should!")
"""

    story_text = pm.extract_story_from_response(test_story_missing1)

    story = Story(story_text, test_hsk_int, required_words1)

    return story

def generate_no_required_words_story() -> Story:
    required_words = []
    hsk_int = 2
    response = """
---
小明和小红是好朋友。一天，他们在公园玩。突然，他们看到两个人很大声地吵架。一个人说：“这是我的！”另一个人说：“不，这是我的！”

小红问小明：“他们为什么吵架？”小明说：“我不知道。我们走吧，我不想看他们吵架。”

小明说：“对！朋友不应该一起开心地玩吗？吵架不好。”

他们和小狗玩了一会儿。天晚了，他们回家了。今天，他们明白了朋友不要吵架。
---

**Notes for the learner:**
*   **吵架 (chǎo jià):** to quarrel / to have an argument. In the story, two people are **吵架** in the park.
*   **遇到 (yù dào):** to meet / to encounter (by chance). The friends **遇到** a cute dog.
*   **难道 (nán dào):** used to turn a statement into a rhetorical question, implying the answer is "yes" or "obviously". **难道** friends shouldn't play happily together? (The implied answer is: "Of course they should!")
"""
    story_text = pm.extract_story_from_response(response)
    
    story = Story(story_text, hsk_int, required_words)

    return story
