# Java NIO初探

- time: 2014-08-13 12:00
- tags: Java, NIO

---

有人称NIO为**New IO**,有人称其为**non-blocking IO**,两个都是NIO的特征表现

NIO有两个版本，下面内容基于版本１

它是JDK提供的标准库，让你突破标准同步IO的瓶颈，实现异步非阻塞的IO执行操作，它利用将多个IO的阻塞复用在同一个selector上（IO多路复用技术），使得单线程也能够处理多个client对server的请求，有效避免了大量线程的资源开销，如果再结合多线程，能承受很大的并发量

重点学习下NIO Socket知识

### Blocking versus non-blocing IO

看两张图，分别是阻塞IO的工作方式和非阻塞IO的工作方式（图片摘自《Netty in Action》）

![blocking IO](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/bIO.png)

![non-blocking IO](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/nbIO.png)

- IO面向流<->NIO面向通道与缓冲：IO从流中读取数据直至读完，读取的数据没有缓存;NIO从通道读取数据到buffer，灵活性加强，但处理容易出错
- 阻塞IO<->非阻塞IO：阻塞IO中线程请求读写操作时，处于阻塞状态，直至数据读取操作完成前，不能进行其余事件;而NIO的一个线程从一个通道请求读取数据后，处于非阻塞模式，无需等待数据读取完成，而是利用这段空闲时间，线程去进行其余通道的IO操作


### NIO的核心

- Channels
- Buffers
- Selectors

NIO基于Channel和Buffer进行工作，数据在Channel和Buffer之间进行传递

![Channel-Buffer](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/cb.png)

Selector用于监听许许多多的Channel，是IO多路复用的关键（见上图）

### Channel

Java NIO有哪些通道？

- FileChannel：File
- DatagramChannel：UDP
- ScoketChannel：TCP
- ServerSocketChannel：监听TCP连接

### Buffer

Buffer内部结构：（图片拷贝自[并发编程网站](http://ifeve.com/)），图非常好！

![Buufer](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/buffer.png)

- capacity：标志Buffer的存储大小，若Buffer数据存储已满，需要及时清除
- limit：写模式下代表还能往里面写多少数据，读模式代表最多能读到多少数据
- position：写数据时候position是当前位置，读数据时候看情况：可以从特定位置读取，还有从写模式切换到读模式，position就被重置为0

有许多Buffer类型，说一下ByteBuffer（其余类似）

典型用法：

- 写data到ByteBuffer
- ByteBuffer.flip（），将Buffer从写模式到读模式
- 从ByteBuffer读数据
- ByteBuffer.clear()或者ByteBuffer.compact()（前一种是清楚Buffer中所有数据，后一种是清楚已读数据，将未读数据拷贝到ByteBuffer起始位置）

还有两个方法值得一提：

- **ByteBuffer.allocate(1024)：**对Buffer对象进行分配，这里分配了1024字节
- **ByteBuffer.duplicate()：**对ByteBuffer对象复制，返回值是复制后的ByteBuffer

还有一种创建ByteBuffer的方法：ByteBuffer,allocateDirect(int)，这是在JVM heap外申请内存，使得ByteBuffer突破JVM内存限制，调用系统直接分配的内存，此时ByteBuffer不为JVM相关工具所管理，JVM垃圾回收机制不作用于ByteBuffer，所以监控ByteBuffer很困难，内存泄漏定位不清晰，可以用GC机制强行垃圾回收。当使用较大数据块的时候，就能提高效率

### Selector

线程的花销很大，selector帮助开发者突破IO的瓶颈，是处理多个Channel的组件，管理着channel的连接，数据读写等操作！

典型用法：

- 创建selector：`Selector selector = Selector.open()`
- 将通道注册进Selector：此时为了与Selector一起使用，需将Channel设为非阻塞模式：`channel.configureBlocking(false)`，然后将Channel注册进去：`channel.register(selector, SelectionKey.OP_ACCEPT)`
- 当channel被注册，你需要指定你感兴趣的监听事件：**OP_ACCEPT,OP_CONNECT,OP_READ,OP_WRITE**
- 运行Selector.select()进入阻塞，直到某个事件发生
- 如果某些通道准备就绪，select()方法就非阻塞，通过selector的selectedkeys()方法获取所有**SelectionKey(集合)**，之后遍历key集合，进行你想要的操作

```java
Set selectedKeys = selector.selectedKeys();
Iterator keyIterator = selectedKeys.iterator();
while(keyIterator.hasNext()) 
{
    SelectionKey key = keyIterator.next();
    if(key.isAcceptable()) 
    {
        // TODO
    }
    if(key.isConnectable()) 
    {
        // TODO 
    }
    if(key.isReadable())
    {
        // TODO
    }
    if(key.isWritable())
    {
        // TODO
    }
}
```

值得一提：可以将数据attach到SelectionKey上，就可以让Channel拥有自己专属的ByteBuffer

- 将数据附加到key：**selectionKey.attch(ByteBuffer)**
- 将key上附加的数据取出：**ByteBuffer a = (ByteBuffer)selectionKey.attachment()**

完整Server端实例：[View](https://github.com/su-kaiyao/Java-Practice/blob/master/test/src/main/java/com/kaiyao/test/NioEchoServer.java)

### NIO problems

- 跨平台兼容性问题：在linux下正常使用NIO，不代表windows下同样如此
- ByteBuffer无扩展性：如果你想尽量减少内存拷贝，想用ByteBuffer数组扩容，来代替先前的ByteBuffer,这是不可能的，JDK NIO的ByteBuffer有一个私有的构造函数，我们无法去扩展ByteBuffer
- 分散和收集机制可能会导致内存泄漏
- epoll bug：如果没有事件发生，那你的`selector.select()`语句将一直在while(true)中阻塞，有吃掉内存的隐患

...

Those are reasons why we choose Netty



