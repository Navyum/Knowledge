---
title: systemtap笔记
date: 2025-04-17 18:27:34
author: Navyum
tags: 
 - systemtap 语法
categories: 
 - 笔记
---

## 笔记
* SystemTap的语法基础跟C语言类似，这里只记录存在差异的点和systemtap特有的语法
* SystemTap的语言是`强类型、无声明的过程式语言`，受dtrace和awk的启发

----
### 一、命令行参数
以下列举几个常用的参数

#### -x PID
-x用于传递PID参数给systemtap脚本，程序内部可以通过内置函数`target()`获取到
e.g.：`target() == pid()`

#### -T seconds
-T用于设置脚本执行时间， seconds秒之后退出

#### -L
列举出二进制文件对应的函数在哪里（所在文件和行数）。
<span style="color: rgb(255, 41, 65);">注意：二进制文件必须有调试信息</span>
e.g.：`stap -L 'process("/usr/local/openresty/nginx/sbin/nginx").function("*")'`

#### -G VAR=VAL
设置全局变量VAR的值为VAL，并传入stp脚本

#### -I Tapset_DIR
添加tapset扩展，例如官方扩展、nginx tapset
注意：添加扩展后，在相应的脚本中还需要引入
e.g.
```stp
# stap++ -I ./tapset -x 4031 ngx-sync-get.stp

@use nginx.request
probe process("x").function("f"){
...

}
...

```

----
### 二、systemtap脚本分类
* 探测脚本
* tapset脚本（类似于库的概念）

----
### systemtap主要外层结构
* probes 探测
* function 函数

----
### 三、探测事件定义：
```stp
probe event { 
  STMT 
}
```
即：探测事件 + 探测声明

e.g.
* *probe kernel.function("tcp*"){ ... }*
* *probe process("nginx").function("ngx_*"){ ... }*

#### 探测事件分类：
* 按照事件类型分类：
    * 同步事件：程序执行到特定代码位置时，触发同步事件（参考断点）
        * 与代码相关的都是同步事件

    * 异步事件：与程序代码、位置无关，通过定时器、计数器触发（代码无关）,num表示执行的顺序权重
        * begin(num) 在脚本开始执行
        * end(num) 在脚本结束执行，发生错误不会执行
        * timer(tm) 定义定期触发的探测点
        * never 用不执行
        * error(num) 在脚本发生错误时执行
* 按照探测点功能分类：
    * 内核事件：*kernel.function(PATTERN)*
    * 内核模块事件：*module(MODULE).function(PATTERN)*
    * 系统调用：*syscall*
    * 用户事件：*process(PATH).function(PATTERN)*

### 四、探测点

#### PATTERN 语法
`函数名[@文件名][:行号]`
e.g.：`ngx_http_writer@src/http/ngx_http_request.c:2786`
注意：函数名支持使用通配符*的写法

#### function、statement区别
探测事件除了用`function`，还可以使用`statement`
*process(PATH).statement(PATTERN)*
statement用来在精确的位置放置一个探测点，暴露在该位置可见的局部变量。所以需要指定文件名和对应行号。
一般用来观察变量的多次变化情况

#### 事件调用时机
在不同的时机定义探测点，例如函数调用、函数返回：
* call
* return

e.g：
```
probe kernel.function("*@net/socket.c").call {
  printf ("%s -> %s\n", thread_indent(1), probefunc())
}
probe kernel.function("*@net/socket.c").return {
  printf ("%s <- %s\n", thread_indent(-1), probefunc())
}
```

#### 用户空间探测
用户空间内定义不同的时机的探测
* 当用户程序函数探测：*process(PATH).function(PATTERN)*
* 当用户程序进程创建：*process(PATH).begin*
* 当用户程序进程销毁：*process(PATH).end*
* 当用户程序线程创建：*process(PATH).thread.begin*
* 当用户程序线程销毁：*process(PATH).thread.end*
* 当用户程序发生系统调用：process(PATH).syscall
* 当用户程序系统调用返回：process(PATH).syscall.return

### 五、探测点的STMT

#### 脚本变量
* 使用*global*关键字定义全局变量
* 变量无需申明类型；在printf时，需要指定类型

##### 目标变量
* 在待探测程序的源码中，该位置可见的变量值
* 如果目标变量是局部变量，可以`$varname`的方式获取
* 如果目标变量是全局变量，可以通过`@var("varname@src/file.c")`或者`@var("varname", "/path/to/exe/or/lib")`方式获取

