## markdown高级技巧


### 解决图片居中和大小问题
* 常见方案：
```markdown
    ![Img](url){width="60%"}  有些编辑器不认
    ![Img](url =600x600)  有些编辑器不认
```
* 解决方案：使用p标签
```markdown
    <p align = "center"><img  src="url" width="60%" /></p>
```

### 解决表格等其他复杂元素的居中
方案：使用div标签
```markdown
    <div align = "center">
    ...
    </div>
```



### 如何学习markdown
* github上的开源项目README.md