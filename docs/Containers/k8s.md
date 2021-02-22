# Kubernetes

## kubectl Cheats
Get containers (IDs) in a Pod:
    $ k describe pod/POD-NAME -n default

Watch events:
    $ k get events --watch

Run a container with no yaml:
    k run [-n NS] POD-NAME -i -t --rm --image=busybox --restart=Never -- /bin/sh

Delete a pod:
    k delete [-n NS] pod POD-NAME

Get mode pod info:
    k get pods nginx-deployment-6b474476c4-bsg92 -o json

Select a kubectl context:
    k config get-contexts
    k config use-context CONTEXT-NAME
