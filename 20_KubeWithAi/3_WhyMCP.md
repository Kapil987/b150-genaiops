## What is MCP ?

MCP = Model Context Protocol

It is a standard way for AI models to communicate with:

* Tools
* APIs
* Databases
* Files
* IDEs
* Kubernetes
* GitHub
* Slack
* Cloud systems

Think of it like:

> USB-C for AI tools

Instead of custom integration for every AI + tool combination.

---

## Without MCP

Every AI integration becomes custom.

Example:

| AI Model            | Tool | Need Custom Code? |
| ------------------- | ---- | ----------------- |
| Claude → Kubernetes | Yes  |                   |
| OpenAI → Kubernetes | Yes  |                   |
| Gemini → Kubernetes | Yes  |                   |
| Claude → GitHub     | Yes  |                   |

This becomes:

```text
N Models × M Tools integrations
```

Huge maintenance overhead.

---

## With MCP

All tools expose a standard MCP server.

Now:

```text
Any MCP-compatible AI ↔ Any MCP-compatible Tool
```

No custom integration each time.

---

# Practical Example

## Without MCP

Your AI agent wants to:

* Read Kubernetes pods
* Query Prometheus
* Create Jira ticket
* Access GitHub PR

You must manually code:

* APIs
* Authentication
* Tool schemas
* JSON formats
* Error handling

for every LLM separately.

---

## With MCP

You simply connect MCP servers:

| MCP Server     | Capability         |
| -------------- | ------------------ |
| Kubernetes MCP | Cluster operations |
| GitHub MCP     | Repo access        |
| Prometheus MCP | Metrics            |
| Filesystem MCP | Local files        |

AI automatically discovers tools and uses them.

---

# Why Radar Has MCP

Your Radar logs show:

```text
MCP server enabled at http://localhost:9280/mcp
```

Meaning Radar exposes Kubernetes cluster context via MCP.

So AI tools can:

* Inspect cluster
* Read workloads
* Analyze failures
* Query logs
* Recommend fixes

directly through standardized protocol.

---

# If You Disable MCP

Using:

```bash
kubectl radar --no-mcp
```

Radar UI still works.

But AI integrations stop working.

You lose:

* AI agent connectivity
* External AI tool access
* Standardized tool calling
* Agent interoperability

Only manual UI remains.

---

# Real DevOps Impact

## Without MCP

You build:

```text
Custom LangChain tools
Custom APIs
Custom wrappers
Custom auth
Custom schemas
```

for every project.

---

## With MCP

You reuse standard servers.

Example:

* Cursor
* Claude Desktop
* OpenAI Agents
* LangGraph
* VSCode AI
* Radar

can all consume same MCP server.

Huge reduction in engineering effort.

---

# MCP vs Traditional API

| Feature                | Traditional API | MCP       |
| ---------------------- | --------------- | --------- |
| Human-centric          | Mostly          | No        |
| AI-native              | No              | Yes       |
| Tool discovery         | Manual          | Automatic |
| Schema standardization | Varies          | Standard  |
| Agent interoperability | Poor            | Strong    |
| Context aware          | Limited         | Yes       |

---

# MCP vs RAG

| MCP               | RAG                 |
| ----------------- | ------------------- |
| Performs actions  | Retrieves knowledge |
| Dynamic tools     | Static documents    |
| Can execute       | Mostly read-only    |
| Real-time systems | Indexed data        |

You often use BOTH together.

---

# Important Security Concern

MCP is powerful but currently has security risks:

* Prompt injection
* Tool poisoning
* Remote code execution risks
* Over-permissioned agents

So production MCP servers need:

* Sandboxing
* RBAC
* Tool whitelisting
* Authentication
* Network isolation


[1]: https://www.anthropic.com/news/model-context-protocol "Introducing the Model Context Protocol"
[2]: https://www.backslash.security/blog/what-is-mcp-model-context-protocol "What is MCP? The Universal Connector for AI Explained"
[3]: https://cloud.google.com/discover/what-is-model-context-protocol "What is Model Context Protocol (MCP)? A guide"
[4]: https://www.tomshardware.com/tech-industry/artificial-intelligence/anthropics-model-context-protocol-has-critical-security-flaw-exposed "Anthropic's Model Context Protocol includes a critical remote code execution vulnerability - newly discovered exploit puts 200,000 AI servers at risk"
