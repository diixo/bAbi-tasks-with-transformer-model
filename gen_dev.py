
from utils import items_to_story, items_to_turns
import random


workflow = {

    "State":
    {
        "JUST REGISTERED": [ "To Blocked", "To Suspended", "To Do" ],
        "TO DO": [ "To Blocked", "To Suspended", "To Implement", "To Under Verification", ],
        "IMPLEMENTATION": [ "To Blocked", "To Suspended", "To Under Verification", "To Test", "To Do", ],
        "IN SW TESTING": [ "To Blocked", "To Suspended", "To Integrate" ],
        "IN SYSTEM INTEGRATION": [ "To Blocked", "To Suspended", "To Verification" ],
        "UNDER VERIFICATION": [ "To Blocked", "To Suspended", "Fixes Needed", "Close ADMIN", ],
        "BLOCKED": [
            "Back To Do",
            "Back to Just Registered",
            "Back to Under Verification",
            "Back to SW Testing",
            "Back to System Integration",
            "Back to Implementation",
            ],
        "SUSPENDED": [
            "Back To Do",
            "Back to Implementation",
            "Back to Under Verification",
            "Back to Just Registered",
            "Back to SW Testing",
            "Back to System Integration"
            ],
        "CLOSED": [ "To Blocked", "Reopen", ],
    },
    "Transition":
    {
        "To Implement": "IMPLEMENTATION",
        "Fixes Needed": "IMPLEMENTATION",
        "Back to Implementation": "IMPLEMENTATION",
        "Back To Do": "TO DO",
        "To Under Verification": "UNDER VERIFICATION",
        "Back to Under Verification": "UNDER VERIFICATION",
        "To Just Registered": "JUST REGISTERED",
        "Create": "JUST REGISTERED",
        "Back to Just Registered": "JUST REGISTERED",
        "Reopen": "JUST REGISTERED",
        "Back to SW Testing": "IN SW TESTING",
        "Back to System Integration": "IN SYSTEM INTEGRATION",
        "To Integrate": "IN SYSTEM INTEGRATION",
        "To Test": "IN SW TESTING",
        "To Blocked": "BLOCKED",
        "To Suspended": "SUSPENDED",
        "To Verification": "UNDER VERIFICATION",
        "Close ADMIN": "CLOSED",
        "To Do": "TO DO",
    }
}


intent_examples = {
    "To Implement": ["I started implementation.", "Beginning to write code.", "Starting development work."],
    "To Test": [
        "The feature is ready for testing.",
        "I need to test the changes.",
        "Ready for QA.",
        "I have to finish the implementation for today",
        "Finish the implementation",
        "Prepare for testing",
        "Have to finish implementation",
        "Continue and finish implementation",
        ],
    "To Under Verification": ["Changes are under verification.", "I sent it for verification.", "Verifying the fix.", "verify fix"],
    "To Blocked": [
        "I'm blocked by missing data.",
        "Waiting for input from customer.",
        "Work is blocked.",
        "Need more information.",
        "implementation is blocked",
        "waiting additional information from customer",
        "waiting more information from customer",
        ],
    "To Suspended": ["Pausing work temporarily.", "The task is suspended until next sprint."],
    "To Do": ["I\'ll start this task soon.", "Planning to pick it up next."],
    "Close ADMIN": ["The issue is resolved and can be closed.", "Closing the ticket after verification."],
    "Reopen": ["Need to reopen the ticket.", "Reopening for rework."],
    "Fixes Needed": ["Verification failed, fixes required.", "Need to redo the implementation."],
    "Back To Do": ["Returning to To Do for reassignment.", "Putting task back in To Do for someone else."],
    "Back to Implementation": ["Resuming implementation after pause.", "Getting back to development."],
    "Back to Under Verification": ["Retrying verification again."],
    "Back to SW Testing": ["Retesting in QA environment."],
    "Back to System Integration": ["Going back to integration testing stage."],
}


