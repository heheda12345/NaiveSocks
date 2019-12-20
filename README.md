# NaiveSocks

参考https://github.com/linw1995/lightsocks-python

以下文件是直接复制粘贴的
```
run_local.py, run_server.py, utils/config.py
```

加解密相关的东西先粘过来，后面还要用公钥/私钥重写
```
cipher.py, password.py
```

暂时没有做数据完整性保护

使用示例：
```
python run_remote.py -k abc -s 127.0.0.1
python run_local.py -k abs -s 127.0.0.1 # 应该改成远程服务器地址
```