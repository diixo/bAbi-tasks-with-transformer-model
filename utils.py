import re

def remove_punctuation_comma(text):
    cleaned_text = re.sub(r"[^\w\s!,-]", "", text)
    return cleaned_text


def str_tokenize_words(s: str):
    import re
    s = re.findall("(\.?\w[\w'\.&-]*\w|\w\+*#?)", s)
    if s: return s
    return []


def parse_answer(text: str, eos_token):
    text = text.replace(eos_token,"")
    try:
        answer_start = text.index("Answer:")
        answer = remove_punctuation_comma(text[answer_start:].split(":")[1].strip().split("\n")[0])
    except:
        answer = ""
    return answer


def items_to_story(items: list) -> str:
    return "".join([ f"{id+1} {item}\n" for id, item in enumerate(items) ])

def items_to_turns(items: list[str]) -> list:
    turn_list = []
    for item in items:
        if item.find("System: ") == 0 or item.find("User:") == 0:
            turn_list.append(item)
        if item.find("Assistant: ") == 0:
            separator = item.find(":")
            assistant = item[:separator+1]
            utterance = item[separator+1:]
            turn_list.append(f"{assistant.strip()}\t{utterance.strip()}\t0")
    return turn_list
