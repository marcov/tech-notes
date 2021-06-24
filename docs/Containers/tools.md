# Container Tools
This is a list of good to know open source tools for interacting with container
images and registries:

- skopeo: interact with local and remote container images
- umoci: create and manipulate container images
- reg: registry command line client

These tools come handy in the common use cases described here.

## Unpacking and Modifying Container Images
You can modify a container image without the need to write a Dockerfile and then
run docker build. Here are the steps involved to change the rootfs content of an
existing container image.

## Retrieve a Container Image
skopeo is used to copy container images from a source to a destination.
For example the source/destination (a.k.a. transport) can be:

docker:// : an upstream container registry
docker-daemon : the local Docker images storage
dir : a local directory
In this example, the image is hosted by the docker.io registry:

```
$ skopeo copy docker://docker.io/alpine:latest oci:alpine:latest
```
## Unpack a Container Image rootfs
umoci allows to pack & unpack a container image rootfs, without the need to start
a container (mind the sudo):

```
$ sudo umoci unpack --image alpine:latest alpine-bundle
```
## Modify a Container Image rootfs
You can now do any change inside the rootfs folder of the unpacked bundle, e.g.:

```
$ sudo chroot alpine-bundle/rootfs /sbin/apk add vim
```
## Pack a rootfs into a Container Image
```
$ sudo umoci repack --image alpine:custom alpine-bundle
```
## Copy a Container Image to the Docker Storage
Just use the skopeo transport docker-daemon :

```
$ sudo skopeo copy oci:alpine:custom docker-daemon:alpine:custom
```

## Now you can just start a container in Docker using this new image:

```
$ docker run -it --rm alpine:custom vim --version
VIM - Vi IMproved 8.2 (2019 Dec 12, compiled May 15 2020 18:14:07)
```

## Listing all Repositories (a.k.a. Images) of a Container Registry
The reg tool can be used to interact with a Container Registry, e.g. listing all
the container images.

```
$ reg ls --insecure registry.ec2.dev:5000
```

>
> NOTE: listing container images & tags may not be possible, if it's blocked by
> the registry configuration.
>
