
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
            #Customer: Perfect, I’ll place the order.
            #Seller: Thank you! I’ll send you the payment link now.
            items.append(f"User: {random.choice(approve)} I'll take it.")
            answer = "yes"
        else:
            items.append(f"User: No, {random.choice(waiting)}")
            answer = "no"

        items.append(f"{random.choice(question_intent)}\t{answer}\t0")

        story = "".join([ f"{id+1} {item}\n" for id, item in enumerate(items) ])
        stories.append(story)

    return stories


if __name__ == "__main__":

    samples = 2000
    question_per_story = 8
    stories = int(samples / question_per_story)
    print(f"sampeles={samples}, question_per_story={question_per_story}, stories={stories}")

    train_stories = generate_q8(stories)

    with open("datasets/babi-qa-shopping_train.txt", "w", encoding="utf-8") as f:
        f.writelines(train_stories)

