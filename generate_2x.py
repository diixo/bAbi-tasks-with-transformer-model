
import random


random.seed(random.randint(1, 2080))

INPUT_TEMPLATE = """
### Context:
{context}

### Question:
{question}

### Answer:
{answer}
"""

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

roles = ["assistant", "Assistant",]


assortment = ["T-shirt", "dress", "sweater", "shirt", "jacket", "skirt", "scarf", "backpack", "bodice", "hoodie",]

assortment_s = ["T-shirts", "dresses", "sweaters", "shirts", "jackets", "skirts", "scarves", "backpacks", "bodices", "hoodies",]

assortment_na = ["shawl", "pants", "cap", "sneakers", "hat", "sundress", "headscarf", "jumpsuit", "swimsuit", "bodysuit",]

assortment_rnd = assortment_na + [
    "apple", "box", "laptop", "lamp", "charger", "toy", "football", "TV-set", "phone", "spray", "deodorant", "server", "monitor",
    "display", "shoes", "tomato", "airplane", "cooler", "byke", "conditioner", "lighthouse", "airport", "spaceship", "redis", "fish",
    "chair", "passport", "scissors", "bear", "beer",
    "deer", "developer", "mirror", "tongue", "parking", "tea", "banana", "dog", "door", "penguin",

    "Sofa", "Bed", "Pillow", "Blanket", "Mattress", "Wardrobe", "Drawer", "Shelf", "Cupboard", "Desk",

    "Headphones", "Plate", "Bowl", "Cup", "Glass", "Mug", "Fork", "Knife", "Spoon", "Teapot",
    "Pan", "Pot", "Frying-pan", "Kettle", "Oven", "Stove", "Microwave", "Fridge", "Freezer", "Dishwasher",

    "Sink", "Soap", "Towel", "Toothbrush", "Toothpaste", "Comb", "Hairbrush", "Shampoo", "Razor", "Toilet-paper",

    "Washing-machine", "Dryer", "Iron", "Ironing-board", "Vacuum-cleaner", "Broom", "Mop", "Bucket", "Dustpan", "Sponge",
    "Needle", "Thread", "Tape", "Glue", "Pen", "Pencil", "Eraser", "Notebook", "Paper", "Book",
    "Magazine", "Newspaper", "Bag", "Wallet", "Purse", "Key", "Keychain", "Umbrella", "Slippers", "Coat",
    # "Socks", 
]

sizes = ["size XS", "size S", "size M", "size L", "size XL", "size XXL",]

colors = ["red", "blue", "green", "white", "beige", "black", "yellow", "grey",]

intents = ["I'm interested in", "I want to buy",]

hi_user = ["Hello,", "Hi,"]

approve = ["Ok.", "Great.", "Good.", "Okay.", "Perfect."]

question_price = ["How much?", "Whats is the price?", "How much it cost?", "What price?", "How much is it?", "What's the price?"]

question_intent = ["Purchase intent?", "Intent to buy?",]

question_available = [
    "Will this item be available in the future?",
    "Will this product become available later?",
    "Is this product expected to be in stock in the future?",
]

waiting = ["too long.", "too long to wait.", "too long of waiting."]


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



