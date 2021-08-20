# Kubernetes in Docker
An attempt at implementation of the application of Kubernetes in Docker. I am going to continue working on this, but I am making a formal document on my progress, 
where you can go to learn about the technology, and the like (in case anybody else wants to try their hand at this).

Windows Pro
-----
If you're using Windows, make sure you have this version of the OS. I found that on some insider builds of Home, Docker Desktop will still require Hyper-V containers,
a feature that is only availabe with Windows Pro or above. There is a workaround that I have documented on the Docker repository (https://github.com/sabary661990615/docker.github.io/blob/master/docker-for-windows/home-issue.md).

Bash Emulator
-----
Again, if you're using Windows, you will want to use a capable bash emulator. As we will see, kind is primarily designed for use with Linux and Mac, and although there are tutorials
for Windows, it it much more of a workaround and much less documented. You can use an Ubuntu shell (again, make sure you've turned on WSL) but I have found that it doesn't always work,
especially with git. Something like Cygwin will be more suitable - you will want to use this for everything moving forward.

Quickstart
-----
Once you have Docker working, make sure you can run the MLX quickstart before moving forward. This will at least give you an idea of what your local machine is capable
of, and if running on Docker Destop is viable at all for you. It will also allow you to troubleshoot your Docker set-up (if you're using Windows, make sure to have WSL enabled).

KIND
-----
There are multiple ways to install (https://kind.sigs.k8s.io/docs/user/quick-start/) this but if you're using Windows, I found using Chocolately via the PowerShell to be the easiest route.
Follow the quick start guide, and make sure you can run kind with the default image before moving forward. 

Kubeflow Pipelines
-----
Once you have kind running, you will want to test that you can use custom images and more with kind. Follow the guide at (https://www.kubeflow.org/docs/components/pipelines/installation/localcluster-deployment/)
you should be able to create a cluster using kind.


Into the Unknown
-----
This is as far as I was able to get, unfortunately. With the amount of time that it took me to learn the technology along with the many technical hurdles, a lot was out of my range.
Here's hoping I make a breakthrough going forward!
