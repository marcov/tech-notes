# Kubernetes

## kubectl Cheats
Get containers (IDs) in a Pod:
    $ k describe pod/POD-NAME -n default

Watch events:
    $ k get events --watch

Run a container with no yaml:
    k run -i -t busybox --image=busybox --restart=Never

Get mode pod info:
    k get pods nginx-deployment-6b474476c4-bsg92 -o json
