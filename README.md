# Netease Cloud Music Playlist Syncer

——网易云音乐播放列表同步(Python 3.6)



## 功能

- 同步播放列表
- 将服务器端的播放列表与本机存储的信息进行同步
- 下载播放列表中新增的音乐（ID3信息完整）



## 引用库

- Mutagen https://github.com/quodlibet/mutagen
- Pillow(PIL) https://github.com/python-pillow/Pillow
- MusicBoxApi(二次修改) https://github.com/LuRenJiasWorld/MusicBoxApi

## 使用方法

1. 安装以上的引用库
2. 打开init.py，输入你的个人信息(`phone_number`为手机号，`password`为密码（如果使用邮箱登录，`email为邮箱地址，email_password为密码`），`playlist_id`获取方式见博客[https://untitled.pw/development/511.html]
3. 将浏览器中`_ntes_nnid`  与 `_ntes_nuid` 两个Cookie输入进header_cookie中，格式参照html请求头中的参数 ，示例：`_ntes_nnid=示例; _ntes_nuid=示例` ，Cookie来源于[https://music.163.com/]，Cookie获取方式由于各个浏览器差异，无法一一列举，请自行翻阅资料
4. （仅第一次需要以上配置，各配置均可重复使用，Cookie的过期时间长到可以无视）
5. 打开local.dat，输入按照以上教程链接方式获取的该播放列表最新音乐ID（不要换行），保存
6. 运行init.py



### 作为定时任务

示例：每小时执行一次

```bash
0 * * * * python3 /blablablabla/init.py
```

（调用python3的命令在不同操作系统上不同，具体请参考操作系统的环境变量，还不清楚的话：百度，请！）

