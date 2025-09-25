
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


roles = ["assistant", "Assistant",]

#assortment_ext = ["headscarf", "shawl",]

assortment = ["T-shirt", "dress", "sweater", "shirt", "jacket", "skirt", "scarf", "backpack", "bodice", "hoodie",]

assortment_s = ["T-shirts", "dresses", "sweaters", "shirts", "jackets", "skirts", "scarves", "backpacks", "bodices", "hoodies",]

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


def test():

    for id in range(10):

        on_sale = [assortment[0], assortment[1], assortment[2], assortment[3]]
        commodity = random.choice(assortment)

        context = f"You are {random.choice(roles)}. Sales assortment: {on_sale[0]}, {on_sale[1]}, {on_sale[2]}, {on_sale[3]}"

        question = f"Hello, {random.choice(intents)} the {commodity}, {random.choice(sizes)}. Is it available?"

        answer = "yes" if commodity in on_sale else "no"

        cqa = {
            "context": context,
            "question": question,
            "answer": answer
        }

        item = INPUT_TEMPLATE.format_map(cqa).strip() + "\n"

        print(id, item.strip())
        print("-------------------------------------------")


    for id in range(10):

        on_sale = [assortment[0], assortment[1], assortment[2], assortment[3]]
        commodity = random.choice(assortment)

        context = f"You are an online shopping {random.choice(roles)}. Sales assortment: {on_sale[0]}, {on_sale[1]}, {on_sale[2]}, {on_sale[3]}"

        question = f"Hi, is the {commodity} still available in {random.choice(sizes)}?"

        answer = "yes" if commodity in on_sale else "no"

        cqa = {
            "context": context,
            "question": question,
            "answer": answer
        }

        item = INPUT_TEMPLATE.format_map(cqa).strip() + "\n"

        print(id, item.strip())
        print("-------------------------------------------")


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
            items.append(f"Assistant: Thank you! I'll send you the payment link after.")
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


def generate_v3(samples: int) -> list:

    question_per_story = 4
    story_count = int(samples / question_per_story)

    stories = []

    for _ in range(story_count):

        available_txt = [
            "The following items are available:",
            "Items in stock:",
            "Available items:",
            "Our product range includes:",
            "Product range:",
            "Sales range includes:",
            "Our assortment in stock includes:",
            "Items currently in stock:",
            "Our available assortment:",
            "Products we have in stock:",
            ]
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

        p1 = random.randint(0, 1)
        p2 = random.randint(2, 3)
        p3 = random.randint(4, 5)   # to ask as missing item
        p4 = random.randint(6, 7)
        p5 = random.randint(8, 9)

        items = []
        items.append(f"System: You are online shopping {random.choice(roles)}")
        items.append(f"Assistant: {random.choice(available_txt)} {assortment_s[p1]}, {assortment_s[p2]}, {assortment_s[p3]}, {assortment_s[p4]}, {assortment_s[p5]}")
        items.append(f"User: I'll {random.choice(['take', 'purchase', 'have to buy',])} the {assortment[p5]}, the {assortment[p1]}, the {assortment[p4]}, the {assortment[p3]}, the {assortment[p2]}.")
        items.append(f"Assistant: {random.choice(add_to_cart)}")
        items.append(f"User: I have added the {assortment[p4]}, the {assortment[p1]}, the {assortment[p5]}, the {assortment[p2]} to the card.")

        about_forgot = [
            "It seems you forgot to add another item from the ones you wanted.",
            "It seems you didn't add all the items you wanted.",
            "It seems some items you wanted are missing in the card.",
            "It looks like not all items you wanted are in the card.",
        ]

        items.append(f"Assistant: {random.choice(about_forgot)}")

        items.append(f"{random.choice(ask_forgot_item)}\t{assortment[p3]}\t0")

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

        items.append(f"{random.choice(q_propose)}\t{turn}\t0")

        ###############################################################
        items.append(f"{random.choice(question)}\t{assortment[p3]}\t0")


        q_confirm = [
            "Was the order confirmed for all the items",
            "Has the order been confirmed for all the items",
            "Has the order been confirmed for all these items",
            "Was the order placed for all following items",
        ]
        items.append(f"{random.choice(q_confirm)}: the {assortment[p2]}, the {assortment[p3]}, the {assortment[p5]}, the {assortment[p1]}, the {assortment[p4]}?\t{turn}\t0")

        q_confirm = [
            "Are all these items included in the list",
            "Do all these items appear list",
            "Are all of these items in the list",
            "Does the order include all these list",
        ]
        items.append(f"{random.choice(q_confirm)}: the {assortment[p1]}, the {assortment[p4]}, the {assortment[p2]}, the {assortment[p3]}?\t{turn}\t0")

        #print(items_to_story(items))
        stories.append(items_to_story(items))
    return stories



actions = [
    "place an order",
    "confirm an order",
    "cancel an order",
    "check order status",
    "request delivery details"
]


def generate_order_dialogue():
    dialogue = []
    customer = "User"
    seller = "Assistant"

    action = random.choice(actions[:2])  # чаще place/confirm
    #dialogue.append(f"{customer} wants to {action}.")
    dialogue.append(f"{customer}: Hello, I would like to {action}.")
    dialogue.append(f"{seller}: Sure, your request to {action} has been received.")

    for _ in range(random.randint(1, 2)):
        next_action = random.choice(actions[1:])
        dialogue.append(f"{customer}: I want to {next_action}.")
        dialogue.append(f"{seller}: Your request to {next_action} has been processed.")

    story = "".join([ f"{id+1} {item}\n" for id, item in enumerate(dialogue) ])

    print(story)
    #“Was John’s order confirmed?” “Yes.” or “No.”

    #“What actions were taken regarding Emma’s order?”
    #“Placed, confirmed, requested delivery details.”

    #“Was John’s order=.. confirmed?”“Yes.” или “No.”
    #“Was order=.. cancelled?”

    return dialogue


if __name__ == "__main__":

    samples = 1000

    if False:

        train_stories = generate_v2(samples)

        with open("datasets/qa21-shopping-dialogue_train.txt", "w", encoding="utf-8") as f:
            f.writelines(train_stories)

        test_stories = generate_v2(samples)

        with open("datasets/qa21-shopping-dialogue_test.txt", "w", encoding="utf-8") as f:
            f.writelines(test_stories)
    else:

        train_stories = generate_v3(samples)

        with open("datasets/qa22-shopping-items_train.txt", "w", encoding="utf-8") as f:
            f.writelines(train_stories)

        test_stories = generate_v3(samples)

        with open("datasets/qa22-shopping-items_test.txt", "w", encoding="utf-8") as f:
            f.writelines(test_stories)

    print(f"sampeles={samples}")