# actions = { action: current_status }
actions = {
    "continue implementation": "IMPLEMENTATION",
    "continue analysis": "TO DO",
    "continue testing": "IN SW TESTING",
    "continue verification": "UNDER VERIFICATION",
    "finish implementation": "IMPLEMENTATION",
    "finish analysis": "TO DO",
    "finish testing": "IN SW TESTING",
    "finish verification": "UNDER VERIFICATION",
    "finish integration": "IN SYSTEM INTEGRATION",
    "continue integration": "IN SYSTEM INTEGRATION",
    }

target_states = {
    "TO DO": "IMPLEMENTATION",
    "IMPLEMENTATION": "IN SW TESTING",
    "IN SW TESTING": "IN SYSTEM INTEGRATION",
    "IN SYSTEM INTEGRATION": "UNDER VERIFICATION",
    "UNDER VERIFICATION": "CLOSED",
    }


def generate_story(story: list):
    max_steps = 7
    ticket_id = random.randint(99, 9999)

    #story = [f"1 Assistant: Ticket #{ticket_id} was just registered."]
    current_state = random.choice(list(workflow["State"].keys()))   # "JUST REGISTERED"
    current_state = random.choice(["JUST REGISTERED", "TO DO", "IMPLEMENTATION", "IN SW TESTING",])

    story.append("System: You are development Assistant.")
    story.append("Assistant: Hi, I am development Assistant.")

    asking = ["Hello", "Hi", "hello", "hi", "ok", "yes", "maybe", "Ok", "Yes", "Maybe", "continue", "Continue", "Let's go", "let's go"]
    story.append(f"User: {random.choice(asking)}")

    story.append("Assistant: Do you have any tickets assigned on you?")

    story.append(f"User: ticket {ticket_id}, in status: {current_state.lower()}")
    story.append(f"ticket {ticket_id} current status?\t{current_state}\t0")
    story.append(f"ticket {ticket_id} target status?\t{current_state}\t0")

    story.append("Assistant: What do you plan to do with it?")

    # action = random.choice(list(actions.keys()))
    # story.append(f"User: {action}")

    # current_state = actions[action]

    # story.append(f"current status of ticket {ticket_id}?\t{current_state}\t0")
    # story.append(f"target status of ticket {ticket_id}?\t{target_states[current_state]}\t0")


    for _ in range(max_steps):

        transitions = workflow["State"].get(current_state, [])
        if not transitions: break
        transition = random.choice(transitions)
        next_state = workflow["Transition"][transition]

        intent = random.choice(intent_examples.get(transition, [f"I will perform {transition}."]))
        
        story.append(f"User: {intent}")

        story.append(f"ticket {ticket_id} next status?\t{next_state}\t0")

        story.append(f"Assistant: Use transition \"{transition}\" → move ticket to \"{next_state}\".")
        current_state = next_state

    story.append(f"ticket {ticket_id} next status?\t{current_state}\t0")



def generate_story_short(story: list):

    ticket_id = random.randint(99, 9999)

    current_state = random.choice(list(workflow["State"].keys()))
    current_state = random.choice(["JUST REGISTERED", "TO DO", "IMPLEMENTATION", "IN SW TESTING",])

    story.append("System: You are development Assistant.")
    story.append("Assistant: Hi, I am development Assistant.")

    asking = ["Hello", "Hi", "hello", "hi", "ok", "yes", "maybe", "Ok", "Yes", "Maybe", "continue", "Continue", "Let's go", "let's go"]
    story.append(f"User: {random.choice(asking)}")

    story.append("Assistant: Do you have any tickets assigned on you?")

    story.append(f"User: ticket {ticket_id}")


    story.append("Assistant: What do you plan to do with it?")

    action = random.choice(list(actions.keys()))
    story.append(f"User: {action}")

    current_state = actions[action]

    story.append(f"current status of ticket {ticket_id}?\t{current_state}\t0")

    target_state = target_states[current_state]
    story.append(f"intent status of ticket {ticket_id}?\t{target_state}\t0")

    for transition in workflow["State"][current_state]:
        if workflow["Transition"][transition] == target_state:
            target_transition = transition

    story.append(f"intent transition of ticket {ticket_id}?\t\"{target_transition}\"\t0")

    story.append(f"What transition from \"{current_state}\" to \"{target_state}\"?\t\"{target_transition}\"\t0")
    story.append(f"Assistant: Use transition \"{target_transition}\" → move ticket to \"{target_state}\" when you finished.")


