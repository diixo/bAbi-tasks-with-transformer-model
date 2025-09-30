
import random

random.seed(random.randint(1, 2080))

roles = ["assistant", "Assistant",]

available_txt = [
    "The following items are available:",
    "Items in stock:",
    "Available items:",
    "Products range includes:",
    "Products range:",
    "Sales range includes:",
    "Our assortment in stock includes:",
    "Items currently in stock:",
    "Our available assortment:",
    "Products, that have in stock:",
]

welcome_search = [
    "What product are you interested in?",
    "Which product are you looking for?",
    "What item are you interested in?",

    "Which product would you like to purchase?",
    "What product would you like to buy?",
    "Which item are you planning to purchase?",
]

assortment = [
    ["T-shirt", "dress", "sweater", "shirt", "jacket", "skirt", "scarf", "backpack", "bodice", "hoodie",],

    ["box", "laptop", "lamp", "charger", "toy", "football", "TV-set", "phone", "spray", "deodorant",],

    ["sofa", "bed", "pillow", "blanket", "mattress", "wardrobe", "drawer", "shelf", "cupboard", "desk",],

    ["headphones", "plate", "bowl", "cup", "glass", "mug", "fork", "knife", "spoon", "teapot",],

    ["pan", "pot", "frying-pan", "kettle", "oven", "stove", "microwave", "fridge", "freezer", "dishwasher",],

    ["sink", "soap", "towel", "toothbrush", "toothpaste", "comb", "hairbrush", "shampoo", "razor", "toilet-paper",],

    ["washing-machine", "dryer", "iron", "ironing-board", "vacuum-cleaner", "broom", "mop", "bucket", "dustpan", "sponge",],

    ["needle", "thread", "tape", "glue", "pen", "pencil", "eraser", "notebook", "paper", "book",],

    ["magazine", "newspaper", "bag", "wallet", "purse", "key", "keychain", "umbrella", "slippers", "coat",],

    ["shawl", "pants", "cap", "sneakers", "hat", "sundress", "headscarf", "jumpsuit", "swimsuit", "bodysuit",],
]

flat = [item for array in assortment for item in array]

print(len(flat))


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


def generate_v6(samples: int) -> list:

    question_per_story = 10
    story_count = int(samples / question_per_story)

    stories = []
    turn_stories = []

    ask_availability = [
        "Can you check if it is in stock?",
        "Could you verify if it's available?",
        "Can you see whether it's available?",
        "Could you check the availability?",
    ]

    interesting = [ "\'ll take", " will purchase", " have to buy", "\'m interested in" ]

    propose_another_product = [
        "You can try looking for another product.",
        "You may try searching for another item.",
        "You could try to find a different product.",
        "Perhaps you\'d like to look for another product?",
    ]

    for _ in range(story_count):
        items = []

        rnd_size = random.randint(0, 3)

        a_set = set([ random.choice(sublist) for sublist in assortment[:rnd_size] ])
        na_set = list(a_set ^ set(flat))
        mix_set = set(a_set)

        if rnd_size > 0:
            avail_txt = ", ".join([product for product in a_set])
            items.append(f"System: You are online shopping {random.choice(roles)}. {random.choice(available_txt)} {avail_txt}")
            items.append(f"Assistant: Hi. I am online shopping Assistant. What product are you interested in?")
            items.append("Is the available items list empty?\tno\t0")
        else:
            items.append(f"System: You are online shopping {random.choice(roles)}.")
            items.append(f"Assistant: Hi. I am online shopping Assistant. {random.choice(welcome_search)}")
            items.append("Is the available items list empty?\tyes\t0")

        while len(mix_set) < 8:
            mix_set.add(random.choice(na_set))
            if len(mix_set)==8:
                break
        mix_set = list(mix_set)
        random.shuffle(mix_set)

        for id, product in enumerate(mix_set):
            # available
            if product in a_set:
                if id % 2 == 0:
                    items.append(f"User: {product}")
                    items.append(f"Is {product} available?\tyes\t0")
                    items.append(f"Assistant: Yes. It is available.")
                else:
                    items.append(f"User: I{random.choice(interesting)} the {product}.")
                    items.append(f"Is {product} available?\tyes\t0")
                    items.append(f"Assistant: Yes.")
                    #items.append(f"Assistant: Yes. It is available.")
            else:   # not available
                if id % 2 == 0:
                    items.append(f"User: {product}")
                    items.append(f"Is {product} available?\tno\t0")
                    items.append(f"Assistant: No. It is not available.")
                else:
                    items.append(f"User: I{random.choice(interesting)} the {product}.")
                    items.append(f"Is {product} available?\tno\t0")
                    items.append(f"Assistant: No.")
                    #items.append(f"Assistant: No. It is not available.")

        ###################
        items.append("User: Okay, show me what is available.")

        if len(a_set) > 0:
            items.append("Is the available items list empty?\tno\t0")

            avail_txt = ", ".join([product for product in a_set])
            items.append(f"Assistant: Sure! Our available items list: {avail_txt}. Would you like to choose from these?")
        else:
            items.append("Is the available items list empty?\tyes\t0")
            items.append(f"Assistant: our available items list is empty.")

        stories.append(items_to_story(items))

        turns = items_to_turns(items)
        turn_stories.append(items_to_story(turns))

    return stories, turn_stories


if __name__ == "__main__":

    samples = 1000

    train_stories, train_turns = generate_v6(samples)

    with open("datasets/qa26-shopping-available_train.txt", "w", encoding="utf-8") as f:
        f.writelines(train_stories)

    with open("datasets/qa27-shopping-available-turns_train.txt", "w", encoding="utf-8") as f:
        f.writelines(train_turns)

    test_stories, test_turns = generate_v6(samples)

    with open("datasets/qa26-shopping-available_test.txt", "w", encoding="utf-8") as f:
        f.writelines(test_stories)

    with open("datasets/qa27-shopping-available-turns_test.txt", "w", encoding="utf-8") as f:
        f.writelines(test_turns)

    print(f"sampeles={samples}, train_stories={len(train_stories)}, train_turns={len(train_turns)} ")
