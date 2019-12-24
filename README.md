# NaiveSocks

参考设计：

实现了加密性 & 数据完整性保护

支持密码和密钥认证，提供了配置文件保存功能

Python Version >= 3.6

使用示例：
```
python client.py -k abc -s 127.0.0.1
python server.py -k abc -s 127.0.0.1
```

可以通过添加 `--help` 选项了解其他选项的使用方法

参考设计：https://github.com/linw1995/lightsocks-python