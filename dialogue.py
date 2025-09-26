
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from collections import deque


class Chatbot_gpt2:

    def __init__(self, system_prompt: str):
        model_dir = "gpt2-babi"
        self.system_prompt = system_prompt
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
        self.model = GPT2LMHeadModel.from_pretrained(model_dir)


    def build_prompt(self, conversation_history, user_message):
        # Create prompt for model in format:
        """
        System:
        {system_message}
        User:
        {user_message}
        Assistant:
        {response}
        """
        prompt = f"System:\n{self.system_prompt}\n"

        for role, content in conversation_history:
            if role == "user":
                prompt += f"User:\n{content}\n"
            elif role == "assistant":
                prompt += f"Assistant:\n{content}\n"

        prompt += f"User:\n{user_message}\n"
        prompt += f"Assistant:\n"
        return prompt


    def generate_response(self, prompt, max_new_tokens=100):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.8,
            pad_token_id=self.tokenizer.eos_token_id
        )
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
        marker = "<|im_start|> assistant"
        if marker in text:
            text = text.split(marker)[-1].strip()
            text = text.split("<|im_end|>")[0].strip()
        return text


    def handle_user_message(self, conversation_history, user_message):
        # Build prompt
        prompt = self.build_prompt(conversation_history, user_message)

        # LLM response
        assistant_reply = self.generate_response(prompt)

        # Update history
        conversation_history.append(("user", user_message))
        conversation_history.append(("assistant", assistant_reply))
        # TODO: return real mood-level
        return assistant_reply, conversation_history


if __name__ == "__main__":

    conversation_history = deque(maxlen=4)

    chat = Chatbot_gpt2("You are online shopping Assistant.")

    while True:
        user_message = input("User: ")

        if user_message.strip().lower() == "exit":
            break

        assistant_reply, conversation_history = chat.handle_user_message(conversation_history, user_message)

        print(f"Assistant: {assistant_reply}")
