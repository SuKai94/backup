第3章 Java程序优化
===

## 3.1 字符串优化处理

### 3.1.4 StringBuffer和StringBuilder

StringBuffer是线程安全的，StringBuilder无法保证线程安全。

#### 5.容量参数

无论是StringBuilder和StringBuffer，在初始化时都可以设置一个容量参数，在不指定容量参数时，默认是16字节 

```java
AbstractStringBuilder(int capacity) {
    value = new char[capacity]
}
```

在追加字符串时，如果容量超过实际char数组长度，则需要进行扩容：扩容策略是将容量翻倍，以新容量申请内存空间，建立新的char数组，再将原数组内容复制到新数组，因此，对于大对象的扩容会涉及大量内存复制操作。所以，如果能预先评估StringBuilder大小，能有效地节省操作，提升性能。

```java
StringBuffer sb = new StringBuffer(5888890);
StringBuilder sb = new StringBuilder(5888890);
```

## 3.2 核心数据结构

## 3.3 使用NIO提升性能

### 3.3.2 Buffer的基本原理

Buffer中三个重要参数：position, capacity, limit

```java
ByteBuffer b = ByteBuffer.allocate(15);
b.limit()
b.postion()
b.capacity()
```

### 3.3.3 Buffer的相关操作

#### 1.Buffer的创建
```java
//从堆中分配
ByteBuffer buffer = ByteBuffer.allocate(1024);
//从既有数组中创建
byte array[] = new byte[1024];
ByteBuffer buffer = ByteBuffer.wrap(array);
```

#### 2.重置和清空缓冲区

```java
rewind()：用于提取Buffer的有效数据
clear()：为重写Buffer做准备
flip()：读写模式转化
```

#### 3.读/写缓冲区

#### 4.标志缓冲区

```java
mark()：记录当前位置
reset()：恢复到mark所在位置
```

#### 5.复制缓冲区

`public ByteBuffer duplicate()`：新生成的缓冲区和原缓冲区共享相同的内存数据，新旧缓冲区独立维护各自的position, limit, mark，但新缓冲区对内存数据做写操作，原Buffer相同位置也会有相同变化

#### 6.缓存区分片

`slice()`：将在现有的缓冲区，创建新的子缓冲区，并与父缓冲区共享数据。在子缓冲区修改数据，读取父缓冲区会看到这些变化

#### 7.只读缓冲区

```java
ByteBuffer b = ByteBuffer.alllocate(15);
ByteBuffer readOnly = b.asReadOnlyBuffer();
```

只读缓冲区有效保证核心数据安全，试图对只读缓冲区做修改，会抛出java.nio.ReadOnlyBufferException。修改原缓冲区，只读缓冲区也会修改，因为是共享内存块

