import unittest
import src.compare_text as ct
import src.db_manager as dbm

class TestStoryExtractor(unittest.TestCase):
    def test_extract_story_from_response(self):
        test_story1 = """---
小明的家很小。爸爸和妈妈在客厅，他们在吵架。妈妈说：“你很难！”爸爸说：“你也很难！”小明在房间，他很难过。他不想听他们吵架。他想要一个大的家，爸爸不难，妈妈也不难。小明去客厅，他说：“不要吵架。我爱你们。”爸爸和妈妈不吵架了。他们爱小明。现在，他们不难了。家很小，可是爱很大。
---
"""

        test_story2 = """
---

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

---

**Story Notes for Learning:**  
- **遇到 (yù dào):** to encounter / meet  
- **吵架 (chǎo jià):** to quarrel / argue  
- **猜 (cāi):** to guess  
- **体会 (tǐ huì):** to realize / experience personally  
- **麻烦 (má fan):** trouble / inconvenient  

This short story uses only HSK2-level vocabulary and grammar, focusing on the requested words in a simple, meaningful context to aid memorization and comprehension.
"""
    

        parsed_text = ct.extract_story_from_response(test_story2)

        # print(parsed_text)
        with self.subTest():
            self.assertEqual(
                """小明的猫不见了。他出去找猫，在公园里**遇到**了他的朋友小红。  
小红说：“我听见那边有两个人**吵架**，不知道是不是因为猫？”  
小明说：“我**猜**我的猫可能在那里。”  
他们走过去，看见两个人正在大声说话。  
小明**体会**到他们很生气。  
他说：“对不起，我的猫不见了，你们看见一只白猫吗？”  
那两个人不**吵架**了。一个人说：“我看见了！它在树上。”  
小明很高兴，但是猫在很高的地方，有点儿**麻烦**。  
小红说：“我们可以帮你。”  
最后，他们一起让猫下来了。小明说：“谢谢你们！今天我真**体会**到了朋友很重要。”""",
            parsed_text
            )


class TestTextEvaluation(unittest.TestCase):
    def test_group_counts(self):
        cursor = dbm.get_db_cursor()
        required_words = ['吵架', '遇到', '难道']
        test_story = """
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
        story_text = ct.extract_story_from_response(test_story)
        
        story_groups_dict = ct.get_story_groups_dict(story_text)
        group_counts_dict = ct.get_group_counts(story_groups_dict, [])


        violations = ct.hsk_level_violations_checker(group_counts_dict, 2)
        print(violations)