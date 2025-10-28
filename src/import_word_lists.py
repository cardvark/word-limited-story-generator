import csv

def get_word_groups_from_csv(csv_file_path):
    word_groups = {}

    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)

        for row in csv_reader:
            group = row[3]
            word = row[0]
            # print(f"Found word: {word} in group: {group}")
            if group in word_groups:
                word_groups[group].append(word)
            else:
                word_groups[group] = [word]
                
    return word_groups