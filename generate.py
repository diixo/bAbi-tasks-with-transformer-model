
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

welcome_help = [
    "Which product can I help you with?",
    "How can I assist you with your product search?",
    "Is there a particular product you'd like help with?",
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

    # "Sofa", "Bed", "Pillow", "Blanket", "Mattress", "Wardrobe", "Drawer", "Shelf", "Cupboard", "Desk",

    # "Headphones", "Plate", "Bowl", "Cup", "Glass", "Mug", "Fork", "Knife", "Spoon", "Teapot",
    # "Pan", "Pot", "Frying-pan", "Kettle", "Oven", "Stove", "Microwave", "Fridge", "Freezer", "Dishwasher",

    # "Sink", "Soap", "Towel", "Toothbrush", "Toothpaste", "Comb", "Hairbrush", "Shampoo", "Razor", "Toilet-paper",

    # "Washing-machine", "Dryer", "Iron", "Ironing-board", "Vacuum-cleaner", "Broom", "Mop", "Bucket", "Dustpan", "Sponge",
    # "Needle", "Thread", "Tape", "Glue", "Pen", "Pencil", "Eraser", "Notebook", "Paper", "Book",
    # "Magazine", "Newspaper", "Bag", "Backpack", "Wallet", "Purse", "Key", "Keychain", "Umbrella", "Slippers",
    #"Socks", "Coat",
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


def generate_v2(samples: int) -> list:

    question_per_story = 5
    story_count = int(samples / question_per_story)

    stories = []

    for _ in range(story_count):

        items = []

        on_sale = [assortment[0], assortment[1], assortment[2], assortment[3]]
        commodity = random.choice(on_sale)

        items.append(f"System: You are online shopping {random.choice(roles)}")

        items.append(f"User: {random.choice(hi_user)} {random.choice(intents)} the {commodity}, {random.choice(sizes)}. Is it available?")

        items.append(f"Assistant::System action request={commodity}")

        if random.randint(0, 1) > 0:
            amount = random.randint(1, 20)
            items.append(f"System::Assistant response {commodity} amount={amount}")

            items.append(f"Is {commodity} available in stock?\t{'yes'}\t0")
            items.append(f"How many {commodity}?\t{amount}\t0")

            fact_stock = ["we have it in stock", "it's in stock",]
            items.append(f"Assistant: Yes, {random.choice(fact_stock)}.")
        else:
            amount = 0
            items.append(f"System::Assistant response {commodity} amount={amount}.")

            items.append(f"Assistant: No, it's absent now.")

            items.append(f"Is {commodity} available in stock?\t{'no'}\t0")
            items.append(f"How many {commodity}?\t{amount}\t0")

            items.append(f"User: {random.choice(question_available)}")
            items.append("Assistant: Yes")

        items.append(f"User: {random.choice(question_price)}")

        items.append(f"Assistant::System action {commodity} price")

        price = random.randint(10, 199)
        items.append(f"System::Assistant response {commodity} price={price}")

        items.append(f"Assistant: {commodity} price?\t{price}\t0")

        items.append(f"Assistant: ${price}")

        items.append(f"User: Got it. How long does delivery take?")
        items.append("Assistant: Standard shipping takes 3-5 business days.")

        choice = random.randint(0, 1)
        if choice > 0:
            items.append(f"User: {random.choice(approve)} I'll place the order.")
            items.append(f"Assistant: Thank you! I will send you the payment link after.")
            #Customer: Perfect, I'll place the order.
            #Seller: Thank you! I'll send you the payment link now.
            #"Was an order placed?"
            #items.append(f"User: {random.choice(approve)} I'll take it.")
            answer = "yes"
        else:
            items.append(f"User: No, {random.choice(waiting)}")
            answer = "no"

        items.append(f"Will an order be placed?\t{answer}\t0")
        items.append(f"{random.choice(question_intent)}\t{answer}\t0")

        stories.append(items_to_story(items))
    return stories


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


def generate_v3(samples: int) -> list:

    question_per_story = 10
    story_count = int(samples / question_per_story)

    stories = []
    turn_stories = []

    for _ in range(story_count):

        add_to_cart = [
            "You need to add all the items to your shopping cart.",
            "Please make sure to add all the items to your cart.",
            "All items must be added to the shopping cart.",
            ]

        ask_forgot_item = [
            "What was the order forgotten for?",
            "Which item was the order forgotten for?",
            "What item was missed in the order?",
            "What item was the order forgotten for?",
            "Which item did we forget to order?",
        ]

        # ask_forgot_about = [
        #     "Was an order forgotten for something?",
        #     "Was an order left unplaced for something?",
        #     "Did we forget to order something?",
        #     "Was there something we forgot to order?",
        # ]

        # product available
        pa1 = random.randint(0, 1)
        pa2 = random.randint(2, 3)
        pa3 = random.randint(4, 5)   # to ask as missing item
        pa4 = random.randint(6, 7)
        pa5 = random.randint(8, 9)

        # pna1 = 1 if pa1==0 else 0
        # pna2 = 3 if pa2==2 else 2
        # pna3 = 5 if pa3==4 else 4
        # pna4 = 7 if pa4==6 else 6
        # pna5 = 9 if pa5==8 else 8

        ask_availability = [
            "Can you check if it is in stock?",
            "Could you verify if it's available?",
            "Can you see whether it's available?",
            "Could you check the availability?",
        ]

        interesting = [ "\'ll take", " will purchase", " have to buy", "\'m interested in" ]

        items = []
        items.append(f"System: You are online shopping {random.choice(roles)}. {random.choice(available_txt)} {assortment_s[pa1]}, {assortment_s[pa2]}, {assortment_s[pa3]}, {assortment_s[pa4]}, {assortment_s[pa5]}")
        items.append(f"Assistant: {random.choice(welcome_search)}")

        items.append(f"Is {assortment[pa5]} available?\tyes\t0")
        items.append(f"Is {assortment[pa1]} available?\tyes\t0")
        items.append(f"Is {assortment[pa4]} available?\tyes\t0")
        items.append(f"Is {assortment[pa3]} available?\tyes\t0")
        items.append(f"Is {assortment[pa2]} available?\tyes\t0")

        items.append(f"User: I{random.choice(interesting)} the {assortment[pa5]}. {random.choice(ask_availability)}")
        items.append(f"Assistant: Yes, it is available.")
        items.append(f"User: I{random.choice(interesting)} the {assortment[pa1]}. {random.choice(ask_availability)}")
        items.append(f"Assistant: Sure. Yes, it\'s available.")
        items.append(f"User: I{random.choice(interesting)} the {assortment[pa4]}. {random.choice(ask_availability)}")
        items.append(f"Assistant: Yes, it is available.")
        items.append(f"User: I{random.choice(interesting)} the {assortment[pa3]}. {random.choice(ask_availability)}")
        items.append(f"Assistant: Yes, it\'s available.")
        items.append(f"User: I{random.choice(interesting)} the {assortment[pa2]}. {random.choice(ask_availability)}")
        items.append(f"Assistant: Let me check. Yes, it is available.")

        items.append(f"User: I am ready to buy all available items.")
        items.append(f"Assistant: {random.choice(add_to_cart)}")

        items.append(f"User: I have added the {assortment[pa4]}, the {assortment[pa1]}, the {assortment[pa5]}, the {assortment[pa2]} to the card.")

        about_forgot = [
            "It seems you forgot to add another item from the ones you wanted.",
            "It seems you didn't add all the items you wanted.",
            "It seems some items you wanted are missing in the card.",
            "It looks like not all items you wanted are in the card.",
        ]

        items.append(f"Assistant: {random.choice(about_forgot)}")

        items.append(f"{random.choice(ask_forgot_item)}\t{assortment[pa3]}\t0")

        #reaction_1 = ["Exactly, I forgot.", "Yes, I forgot.", ]
        #reaction_2 = ["Yes, I know.", "Yes, I'm aware."]

        agree = ["Yes, that's right.", "Yes, you are right.",]

        req_add = [
            "Add missing item to order.",

            "I forgot. Please add the missing item.",
            "I forgot. Add the one I missed.",

            "Add the remaining item to complete my order.",
            "Complete the order with the missing item.",
            "Add the missing item to complete my order.",
        ]

        req_skip = [
            "Yes, I know. Leave it as is.",
            "Yes, I'm aware. Keep it as it is.",
            "Yes, That's correct. Skip it.",
            "Yes, Exactly. You can skip that one.",
        ]

        turn = random.randint(0, 1)
        if turn > 0:    # add item
            items.append(f"User: {random.choice(agree)} {random.choice(req_add)}")
            turn = "yes"
            question = [
                "Which item should be added to the order?",
                "What item should the order be completed with?",
                "Which item should be added to expand the order?",
                "What item should be included to extend the order?",
            ]
        else:
            items.append(f"User: {random.choice(req_skip)}")
            turn = "no"
            question = [
                "Which item in the order should be skipped?",
                "Which item should be left out of the order?",
                "Which item are we skipping in the order?",
            ]

        ############### proposition to ask of adding new item

        q_propose = [
            "Would it be appropriate to suggest adding the missing item?",
            "Is it necessary to suggest adding the missing item?",
            "Is it necessary to propose adding the missing item?",
        ]

        # try to understand the necessity to ask adding new item by answer
        #items.append(f"{random.choice(q_propose)}\t{turn}\t0")

        ###############################################################
        items.append(f"{random.choice(question)}\t{assortment[pa3]}\t0")

        q_confirm = [
            "Are all these items included in the order",
            "Are all of these items in the list included in the order",
            "Does the order include all items from this list",
        ]
        items.append(f"{random.choice(q_confirm)}: the {assortment[pa1]}, the {assortment[pa4]}, the {assortment[pa2]}, the {assortment[pa3]}, the {assortment[pa5]}?\t{turn}\t0")

        ask_confirmation = [
            "Do you want to confirm the purchase?",
            "Would you like to confirm your order?",
            "Shall I confirm the purchase for you?",
        ]

        #####################################################################
        q_confirm = [
            "Was the order confirmed for all these items",
            "Has the order been confirmed for all these items",
            #"Was the order placed for all following items",
        ]
        items.append(f"{random.choice(q_confirm)}: the {assortment[pa2]}, the {assortment[pa3]}, the {assortment[pa5]}, the {assortment[pa1]}, the {assortment[pa4]}?\tno\t0")

        items.append(f"Assistant: {random.choice(ask_confirmation)}")
        items.append("User: yes")
        q_confirm = [
            "Was the order confirmed for all these items",
            "Has the order been confirmed for all these items",
            #"Was the order placed for all following items",
        ]
        items.append(f"{random.choice(q_confirm)}: the {assortment[pa2]}, the {assortment[pa3]}, the {assortment[pa5]}, the {assortment[pa1]}, the {assortment[pa4]}?\t{turn}\t0")
        #####################################################################
        items.append("Assistant: I will send you a link for online payment.")

        #####################################################################
        #print(items_to_story(items))
        stories.append(items_to_story(items))

        # valid if only questions per for turns and simple story the same
        turns = items_to_turns(items)
        turn_stories.append(items_to_story(turns))

    return stories, turn_stories


actions = [
    "place an order",
    "confirm an order",
    "cancel an order",
    "check order status",
    "request delivery details"
]


if __name__ == "__main__":

    samples = 1000

    if False:

        train_stories = generate_v2(samples)

        with open("datasets/qa21-shopping-dialogue_train.txt", "w", encoding="utf-8") as f:
            f.writelines(train_stories)

        test_stories = generate_v2(samples)

        with open("datasets/qa21-shopping-dialogue_test.txt", "w", encoding="utf-8") as f:
            f.writelines(test_stories)
    if False:

        train_stories, train_turns = generate_v3(samples)

        with open("datasets/qa22-shopping-items_train.txt", "w", encoding="utf-8") as f:
            f.writelines(train_stories)

        with open("datasets/qa23-shopping-turns_train.txt", "w", encoding="utf-8") as f:
            f.writelines(train_turns)

        test_stories, test_turns = generate_v3(samples)

        with open("datasets/qa22-shopping-items_test.txt", "w", encoding="utf-8") as f:
            f.writelines(test_stories)

        with open("datasets/qa23-shopping-turns_test.txt", "w", encoding="utf-8") as f:
            f.writelines(test_turns)

    #print(f"sampeles={samples}, train_stories={len(train_stories)}, train_turns={len(train_turns)} ")
