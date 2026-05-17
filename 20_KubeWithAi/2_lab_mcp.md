
---

# Radar MCP to Amazon Q CLI
https://github.com/skyhook-io/radar/blob/main/docs/mcp.md
https://mcpservers.org/

## Pre-requisite
- aws account
- aws cli and aws configure cli with access and secret keys
- create a kind cluster on ec2
- install radar curl -fsSL https://get.radarhq.io | sh && kubectl radar
- kubectl radar --host 0.0.0.0
- for port forwarding use ssh -L 9280:localhost:9280 ubuntu@<EC2-PUBLIC-IP>
  
## Step 1 — Locate Amazon Q Config Directory

Usually:

```bash
cd ~/.aws/amazonq/
```

---

## Step 2 — Create MCP Config

Create file:

```bash id="hgnmtg"
mkdir -p ~/.aws/amazonq
nano ~/.aws/amazonq/mcp.json
```

Add:

```json
{
  "mcpServers": {
    "radar": {
      "type": "http",
      "url": "http://localhost:9280/mcp"
    }
  }
}
```

---

## Step 3 — Restart Amazon Q

```bash
q chat
```

OR restart terminal.

---

## Step 4 — Verify MCP Connected

Inside Q:

```bash
/tools
```

You should see Radar tools like:

* `get_dashboard`
* `get_resource`
* `get_pod_logs`
* `get_topology`


---

## Example Prompts

### Cluster Health

```text
Show Kubernetes cluster health
```

---

### Pod Logs

```text
Get logs for nginx pod
```

---

### Topology

```text
Show cluster topology
```

---

### Deployment Issues

```text
Why is my deployment failing?
```

---

## Important

Since Radar MCP is local:

```text
http://localhost:9280/mcp
```

Amazon Q CLI must run on SAME machine where Radar is running.

If using EC2:

* Run Q CLI on EC2 itself
  OR
* Use SSH tunnel.

---

## Your Radar Already Has MCP Enabled

Your logs confirm:

```bash
MCP server enabled at http://localhost:9280/mcp
```

