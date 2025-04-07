# README

## 动态追踪原理
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/8299a9ca33a70fb4ff37387be18a0b2c.png" width="80%"></p>


## linux系统动态追踪工具
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/ea0a557b76ea96275495ade94475e2b4.png" width="80%"></p>


### 查看可以进行跟踪的内核符号-kprobe

```
sudo bpftrace -l
```

### 查看可以进行跟踪的用户态符号-uprobe

```
nm /path-to-binary
```