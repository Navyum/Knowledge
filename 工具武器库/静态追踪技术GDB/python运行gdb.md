---
title: python运行gdb
date: 2025-06-17 11:38:29
author: Navyum
tags: 
 - 性能分析
 - 可视化
 - GDB
 - luajit
 - btrace
categories: 
 - 工具
 - 性能分析
 - GDB
article: true
index: true

headerDepth: 2
sticky: true
star: true
---

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


### openresty-gdb-utils
| 命令 | 描述 |
| --- | --- |
| `bt [full]` | 获取当前C级别的函数调用栈 |
| `lbt [full] [L]` | 获取当前lua线程的函数调用栈 |
| `lvmst [L]` | 获取当前LuaJIT 2.1 VM state |
| `lmainL` | 获取main LuaJIT VM state的lua_State指针 |
| `lcurL` | 获取当前运行的lua线程的 LuaJIT VM state的lua_State指针 |
| `lg [L]` | 获取当前main LuaJIT VM state或者指定的lua_state的global_State指针 |
| `lglobtab [L]` | 获取当前main LuaJIT VM state或者指定的lua_state的`全局环境表 global envirement` |
| `ltabgets tab field` | 获取某个tab的 field 对应值 |
| `lval tvalue/gcobj` | 获取tvalue/gcobj的内容 |
| `lfunc file lineno` | 获取指定文件指定行号的指针，进行使用luv打印值 |
| `luv func` | 获取func的upvalue |
| `lgc [L]` | 获取LuaJIT VM 对应的GC垃圾回收占用内存大小 |
| `lgcstat` | 获取LuaJIT VM 对应的GC垃圾回收对象的统计信息 |
| `lgcpath` | 按照字节设置阈值，获取当前存活的指定类型的GC对象。并打印垃圾回收根节点到该对象的完整引用路径 |

### 案例分析 查看某个请求：
```bt 命令查看C栈信息
(gdb) bt
#0  0x00007fb4238df2ee in lj_alloc_free (msp=0x7fb424565010, ptr=<optimized out>) at lj_alloc.c:1415
#1  0x00007fb42387e8ef in gc_sweep (g=g@entry=0x7fb4245653f0, p=0x7fb40c0ca430, lim=32, lim@entry=40) at lj_gc.c:414
#2  0x00007fb42387fd6d in gc_onestep (L=L@entry=0x7fb40bc0b950) at lj_gc.c:674
#3  0x00007fb423880695 in lj_gc_step (L=L@entry=0x7fb40bc0b950) at lj_gc.c:726
#4  0x00007fb4238807bb in lj_gc_step_jit (g=<optimized out>, steps=5) at lj_gc.c:759
#5  0x00007fb42be197d5 in ?? ()
#6  0x0000000001a08230 in ?? ()
#7  0x0000000001a08fb8 in ?? ()
#8  0x0000000000b10720 in ngx_http_lua_set_handlers ()
#9  0x00000000038c4620 in ?? ()
#10 0x0000000001a08fb8 in ?? ()
#11 0x000000000054bb6d in ngx_http_lua_set_output_header (r=0x7fb40bbe7338, ctx=0x7fb40bbe7338, key=..., value=..., override=202155056)
    at ../ngx_lua-0.10.19/src/ngx_http_lua_headers_out.c:543
#12 0x00007fb4245653f0 in ?? ()
#13 0x00007fb40c0ca430 in ?? ()
#14 0x00007fb40ba03480 in ?? ()
#15 0x0000000000000001 in ?? ()
#16 0x00007fb4245653f0 in ?? ()
#17 0x00007fb40c0ca430 in ?? ()
#18 0x0000000000000022 in ?? ()
#19 0x00007fb417d34a80 in ?? ()
#20 0x00007fb42387e8ef in gc_sweep (g=g@entry=0x7fb4245653f0, p=0x7fb40beb9340, lim=399723135, lim@entry=40) at lj_gc.c:414
#21 0x00007fb42387fd6d in gc_onestep (L=L@entry=0x7fb40bc0b950) at lj_gc.c:674
#22 0x00007fb423880695 in lj_gc_step (L=L@entry=0x7fb40bc0b950) at lj_gc.c:726
#23 0x00007fb4238807bb in lj_gc_step_jit (g=<optimized out>, steps=0) at lj_gc.c:759
#24 0x00007fb42be2be7f in ?? ()
#25 0x0000000000000001 in ?? ()
#26 0x00007fb403f05ee0 in ?? ()
#27 0x00007fb40d410b50 in ?? ()
#28 0x00007fb40b936b40 in ?? ()
#29 0x00007fb424546018 in ?? ()
#30 0x0000000000000000 in ?? ()
```

