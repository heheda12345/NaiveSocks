# NaiveSocks

一款简单的加密代理应用。

支持密码和密钥认证，提供了配置文件保存功能。

实现了加密性 & 数据完整性保护，内部加密算法为 AES，哈希函数为 MD5。

Python 版本应不低于 3.6。

使用示例：
```
python client.py -k abc -s 127.0.0.1
python server.py -k abc -s 127.0.0.1
```

可以通过添加 `--help` 选项了解具体选项的使用方法。

参考设计：https://github.com/linw1995/lightsocks-python