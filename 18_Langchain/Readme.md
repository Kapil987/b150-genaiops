#### Same code, just change the provider
```python
from litellm import completion

response = completion(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

print(response.choices[0].message.content)
```
#### Fallback
```python
from litellm import completion

models = [
    "openai/gpt-4o",
    "anthropic/claude-sonnet-4"
]

for model in models:
    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": "Summarize logs"}]
        )
        print("Success:", model)
        print(response.choices[0].message.content)
        break
    except Exception:
        print("Failed:", model)
```

