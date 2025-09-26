
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from collections import deque


class Chatbot_gpt2:

    def __init__(self, system_prompt: str):
        model_dir = "gpt2-babi"
        self.system_prompt = system_prompt
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
        self.model = GPT2LMHeadModel.from_pretrained(model_dir)
        #check_special_tokens(self.tokenizer)


    def build_prompt(self, conversation_history, user_message):
        # Create prompt for model in format:
        """
        <|im_start|>system
        {system_message}<|im_end|>
        <|im_start|>user
        {user_message}<|im_end|>
        <|im_start|>assistant
        """
        prompt = f"<|im_start|>system\n{self.system_prompt}<|im_end|>\n"

        for role, content in conversation_history:
            if role == "user":
                prompt += f"<|im_start|>user\n{content}<|im_end|>\n"
            elif role == "assistant":
                prompt += f"<|im_start|>assistant\n{content}<|im_end|>\n"

        prompt += f"<|im_start|>user\n{user_message}<|im_end|>\n"
        prompt += f"<|im_start|>assistant\n"
        return prompt


    def generate_llm_response(self, prompt, max_new_tokens=100):
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
        assistant_reply = self.generate_llm_response(prompt)

        # Update history
        conversation_history.append(("user", user_message))
        conversation_history.append(("assistant", assistant_reply))
        # TODO: return real mood-level
        return assistant_reply, conversation_history


if __name__ == "__main__":

    conversation_history = deque(maxlen=4)

    chat = Chatbot_gpt2("You are helpful car driver assistant.")

    while True:
        user_message = input("User: ")

        if user_message.strip().lower() == "exit":
            break

        assistant_reply, conversation_history = chat.handle_user_message(conversation_history, user_message)

        print(f"Assistant: {assistant_reply}")