```lbt 命令查看lua栈信息
(gdb) lbt
@/usr/local/openresty/lualib/resty/core/request.lua:121
@/usr/local/openresty/nginx/conf/util.lua:1083
@/usr/local/openresty/nginx/conf/purchase/cs/xxxxx.lua:540
```


### 案例分析 分析openresty的内存占用情况：
```python
# -*- coding: utf-8 -*-
import gdbutils
import ngxlua
import luajit21
import gdb
import nginx
import json
from collections import Counter

globalvar = gdbutils.globalvar
typ = gdbutils.typ

def convert_bytes(size):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return "%.2f%s" % (size, unit)
        size /= 1024
    return "%.2f%s" % (size, 'TB')

class NgxMemAnalyzer(gdb.Command):
    """Analyze OpenResty memory usage including LuaJIT, shared memory and other components.
Usage: ngx_mem_analyzer [all]"""

    def __init__(self):
        super(NgxMemAnalyzer, self).__init__("ngx_mem_analyzer", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        print("Analyzing OpenResty memory usage...")
        argv = gdb.string_to_argv(args)
        
        # Get memory statistics
        result = self._analyze_memory()
        
        # Print results
        if len(argv) > 0 and argv[0] == 'all':
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(result['summary'], indent=2))

    def _analyze_memory(self):
        """Analyze different memory components"""
        result = {
            'summary': {},
            'details': {}
        }

        # Analyze LuaJIT memory
        lua_mem = self._analyze_luajit_memory()
        result['summary']['luajit'] = lua_mem['summary']
        result['details']['luajit'] = lua_mem['details']

        # Analyze shared memory
        shm_mem = self._analyze_ngx_shared_memory()
        result['summary']['ngx_shared'] = shm_mem['summary']

        # Analyze glibc memory
        glibc_mem = self._analyze_glibc_memory()
        result['summary']['glibc_mmap'] = glibc_mem['summary']['mmap']
        result['summary']['glibc_marea'] = glibc_mem['summary']['marea']
        result['details']['glibc'] = glibc_mem['details']

        # Analyze shared objects memory
        so_mem = self._analyze_shared_objects()
        result['summary']['shared_objects'] = so_mem['summary']
        result['details']['shared_objects'] = so_mem['details']

        # Calculate total memory
        total_mem = sum(result['summary'].values())
        result['summary']['total'] = convert_bytes(total_mem)

        # Convert all summary values to MB
        for key in result['summary']:
            if key != 'total':  # Skip total as it's already in MB
                result['summary'][key] = convert_bytes(result['summary'][key])

        return result

    def _analyze_luajit_memory(self):
        """Analyze LuaJIT memory usage"""
        lua_mem = {
            'summary': 0,
            'details': {}
        }

        try:
            # 获取 Lua 状态
            L = luajit21.get_global_L()
            if not L:
                return lua_mem

            # 获取 GC 状态
            g = luajit21.G(L)
            gc = g['gc']

            # 计算总内存使用
            total = int(gc['total'])
            lua_mem['summary'] = total

            # 获取详细内存信息
            lua_mem['details'] = {
                'total': convert_bytes(total),
                'threshold': convert_bytes(int(gc['threshold'])),
                'debt': convert_bytes(int(gc['debt'])),
                'estimate': convert_bytes(int(gc['estimate']))
            }

        except Exception as e:
            print("Error analyzing LuaJIT memory: %s" % str(e))

        return lua_mem

    def _analyze_ngx_shared_memory(self):
        """Analyze shared memory usage"""
        shm_mem = {
            'summary': 0,
            'details': []
        }

        try:
            # Get shared memory zones
            ngx_cycle = nginx.get_ngx_cycle()
            shared_memory = ngx_cycle['shared_memory']
            part = shared_memory['part']
            shm_zones = part['elts'].cast(typ("ngx_shm_zone_t*"))

            total_size = 0
            while part:
                for idx in xrange(0, part['nelts']):
                    item = shm_zones[idx]
                    size = int(item['shm']['size'])
                    total_size += size
                    
                    # 获取共享内存区域名称
                    name = ""
                    try:
                        # 从 shm_zone 的 shm_name 字段获取名称
                        shm_name = item['shm_name']
                        if shm_name:
                            name = str(shm_name['data'])
                    except:
                        # 如果无法获取名称，使用地址作为标识
                        name = "shm_zone_%s" % gdbutils.gdb_val_to_hex_str(item['shm']['addr'])
                    
                    shm_mem['details'].append({
                        'name': name,
                        'size': convert_bytes(size),
                        'address': gdbutils.gdb_val_to_hex_str(item['shm']['addr'])
                    })

                part = part['next']
                if part == 0:
                    break
                shm_zones = part['elts'].cast(typ("ngx_shm_zone_t*"))

            shm_mem['summary'] = total_size

        except Exception, e:
            print("Error analyzing shared memory: %s" % str(e))

        return shm_mem

    def _analyze_glibc_memory(self):
        """Analyze glibc memory usage"""
        glibc_mem = {
            'summary': {
                'mmap': 0,
                'marea': 0,
                'total': 0
            },
            'details': {
                'mmap': {
                    'total': 0,
                    'max': 0,
                    'chunks': []
                },
                'marea': {
                    'total': 0,
                    'max': 0,
                    'free_chunks': [],
                    'used_chunks': []
                }
            }
        }

        try:
            # 从全局变量获取 main_arena
            main_arena = gdb.parse_and_eval("main_arena")
            
            # Get marea stats
            marea_total = int(main_arena['system_mem'])
            marea_max = int(main_arena['max_system_mem'])
            glibc_mem['details']['marea']['total'] = convert_bytes(marea_total)
            glibc_mem['details']['marea']['max'] = convert_bytes(marea_max)
            glibc_mem['summary']['marea'] = marea_total

            # Get mmap stats
            try:
                mp_ = gdb.parse_and_eval("mp_")
            
                mmap_total = int(mp_['mmapped_mem'])
                mmap_max = int(mp_['max_mmapped_mem'])
                glibc_mem['details']['mmap']['total'] = convert_bytes(mmap_total)
                glibc_mem['details']['mmap']['max'] = convert_bytes(mmap_max)
                glibc_mem['summary']['mmap'] = mmap_total
            except Exception as e:
                print("Error retrieving mmap stats: %s" % str(e))
                glibc_mem['summary']['mmap'] = 0  # Set to 0 if there's an error

            # Calculate total
            total_mem = marea_total + mmap_total
            glibc_mem['summary']['total'] = total_mem

        except Exception as e:
            print("Error analyzing glibc memory: %s" % str(e))

        return glibc_mem

    def _analyze_shared_objects(self):
        """Analyze shared objects memory usage"""
        so_mem = {
            'summary': 0,
            'details': []
        }

        try:
            # 获取所有加载的共享库
            libs = gdb.execute("info shared", to_string=True)
            for line in libs.split('\n'):
                if not line.strip():
                    continue
                    
                # 解析共享库信息
                parts = line.split()
                if len(parts) < 4:
                    continue
                    
                try:
                    # 获取共享库的基地址
                    base_addr = int(parts[0], 16)
                    # 获取共享库的路径
                    lib_path = parts[-1]
                    
                    # 获取共享库的内存映射信息
                    maps = gdb.execute("info proc mappings", to_string=True)
                    lib_size = 0
                    
                    for map_line in maps.split('\n'):
                        if not map_line.strip():
                            continue
                            
                        map_parts = map_line.split()
                        if len(map_parts) < 3:
                            continue
                            
                        try:
                            start_addr = int(map_parts[0], 16)
                            end_addr = int(map_parts[1], 16)
                            size = end_addr - start_addr
                            
                            # 检查是否属于当前共享库
                            if start_addr >= base_addr and start_addr < base_addr + 0x1000000:  # 假设最大偏移为16MB
                                lib_size += size
                                        
                        except ValueError:
                            continue
                    
                    if lib_size > 0:
                        so_mem['summary'] += lib_size
                        so_mem['details'].append({
                            'name': lib_path,
                            'address': hex(base_addr),
                            'size': convert_bytes(lib_size)
                        })
                        
                except (ValueError, IndexError):
                    continue

        except Exception, e:
            print("Error analyzing shared objects memory: %s" % str(e))

        return so_mem


# Register the command
NgxMemAnalyzer()
```