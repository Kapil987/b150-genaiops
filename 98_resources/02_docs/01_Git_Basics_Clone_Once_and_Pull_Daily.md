
---

# Git Basics: Clone Once and Pull Daily

## 1. Clone the Repository (One Time Setup)

Use `git clone` to download a copy of a remote repository to your local machine.

```bash
git clone <repository-url>
```

Example:

```bash
git clone https://github.com/Kapil987/b150-genaiops.git
```

### What Happens

* Creates a folder with the repository name.
* Downloads all files and history.
* Connects your local repo to the remote repository called **origin**. ([GitHub Docs][1])

Example:

```bash
git clone https://github.com/Kapil987/b150-genaiops.git
cd b150-genaiops
```

---

# 2. Daily Workflow: Pull Latest Changes

Every day before working, run:

```bash
git pull
```

### What `git pull` Does

* Downloads new commits from the remote repository.
* Updates your local files to match the latest version. 

Meaning:

1. Fetch new changes from the server.
2. Merge them into your local branch. ([Git][3])

---

# Simple Daily Routine

```bash
cd project
git pull
```

That’s it.

---

# Visual Workflow

```
Remote Repository (GitHub / GitLab)
            ↓
      git clone (once)
            ↓
      Local Repository
            ↓
        git pull
            ↓
     Stay updated daily
```

---

# Quick Summary

| Task                           | Command                |
| ------------------------------ | ---------------------- |
| Download repository first time | `git clone <repo-url>` |
| Go inside repository           | `cd repo-name`         |
| Update code daily              | `git pull`             |

---
