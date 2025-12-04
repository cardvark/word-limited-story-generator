import unittest
from src.story_object import Story
import src.prompt_management as pm

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

test_story_notmissing1 = """
---
小明和小红是好朋友。一天，他们在公园玩。突然，他们看到两个人很大声地吵架。一个人说：“这是我的！”另一个人说：“不，这是我的！”

小红问小明：“他们为什么吵架？”小明说：“我不知道。我们走吧，我不想看他们吵架。”

他们走开了。然后，他们遇到一只小狗。小狗很可爱，他们和小狗玩。小红很高兴，她说：“看，小狗比吵架好！”

小明说：“对！难道朋友不应该一起开心地玩吗？吵架不好。”

他们和小狗玩了一会儿。天晚了，他们回家了。今天，他们明白了朋友不要吵架。
---

**Notes for the learner:**
*   **吵架 (chǎo jià):** to quarrel / to have an argument. In the story, two people are **吵架** in the park.
*   **遇到 (yù dào):** to meet / to encounter (by chance). The friends **遇到** a cute dog.
*   **难道 (nán dào):** used to turn a statement into a rhetorical question, implying the answer is "yes" or "obviously". **难道** friends shouldn't play happily together? (The implied answer is: "Of course they should!")
"""

class TestStoryObject(unittest.TestCase):
    def test_001_create_story_object(self):
        story_text = pm.extract_story_from_response(test_story_missing1)

        story = Story(story_text, test_hsk_int, required_words1)

        with self.subTest():
            self.assertEqual(
                story.hsk_int,
                2
            )
        
        with self.subTest():
            self.assertEqual(
                story.group_counts_dict,
                {}
            )

        print(story.get_group_counts_dict())
        print(story.get_required_words_count())
        print(story.get_missing_required_words_list())
        print(story.get_HSK_violations_dict())
        print(story.get_hsk_violations_perc())
        print(story.get_required_words_count())

