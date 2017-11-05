---
layout: post
title:  "Implementation of Virtual Router in User Space by Bypassing the Kernel using Snabb"
date:   2017-06-10 10:20:19 +0530
category: projects
---

This was the topic of my BE Project.

## Abstract
As network adapters get faster, the time between packets i.e. the time the kernel has to process each packet gets smaller. That does not leave a lot of time for kernel to figure out what to do with each packet. The kernel has traditionally not done a great job with this kind of network-intensive workload. This is due to the latency of multiple system calls involved while an application reads packets from the network interface. This has led to existence of a number of networking implementations that bypass the kernel's network stack entirely. We use Snabb which is one of many such implementations. Snabb allows us to build our own network design on top of the Snabb core, bypassing the kernel. Our virtual router is built on top of Snabb. The virtual router runs in user space and also bypasses the kernel entirely. This capability allows us to make fast and intelligent forwarding decisions in the virtual router. This is suitable for dedicated servers which have high network traffic and require fast packet forwarding.


## Links 
[Published paper](http://ijarcce.com/upload/2017/june-17/IJARCCE%2067.pdf){:target="_blank"}

[Project report](https://drive.google.com/file/d/0BzDiqW98EP5dLUZOeTB1WHktdWUwbmNudnUxazRmSjJNVE80/view?usp=sharing){:target="_blank"}

[Final Demonstration Slides](https://docs.google.com/presentation/d/1vEibUEoe_LRO_fN9uTP5lzyjItHd-6swrcsh0d7wTKU/edit?usp=sharing){:target="_blank"}