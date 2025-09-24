
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


if __name__ == "__main__":

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

