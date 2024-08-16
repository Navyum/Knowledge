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
  return str.replace(/\b(\w)/g, function (match, capture) {
    return capture.toUpperCase()
  }).replace(/-|_/g, ' ')
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
      mapDeep[file] = curIndex + 1

      if (stats.isDirectory()) { //判断是否为文件夹类型
        return getMap(subPath, mapDeep[file]) //递归读取文件夹
      }

    })
  }

  getMap(dir, mapDeep[dir])
  console.log("dirs",mapDeep)

  //深度遍历生成完整 mapDeep 对象
  function readdirs(dir, folderName, myroot) {
    console.log("current", dir)
    //构造文件夹数据
    var result = {
      path: dir,
      title: path.basename(dir),
      type: 'directory',
      deep: mapDeep[folderName]
    }
  
    var files = fs.readdirSync(dir) //同步拿到文件目录下的所有文件名
  
    //构造文件夹childen数据
    result.children = files.map(  function (file) {
        //var subPath = path.resolve(dir, file) //拼接为绝对路径
        var subPath = path.join(dir, file) //拼接为相对路径
        var stats   = fs.statSync(subPath) //拿到文件信息对象
  
        //文件夹过滤,开头.隐藏文件夹
        //判断是否为文件夹类型
        if (stats.isDirectory() && !file.startsWith('.')) { 
          return readdirs(subPath, file, file) //递归读取文件夹
        }
  
        // 文件过滤,开头_的md文件
        // 仅输出.md文件类型文件的数据
        if (ignoreFiles.indexOf(file) == 1) {
          console.log("file ---> ", file)
        }
  
        if (path.extname(file) === '.md' && !file.startsWith('_') ) {
          const path =  subPath.replace(rootDir + '/', '');
          return {
            path: path,
            name: file.replace('.md',''),
            type: 'file',
            deep: mapDeep[folderName] + 1,
          }
        }
      
    })
  
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
          tree += os.EOL + blankspace + '- ' + toCamelCase(item.title) + os.EOL

        } else if (item.type === 'file') {
          tree += os.EOL + blankspace + '- [' + item.name + '](' + item.path + ')' + os.EOL

        }

        console.log("tree", tree)
        // 深度遍历
        if (item.children) {
          getMdStream(item.children)
        }

      }
    }
  }
}


// 入口函数
function main (path = './', sidebar = '_sidebar.md', replace = 'false') {
  // 获取当前目录
  const cwdPath = cwd(path || '.')

  if (!exists(cwdPath)) {
    console.error(`${cwdPath} directory does not exist.`)
  }

  const sidebarPath = cwdPath + '/' + sidebar 
  
  if (exists(sidebarPath) && !replace ) {
    console.error(`The sidebar file '${sidebar}' already exists., Use third params to ignore`)
    process.exitCode = 1
    return false
  }
  
  genSidebar(cwdPath, sidebarPath)
  console.log(`Successfully generated the sidebar file '${sidebar}'.`)
  
  return true
}


// entrypoint
const args = require('minimist')(process.argv.slice(2))

let dir     = args['dir']
let name    = args['name']
let replace = args['replace']

main(dir, name, replace)
