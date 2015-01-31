# Android导航抽屉初使用

- time: 2014-12-21 12:55
- tags: Android

---

我翻看过许多Android平台的APP，发现绝大部分APP导航功能都是使用Navigation Drawer和ActionBar，于是研究如何使用导航抽屉。

### Navigation Drawer [介绍](http://hddev.blog.51cto.com/3365350/1254472)

### Navigation Drawer [使用Demo](http://blog.chengyunfeng.com/?p=493)

### 使用过程记录

`activity_main.xml`中ListView用来设置抽屉菜单内容；我用ImageView和TextView实现一个list_item，效果如下：

未打开抽屉前：

![未打开android抽屉菜单](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/android_na_before.png)

打开抽屉后：

![打开android抽屉菜单](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/android_na_after.png)

实现很简单，只需为ListView添加一个自定义适配器即可

这里涉及点击高亮显示问题：

在`drawer_list.xml`layout文件中，需要将`android:background="?android:attr/activatedBackgroundIndicator"`属性添加在`LinearLayout`中，而非`LinearLayout`的`ImageView`或`TextView`中，不然可能造成`ImageView`或`TextView`其中一个不能高亮显示

