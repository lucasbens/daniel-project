import re
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import unicodedata



def remove_non_alphabetical(text):

    # Remove accent
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')

    
    text = text.strip()

    # Remove non alphabetical and keep hyphens and spaces
    text = re.sub(r'[^a-zA-Z-\s]', '', text)

    # Replace spaces & hyphens with a single hyphen
    text = re.sub(r'[\s-]+', '-', text)

    return text.lower()





def suggestion(full_name, table_dico, limit=5):

    return [(tup[0], table_dico[tup[0]]) for tup in process.extract(full_name, table_dico.keys(), limit=5)]



    



def test():
    assert remove_non_alphabetical("Jean-Pierre") == "jean-pierre"
    assert remove_non_alphabetical("Jean- Pierre") == "jean-pierre"
    assert remove_non_alphabetical("Jean Pierre") == "jean-pierre"
    assert remove_non_alphabetical("Jean  Pierre") == "jean-pierre"
    assert remove_non_alphabetical('jean  . --- -   --  pierre')
    assert remove_non_alphabetical("`ilana ") == "ilana"
    assert remove_non_alphabetical("` !@ilana .") == "ilana"


    test_cases = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'à': 'a',
        'è': 'e',
        'ì': 'i',
        'ò': 'o',
        'ù': 'u',
        'â': 'a',
        'ê': 'e',
        'î': 'i',
        'ô': 'o',
        'û': 'u',
        'ä': 'a',
        'ë': 'e',
        'ï': 'i',
        'ö': 'o',
        'ü': 'u'
    }

    for accent, base_letter in test_cases.items():
        assert remove_accents(accent) == base_letter, f"Failed for accent: {accent}"

    print("All assertions passed!")











