# Local Git Setup

## Local setup

Go to your project directory:

```powershell
cd <your-project-folder>
```

Initialize Git:

```powershell
git init .
```

Create `main.py` and add a print statement:

```python
print("Hello from main.py")
```

Create a `.env` file:

```powershell
New-Item .env -ItemType File
```

Initialize the project with `uv` and create a virtual environment:

```powershell
uv init .
uv venv
```

Check Git status:

```powershell
git status
```

Create `.gitignore` and ignore `.env`:

```gitignore
.env
.venv/
__pycache__/
```

Check branches and rename the default branch to `main`:

```powershell
git branch -a
git branch -m main
git branch -a
```

Check status again. `.env` should not appear now:

```powershell
git status
```

Stage and commit your files:

```powershell
git add .
git status
git commit -m "chore: initialize local uv project"
```

View commit history:

```powershell
git log
git log --oneline
```

Install the VS Code extension `mhutchie.git-graph` to view commits visually.

Edit a file, then repeat `git add .`, `git commit -m "..."`, and `git log --oneline` to create and review a second commit.

## GitHub setup

Create a new repository on GitHub:

- Repository name: `<repo-name>`
- Description: `This repo is related to ...`
- Visibility: `Public` or `Private`

Check your current remotes:

```powershell
git remote -v
```

Add your GitHub SSH remote:

```powershell
git remote add origin git@github.com:<your-username>/<repo-name>.git
```

Generate an SSH key on your system:

```powershell
ssh-keygen
```

Add your public key to GitHub:

- GitHub SSH keys: <https://github.com/settings/keys>

Push your code:

```powershell
git push -u origin main
```

If push fails, the SSH key is usually not configured correctly yet.

After pushing, verify on GitHub that `.env` was not uploaded.

## Clone on another machine

Using HTTPS:

```powershell
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

Pull the latest changes:

```powershell
git pull
```

If this is a `uv` project:

```powershell
uv sync
```

Run the Flask app:

```powershell
flask --app main run --host=0.0.0.0
```

Open the page in a browser, then inspect:

- Developer Tools
- Network tab
- Response
- Headers

### Flask dir structure
my_flask_app/
├── app/                    # Main application package
│   ├── __init__.py        # Makes 'app' a package and initializes Flask
│   ├── routes.py          # URL declarations (your @app.route stuff)
│   ├── models.py          # Database structures
│   ├── static/            # CSS, JavaScript, and Images
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   └── templates/         # HTML files
│       ├── base.html
│       └── index.html
├── venv/                  # Python Virtual Environment
├── .gitignore             # Files to exclude from Git (like venv/)
├── config.py              # Secret keys and database URLs
├── main.py                # The entry point to start the app
└── requirements.txt       # List of dependencies (Flask, etc.)

---

### Comparison GET and POST request

| Feature | GET (The Postcard) | POST (The Sealed Package) |
| :--- | :--- | :--- |
| **Visibility** | Everything is in the URL. | Hidden inside the request body. |
| **Primary Goal** | **Get**ting information. | **Send**ing/Changing information. |
| **Security** | Low (Don't use for passwords!). | Higher (Better for sensitive data). |
| **History** | Can be bookmarked in a browser. | Cannot be bookmarked. |

**Pro-Tip for Students:** If you see a `?` in your browser's address bar followed by words (like `?user=john&id=123`), you are looking at a **GET** request in action!
