'use strict'

const fs        = require('fs')
const os        = require('os')
const path      = require('path')
const resolve   = require('path').resolve

const ignoreFiles = ['_navbar.md', '_coverpage.md', '_sidebar.md']

// common funcs
function exists (path) {
  if (fs.existsSync(path)) {
    return path
  }

  return undefined
}

function cwd (path) {
  return resolve(process.cwd(), path || '.')
}

function pwd (path) {
  return resolve(require('path').dirname(__dirname), path)
}

function toCamelCase(str) {
  return str
    .replace(/(\d+)\./g, '$1-') // 将数字后的点改为连字符（如 01. -> 01-）
    .replace(/\s+/g, '-')       // 将空格替换为连字符
    .replace(/\b(\w)/g, (match, capture) => capture.toUpperCase())
    .replace(/[-_]/g, ' ')
}

//----------------


// 待写入的md的文件流
let tree = '';

function genSidebar(cwdPath, sidebarPath) {
  let lastPath = ''
  let nodeName = ''
  let blankspace = '';
  let test = 0;

  const files = getFiles(cwdPath);
  //console.log("files---> :" ,JSON.stringify(files));
  getMdStream(files);

  fs.writeFile(sidebarPath, tree, 'utf8', err => {
    if (err) {
      console.error(`Couldn't generate the sidebar file, error: ${err.message}`)
    }
  })

  return
}

function getFiles (dir) {

  let rootDir       = dir;
  var filesNameArr  = []
  let cur           = 0

  // 用个hash队列保存每个目录的深度
  var mapDeep       = {}
  mapDeep[dir]      = 0

  // 先遍历一遍给其建立深度索引
  function getMap(dir, curIndex) {

    var files = fs.readdirSync(dir) //同步拿到文件目录下的所有文件名
    files.map(function (file) {

      //var subPath = path.resolve(dir, file) //拼接为绝对路径
      var subPath   = path.join(dir, file) //拼接为相对路径
      var stats     = fs.statSync(subPath) //拿到文件信息对象
      //console.log("files B---> :" ,subPath);
      // 必须过滤掉node_modules文件夹
      if (file != 'node_modules') {
        mapDeep[file] = curIndex + 1

        if (stats.isDirectory()) { //判断是否为文件夹类型
          return getMap(subPath, mapDeep[file]) //递归读取文件夹
        }
      }

    })
  }

  getMap(dir, mapDeep[dir])
  //console.log("dirs", mapDeep)

  //深度遍历生成完整 mapDeep 对象
  function readdirs(dir, folderName, myroot) {
    //构造文件夹数据
    var result = {
      path: dir,
      title: path.basename(dir),
      type: 'directory',
      deep: mapDeep[folderName]
    }
  
    var files = fs.readdirSync(dir) //同步拿到文件目录下的所有文件名
  
    // 新增排序：目录优先，按名称不区分大小写排序
    files.sort((a, b) => {
      const aPath = path.join(dir, a);
      const bPath = path.join(dir, b);
      const aIsDir = fs.statSync(aPath).isDirectory();
      const bIsDir = fs.statSync(bPath).isDirectory();
      
      // 目录优先排序
      if (aIsDir !== bIsDir) {
        return aIsDir ? -1 : 1;
      }
      // 相同类型时按名称排序
      return a.localeCompare(b, undefined, { sensitivity: 'base' });
    });

    // 构造文件夹childen数据
    result.children = files.map(function (file) {
        //var subPath = path.resolve(dir, file) //拼接为绝对路径
        var subPath = path.join(dir, file) //拼接为相对路径
        var stats   = fs.statSync(subPath) //拿到文件信息对象

        //文件夹过滤,开头.隐藏文件夹
        //判断是否为文件夹类型
        if (stats.isDirectory()) {
          if (!file.startsWith('.') && file != "node_modules" ) { 
            console.log("[dir add]:" ,subPath);
            return readdirs(subPath, file, file) //递归读取文件夹
          } else {
            console.log("[dir remove]:" ,subPath);
          }
        }
  
        // 文件过滤,开头_的md文件
        // 仅输出.md文件类型文件的数据
        if (path.extname(file) === '.md' && !file.startsWith('_') ) {
          const path =  subPath.replace(rootDir + '/', '');
          console.log("[file add]:",subPath);
          return {
            path: path,
            name: file.replace('.md',''),
            type: 'file',
            deep: mapDeep[folderName] + 1,
          }
        } else {
          console.log("[file remove]:",subPath);
        }
      
    })
  
    //console.log("result:",JSON.stringify(result));
    return result
  }

  filesNameArr.push(readdirs(dir, dir))
  return filesNameArr
}

//深度遍历构造md流数据，formater函数
function getMdStream(files) {
  for (let i=0; i<files.length; i++) {
    const item = files[i];
    if (item ) {

      // 第一层的*.md文件没有添加到md流
      if (item.deep === 0) {
        // do nothing
        if (item.children) {
          getMdStream(item.children)
        }
      } else {

        let blankspace = ''
        // 基于深度，添加对应的层级
        for (let i = 1; i < item.deep; i++) {
          blankspace += '  '
        }

        if (item.type === 'directory') {
          //前后带换行 os.EOL
          tree += blankspace + '- ' + '📁 ' + toCamelCase(item.title) + os.EOL 
          //tree += blankspace + '- ' + '🗂 ' + toCamelCase(item.title) + os.EOL 

        } else if (item.type === 'file') {
          //tree += os.EOL + blankspace + '- [' + item.name + '](' + item.path + ')' + os.EOL
          tree += blankspace + '- [' + toCamelCase(item.name) + '](' + item.path + ')' + os.EOL

        }

        // 深度遍历
        if (item.children) {
          getMdStream(item.children)
        }

      }
    }
  }
}


// 入口函数
function main (path = './', outpath = './',  sidebar = '_sidebar.md', replace = 'false') {
  // 获取当前目录
  const cwdPath = cwd(path || '.')

  if (!exists(outpath)) {
    console.error(`${outpath} directory does not exist.`)
  }

  const sidebarPath = outpath + '/' + sidebar 
  
  if (exists(sidebarPath) && !replace ) {
    console.error(`The sidebar file '${sidebar}' already exists., Use third params to ignore`)
    process.exitCode = 1
    return false
  }
  
  genSidebar(cwdPath, sidebarPath)
  console.log(`Successfully generated the sidebar file '${sidebarPath}'.`)
  
  return true
}


// entrypoint
const args = require('minimist')(process.argv.slice(2))

let dir     = args['dir']
let outdir  = args['outdir']
let name    = args['name']
let replace = args['replace']

main(dir, outdir, name, replace)
