
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
    "To Test": ["The feature is ready for testing.", "I need to test the changes.", "Ready for QA."],
    "To Under Verification": ["Changes are under verification.", "I sent it for verification.", "Verifying the fix."],
    "To Blocked": ["I'm blocked by missing data.", "Waiting for input from customer.", "Work is blocked.", "Need more information."],
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

def generate_story():
    max_steps = 5
    ticket_id = random.randint(999, 999999)

    current_state = random.choice(list(workflow["State"].keys()))   # "JUST REGISTERED"
    #story = [f"1 Assistant: Ticket #{ticket_id} was just registered."]
    story = []

    story.append("0 System: You are development Assistant.")
    story.append("0 Assistant: Hi, I am development Assistant.")

    asking = ["ok", "yes", "maybe", "Ok", "Yes", "Maybe", "continue", "Continue", "Let's go", "let's go"]
    story.append(f"1 User: {random.choice(asking)}")

    story.append("2 Assistant: Do you have any assigned tickets on you?")

    story.append(f"3 User: ticket #{ticket_id}, in state={current_state}")

    story.append(f"4 Assistant: What do you plan to do with it?")

    step = 5

    for _ in range(max_steps):
        transitions = workflow["State"].get(current_state, [])
        if not transitions: break
        transition = random.choice(transitions)
        next_state = workflow["Transition"][transition]

        intent = random.choice(intent_examples.get(transition, [f"I perform {transition}."]))
        
        story.append(f"{step} Developer: {intent}"); step += 1
        story.append(f"{step} Assistant: Use transition \"{transition}\" → move ticket to \"{next_state}\"."); step += 1
        current_state = next_state

    story.append(f"\nQ: What is the current state of ticket #{ticket_id}?")
    story.append(f"A: {current_state}")
    return "\n".join(story)


States = [k for k, v in workflow["State"].items()]
Transitions = [k for k, v in workflow["Transition"].items()]


def generate_v1(samples: int) -> list:

    stories = []
    turn_stories = []

    question_per_story = 10
    story_count = int(samples / question_per_story)

    for _ in range(story_count):

        items = []

        items.append("System: You are development Assistant.")
        items.append("Assistant: Hi, I am development Assistant.")

        for state in States:
            items.append(f"User: \"{state}\". What does it means?")

            transitions = workflow["State"][state]
            transitions_txt = ", ".join(["\"" + t + "\"" for t in transitions])
            items.append(f"Assistant: {state} is ticket status from project workflow. Applicable transition actions to change current status: {transitions_txt}.")

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

    # print(States)

    # print(Transitions)

    # items, stories = generate_v1(1000)

    for i in range(1, 3):
        print(generate_story())
        print("\n" + "-"*80 + "\n")