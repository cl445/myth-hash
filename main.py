import hashlib
import json
from pathlib import Path
from typing import List

from words import NominativAdjective, CharacterNoun


def main():
    character = load_character()
    physical_attributes = load_attributes(Path(__file__).parent / 'physical_attributes.json')
    personality_attributes = load_attributes(Path(__file__).parent / 'personality_attributes.json')
    print(hash_name("Sven Norman", physical_attributes, personality_attributes, character))
    for i in range(10):
        name_de, name_en = hash_name(f"test{i}", physical_attributes, personality_attributes, character)
        print(f"{name_de} - {name_en}")


def load_attributes(file_path: Path) -> List[NominativAdjective]:
    with open(file_path, 'r') as f:
        json_dict = json.load(f)
    return [NominativAdjective(word_id, data["words"]) for word_id, data in json_dict.items()]


def load_character() -> List[CharacterNoun]:
    with open(Path(__file__).parent / 'character_nouns.json', 'r') as f:
        json_dict = json.load(f)
    return [CharacterNoun(char_id, data["data"]) for char_id, data in json_dict.items()]


def hash_name(input_string: str,
              non_character_adjectives: List[NominativAdjective],
              character_adjectives: List[NominativAdjective],
              character: List[CharacterNoun]) -> (str, str):
    md5 = hashlib.md5(input_string.encode())
    d = md5.digest()

    non_character_adjectives_index = d[0] ^ d[1] ^ d[2] ^ d[3] ^ d[4]
    character_adjectives_index = d[5] ^ d[6] ^ d[7] ^ d[8] ^ d[9]
    character_index = d[10] ^ d[11] ^ d[12] ^ d[13] ^ d[14] ^ d[15]

    non_character_adjectives_index = non_character_adjectives_index % len(non_character_adjectives)
    character_adjectives_index = character_adjectives_index % len(character_adjectives)
    character_index = character_index % len(character)

    character_1 = character[character_index]
    adj_1_de = non_character_adjectives[non_character_adjectives_index].word("de",
                                                                             character_1.get_attribute("de", "gender"))
    adj_1_en = non_character_adjectives[non_character_adjectives_index].word("en",
                                                                             character_1.get_attribute("en", "gender"))
    adj_2_de = character_adjectives[character_adjectives_index].word("de", character_1.get_attribute("de", "gender"))
    adj_2_en = character_adjectives[character_adjectives_index].word("en", character_1.get_attribute("en", "gender"))
    name_de = f"{adj_1_de}-{adj_2_de}-{str(character_1.get_attribute('de', 'word')).replace(' ', '')}"
    name_en = f"{adj_1_en}-{adj_2_en}-{str(character_1.get_attribute('en', 'word')).replace(' ', '')}"
    return name_de, name_en


def filter_nouns(nouns: List[CharacterNoun]) -> List[CharacterNoun]:
    drop_list = list()
    for i in range(len(nouns)):
        for j in range(i + 1, len(nouns)):
            if nouns[i].get_attribute("en", "word") == nouns[j].get_attribute("en", "word"):
                if nouns[i].get_attribute("de", "gender") == "feminine" and nouns[j].get_attribute("de",
                                                                                                   "gender") == "masculine":
                    drop_list.append(i)
                elif nouns[i].get_attribute("de", "gender") == "masculine" and nouns[j].get_attribute("de",
                                                                                                      "gender") == "feminine":
                    drop_list.append(j)
                else:
                    drop_list.append(i)
    drop_list = list(set(drop_list))
    for i in sorted(drop_list, reverse=True):
        print(
            f"Drop {nouns[i].get_attribute('en', 'word')} - {nouns[i].get_attribute('de', 'word')} - {nouns[i].get_attribute('de', 'gender')}")
        nouns.pop(i)
    return nouns


if __name__ == '__main__':
    main()
