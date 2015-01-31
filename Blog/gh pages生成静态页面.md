# gh-pages分支生成静态页面

- time: 2014-07-16 12:00
- tags: Github

---

###背景

Github创建项目仓库后随即只产生一个master分支，只需要再添加`gh-pages`分支就可以创建静态页面了，创建后的页面url是：`Github用户名.github.io/创建的仓库名`，这利用了项目站点（即`Project Pages`）的方式，还有一种创建站点的方式叫做`User/Organization Pages`

###使用Project Pages创建静态页面

1.在Github上创建一个项目仓库，暂时叫MyPages

2.建立与之对应的本地仓库：

```bash
cd 你要存放的目录
mkdir MyPages
cd MyPages
git init
git remote add origin https://github.com/Github用户名/项目仓库名.git
touch README.md
git add README.md
git commit -m "init"
git push origin master
```

3.使用命令行创建干净的`gh-pages`分支，用到git底层命令：`git symbolic-ref`

```bash
git symbolic-ref HEAD refs/heads/gh-pages
rm .git/index
git clean -fdx
echo "My Pages Works">index.html
git add index.html
git commit -m "init My Pages"
git push origin gh-pages
```

4.OK，访问一下上面提及到的url吧：`Github用户名.github.io/创建的仓库名`（刚执行完上述命令，可能需要等待一段时间再去访问），是不是出现了`My Pages Works`

5.修改index.html，改成你想要显示的一切内容

如果你不会写html的话，你可以先用`MarkDown`写下你想表达的内容，然后转化成html就行

修改好index.html，别忘记再把它提交到项目的gh-pages分支
