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


def main():
    am.generate_initial_prompt()

if __name__ == "__main__":
    main()
