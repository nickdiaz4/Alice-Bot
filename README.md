---
tags:
- conversational
- not-for-all-audiences
pipeline_tag: text-generation
library_name: transformers
---

# Alice Bot
Alice is a Discord AI chatbot trained on Microsoft's DialoGPT small model. To interact with the model, visit my [Hugging Face model card] (https://huggingface.co/walletfullofones/DialoGPT-small-Alice). 

# Contents
## 

# Indiviudal use
If you would like to interact with the model in your own code, simply copy and paste the following block of code. 
```python
from huggingface_hub import InferenceClient

client = InferenceClient(
    "walletfullofones/DialoGPT-small-Alice",
    token="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # REPLACE THIS WITH YOUR OWN HUGGING FACE ACCESS TOKEN
)

while True:
    user_input = input("User: ")
    
    for message in client.chat_completion(
            messages=[{
                "role": "user",
                "content": user_input
            }],
            max_tokens=500,
            stream=True,
    ):
        print(message.choices[0].delta.content, end="")
    
    print()
```
