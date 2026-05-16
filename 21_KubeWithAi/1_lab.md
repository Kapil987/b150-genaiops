## Kube and Infra Management with AI

### Pre-requisite
- install kind cluster
- install and configure amazon q cli

### create kind cluster
```bash
kind create cluster --config kind-config.yml
```

### create a deployment to create pod
```bash
kubectl apply -f nginx-deploy.yml
```

### verify pod
```bash
kubectl get po
```

### Observe the error in deployment
```bash
ubuntu@ip-172-31-19-109:~/demo$ kubectl get pods
NAME                                READY   STATUS         RESTARTS   AGE
nginx-deployment-5698676c9c-b8d6c   0/1     ErrImagePull   0          4s
nginx-deployment-5698676c9c-zjjgq   0/1     ErrImagePull   0          4s
ubuntu@ip-172-31-19-109:~/demo$
```

### Fix Errors using amazon q cli
#### Invoke/start amazon q cli
```bash
q # this will start q cli

/tools # this is to check tool permissons
```
#### Trusting tools
```bash
Tool              Permission
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔                                                                                                                                Built-in:
- execute_bash    * not trusted
- fs_read         * trust working directory
- fs_write        * not trusted
- introspect      * trusted
- report_issue    * trusted
- use_aws         * trust read-only commands


> /tools trust-all

All tools are now trusted (!). Amazon Q will execute tools without asking for confirmation.
Agents can sometimes do unexpected things so understand the risks.

Learn more at https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-chat-security.html#command-line-chat-trustall-safety
!> /tools


Tool              Permission
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔                                                                                                                                Built-in:
- execute_bash    * trusted
- fs_read         * trusted
- fs_write        * trusted
- introspect      * trusted
- report_issue    * trusted
- use_aws         * trusted

```


### Delete a deployment
```bash
kubectl delete -f nginx-deploy.yml
```

### Deleting a cluster
```bash
kkind get clusters
kind delete cluster --name clusterNAME
```
### Prompts
- can you fix my nginx pod and then show me kubectl get po status
- can you push a temporary file in bucket MYBUCKETNAME to check connectivity
- show me the status for all of my instances in us-east-1 region in table properly formated for linux terminal