##### 目标变量美化
* 特殊的变量
    * `$$vars`：探针点作用域内的每个变量（局部变量 + 函数参数）
    * `$$locals`：探针点作用域内的局部变量
    * `$$vars`：探针点作用域内的函数参数
    * `$$vars`：探针点的返回值，仅当探针存在返回值时可用
* `$`后缀的使用
    * `$`后缀：  美化非结构体指针字段，例如打印指针指向的常量值
    * `$$`后缀： 美化结构体中的字段，解析结构体中的字段
    * 注意事项：`$$`后缀受最大字符串大小的限制，容易被截断（256/512字节）。可以使用`MAXSTRINGLEN`修改
* 结构体成员
    * 使用 -> 操作符获取 
    * e.g. `printf("%s\n", $file->f_pos_lock$`

##### @cast 目标变量类型转换
* 使用时机：
    * 目标变量是 void 指针
    * tapset中函数的参数使用long类型，来代替有类型的指针
* e.g. 
  ```
  @cast(task, “taskstruct”, “kernel<linux/sched.h>”)->tgid
  ```

##### @defined 检查目标变量的可用性
* 程序源码随着演进，可用的目标变量可能会发生变化
* 通过@defined 加三目运算，选择合适的可用变量
* e.g.
  ```
    write_access = (@defined($flags) ? $flags & FAULT_FLAG_WRITE : $write)
  ```

#### 关联数组
* 作用：存储统计信息
* 关联数组是一组唯一的键，数组中的每个键都有一个与之关联的值。即dict字典。
* 最多可以指定九个索引表达式
* <span style="color: rgb(255, 41, 65);">注意：所有关联数组都必须声明为全局变量</span>
* e.g.
  ```
  device[pid(),execname(),uid(),ppid(),"W"] = devname  # 对应C语言的数组，实际是获取 device[pid()][execname()][uid()][ppid()]["W"]
  ```

##### 遍历数组
* 定义：
  ```
  foreach (element in array_name)    # 注意：不需要花括号 {}
    statement
  ```

* 正序、逆序遍历：`foreach (element in array_name+)`、`foreach (element in array_name-)`
* 限定遍历的元素数量：`foreach (element in array_name+ limit 2)`

##### 删除数组元素
`delete array_name[element]`、`delete array_name`

##### 数组统计聚合
* 添加统计聚合值 array_name[element] <<< value：`reads[execname()] <<< $count` （注意：与直接赋值的区别在于，<<< 实际是将每次的结果单独存到关联数组对应的键中）
* count：返回每个唯一键存储的值的数量 `@count(reads[execname()])`
* sum
* min
* max
* avg

##### 关联数组的可视化
* 线性直方图：`print( @hist_log(histogram) )`
* 2为底对数直方图：`print( @hist_linear(reads, 0, 1024, 100) )`

#### 高频常用函数
* printf() 格式化打印
* println() 格式化打印带换行
* tid() 当前线程ID
* cpu() 当前CPU编号
* ctime() 当前UNIX epoch秒数
* pp() 当前探测点的描述字符串
* thread_indent() 输出当前probe所处的可执行程序名称、线程id、函数执行的相对时间和执行的次数（通过空格的数量）信息
* name 系统调用的名称字符串
* execname() 当前运行的进程名称
* probefunc() 探测点函数名称


### 六、stap++ 解读
* stap++ 使用Perl对stap进行了更高层的统一封装，主要有如下优化：
    * 变量替换系统
    * 自动处理动态库依赖
    * 进程跟踪增强
    * 模块化和tapset库支持
    * 安全限制预设
