import re
from fuzzywuzzy import process
from fuzzywuzzy import fuzz


def remove_non_alphabetical(text):
    pattern = r"[^a-zA-Z]"
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text.lower()


def suggestion(full_name, key_table_dico):

    return [tup[0] for tup in process.extract(full_name, key_table_dico, limit=5)]

    



def test():
    assert remove_non_alphabetical("Jean-Pierre") == "JeanPierre"
    assert remove_non_alphabetical("`ilana ") == "ilana"
    assert remove_non_alphabetical("` !@ilana .") == "ilana"
