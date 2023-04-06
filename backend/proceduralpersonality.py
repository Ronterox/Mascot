import tracery as tr
from tracery.modifiers import base_english
from func.moduler import module_path
import json

# Tracery syntax
# --------------------------------
# Basic syntax
# "keyword"": ["list", "of", "possible", "outputs"]

# Replace syntax
# "keyword": ["#replace#"]

# Modfiers syntax
# replace, capitalizeAll, capitalize, a, firstS, uppercase, ed, lowercase
# print(base_english)

# Action syntax
# "origin": ["#[action:#replace#]replace#"]

# Advanced syntax
# "setActions": ["[occupations:#occupations#][animals:#animals#, human, robot]"]
# "origin": ["#[#setActions#]replace#"]

DATA_PATH = module_path("data/personality.json", __name__)

data = json.load(open(DATA_PATH, "r", encoding="utf-8"))

phrases = tr.Grammar({
    "greeting": data["greetings"],
    "farewell": data["farewells"],
    "question": data["how_are_you"],
    "response": data["how_are_you_responses"],
    "meaning_of_life": data["meaning_of_life"],
    "cheer_up": data["cheer_up"],
    "waste_time": data["waste_time"],
    "sound": data["sounds"],
    "presentation": data["presentation"],
    "getName": ["#sound##sound#", "#sound##sound##sound#"],
    "salutation": "#greeting# #presentation.lowercase# #name.capitalize# #getName.capitalize#",
    "something": ["#cheer_up#", "#waste_time#"],
    "meaning": ["there is nothing like #meaning_of_life#", "I believe that the meaning of life is #meaning_of_life#", "without #meaning_of_life# I'm nothing"],
    "goodbye": "I believe that the meaning of life is #meaning_of_life#\nNow #something.lowercase#\n#farewell.capitalize#,",
    "origin": ["#salutation#", "#question# #response#", "#something#", "#goodbye#", "#meaning_of_life#", "#meaning#", "#meaning_of_life# #something#", "#meaning_of_life# #meaning_of_life# and #meaning_of_life#"]
})
phrases.add_modifiers(base_english)


def get_response(txt, seed=None):
    if seed:
        tr.random.seed(seed)
    return phrases.flatten(txt)


if __name__ == "__main__":
    tr.random.seed(2217771)
    print(get_response("[name:#getName#]#salutation#, \n#goodbye#"))
