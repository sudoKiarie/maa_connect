import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

class TinyLlamaChatbot:
    def __init__(self):
        """
        Initialize the TinyLlama model and tokenizer.
        """
        self.model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, torch_dtype=torch.bfloat16, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    @staticmethod
    def remove_redundant_steps(text) -> str:
        """
        Remove redundant lines from the generated response.
        """
        lines = text.split("\n")
        seen = set()
        return "\n".join([line for line in lines if line.strip() and line not in seen and not seen.add(line)])

    def format_conversation(self, question) -> str:
        """
        Format the conversation history for the model input.
        """
        messages = [
            {"role": "system", "content": "You are a helpful chatbot who helps with troubleshooting network issues."},
            {"role": "user", "content": question}
        ]

        conversation_history = ""
        for message in messages:
            conversation_history += f"<|{message['role']}|> {message['content']} </|{message['role']}|>\n"
        return conversation_history

    def generate_response(self, question) -> str:
        """
        Generate a response for the given question.
        """
        # Format the input conversation
        conversation_history = self.format_conversation(question)

        # Encode the prompt
        inputs = self.tokenizer(conversation_history, return_tensors="pt")

        # Generate a response
        outputs = self.model.generate(
            inputs["input_ids"], max_length=128, do_sample=True, temperature=0.6, top_k=30, top_p=0.8
        )

        # Decode and clean the output
        decoded_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = self.remove_redundant_steps(decoded_output)

        return response
