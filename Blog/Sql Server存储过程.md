# Sql Server存储过程

- time: 2014-05-28 12:00
- tags: Sql Server

---

###1.概述：什么是存储过程
存储过程是一组为了完成特定功能的SQL语句集，经预编译后存储在数据库中的。可以由应用程序调用执行。

#####有以下几个特点（优点）：

1.存储过程是预编译的。在首次运行一个存储过程时，系统对其进行分析，优化，并给出最终存放到系统表中的执行计划,方便之后用户程序的调用。如果某程序需要使用大量T-SQL代码或者需要重复执行某个功能，存储过程执行速度肯定比单纯使用T-SQL批量处理代码要快得多。使用T-SQL批量处理代码，sql server需要每次对其进行编译和优化，而存储过程只需要第一次的编译和优化。

2.减少了客户机和服务器之间的通信量。应用程序只需要通过网络向服务器发送存储过程的名字和参数，就可以得到自己想要的功能或数据。不像单纯使用数百行的T-SQL代码，这需要向服务器发送数百行的代码。

3.允许模块化程序设计。存储过程在被创建之后可以被应用程序多次调用执行。使用过程中也可以随时对存储过程进行修改，但对你的应用程序代码毫无影响，大大提高了程序的可移植性。

#####存储过程的分类：
1.系统存储过程

2.用户自定义的存储过程

###2.用户自定义存储过程，基本语法

#####1.变量声明：
```bash
--定义一个存储过程需要使用的变量
declare @variable int
--多变量声明
declare @variable int, @va varchar(10), .... 
```
```bash
--存储过程需要传入的参数变量定义
@variable int
```
```bash
--实例
create procedure procedure_name
	@variable int                --参数声明
as
begin
	declare @va varchar(10)      --变量声明
	select @variable = 22        --变量赋值
	...
end

--执行存储过程
exec procedure 22    --22为传入的参数
```

#####2.变量赋值
再变量前加上select 或者 set，但是二者有所不同

```bash
				          set 		      select
同时对多个变量同时赋值        不支持		      支持
表达式返回多个值时           出错			  将返回的最后一个值赋给变量
表达式未返回值              变量被赋为null	  变量保持原值
```

#####3.条件控制语句
```bash
if(condition)
begin
	...
end
```

#####4.循环控制语句
```bash
while(condition)
begin
	...
end
```

###3.实例分析
#####1.带输入参数的存储过程
```bash
--创建存储过程
create procedure pro_name1
	@variable varchar(20)  				--参数声明
as 
begin
	....
end

--执行存储过程
--参数传递方式1,多个参数以 , 号隔开
exec pro_name1 @variable = 'Worlds' 	-- 参数传入
--参数传递方式2
exec pro_name1 'Worlds'					-- 参数传入
```

#####2.带输出参数的存储过程
```bash
--创建存储过程
create procedure pro_name2
@variable1 varchar(20),  				--参数声明
@variable2 varchar(20) output 			--输出参数：output标识
as
begin
	...
end

--执行存储过程
declare @returnname varchar(20)
exec pro_name2 'Worlds', @returnname output  -- 参数传入
select @returnname
```

###4.实战分析
```bash
题目：
假设数据库中有个一个表，为KC表，建表的语句如下。
CREATE TABLE kc
(
	K VARCHAR(100),
	V VARCHAR(100)
)

要求编写一个存储过程Insert_data，要求完成如下功

1. 传入2个字符串变量，其中，每个字符串是用分号（；）分隔的字串形式，比如str1=’ab12;ab;cccc;tty’, str2=’1;6sf;8fffff;dd’, 注意，字符串是用户输入的，不能固定值、长度、和分号个数。
2. 执行完毕存储过程后，要求根据分号提取字符串的字串，并一一插入到表Kc中。例如上面的str1, str2传入后，kc表中数据为：
k        c
ab12     1
ab       6sf
cccc     8fffff
tty      dd
```

代码如下：

```bash
--建立存储过程insert_data
create proc insert_data
	@str1 varchar(max),
	@str2 varchar(max)
as
begin
	declare @len1 int,
				@len2 int,
				@start1 int,
				@start2 int,
				@pos1 int,
				@pos2 int,
				@leftstring1 varchar(max),
				@leftstring2 varchar(max),
				@substring1 varchar(max),
				@substring2 varchar(max)
	select @len1 = len(@str1);
	select @len2 = len(@str2);
	select @start1 = 1;
	select @start2 = 1;
	select @leftstring1 = 'x';
	select @leftstring2 = 'x';
	while(len(@leftstring1) !=0 or len(@leftstring2) != 0 )
	begin
		select @pos1 = charindex(';', @str1, @start1);
		select @pos2 = charindex(';', @str2, @start2);
		if(@pos1 = 0 and @pos2 = 0)
		begin
			select @substring1 = substring(@str1, @start1 , @len1-@start1+1);
			select @substring2 = substring(@str2, @start2 , @len2-@start2+1);
			select @leftstring1 = NULL;
			select @leftstring2 = NULL;
		end
		else if(@pos1 = 0 and @pos2 != 0)
		begin
			select @substring1 = substring(@str1, @start1 , @len1-@start1+1);
			select @substring2 = substring(@str2, @start2 , @pos2-@start2);
			select @start1 = @len1 + 1;
			select @start2 = @pos2 + 1;
			select @leftstring1 = NULL;
			select @leftstring2 = substring(@str2, @start2, @len2-@start2+1);
		end
		else if(@pos1 != 0 and @pos2 = 0)
		begin
			select @substring1 = substring(@str1, @start1 , @pos1-@start1);
			select @substring2 = substring(@str2, @start2 , @len2-@start2+1);
			select @start1 = @pos1 + 1;
			select @start2 = @len2 + 1;
			select @leftstring1 = substring(@str1, @start1, @len1-@start1+1);
			select @leftstring2 = NULL;
		end
		else
		begin
			select @substring1=substring(@str1, @start1,@pos1-@start1);
			select @substring2=substring(@str2, @start2,@pos2-@start2);
			select @start1=@pos1+1;
			select @start2=@pos2+1;
			select @leftstring1 = substring(@str1, @start1, @len1-@start1+1);
			select @leftstring2 = substring(@str2, @start2, @len2-@start2+1);
		end
		insert into kc values(@substring1, @substring2);
	end
end
```
```bash
---执行存储过程
execute insert_data 'a;b;c;d;;f', 'e;f;g;h;z;l;m'
```

