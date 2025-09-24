
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

assortment = ["T-shirt", "dress", "sweater", "jacket", "skirt", "pants", "jeans", "bodice",]

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


def generate_q8(story_count: int) -> list:

    stories = []

    for _ in range(story_count):

        items = []

        on_sale = [assortment[0], assortment[1], assortment[2], assortment[3]]
        commodity = random.choice(on_sale)

        items.append(f"System: You are online shopping {random.choice(roles)}")

        items.append(f"User: {random.choice(hi_user)} {random.choice(intents)} the {commodity}, {random.choice(sizes)}. Is it available?")

        items.append(f"Assistant: API:action request={commodity}")

        items.append(f"What API:action?\trequest\t0")
        items.append(f"What API:action request for?\t{commodity}\t0")

        amount = random.randint(1, 20)
        items.append(f"API:action request {commodity} amount={amount}")

        items.append(f"How many {commodity}?\t{amount}\t0")

        items.append(f"User: Is {commodity} available in stock?\t{'yes'}\t0")

        items.append(f"Assistant: Yes, it's in stock")

        items.append(f"User: {random.choice(question_price)}")

        items.append(f"Assistant: API:action price={commodity}")
        price = random.randint(10, 159)
        items.append(f"API:action price {commodity}={price}")

        items.append(f"What API:action?\tprice\t0")
        items.append(f"What API:action price for?\t{commodity}\t0")
        items.append(f"What API:action price?\t{price}\t0")

        items.append(f"Assistant: ${price}")

        items.append(f"User: {random.choice(approve)} How long does delivery take?")
        items.append("Assistant: Standard shipping takes 3-5 business days.")

        choice = random.randint(0, 1)
        if choice > 0:
            #Customer: Perfect, I'll place the order.
            #Seller: Thank you! I'll send you the payment link now.
            #"Was an order placed?"
            items.append(f"User: {random.choice(approve)} I'll take it.")
            answer = "yes"
        else:
            items.append(f"User: No, {random.choice(waiting)}")
            answer = "no"

        items.append(f"{random.choice(question_intent)}\t{answer}\t0")

        story = "".join([ f"{id+1} {item}\n" for id, item in enumerate(items) ])
        stories.append(story)
    return stories


def generate_v2(story_count: int) -> list:
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
            #"Was an order placed?"
            #items.append(f"User: {random.choice(approve)} I'll take it.")
            answer = "yes"
        else:
            items.append(f"User: No, {random.choice(waiting)}")
            answer = "no"

        items.append(f"Will an order be placed?\t{answer}\t0")
        items.append(f"{random.choice(question_intent)}\t{answer}\t0")

        story = "".join([ f"{id+1} {item}\n" for id, item in enumerate(items) ])
        stories.append(story)
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
    question_per_story = 5
    stories = int(samples / question_per_story)
    print(f"sampeles={samples}, question_per_story={question_per_story}, stories={stories}")

    train_stories = generate_v2(200)

    with open("datasets/babi-qa-shopping_train.txt", "w", encoding="utf-8") as f:
        f.writelines(train_stories)

    test_stories = generate_v2(200)

    with open("datasets/babi-qa-shopping_test.txt", "w", encoding="utf-8") as f:
        f.writelines(test_stories)