def generate_item(story: list):

    ticket_id = random.randint(99, 9999)

    #story = [f"1 Assistant: Ticket #{ticket_id} was just registered."]
    current_state = random.choice(list(workflow["State"].keys()))   # "JUST REGISTERED"
    current_state = random.choice(["JUST REGISTERED", "TO DO", "IMPLEMENTATION",])

    story.append("System: You are development Assistant.")
    story.append("Assistant: Hi, I am development Assistant.")

    asking = ["Hello", "Hi", "hello", "hi", "ok", "yes", "maybe", "Ok", "Yes", "Maybe", "continue", "Continue", "Let's go", "let's go"]
    story.append(f"User: {random.choice(asking)}")

    story.append("Assistant: Do you have tickets assigned on you?")

    story.append(f"User: ticket {ticket_id}")

    story.append("Assistant: What do you plan to do with it?")
    max_steps = 5

    for _ in range(max_steps):

        transitions = workflow["State"].get(current_state, [])
        if not transitions: break
        transition = random.choice(transitions)
        next_state = workflow["Transition"][transition]

        intent = random.choice(intent_examples.get(transition, [f"I will perform \"{transition}\"."]))
        
        story.append(f"User: {intent}")

        story.append(f"ticket {ticket_id} current status?\t{current_state}\t0")
        story.append(f"ticket {ticket_id} next status?\t{next_state}\t0")

        story.append(f"Assistant: Use transition \"{transition}\" → move ticket to \"{next_state}\".")
        current_state = next_state

    story.append(f"User: what current status?")
    story.append(f"Assistant: {current_state}")
    story.append(f"User: {random.choice(asking)}")
    story.append("Assistant: Do you have any tickets assigned on you?")


def generate_dev(samples: int) -> list:

    stories = []
    turn_stories = []

    question_per_story = 4
    story_count = int(samples / question_per_story)

    for _ in range(story_count):

        items = []

        generate_story_short(items)

        stories.append(items_to_story(items))

        turns = items_to_turns(items)
        turn_stories.append(items_to_story(turns))

    return stories, turn_stories


def generate_v2(samples: int) -> list:

    stories = []
    turn_stories = []

    question_per_story = 10
    story_count = int(samples / question_per_story)

    for _ in range(story_count):

        items = []

        items.append("System: You are development Assistant.")
        items.append("Assistant: Hi, I am development Assistant.")

        asking = ["ok", "yes", "maybe", "Ok", "Yes", "Maybe", "continue", "Continue", "Let's go", "let's go"]
        items.append(f"User: {random.choice(asking)}")

        items.append("Assistant: Do you have any assigned tickets on you?")

        if False:
            items.append("User: No")

            items.append("Assistant: You should ask your Line Manager to assign task on you, or create new one by yourself.")

            items.append("User: I created ticket SWT123")

        else:
            items.append("User: Yes")

            items.append("Assistant: What is ID of your ticket?")

            items.append("User: ticket SWT123")
        
        ###########################################################

        items.append("Assistant: what is status of ticket SWT123?")


if __name__ == "__main__":

    samples = 1000

    train_stories, train_turns = generate_dev(samples)

    with open("datasets/qa26-dev_train.txt", "w", encoding="utf-8") as f:
        f.writelines(train_stories)

    with open("datasets/qa27-dev-turns_train.txt", "w", encoding="utf-8") as f:
        f.writelines(train_turns)

    print(f"Train: sampeles={samples}, train_stories={len(train_stories)}, train_turns={len(train_turns)} ")


    test_stories, test_turns = generate_dev(samples)

    with open("datasets/qa26-dev_test.txt", "w", encoding="utf-8") as f:
        f.writelines(test_stories)

    with open("datasets/qa27-dev-turns_test.txt", "w", encoding="utf-8") as f:
        f.writelines(test_turns)

    print(f"Test: sampeles={samples}, test_stories={len(test_stories)}, test_turns={len(test_turns)} ")

