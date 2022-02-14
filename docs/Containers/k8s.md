# Kubernetes

## kubectl Cheats
Get containers (IDs) in a Pod:
    $ k describe pod/POD-NAME -n default

Watch events:
    $ k get events --watch

Run a container with no yaml:
    k run [-n NS] POD-NAME -i -t --rm --image=busybox --restart=Never -- /bin/sh

Run a deployment with no yaml:
    kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0

Delete a pod:
    k delete [-n NS] pod POD-NAME

Get mode pod info:
    k get pods nginx-deployment-6b474476c4-bsg92 -o json

Select a kubectl context:
    k config get-contexts
    k config use-context CONTEXT-NAME

Create a job on the fly from a cronjob:
    kubectl create job --from=cronjob/rclone rclone-test

Watch for k8s events:
```
$ kubectl get events --watch-only
```

List the containers in a pod:
```
$ kubectl get pods -n NAMESPACE pod/POD-NAME -o jsonpath='{.spec.containers[*].name}'
```

Restart a deployment:
```
$ kubectl -n NAMESPACE rollout restart deployment/DEPLOYMENT-NAME
```
or:
```
$ k scale -n NAMESPACE deployment DEPLOYMENT --replicas=0
deployment.apps/fargate-demo scaled

$ k scale -n NAMESPACE deployment DEPLOYMENT --replicas=1
deployment.apps/fargate-demo scaled
```

Get images ID and hash of a pod:
```
$ kubectl get pod -n NAMESPACE POD-NAME -o json | jq '.status.containerStatuses[] | { "image": .image, "imageID": .imageID }'
```

Run a privileged pod for debug purposes:
```
k debug -n NAMESPACE node/NODE-NAME -it --image=busybox
```

Select a pod using labels
Assuming you have a pod spec with:
```
spec
  metadata:
    labels:
      app: myapp
```
You can specify a pod using the kubectl flag `-l app=myapp`.
E.g.:
```
$ kubectl describe  pod -l app=myapp
$ kubectl logs -f -l app=myapp
```

Inspect a certificate from a secret:
```
k get secrets SECRET-NAME --template='{{index .data "tls.crt"}}' | base64 -d | openssl x509 -in - -text -noout
```