* 另外，该仓库针对nginx、lua、luajit 添加了对应的tapset库，方便进行测试
* [官方地址](https://github.com/openresty/stapxx)

#### stap++ 源码解读：
```perl
#!/usr/bin/env perl
# 使用环境中的perl解释器执行此脚本

# 启用严格模式和警告，提高代码质量和安全性
use strict;
use warnings;

# 导入必要的Perl模块
use Getopt::Long qw( GetOptions :config no_ignore_case); # 命令行参数解析，保持大小写敏感
use File::Spec (); # 跨平台文件路径处理
use File::Temp qw( tempdir ); # 临时目录创建与管理
use FindBin (); # 获取脚本所在目录路径

# 前向声明shell参数引用函数
sub quote_sh_args ($);

# 解析命令行参数
GetOptions("D=s@",          \(my $D_opts),      # 预处理器宏定义，如 -DMAXACTION=100000
           "c=s",           \(my $shcmd),       # 执行命令并在命令结束后退出
           "d=s@",          \(my $d_opts),      # 加载指定对象的调试信息
           "arg=s%",        \(my $args),        # 用户自定义参数，用于 $^arg_NAME 变量
           "args",          \(my $print_args),  # 打印所有可用的 --arg 参数
           "dump-src",      \(my $dump_src),    # 输出生成的脚本源码
           "sample-pid=i",  \(my $sample_pid),  # 采样进程以检查DSO对象
           "exec=s",        \(my $exec_path),   # 指定要跟踪的可执行文件路径
           "help",          \(my $help),        # 显示帮助信息
           "master=i",      \(my $master_pid),  # 指定主进程ID，跟踪其所有子进程
           "x=i",           \(my $pid),         # 设置目标进程ID
           "e=s",           \(my $src),         # 直接运行给定脚本
           "v",             \(my $verbose),     # 详细输出模式
           "skip-badvars",  \(my $skip_badvars), # 跳过无效变量
           "I=s@",          \(my $Inc))         # 指定stap++库搜索目录
   or die usage();  # 参数解析失败时显示用法并退出

# 添加默认的tapset库搜索路径：当前目录和脚本所在目录下的tapset子目录
push @$Inc, '.', "$FindBin::Bin/tapset";

# 操作系统兼容性检查
if ($^O ne 'linux') {
    die "Only linux is supported but I am on $^O.\n";  # 仅支持Linux系统
}

# 参数冲突检查：--args和--arg不能同时使用
if ($print_args && $args && %$args) {
    die "No --arg is allowed when --args is specified.\n";
}

# 检查SystemTap是否已安装并获取版本信息
my $ver = `stap -V 2>&1`;
if (!defined $ver) {
    die "Systemtap not installed or its \"stap\" utility is not visible to the PATH environment: $!\n";
}

# 解析SystemTap版本并检查最低版本要求
if ($ver =~ /version\s+(\d+\.\d+)/i) {
    my $v = $1;
    my $min_ver = 2.3;  # 最低要求版本2.3
    if ($v < $min_ver) {
        die "ERROR: at least systemtap $min_ver is required but found $v\n";
    }
} else {
    die "ERROR: unknown version of systemtap:\n$ver\n";
}

# 如果指定了--help参数，显示帮助信息并退出
if ($help) {
    print usage();
    exit;
}

# 处理预处理器宏定义
my %set_D_opts;
for my $opt (@$D_opts) {
    # 记录已设置的宏名称
    if ($opt =~ /^([_A-Z]+)=/) {
        $set_D_opts{$1} = 1;
    }
}

# 设置默认的性能安全参数（如果用户未指定）
if (!$set_D_opts{MAXACTION}) {
    push @$D_opts, "MAXACTION=100000";  # 限制单个探针最大执行次数
}

if (!$set_D_opts{MAXMAPENTRIES}) {
    push @$D_opts, "MAXMAPENTRIES=5000";  # 限制哈希表最大条目数
}

if (!$set_D_opts{MAXBACKTRACE}) {
    push @$D_opts, "MAXBACKTRACE=200";  # 限制调用栈最大深度
}

# 处理输入源：文件或直接脚本
my $infile;
if (!defined $src) {
    # 从命令行获取输入文件
    $infile = shift
        or die "No input file specified.\n";
    
    # 读取源文件内容
    $src = read_src_file($infile);
} else {
    # 使用-e参数直接提供的脚本内容
    $infile = "-e";
}

# 初始化全局数据结构
my (%StdVars,     # 标准变量存储
    %UsedLibs,    # 已使用的库文件
    %DSOs,        # 动态共享对象路径
    %LibPaths,    # 库文件路径缓存
    %UsedStdVars  # 已使用的标准变量跟踪
);

# 构建stap命令行参数数组
my @stap_opts;

# 添加详细输出选项
if ($verbose) {
    push @stap_opts, "-v";
}

# 添加调试对象选项
if ($d_opts) {
    for my $opt (@$d_opts) {
        push @stap_opts, '-d', $opt;
    }
}

# 添加跳过无效变量选项
if (defined $skip_badvars) {
    push @stap_opts, "--skip-badvars";
}

# 添加预处理器宏定义
for my $opt (@$D_opts) {
    push @stap_opts, "-D$opt";
}

# 处理通过 --exec 参数指定的可执行文件
if (defined $exec_path) {
    # 检查可执行文件是否存在
    if (!-f $exec_path) {
        die "$exec_path not found.\n";
    }

    # 设置标准变量 exec_path 并添加调试信息
    $StdVars{exec_path} = $exec_path;
    push @stap_opts, '-d', $exec_path;

    # 使用 ldd 命令获取可执行文件的动态库依赖
    open my $in, "ldd $exec_path|"
        or die "cannot run the command \"ldd $exec_path\": $!\n";
    while (<$in>) {
        # 匹配动态库路径（如 /lib64/libc.so.6）
        if (m{\s+(\/\S+\.so(?:\.\d+)*)}) {
            my $path = $1;
            #warn "Found DSO $path.\n";
            $DSOs{$path} = 1;  # 记录到动态库哈希表中
        }
    }

    # 为所有发现的动态库添加调试信息选项
    for my $path (sort keys %DSOs) {
        push @stap_opts, '-d', $path;
    }

    close $in;
}

# 处理通过 -x 参数指定的目标进程
if (defined $pid) {
    # 检查是否与 --master 参数冲突
    if (defined $master_pid) {
        die "-x <pid> and --master <pid> are exclusive.\n";
    }

    # 添加 stap 的 -x 选项
    push @stap_opts, "-x", $pid;
        
        # 获取进程的可执行文件路径
        my $exec_file = "/proc/$pid/exe";
        if (!-f $exec_file) {
            die "Nginx process $pid is not running or ",
                "you do not have enough permissions.\n";
        }

        # 设置进程过滤条件和目标标识
        $StdVars{pid_ok} = gen_pid_test_condition();  # 生成 pid 过滤表达式
        $StdVars{target} = $pid;

        # 如果未指定可执行文件路径，则从进程信息中获取
        if (!defined $exec_path) {
            $exec_path = readlink $exec_file;  # 解析符号链接获取真实路径
            $StdVars{exec_path} = $exec_path;
            push @stap_opts, "-d", $exec_path;
        }

        # 处理进程加载的动态库
        process_dso($pid);
}

# 处理通过 --master 参数指定的主进程（用于跟踪其所有子进程）
if (defined $master_pid) {
#push @stap_opts, "-x", $master_pid;  # 注释掉的代码，不直接跟踪主进程
    
    # 获取主进程的可执行文件路径
    my $exec_file = "/proc/$master_pid/exe";
    if (!-f $exec_file) {
        die "Nginx process $master_pid is not running or ",
            "you do not have enough permissions.\n";
    }

    # 如果未指定可执行文件路径，则从主进程信息中获取
    if (!defined $exec_path) {
        $exec_path = readlink $exec_file;
        $StdVars{exec_path} = $exec_path;
        push @stap_opts, "-d", $exec_path;
    }

    # 获取主进程的所有子进程
    my @pids = get_child_processes($master_pid);
    if (@pids == 0) {
        die "No child processes found for $master_pid.\n";
    }

    # 生成包含所有子进程的过滤条件
    $StdVars{pid_ok} = gen_pid_test_condition(\@pids);
    $StdVars{target} = "@pids";  # 将所有子进程ID作为空格分隔的字符串

    # 使用第一个子进程来处理动态库依赖
    my $pid = $pids[0];
    process_dso($pid);
}

# 处理通过 --sample-pid 参数指定的采样进程
if ($sample_pid) {
    process_dso($sample_pid);  # 仅用于获取动态库信息，不跟踪该进程
}

# 如果未设置进程过滤条件但指定了可执行文件，则设置默认值
if (!defined $StdVars{pid_ok} && defined $exec_path) {
    $StdVars{pid_ok} = '1';  # 允许所有进程
}

# 如果未设置目标标识但指定了可执行文件，则设置默认值
if (!defined $StdVars{target} && defined $exec_path) {
    $StdVars{target} = 'ANY';  # 表示任意进程
}

# 处理用户自定义参数（--arg 选项）
if (!$print_args) {
    while (my ($k, $v) = each %$args) {
        #warn "getting $k => $v";
        $StdVars{"arg_$k"} = $v;  # 将参数存储为 arg_NAME 格式的标准变量
    }
}

# 初始化用于收集脚本中使用的参数信息
my %used_args;

# 处理源代码并生成最终的 SystemTap 脚本
my $stap_src = process_src($infile, $src);
if ($dump_src) {
    print $stap_src;  # 如果指定了 --dump-src 选项，则输出处理后的脚本内容
    exit;  # 输出后退出程序
}

# 处理 --args 选项：显示脚本中使用的所有参数
if ($print_args) {
    for my $name (sort keys %used_args) {
        my $default = $used_args{$name};  # 获取参数的默认值
        print "\t--arg $name=VALUE";  # 打印参数名称
        if (defined $default) {
            print " (default: $default)\n";  # 如果有默认值，显示默认值
        } else {
            print "\n";  # 没有默认值则只换行
        }
    }
    exit;  # 显示参数后退出程序
}

# 检查未使用的参数并发出警告
for my $key (keys %$args) {
    if (!$UsedStdVars{"arg_$key"}) {  # 检查参数是否在脚本中被使用
        my $val = $args->{$key};
        if (!defined $val) {
            $val = '';
        }
        warn "WARNING: \$^arg_$key is defined by \"--arg $key=$val\", "
             ."but never used.\n";  # 警告用户定义了未使用的参数
    }
}

# 创建临时目录用于存放处理后的库文件
my $tmpdir = tempdir("stapxx-XXXXXXXX", CLEANUP => 1);  # 创建自动清理的临时目录
while (my ($lib, $src) = each %UsedLibs) {
    my $outfile = "$tmpdir/$lib.stp";  # 为每个库创建临时文件
    open my $out, ">$outfile"
        or die "Cannot open $outfile for writing: $!\n";
    print $out $src;  # 将处理后的库内容写入临时文件
    close $out;
}

# 将临时目录添加到 stap 的包含路径
push @stap_opts, "-I", $tmpdir;

# 处理 -c 选项（执行命令并在命令结束后退出）
if (defined $shcmd) {
    push @stap_opts, "-c", $shcmd;
}

# 构建完整的 stap 命令
my $cmd = "stap " . quote_sh_args(\@stap_opts) . " -";  # 使用管道输入脚本内容
warn $cmd;  # 调试用，输出完整命令

open my $in, "|$cmd"  # 打开管道将脚本内容传递给 stap
    or die "Cannot run stap: $!\n";
print $in $stap_src;  # 将处理后的脚本内容写入 stap 的标准输入
close $in;  # 关闭管道，等待 stap 执行完成



#=====================
# 定义一些辅助函数
# 处理用户自定义变量（$*var 格式）
sub eval_usr_var {
    my ($file, $usr_vars, $var) = @_;  # 参数：文件名、变量表、变量名
    if (defined $usr_vars->{$var}) {
        return $usr_vars->{$var};  # 返回变量值
    }

    die "$file: line $.: Undefined user varaible \$*$var.\n";  # 变量未定义则报错
}

# 处理标准内置变量（$^var 格式）
sub eval_std_var {
    my ($file, $var, $trait_name, $trait_val) = @_;  # 参数：文件名、变量名、特性名、特性值

    $UsedStdVars{$var} = 1;  # 标记变量已被使用

    # 如果变量已定义，直接返回其值
    if (defined $StdVars{$var}) {
        return $StdVars{$var};
    }

    # 处理变量特性（如 $^arg_foo:default(123)）
    if (defined $trait_name) {
        #warn "trait: $trait_name";
        if ($trait_name eq 'default') {  # 处理默认值特性
            if ($print_args && $var =~ /^arg_(\w+)$/) {
                $used_args{$1} = $trait_val;  # 记录参数默认值
            }
            $StdVars{$var} = $trait_val;  # 设置变量值为默认值
            return $trait_val;  # 返回默认值
        } else {
            die "$file: line $.: unknown trait name: $trait_name\n";  # 未知特性报错
        }
    }

    # 处理 --args 模式下的变量
    if ($print_args) {
        if ($var =~ /^arg_(\w+)$/) {
            $used_args{$1} = undef;  # 记录参数但不设置默认值
        }
        return '';  # 返回空字符串
    }

    # 处理特殊变量
    if ($var eq 'exec_path') {  # 可执行文件路径
        die "$file: line $.: \$^exec_path is used but neither -x <pid> ",
            "nor --exec <path> is specified.\n";  # 未指定路径则报错

    } elsif ($var =~ /^arg_(\w+)$/) {  # 用户参数
        die "$file: line $.: \$^$var is used but no --arg $1=VAL option is specified.\n";  # 未指定参数则报错

    } elsif ($var =~ /^(lib\w+)_path$/) {  # 库文件路径
        my $prefix = $1;
        my $libpath = find_dso_path($prefix);  # 查找动态库路径
        if (!$libpath) {
            warn "$file: line $.: $prefix is not found, assuming it is statically linked.\n";
            if (!defined $StdVars{exec_path}) {
                die "No -x <pid> option is specified.\n";
            }

            $LibPaths{$prefix} = $StdVars{exec_path};  # 假设静态链接，使用可执行文件路径
            return $StdVars{exec_path};
        }

        return $libpath;  # 返回找到的库路径
    } else {
        die "$file: line $.: Undefined built-in variable \$^$var.\n";  # 未知内置变量报错
    }
}

# 查找动态共享对象(DSO)的路径
sub find_dso_path {
    my $pat = shift;  # 获取库名模式，通常是 libxxx 格式

    # 检查缓存中是否已有该库的路径
    my $path = $LibPaths{$pat};
    if ($path) {
        return $path;  # 如果已缓存，直接返回
    }

    # 解析库名模式，提取实际库名（去掉lib前缀）
    my $name;
    if ($pat !~ /^lib(\S+)/) {
        die "bad pattern: $pat";  # 库名必须以lib开头
    }

    $name = $1;  # 提取lib后面的实际库名

    # 在已发现的DSO列表中查找匹配的库
    my $found_path;
    for my $path (sort keys %DSOs) {
        #warn "checking $path against $pat";
        
        # 尝试精确匹配（如 libssl-1.0.0.so.10）
        if ($path =~ m{\blib\Q$name\E[-.\d]*\.so(?:\.\d+)*$}) {
            $LibPaths{$pat} = $path;  # 缓存结果
            $found_path = $path;
            warn "Found exact match for $pat: $path\n";  # 输出找到的精确匹配
            last;  # 找到精确匹配后立即返回
	}

        # 尝试模糊匹配（处理库名可能有变体的情况）
        if ($path =~ m{\b(?:lib)?\Q$name\E[^/\s]*?\.so(?:\.\d+)*$}) {
            if ($found_path) {
                warn "Ignored ambiguous library $path for \"$pat\"\n";  # 忽略模糊匹配
                next;
            }

            $LibPaths{$pat} = $path;  # 缓存结果
            $found_path = $path;  # 记录找到的路径
        }
    }

    return $found_path;  # 返回找到的路径，如果未找到则为undef
}

# 读取源文件内容
sub read_src_file {
    my $infile = shift;  # 获取输入文件路径
    open my $in, $infile
        or die "Cannot open $infile for reading: $!\n";  # 打开文件失败则报错
    my $src = do { local $/; <$in> };  # 一次性读取整个文件内容
    close $in;  # 关闭文件句柄
    return $src;  # 返回文件内容
}

# 处理@use指令，导入tapset库文件
sub use_libs {
    my ($file, $libs) = @_;  # 参数：当前文件名、库列表字符串
    #warn "libs: $libs";
    
    my @libs = split /\s*,\s*/, $libs;  # 按逗号分隔库名列表
    for my $lib (@libs) {
        #warn "processing $lib...";
        
        # 将点分隔的库名转换为路径（如 ngx.time 变为 ngx/time.sxx）
        my $path = join("/", split /\./, $lib) . ".sxx";
        #warn $path;
        
        # 在所有包含路径中查找库文件
        for my $dir (@$Inc) {
            my $abspath = File::Spec->catfile($dir, $path);  # 构建绝对路径
            warn "Testing $abspath\n";
            warn "exist: ", (-f $abspath) ? 1 : 0;
            
            if (-f $abspath) {  # 如果文件存在
                my $src = read_src_file($abspath);  # 读取库文件内容
                $UsedLibs{$lib} = process_src($abspath, $src);  # 处理库文件内容并缓存
                goto next_lib;  # 跳转到下一个库的处理
            }
        }
        die "$file: line $.: cannot find \@use library $lib\n";  # 找不到库文件则报错
next_lib:  # 处理下一个库的标签
    }
    return "";  # @use指令本身不产生输出
}

# 处理stap源代码，替换变量和指令
sub process_src {
    my ($file, $src) = @_;  # 参数：文件名、源代码内容

    my %usr_vars;  # 存储用户自定义变量
    my @bits;      # 存储处理后的代码片段

    # 定义库名模式（支持点分隔的库名，如 ngx.time）
    my $libname_pat = qr/(?:\w+(?:\.\w+)*)/;
    
    # 处理输入文件
    open my $in, '<', \$src or die $!;  # 从字符串打开文件句柄

    while (<$in>) {
        # 替换脚本首行的 shebang
        if ($. == 1 && /^\#!/) {
            $_ = "#!/usr/bin/env stap\n";  # 确保使用 stap 解释器
            next;
        }

        # 替换参数变量（$^arg_xxx 格式）
        s{\$\^(arg_\w+)(?:\s*:(\w+)\s*\((.*?)\))?}{eval_std_var($file, $1, $2, $3)}eg;
        
        # 替换 @pfunc 函数调用（简化函数引用）
        s{\@pfunc\s*\(\s*(\w+)\s*\)}{process("\$^exec_path").function("$1")}g;
        
        # 替换标准变量（$^xxx 格式）
        s{\$\^(\w+|lib[-.\w]+_path)(?:\s*:(\w+)\s*\((.*?)\))?}{eval_std_var($file, $1, $2, $3)}eg;
        
        # 处理用户变量赋值（$*xxx := @cast(...) 格式）
        s{\$\*(\w+)\s*:=\s*(\&?\@(?:cast|var)\(.*?\)(?:\[\d+\])?)}{$usr_vars{$1} = $2; ""}eg;
        
        # 替换用户变量引用（$*xxx 格式）
        s{\$\*(\w+)}{eval_usr_var($file, \%usr_vars, $1)}eg;
        
        # 处理库导入指令（@use xxx 格式）
        s{\@use\s+($libname_pat(?:\s*,\s*$libname_pat)*)}{use_libs($file, $1)}eg;

    } continue {
        push @bits, $_;  # 将处理后的行添加到结果数组
    }

    close $in;  # 关闭文件句柄
    return join '', @bits;  # 合并所有行并返回
}

# 生成帮助信息
sub usage {
    return <<'_EOC_';
Usage:
    stap++ [optoins] [infile]

Options:
    --arg NM=VAL    Specify extra user arguments (for $^arg_NM).
    --args          Print all available arguments for --arg.
    -c CMD     start the probes, run CMD, and exit when it finishes
    -d PATH         Load debug info for the specified objects
    -D NM=VAL       Emit macro definition into generated C code.
    -e SCRIPT       Run given script.
    --exec PATH     Specify the executable file path to be traced.
    --help          Print this help.
    -I PATH         Specify the stap++ tapset library search directory.
    --master PID    Specify the master pid whose child processes are traced.
    --sample-pid PID  Sample process to inspect DSO objects to load via -d
    -v              Be verbose.
    -x PID          Sets target() to PID (also for $^exec_path and $^libxxx_path).

Examples:
    stap++ -x 12345 -e 'probe begin { println("hello") exit() }'
    stap++ -x 12345 infile.ss
_EOC_
}

# 获取指定进程的所有子进程
sub get_child_processes {
    my $pid = shift;  # 获取父进程ID
    
    # 获取所有进程的状态文件
    my @files = glob "/proc/[0-9]*/stat";
    my @children;  # 存储子进程ID
    
    # 遍历所有进程
    for my $file (@files) {
        #print "file: $file\n";
        
        # 跳过进程自身
        if ($file =~ m{^/proc/$pid/}) {
            next;
        }

        # 读取进程状态信息
        open my $in, $file or next;  # 打开失败则跳过
        my $line = <$in>;
        close $in;
        
        # 解析进程ID和父进程ID
        if ($line =~ /^(\d+) \S+ \S+ (\d+)/) {
            my ($child, $parent) = ($1, $2);
            if ($parent eq $pid) {  # 如果父进程ID匹配
                push @children, $child;  # 添加到子进程列表
            }
        }
    }

    # 按数字顺序排序子进程ID
    @children = sort { $a <=> $b } @children;
    return @children;  # 返回子进程ID列表
}

# 生成进程ID过滤条件
sub gen_pid_test_condition {
    my $pids = shift;  # 获取进程ID列表
    
    # 如果未提供进程ID列表，则使用 target() 函数
    if (!$pids) {
        return "pid() == target()";  # 默认条件：当前进程ID等于目标进程ID
    }

    # 为每个进程ID生成条件
    my @c;
    for my $pid (@$pids) {
        push @c, "pid() == $pid";  # 添加进程ID相等条件
    }
    
    # 使用逻辑或连接所有条件，并用括号包围
    return '(' . join(" || ", @c) . ')';
}

# 处理进程的动态共享对象
sub process_dso {
    my $pid = shift;  # 获取进程ID
    
    # 打开进程的内存映射文件
    my $maps_file = "/proc/$pid/maps";
    open my $in, $maps_file
        or die "Cannot open $maps_file for reading: $!\n";

    # 解析内存映射，查找动态库
    while (<$in>) {
        if (m{\S+\.so(?:\.\d+)*$}) {  # 匹配以 .so 结尾的路径
            my $path = $&;  # 获取匹配的路径
            $DSOs{$path} = 1;  # 记录到动态库哈希表
            #warn "seeing $path";
        }
    }

    # 为所有发现的动态库添加调试信息选项
    for my $path (sort keys %DSOs) {
        push @stap_opts, '-d', $path;
    }
}

# 处理Shell命令参数的引用，确保特殊字符被正确转义
sub quote_sh_args ($) {
    my ($args) = @_;  # 获取参数数组引用
    for my $arg (@$args) {
       # 检查参数是否只包含常见的Shell安全字符
       if ($arg =~ m{^[- "&%;,|?*.+=\w:/()]*$}) {
          # 如果包含空格或特殊字符，用单引号包围
          if ($arg =~ /[ "&%;,|?*()]/) {
             $arg = "'$arg'";
          }
          next;  # 处理下一个参数
       }
       
       # 处理包含更复杂字符的参数，使用$'...'格式（ANSI-C引用）
       $arg =~ s/\\/\\\\/g;  # 转义反斜杠
       $arg =~ s/'/\\'/g;    # 转义单引号
       $arg =~ s/\n/\\n/g;   # 转义换行符
       $arg =~ s/\r/\\r/g;   # 转义回车符
       $arg =~ s/\t/\\t/g;   # 转义制表符
       $arg = "\$'$arg'";    # 使用ANSI-C引用格式
    }
    return "@$args";  # 返回空格连接的参数字符串
}

```

### 七、openresty-systemtap-toolkit 解读
* openresty-systemtap-toolkit 中的脚本也使用Perl对stap进行了更高层的封装。它与stap++的主要区别在于，这个仓库里面的每个脚本都针对当前stap脚本做了具体的处理，而stap++是对stap脚本的笼统的抽象处理。这样对应的执行方式就发生了变化：
    * stap++ ：stap++  script.stp  -x PID
    * tookit ：perl    perl-script -x PID
* 另外，该仓库针对nginx、lua、luajit 添加了对应的tapset库，方便进行测试
* [官方地址](https://github.com/openresty/openresty-systemtap-toolkit)


### 七、stap++、toolkit核心脚本：
#### stap++核心脚本说明：
[lj-lua-stacks.sxx：](https://github.com/openresty/stapxx/blob/master/samples/lj-lua-stacks.sxx) CPU统计工具，获取lua代码堆栈统计

[sample-bt-leaks.sxx：](https://github.com/openresty/stapxx/blob/master/samples/sample-bt-leaks.sxx) 内存工具统计，对glibc内置函数（malloc、calloc、realloc）进行的内存分配采集回溯信息，查看未被释放的内存（一般需要两次采集来进行差异分析）

[lj-gc-objs.sxx：](https://github.com/openresty/stapxx/blob/master/samples/lj-gc-objs.sxx) 内存工具统计，lua类型的内存分配

[lj-str-tab.sxx：](https://github.com/openresty/stapxx/blob/master/samples/lj-str-tab.sxx) 内存工具统计，查看lua全局变量

[ngx-lua-count-timers.sxx：](https://github.com/openresty/stapxx/blob/master/samples/ngx-lua-count-timers.sxx) 统计timer数量

[sample-bt.sxx：](https://github.com/openresty/stapxx/blob/master/samples/sample-bt.sxx) CPU统计工具，获取任意进程（nginx）进行用户态或者内核态采样。输出是汇总后的调用栈（按照总数）。同toolkit中的sample-bt功能一样，但是toolkit的可以自动获取并添加其他so文件信息到stap命令行。

[ngx-upstream-err-log.sxx：](https://github.com/openresty/stapxx/blob/master/samples/ngx-upstream-err-log.sxx) 排查`upstream prematurely closed connection while`等upstream问题

#### toolkit核心脚本说明：
[sample-bt：](https://github.com/openresty/openresty-systemtap-toolkit/blob/master/sample-bt) CPU统计工具，获取任意进程（nginx）进行用户态或者内核态采样。输出是汇总后的调用栈（按照总数）

[sample-bt-off-cpu：](https://github.com/openresty/openresty-systemtap-toolkit/blob/master/sample-bt-off-cpu) CPU统计工具，对进程级别的off-cpu的采样统计

[fix-lua-bt：](https://github.com/openresty/openresty-systemtap-toolkit/blob/master/fix-lua-bt) 对采样结果进行优化，展示更多信息。将`lj-lua-stacks.sxx`的结果根据 lua文件+行号 转换为对应函数

[ngx-phase-handlers：](https://github.com/openresty/openresty-systemtap-toolkit/blob/master/ngx-phase-handlers) 按照真实执行顺序，打印出实际注册的phase和对应的handler。可以用来解决配置handler顺序相关问题。

辅助工具：

[check-debug-info：](https://github.com/openresty/openresty-systemtap-toolkit/blob/master/check-debug-info) 检查当前进程中使用的so文件，哪些没有debuginfo\dwarf信息

[ngx-lua-bt：](https://github.com/openresty/openresty-systemtap-toolkit/blob/master/ngx-lua-bt) 获取Lua的当前调用栈（**在luajit环境没跑通**，代码有大量问题，可以用lj-lua-stacks.sxx替代）