def generate_v5(samples: int) -> list:

    question_per_story = 4
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

    print("gen assortment_rnd size:", len(assortment_rnd))


    propose_another_product = [
        "You can try looking for another product.",
        "You may try searching for another item.",
        "You could try to find a different product.",
        "Perhaps you\'d like to look for another product?",
    ]


    for _ in range(story_count):
        items = []

        rnd_amount = random.randint(0, 2)
        avail_ids = []
        if rnd_amount == 0:
            avail_ids = avail_ids
        if rnd_amount == 1:
            avail_ids = [random.randint(0, 9),]
        if rnd_amount == 2:
            avail_ids = [random.randint(0, 4), random.randint(5, 9),]
        # if rnd_amount == 3:
        #     avail_ids = [random.randint(0, 3), random.randint(4, 6), random.randint(7, 9),]
        # if rnd_amount == 4:
        #     avail_ids = [random.randint(0, 2), random.randint(3, 5), random.randint(6, 7), random.randint(8, 9),]
        # if rnd_amount == 5:
        #     avail_ids = [random.randint(0, 1), random.randint(2, 3), random.randint(4, 5), random.randint(6, 7), random.randint(8, 9),]

        # avail_set = set([ assortment[id] for id in avail_ids ])
        # avail_s_set = set([ assortment_s[id] for id in avail_ids ])

        if len(avail_ids) > 0:
            avail_txt = ", ".join([assortment_s[id] for id in avail_ids])
            items.append(f"System: You are online shopping {random.choice(roles)}. {random.choice(available_txt)} {avail_txt}")
            items.append(f"Assistant: Hi. I am online shopping Assistant. What product are you interested in?")
            items.append("Is the available items list empty?\tno\t0")
        else:
            items.append(f"System: You are online shopping {random.choice(roles)}.")
            items.append(f"Assistant: Hi. I am online shopping Assistant. {random.choice(welcome_search)}")
            items.append("Is the available items list empty?\tyes\t0")

        ###################

        if len(avail_ids) > 1:

            pid_0 = random.randint(0, len(avail_ids)-2)
            pid_1 = pid_0 + 1
            product_0 = assortment[avail_ids[pid_0]]
            product_1 = assortment[avail_ids[pid_1]]

            if random.randint(0, 1) > 0:
                items.append(f"User: {product_0}")
                items.append(f"Is {product_0} available?\tyes\t0")
                items.append(f"Assistant: Yes. It is available.")

                product = product_0
            else:
                product = random.choice(assortment_rnd)
                items.append(f"User: {product}")
                items.append(f"Is {product} available?\tno\t0")
                items.append(f"Assistant: No.")

            ###################

            if random.randint(0, 1) > 0:
                items.append(f"User: I{random.choice(interesting)} the {product_1}.")

                items.append(f"Is {product_1} available?\tyes\t0")
                items.append(f"Assistant: Yes. It is available.")

                product = product_1
            else:
                product = random.choice(assortment_rnd)
                items.append(f"User: I{random.choice(interesting)} the {product}.")
                items.append(f"Is {product} available?\tno\t0")
                items.append(f"Assistant: No. It is not available.")

            #items.append(f"Which product is the customer interested in?\t{product}\t0")
        else:
            product = random.choice(assortment_rnd)
            items.append(f"User: {product}")
            #items.append(f"{random.choice(welcome_search)}\t{product}\t0")

            items.append(f"Is {product} available?\tno\t0")
            items.append(f"Assistant: No. It is not available.")
            #########################

            product = random.choice(assortment_rnd)
            items.append(f"User: I{random.choice(interesting)} the {product}.")

            items.append(f"Is {product} available?\tno\t0")
            items.append(f"Assistant: No. It is not available.")

            #items.append(f"Which product is the customer interested in?\t{product}\t0")

        ###################
        items.append("User: Okay, show me what is available.")

        if len(avail_ids) > 0:
            items.append("Is the available items list empty?\tno\t0")

            avail_txt = ", ".join([assortment_s[id] for id in avail_ids])
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

    train_stories, train_turns = generate_v5(samples)

    with open("datasets/qa24-shopping-available_train.txt", "w", encoding="utf-8") as f:
        f.writelines(train_stories)

    with open("datasets/qa25-shopping-available-turns_train.txt", "w", encoding="utf-8") as f:
        f.writelines(train_turns)

    test_stories, test_turns = generate_v5(samples)

    with open("datasets/qa24-shopping-available_test.txt", "w", encoding="utf-8") as f:
        f.writelines(test_stories)

    with open("datasets/qa25-shopping-available-turns_test.txt", "w", encoding="utf-8") as f:
        f.writelines(test_turns)

    print(f"sampeles={samples}, train_stories={len(train_stories)}, train_turns={len(train_turns)} ")
