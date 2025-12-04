import src.utils as utils

class Story:
    def __init__(
            self, 
            story_text: str,
            hsk_int: int,
            required_words_list: list[str],
            ) -> None:
        self.story_text = story_text
        self.required_words_list = required_words_list
        self.hsk_int = hsk_int
        self.story_groups_dict = utils.get_story_groups_dict(self.story_text)
        self.group_counts_dict = {}
        self.required_words_count_dict = {}
        self.required_words_missing_list = []

    def get_story_groups_dict(self):
        return self.story_groups_dict

    def get_group_counts_dict(self):
        if self.group_counts_dict:
            return self.group_counts_dict
        
        group_counts = {}
        story_groups_dict = self.get_story_groups_dict()
        
        for group, word_list in story_groups_dict.items():
            word_count = 0
            for word in word_list:
                if word in self.required_words_list:
                    continue
                word_count += 1
            group_counts[group] = word_count

        self.group_counts_dict = group_counts

        return self.group_counts_dict
        
    def get_required_words_count(self) -> dict[str, int]:
        if self.required_words_count_dict:
            return self.required_words_count_dict
        
        count_dict = {}
        for word in self.required_words_list:
            word_count = self.story_text.count(word)
            count_dict[word] = word_count

        self.required_words_count_dict = count_dict

        return self.required_words_count_dict

    def get_missing_required_words_list(self) -> list[str]:
        if self.required_words_missing_list:
            return self.required_words_missing_list

        if not self.required_words_count_dict:
            self.get_required_words_count()
        
        missing_words = []
        
        for word, count in self.required_words_count_dict.items():
            if count == 0:
                missing_words.append(word)

        self.required_words_missing_list = missing_words

        return self.required_words_missing_list
    
    def get_hsk_violations_perc(self):
        total_unique_words = 0
        total_violations = 0

        for group_name, count in sorted(self.group_counts_dict.items()):
            if "partial_match" in group_name:
                continue
            
            total_unique_words += count
            if "HSK" in group_name:
                if int(group_name[-1]) <= self.hsk_int:
                    continue
            total_violations += count

        return total_violations / total_unique_words
    
    def get_HSK_violations_dict(self) -> dict[str, list[str]]:
        
        violations_dict = {}
        story_groups_dict = self.get_story_groups_dict()

        for group, list in story_groups_dict.items():
            if "HSK" in group:
                group_level = int(group[-1])
                if group_level > self.hsk_int:
                    violations_dict[group] = list

        return violations_dict