## 🛠️ Installation & Setup

1. **Clone the Repository**

```bash
git clone <repo-url>
cd <repo-name>

```

1.1 **Git sync**
```bash
git pull
```

2. **Initialize & Sync Environment**
We include `ipykernel` as a dev dependency so your notebooks work immediately.

```bash
uv init project_name
uv add --dev ipykernel
uv add groq openai python-dotenv
uv sync
```

### 2. VS Code Kernel Not Found (Windows)

If VS Code can't find the environment for Jupyter Notebooks:

```bash
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\activate.ps1
uv run python -m ipykernel install --user --name=venv --display-name "Python (myenv)"
uv run --active python -m ipykernel install --user --name=venv --display-name "Python (myenv)"
```

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

