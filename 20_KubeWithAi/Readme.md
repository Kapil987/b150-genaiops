# Amazon Q CLI Installation & Usage on Ubuntu

## 1. Install Required Packages

```bash
sudo apt update
sudo apt install -y unzip curl libfuse2
```

---

# 2. Download Amazon Q CLI

## Ubuntu/Linux x86_64

```bash
curl --proto '=https' --tlsv1.2 -sSf \
"https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux.zip" \
-o "q.zip"
```

---

# 3. Extract Files

```bash
unzip q.zip
```

---

# 4. Install Amazon Q CLI

```bash
cd q
./install.sh
```

If you face permission issues:

```bash
chmod +x install.sh
./install.sh
```

---

# 4.1 Login with AWS Builder ID
## Create Free AWS Builder ID

[AWS Builder ID](https://profile.aws.amazon.com/)

During installation:

```bash
✔ Do you want q to modify your shell config (you will have to manually do this otherwise)? · Yes
✔ Select login method · Use for Free with Builder ID
```

Then Amazon Q CLI will display:

```bash
Confirm the following code in the browser
Code: ABCD-XYZZ

Open this URL: https://view.awsapps.com/start/#/device?user_code=ABCD-XYZZ
▰▰▰▰▰▰▱ Logging in...
```

## Browser Authentication

* Open the provided URL
* Login using your AWS Builder ID
* Allow Kiro/Amazon Q access when prompted
* After successful authorization:

```bash
Device authorized
Logged in successfully
ubuntu@ip-172-31-19-109:~/q$
```



---

# 5. Verify Installation

```bash
q --version
```

---

# 6. Start Using Amazon Q

## Open Interactive Chat

```bash
q chat
```

---

# Practical Examples

## Terraform

```bash
q chat "Create Terraform for EKS cluster"
```

---

## Kubernetes Troubleshooting

```bash
q chat "Explain kubectl crashloopbackoff issue"
```

---

## Docker Optimization

```bash
q chat "Optimize this Dockerfile"
```

---

## AWS Queries

```bash
q chat "List EC2 instances in ap-south-1"
```

---

# Optional: Install AWS CLI

## Install AWS CLI

```bash
sudo apt install awscli -y
```

## Configure AWS CLI

```bash
aws configure
```

Once configured, Amazon Q can directly help manage AWS resources.

---

# Important Update

Amazon Q CLI is gradually transitioning internally toward Kiro branding, but the `q` command continues to work normally.

---
alias k='kubectl'
# Official Documentation

* [Amazon Q CLI Documentation](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html)
* [Linux Installation Guide](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-installing.html)
* [Amazon Q CLI GitHub Repository](https://github.com/aws/amazon-q-developer-cli)
* [AWS Builder Guide for Amazon Q CLI](https://builder.aws.com/content/2ulGwNwLFj5grS8hXJBMCN78Qwl/essential-guide-to-installing-amazon-q-developer-cli-on-linux)
