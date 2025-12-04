import unittest
import src.utils as ct
import src.db_manager as dbm
import src.prompt_management as pm


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
        story_text = pm.extract_story_from_response(test_story)
        
        story_groups_dict = ct.get_story_groups_dict(story_text)
        group_counts_dict = ct.get_group_counts(story_groups_dict, [])


        violations = ct.hsk_level_violations_checker(group_counts_dict, 2)
        print(violations)


class TestHSKFix(unittest.TestCase):
    def test_001_get_words_by_group(self):
        
        words_list = ct.get_words_by_group("HSK 1")
        expected = ['大', '多', '高兴', '好', '冷', '天', '女孩儿', '漂亮', '热', '跑', '少', '小', '不', '没有', '很', '太', '都', '会', '能', '想', '和', '这', '那', '喂', '多少', '几', '哪', '哪儿', '什么', '谁', '怎么', '怎么样', '本', '个', '块', '岁', '些', '一点儿', '爸爸', '北京', '杯子', '菜', '茶', '出租车', '点', '电脑', '电视', '电影', '东西', '儿子', '饭店', '飞机', '分钟', '狗', '汉语', '后面', '家', '今天', '老师', '里', '里面', '妈妈', '猫', '米饭', '明天', '名字', '年', '女儿', '朋友', '苹果', '钱', '前面', '人', '上', '商店', '上午', '时候', '书', '水', '水果', '天气', '同学', '下', '先生', '现在', '小姐', '下午', '星期', '学生', '学校', '衣服', '医生', '医院', '椅子', '月', '中国', '中午', '桌子', '字', '昨天', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '号', '的', '了', '吗', '呢', '你', '他', '她', '我', '我们', '不客气', '打电话', '没关系', '在', '爱', '吃', '读', '对不起', '工作', '喝', '回', '叫', '开', '看', '看见', '来', '没有', '买', '请', '去', '认识', '是', '睡觉', '说', '听', '下雨', '写', '谢谢', '喜欢', '学习', '有', '再见', '住', '做', '坐']

        self.assertEqual(
            words_list,
            expected
        )

    def test_002_get_HSK_violations_dict(self):
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
        story_text = pm.extract_story_from_response(test_story)
        
        story_groups_dict = ct.get_story_groups_dict(story_text)
        group_counts_dict = ct.get_group_counts(story_groups_dict, [])


        violations_perc = ct.hsk_level_violations_checker(group_counts_dict, 2)
        print(violations_perc)

        violations_dict = ct.get_HSK_violations_dict(story_groups_dict, 2)
        print(violations_dict)

    def test_003_(self):
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
        story_text = pm.extract_story_from_response(test_story)
        
        story_groups_dict = ct.get_story_groups_dict(story_text)
        hsk_level = 2

        request = pm.generate_HSK_fix_prompt(story_groups_dict, hsk_level)
        print(request)


class TestStoryFixes(unittest.TestCase):
    def test_001_generate_fix_prompt(self):
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

        story_groups_dict = ct.get_story_groups_dict(story_text)
        hsk_level = 2
        required_words1 = ['吵架', '遇到', '难道']
        required_counts_dict = ct.get_required_words_counts_dict(story_text, required_words1)

        prompt = pm.generate_fix_prompt(story_groups_dict, required_words1, required_counts_dict, hsk_level)
        print(prompt)
        pass

    def test_002_generate_fix_prompt_not_missing_words(self):
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
        story_text = pm.extract_story_from_response(test_story_notmissing1)

        story_groups_dict = ct.get_story_groups_dict(story_text)
        hsk_level = 2
        required_words1 = ['吵架', '遇到', '难道']
        required_counts_dict = ct.get_required_words_counts_dict(story_text, required_words1)

        prompt = pm.generate_fix_prompt(story_groups_dict, required_words1, required_counts_dict, hsk_level)
        print(prompt)
        pass
    
class TestRequiredList(unittest.TestCase):
    def test_001_raw_to_chars_list(self):
        # required_chars = input("List chinese words, separated by a comma.")
        test_string = "吵架, 遇到, 难道"

        required_list = pm.raw_to_chars_list(test_string)

        self.assertEqual(
            required_list,
            ['吵架', '遇到', '难道']
        )
    

    def test_002_required_words_count(self):
        test_story = """
        ---
小美和小明是男朋友和女朋友。他们常常一起吃饭、看电影。今天，他们吵架了。

小美说：“你昨天不给我打电话。我不高兴。”
小明说：“我昨天很忙。难道我不能忙吗？”
小美说：“你说‘晚上打电话’。你没有打。”
小明说：“对不起。我忘了。”

小美说：“你不好。你不爱我。”
小明说：“我爱你。但是，我们常常吵架。这不好。”
小美说：“是的，不好。我们不做男朋友和女朋友了。”
小明说：“好。”

第二天，小美在街上遇到小明。他们不说话。小美想：“难道我做错了？”小明也想：“我还能有女朋友吗？”他们都不高兴。

---
"""
        required_list = ['吵架', '遇到', '难道']
        story_text = pm.extract_story_from_response(test_story)

        required_counts_dict = ct.get_required_words_counts_dict(story_text, required_list)

        print(required_counts_dict)

        for word, count in required_counts_dict.items():
            print(f"{word}: {count}") 

            