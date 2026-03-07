
---

````markdown
# Module vs Package vs Library

## 1. Module
A **module** is a **single Python file (`.py`)** containing functions, classes, or variables.

Example

```text
math_utils.py
````

---

## 2. Package

A **package** is a **folder containing multiple modules** (usually with `__init__.py`).

Example

```text
data_processing/
├── __init__.py
├── cleaner.py
└── transformer.py
```

---

## 3. Library

A **library** is a **collection of related packages and modules** distributed together.

Example

```text
numpy/
├── __init__.py
├── linalg/
│   ├── __init__.py
│   └── solver.py
└── random/
    ├── __init__.py
    └── generator.py
```

---

## Visual Hierarchy

```text
Library
└── Package
    └── Module (.py file)
```

---

## Quick Summary

| Concept | Meaning                        |
| ------- | ------------------------------ |
| Module  | Single `.py` file              |
| Package | Folder of modules              |
| Library | Collection of packages/modules |

```

---
