import argparse
import hashlib
import json
from pathlib import Path
from typing import List, Tuple, Dict

from words import NominativAdjective, CharacterNoun


def main(input_string: str, language: str, output_format: str) -> None:
    character_nouns = load_character_nouns()
    physical_attributes = load_attributes(Path(__file__).parent / 'physical_attributes.json')
    personality_attributes = load_attributes(Path(__file__).parent / 'personality_attributes.json')

    physical_attr, personality_attr, character_noun = hash_name(input_string, physical_attributes,
                                                                personality_attributes,
                                                                character_nouns, language)
    if output_format == 'text':
        print(f"{physical_attr}-{personality_attr}-{character_noun.replace(' ', '')}")
    elif output_format == 'json':
        output: Dict[str, str] = {"physical_attribute": physical_attr, "personality_attribute": personality_attr,
                                  "character": character_noun}
        print(json.dumps(output, ensure_ascii=False))


def load_attributes(file_path: Path) -> List[NominativAdjective]:
    with open(file_path, 'r') as f:
        json_dict = json.load(f)
    return [NominativAdjective(word_id, data["words"]) for word_id, data in json_dict.items()]


def load_character_nouns() -> List[CharacterNoun]:
    with open(Path(__file__).parent / 'character_nouns.json', 'r') as f:
        json_dict = json.load(f)
    return [CharacterNoun(char_id, data["data"]) for char_id, data in json_dict.items()]


def generate_indices(input_string: str, list_sizes: List[int]) -> List[int]:
    sha256 = hashlib.sha256(input_string.encode())
    d = sha256.digest()
    hash_length = len(d)
    indices = []

    for i, size in enumerate(list_sizes):
        start = (hash_length // len(list_sizes)) * i
        end = start + (hash_length // len(list_sizes))

        segment = int.from_bytes(d[start:end], 'big')

        index = segment % size
        indices.append(index)

    return indices


def hash_name(input_string: str,
              physical_attributes: List[NominativAdjective],
              personality_attributes: List[NominativAdjective],
              character_nouns: List[CharacterNoun],
              language: str = "en") -> Tuple[str, str, str]:
    indices = generate_indices(input_string,
                               [len(physical_attributes), len(personality_attributes), len(character_nouns)])

    physical_attr_index = indices[0]
    personality_attr_index = indices[1]
    character_nouns_index = indices[2]

    character_noun = character_nouns[character_nouns_index]
    physical_attr = physical_attributes[physical_attr_index].word(language,
                                                                  character_noun.get_attribute(language, "gender"))
    personality_attr = personality_attributes[personality_attr_index].word(language,
                                                                           character_noun.get_attribute(language,
                                                                                                        "gender"))
    return physical_attr, personality_attr, character_noun.get_attribute(language, "word")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates a fantasy name from a hash value of an input string.')
    parser.add_argument('input_string', type=str, help='Input string to hash and generate a fantasy name.')
    parser.add_argument('-l', '--language', type=str, default='en', choices=['en', 'de'],
                        help='Specify the output language. Supported languages: English (en) and German (de). Default is English.')
    parser.add_argument('-f', '--format', type=str, default='text', choices=['text', 'json'],
                        help='Specify the output format. Choose between plain text (text) and JSON (json). Default is text.')

    args = parser.parse_args()

    if not args.input_string.strip():
        parser.error("Input string cannot be empty.")

    main(args.input_string, args.language, args.format)
