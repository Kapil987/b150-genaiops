
# GenAI-Ops (b150)

A streamlined guide for setting up a production-ready Generative AI operations environment using `uv`, AWS, and Groq.

---

## 🚀 Pre-requisites

### Accounts & Access

* **AWS Account**: [Sign up here](https://signin.aws.amazon.com/signup?request_type=register)
* **Groq Cloud**: [Get API Keys](https://console.groq.com/docs/overview)
* **GitHub**: [Create Account](https://github.com/signup)

### Local Tooling

* **AWS CLI**: [Install Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* **VS Code**: [Download](https://code.visualstudio.com/download)
* **uv**: [Installation](https://docs.astral.sh/uv/getting-started/installation/)
* **Git**: [Download](https://git-scm.com/install/)

---

## 🛠️ Installation & Setup

1. **Clone the Repository**

```bash
git clone <repo-url>
cd <repo-name>

```

2. **Initialize & Sync Environment**
We include `ipykernel` as a dev dependency so your notebooks work immediately.

```bash
uv init project_name
uv add openai groq
uv add --dev ipykernel
uv sync

```

3. **Configure Environment Variables**
Create a `.env` file in the root directory:

```ini
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
GROQ_API_KEY=your_groq_key

```

---

## 📂 Project Structure

Run these commands to set up the standard layout:

```bash
mkdir -p src/my_app notebooks tests docs
touch notebooks/01_initial.ipynb README.md
touch src/my_app/__init__.py src/my_app/main.py

```

### Final Directory Layout

```text
my-project/
├── .venv/               # Managed by uv
├── src/                 # Source code root
│   └── my_app/          # Production package code
│       ├── __init__.py
│       └── main.py      # Core logic
├── notebooks/           # Jupyter experiments (.ipynb)
├── tests/               # Automated test suite
├── pyproject.toml       # Project metadata & dependencies
└── uv.lock              # Deterministic lockfile
```

> **💡 Pro‑Tip: Making your code importable**
> To ensure `uv` correctly recognizes your code within the `src` layout and treats `my_app` as an installable package, add the following to `pyproject.toml`:
>
> ```toml
> [build-system]
> requires = ["hatchling"]
> build-backend = "hatchling.build"
>
> [tool.hatch.build.targets.wheel]
> packages = ["src/my_app"]
> ```

## 🔧 Troubleshooting & Cloud Drive Setup

### 1. Cloud Sync Errors (OneDrive / Google Drive)

If working inside a cloud-synced folder, `uv` may fail because these drives don't support "hardlinks."

**Option A: Fix for a single project**

```bash
uv cache clean
rmdir /s /q .venv
uv sync --link-mode=copy

```

**Option B: Global Fix (Recommended for Cloud Users)**

* **Windows (PowerShell)**:

```powershell
[Environment]::SetEnvironmentVariable("UV_LINK_MODE", "copy", "User")

```

* **Mac/Linux (Bash/Zsh)**:
Add `export UV_LINK_MODE=copy` to your `.bashrc` or `.zshrc`.

### 2. VS Code Kernel Not Found (Windows)

If VS Code can't find the environment for Jupyter Notebooks:

```bash
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\activate.ps1
uv run python -m ipykernel install --user --name=venv --display-name "Python (myenv)"

```

---


