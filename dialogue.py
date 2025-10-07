
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from collections import deque


class Dialogue_gpt2:

    def __init__(self, system_prompt: str):
        model_dir = "gpt2-babi"
        self.system_prompt = system_prompt
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
        self.model = GPT2LMHeadModel.from_pretrained(model_dir)

        self.conversation_history = deque(maxlen=512)


    def build_prompt(self, user_message):
        # Create prompt for model in format:
        """
        System:
        {system_message}
        User:
        {user_message}
        Assistant:
        {response}
        """
        prompt = ""

        for role, content in self.conversation_history:
            if role == "user":
                prompt += f"User:\n{content}\n"
            elif role == "assistant":
                prompt += f"Assistant:\n{content}\n"

        if user_message:
            prompt += f"User:\n{user_message}\n"
        prompt += f"Assistant:\n"
        return prompt


    def generate_response(self, prompt, max_new_tokens=100):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=self.tokenizer.eos_token_id
        )[0]
        text = self.tokenizer.decode(outputs, skip_special_tokens=True)
        marker = "Assistant:"
        if marker in text:
            text = text.split(marker)[-1].strip()
        return text


    def handle_user_message(self, user_message=None):

        system = f"System:\n{self.system_prompt}\n"

        # Build prompt
        prompt = self.build_prompt(user_message)

        # create response
        assistant_reply = self.generate_response(system + prompt)

        # Update history by pair: user+prompt.
        if user_message:
            self.conversation_history.append(("User", user_message))
        else: # init, appand prompt as welcole-message
            assistant_reply = prompt + assistant_reply

        self.conversation_history.append(("Assistant", assistant_reply))
        return assistant_reply


    def get_history(self):
        return [
            { "role": role, "utterance": msg.replace("\n", " ").removeprefix(f"{role}: ").strip() }
            for role, msg in self.conversation_history
        ]


if __name__ == "__main__":

    chat = Dialogue_gpt2("You are developer Assistant.")
    start_prompt = chat.handle_user_message()
    
    print(f"{80*'-'}\n{start_prompt}")

    while True:
        user_message = input("User: ")

        if user_message.strip().lower() == "exit":
            break

        assistant_reply = chat.handle_user_message(user_message)

        print(f"Assistant: {assistant_reply}")
