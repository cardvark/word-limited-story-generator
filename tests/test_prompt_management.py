import unittest
import src.utils as ct
import src.db_manager as dbm
import src.prompt_management as pm
import tests.generate_story_objects as gen

class TestStoryExtractor(unittest.TestCase):
    def test_extract_story_from_response(self):
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
    

        parsed_text = pm.extract_story_from_response(test_story2)

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


# class TestStoryFixes(unittest.TestCase):
#     def test_001_generate_fix_prompt(self):
#         story = gen.generate_missing_words_story()
#         story_groups_dict = story.get_story_groups_dict()
#         hsk_int = story.hsk_int
#         required_words1 = story.required_words_list
#         required_counts_dict = story.get_required_words_counts_dict()

#         prompt = pm.generate_fix_prompt(story_groups_dict, required_words1, required_counts_dict, hsk_int)
#         print(prompt)
#         pass


class TestStoryEvaluation(unittest.TestCase):
    def test_001_story_evaluation(self):
        story = gen.generate_missing_words_story()
        response = pm.run_story_evaluation(story)
        print(response)
    
    def test_002_no_required(self):
        story = gen.generate_no_required_words_story()
        response = pm.run_story_evaluation(story)
        print(response)
        