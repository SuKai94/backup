# Hibernate缓存机制

- time: 2014-10-17 12:00
- tags: Hibernate

---

## 什么是缓存？

[百度百科](http://baike.baidu.com/view/2273788.htm)说得好：缓存是介于应用程序和物理数据源之间，其作用是为了降低应用程序对物理数据源访问的频次，从而提高了应用的运行性能。缓存内的数据是对物理数据源中的数据的复制，应用程序在运行时从缓存读写数据，在特定的时刻或事件会同步缓存和物理数据源的数据。

缓存的介质一般是内存，所以读写速度很快。但如果缓存中存放的数据量非常大时，也会用硬盘作为缓存介质。Hibernate缓存包括Session缓存和SessionFactory缓存。

- 一级缓存：session缓存，内置缓存，无法卸载

- 二级缓存：sessionFactory缓存，需要第三方组件支持(比如EHcache)，使用磁盘作为存储介质

![Hibernate缓存视图](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/hibernate%E7%BC%93%E5%AD%98%E6%9C%BA%E5%88%B6.png)

## 一个叼丝级别的缓存实现

```java

public class Cache {

    static Map cache = new HashMap();
    
    public static void main(String[] args) {
        User u = getUser();
    }

    public static User getUser(int id) {
        String key = User.class.getName() + id;
        User user = (User)cache.get(key);
        if(user != null) {
            return user;
        }
        user = getFromDB();
        cache.put(key, user);
        return user;
    }

    private static User getFromDB() {
        //从数据库查询User信息
    }
}
```

上述代码中, `getUser()`功能是根据id值查询User信息，它的第一步是从cache中查询，如果缓存命中，就将缓存中的User信息返回;否则就调用`getFromDB()`从数据库查询此id的User信息

## Hibernate一级缓存

这是强制性缓存，每个数据请求都会经历一级缓存，缓存命中，就取出缓存数据信息;否则就连接数据库进行查询。session对象负责管理实体对象，当你更新多个对象数据时，hibernate会尽可能延迟更新数据对象的时间，以做到减少sql语句发送数量。一旦session被关闭，所有在此session旗下的缓存全部消失。

测试：对某一条数据连续查询两次

```java
Session s = null;

try {
    s = HibernateUtil.getSession();
    User user = (User)s.get(User.class, 3);
    System.out.println(user.getName());
    User user1 = (User)s.get(User.class, 3);
    System.out.println(user1.getName());
} catch (HibernateException e) {
    throw e;
}
```

会看到hibernate仅仅只输出了一条sql语句，因为第一次从数据库查询数据后，将实体对象缓存在内存中，第二次只需从缓存读取数据信息即可，无需和数据库打交道。如果session中途关闭，会怎么样呢？

```java
s = HibernateUtil.getSession();
User user = (User)s.get(User.class, 3);
System.out.println(user.getName());
User user1 = (User)s.get(User.class, 3);
System.out.println(user1.getName());
```

很明显，控制台打印出了两条sql，说明第一次session关闭后，其缓存也跟着丢失。

## Hibernate二级缓存

二级缓存是可选缓存，由sessionFactory负责管理，默认情况下二级缓存不会开启，需要我们借助第三方插件以及配置文件开启。当然，在请求二级缓存之前肯定要去请求hibernate的一级缓存的

这里我们借助的二级缓存包是EHcache，在下载好的hibernate包的lib/optional下可以找到，将其作为第三方依赖包引入Java工程

首先，在hibernate.cfg.xml下配置二级缓存

```bash
<!-- 开启二级缓存 -->
<property name="hibernate.cache.use_second_level_cache">true</property>
<property name="hibernate.cache.region.factory_class">org.hibernate.cache.ehcache.EhCacheRegionFactory</property>
<property name="hibernate.cache.provider_configuration_file_resource_path">ehcache.xml</property>
```

然后，你需要指定缓存区域的属性，也就是要为EHCache设置配置文件：encache.xml，需放在项目根目录

```bash
<ehcache>
    <!--指定二级缓存存放在磁盘上的位置-->
    <diskStore path="user.dir"/>
    <!--我们可以给每个实体类指定一个对应的缓存，如果没有匹配到该类，则使用这个默认的缓存配置-->
    <defaultCache
        maxElementsInMemory="10000"　　//在内存中存放的最大对象数
        eternal="false"
        timeToIdleSeconds="120"
        timeToLiveSeconds="120"
        overflowToDisk="true"　　　　　//如果对象数量超过内存中最大的数，是否将其保存到磁盘中，设置成true
    />

    <!--可以给每个实体类指定一个配置文件，通过name属性指定，要使用类的全名-->
    <cache name="com.kaiyao.hibernate.hibernate.User"
        maxElementsInMemory="10000"
        eternal="false"
        timeToIdleSeconds="300"
        timeToLiveSeconds="600"
        overflowToDisk="true"
    />
</ehcache>   
```

最后一步，在User.hbm.xml增加一行配置即可

```bash
<hibernate-mapping package="com.kaiyao.hibernate.hibernate">
    <class name="User" table="person">
        <!-- 二级缓存一般设置为只读的 -->
        <cache usage="read-only"/>
        <id name="id">
            <generator class="native"/>
        </id>
        <property name="name"/>
        <property name="age"/>
    </class>
</hibernate-mapping>
```

用刚刚测试一级缓存，对某一数据连续查询两次的代码测试一下，发现控制台只打印了一条sql语句，效果显而易见。这说明二级缓存起到了作用，而且二级缓存是sessionFactory级别，即使session关闭了，也不会影响

二级缓存存储的是对象，如果你只查询对象中的某些属性，是不会加入到二级缓存中去的

## Hibernate查询缓存

要使用hibernate查询缓存功能，首先得在hibernate.cfg.xml中设置：

```bash
<!-- 开启查询缓存 -->
<property name="hibernate.cache.use_query_cache">true</property>
```

之后，在每个Query类中调用`setCacheable(boolean)`，for example： 

```java
Session session = SessionFactory.openSession();  
Query query = session.createQuery("FROM EMPLOYEE");  
query.setCacheable(true);  
List users = query.list();  
SessionFactory.closeSession();
```

当然，查询缓存也是sessionFactory级别，而且只有当hql语句完全相同时，查询缓存才产生效果，也就是说hql的参数设置也要相同

Over
