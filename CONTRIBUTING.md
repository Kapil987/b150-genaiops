
---

# 📝 The Ultimate Commit Message Cheatsheet

## 🏗️ The Structure

```text
<type>(<optional-scope>): <description>

[optional body]

[optional footer(s)]

```

---

## 🚀 The "Big Org" Standard (Conventional Commits)

| Type | Intent | Example |
| --- | --- | --- |
| **`feat`** | A new feature | `feat(api): add jwt rotation logic` |
| **`fix`** | A bug fix | `fix(ui): prevent double-click on submit button` |
| **`docs`** | Documentation only | `docs: updated readme and other related resouces` |
| **`style`** | Code style (semi-colons, spacing) | `style: run prettier on auth controller` |
| **`refactor`** | Neither fix nor feature | `refactor: extract validation to middleware` |
| **`perf`** | Performance improvements | `perf: cache expensive database lookups` |
| **`test`** | Adding/fixing tests | `test: add integration tests for checkout flow` |
| **`build`** | Build system / dependencies | `build: upgrade node to v20.10` |
| **`ci`** | CI config (GitHub Actions, etc.) | `ci: add sonarcloud scanning to pipeline` |
| **`chore`** | Maintenance (no src/test change) | `chore: update .gitignore for macos files` |

---

## ✨ Modern "Gitmoji" Variants

*Common in modern startups and high-velocity frontend teams.*

* ✨ **`feat`**: New features
* 🐛 **`fix`**: Bug fixes
* 📝 **`docs`**: Documentation
* 🎨 **`style`**: UI/UX styling changes
* ⚡️ **`perf`**: Performance
* ♻️ **`refactor`**: Refactoring
* 🔒️ **`security`**: Security patches
* 🚑️ **`hotfix`**: Critical production fix

---

## 🚩 Handling Breaking Changes

In large organizations, breaking an API is a big deal. You must signal this by adding a `!` after the type or including `BREAKING CHANGE:` in the footer.

**Example:**

```text
feat(api)!: remove support for legacy XML format

BREAKING CHANGE: The /v1/data endpoint no longer accepts XML. 
Clients must migrate to JSON.

```

---

## 💡 Top 3 Pro-Rules

1. **Imperative Mood:** Use "add" instead of "added." (e.g., `feat: add` ✅ vs `feat: added` ❌). Think of it as giving a command to the codebase.
2. **The 50/72 Rule:** Keep the subject line under **50 characters**. If you need more detail, add a blank line and write the body at **72 characters** per line.
3. **Atomic Commits:** One commit = One task. Don't bundle a `fix` and a `feat` together. It makes "reverting" a nightmare if something breaks.

---
