## GDB（GNU Debugger）
GDB是UNIX/LINUX操作系统下的、基于命令行的、功能强大的程序调试工具。
可以查看程序在执行过程中的内部

[gdb 官方文档](https://sourceware.org/gdb/current/onlinedocs/gdb.html/)

### Python-gdb
----
通过python来运行gdb命令，其本质是利用python语言的灵活性和便利。GDB提供了一套python API，方便用户使用python脚本编写更复杂的GDB脚本
[gdb python api 官方文档](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python.html#Python)


### 案例：openresty-gdb-utils
[openresty-gdb-utils 官方地址](https://github.com/openresty/openresty-gdb-utils/tree/master)

#### 仓库代码解析
仓库包含了两类脚本：
* .gdb：luajit20.gdb、ngx-lua.gdb
    * 传统的gdb脚本，使用C风格的代码编写
* .py：
    * python 脚本，通过gdb api与gdb交互

##### gdb脚本
```luajit20.gdb
...
define lgc
    set $lgc_L = (lua_State *)($arg0)
    set $lgc_global_state = (global_State *)($lgc_L->glref->ptr32)
    set $lgc_gc = $lgc_global_state.gc
    printf "GC memory currently allocated: %d\n", $lgc_gc.total
end

document lgc
    Print Lua garbage collection info of given Lua State   // 打印lua State的gc信息
    Usage: lfullstack addr
end
...
```

##### python脚本
```luajit21.py
...
class lgc(gdb.Command):
    """This command prints out the current size of memory allocated by the LuaJIT GC.    // 打印lua State的gc信息
Usage: lgc [L]"""

    def __init__ (self):
        super (lgc, self).__init__("lgc", gdb.COMMAND_USER)

    def invoke (self, args, from_tty):
        argv = gdb.string_to_argv(args)

        if len(argv) == 1:
            L = gdbutils.parse_ptr(argv[0], "lua_State*")
            if not L or str(L) == "void":
                raise gdb.GdbError("L empty")
        else:
            L = get_global_L()

        g = G(L)
        out("The current memory size (allocated by GC): %d bytes\n" \
                % int(g['gc']['total']))

lgc()

...
```

### gdb脚本使用
* 在GDB调试内加载某个脚本：`(gdb) source scrip.py`
* 使用 *.gdbinit* 批量加载python脚本：
  ```.gdbinit
    directory /xxx/openresty-gdb-utils               #添加工作目录，用于gdb去搜索脚本

    py import sys
    py sys.path.append("/xxx/openresty-gdb-utils")   #添加python模块的搜索路径（例如脚本中用到的一些common方法、依赖等）

    source script1.py                                #加载脚本
    source script2.py                                #加载脚本
    ...

    set python print-stack full                      #启用完整的 Python 堆栈打印，默认情况下只打印异常
  ```

### 案例分析：
