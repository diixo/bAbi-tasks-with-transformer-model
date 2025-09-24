
import random
import json


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

question_price = ["How much?", "Whats is the price?", "How much it cost?", "What price?"]

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


def generate(story_count: int) -> list:

    stories = []

    for id in range(story_count):

        items = []

        on_sale = [assortment[0], assortment[1], assortment[2], assortment[3]]
        commodity = random.choice(on_sale)

        items.append(f"System: You are an online shopping {random.choice(roles)}")

        items.append(f"User: {random.choice(hi_user)} {random.choice(intents)} the {commodity}, {random.choice(sizes)}. Is it available?")

        items.append(f"Assistant: API:action request={commodity}")

        items.append(f"What API:action?\trequest\t0")
        items.append(f"What API:action request for?\t{commodity}\t0")

        amount = random.randint(1, 20)
        items.append(f"API:request {commodity} amount={amount}")

        items.append(f"How many {commodity}?\t{amount}\t{len(items)}\t0")

        items.append(f"User: Is {commodity} available in stock?\t{'yes'}\t0")

        items.append(f"Assistant: Yes, it's in stock")

        items.append(f"User: {random.choice(approve)} {random.choice(question_price)}")

        items.append(f"Assistant: API:action price={commodity}")
        price = random.randint(10, 129)
        items.append(f"Assistant: API:price {commodity}={price}")

        items.append(f"What API:action?\tprice\t0")
        items.append(f"What API:action price for?\t{commodity}\t0")
        items.append(f"What API:action price?\t{commodity}\t0")

        items.append(f"Assistant: ${price}")

        story = "".join([ f"{id+1} {item}\n" for id, item in enumerate(items) ])
        stories.append(story)

        #print(story)
    return stories


if __name__ == "__main__":

    stories = generate(2)

    with open("datasets/babi-shopping.txt", "w", encoding="utf-8") as f:
        for story in stories:
            f.write(story)
