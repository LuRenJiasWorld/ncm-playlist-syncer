# -----------------------------------------------------------
# ------------Netease Cloud Music Playlist Syncer------------
# ---https://github.com/LuRenJiasWorld/ncm-playlist-syncer---
# ----------------- © LuRenJiasWorld 2018 -------------------
# -----------------------------------------------------------

import time
import os
from functions import NetEaseMusicAssistant, Util
from MusicBoxApi import api as NetEaseApi

phone_number = ""
password = ""
# 网易邮箱绑定登录
email = ""
email_password = md5(b'Your Password').hexdigest()
playlist_id = ""


def init():
	# -------------------
	# ------环境配置------
	# -------------------
	# 实例化
	netease = NetEaseApi.NetEase()
	util = Util()
	ncm = NetEaseMusicAssistant()

	# 处理不成功的文件
	unsuccessful = []

	# --------------------------
	# ------开始获取播放列表------
	# --------------------------
	# 登录
	netease.phone_login(phone_number, password)

	# 获取音乐播放列表
	data = netease.playlist_detail(playlist_id)

	# 读取本地音乐库最新音乐ID
	with open("local.dat", "r") as file:
		newest_id = file.read()

	# ----------------------
	# ------检索新增音乐------
	# ----------------------
	# 新音乐列表
	new_music = []

	# 遍历播放列表，寻找本地最新ID所在偏移位置
	for each in range(len(data)):
		if data[each]["id"] != int(newest_id):
			new_music.append(data[each])
		else:
			break

	# 如果没有新音乐，退出
	if len(new_music) == 0:
		print("没有新音乐待下载")
		util.notify("没有新音乐待下载")
		exit()

	# ----------------------
	# ------下载新增音乐------
	# ----------------------
	# 写入数据
	for each in range(len(new_music)):

		# --------------------
		# ------元信息定义------
		# --------------------
		# 临时文件名
		temp_file_path = "tmp/temp.mp3"

		# 封面文件名
		cover_path = "tmp/cover/" + str(new_music[each]["id"]) + ".png"

		# 音乐文件URL
		music_url = NetEaseApi.geturl_new_api(new_music[each])[0]

		# 艺人姓名(ID3使用)
		artists_name = ""
		for each_artist in range(len(new_music[each]["artists"])):
			artists_name = artists_name + new_music[each]["artists"][each_artist]["name"] + ";"
		artists_name = artists_name[:-1]

		# 音乐文件名
		file_path = "tmp/music/" + str(artists_name).replace(";", ",") + " - " + new_music[each]["name"] + ".mp3"

		# 专辑艺术家姓名
		album_artist_name = new_music[each]["album"]["artist"]["name"]

		# 专辑发行年份
		time_obj = time.localtime(int(str(new_music[each]["album"]["publishTime"])[:-3]))
		year = time.strftime("%Y", time_obj)

		print("正在处理" + str(each + 1) + " / " + str(len(new_music)) + "：" + str(artists_name).replace(";", ",") + " - " + new_music[each]["name"] + ".mp3")
		util.notify("正在处理" + str(each + 1) + " / " + str(len(new_music)) + "：" + str(artists_name).replace(";", ",") + " - " + new_music[each]["name"] + ".mp3")

		# ----------------------
		# ------下载所需文件------
		# ----------------------
		# 下载音乐文件
		ncm.download_file(music_url, file_path)

		# 下载封面文件
		ncm.download_file(new_music[each]["album"]["picUrl"], cover_path)

		# -------------------
		# ------处理文件------
		# -------------------
		# 封面缩放
		ncm.image_resize(file_path, (640, 640), 70)

		# 写入ID3信息
		try:
			# 放入临时目录
			os.rename(file_path, temp_file_path)

			# 写入ID3
			ncm.id3_metadata_append(
				temp_file_path,
				cover_path,
				new_music[each]["name"],
				artists_name,
				new_music[each]["album"]["name"],
				album_artist_name,
				str(new_music[each]["no"]),
				year,
			)

			# 放回原目录
			os.rename(temp_file_path, file_path)

		except FileNotFoundError as e:
			print("错误-文件找不到：" + str(e))
			unsuccessful.append([file_path])

	# -------------------
	# ------善后处理------
	# -------------------
	# 写入新的ID
	with open("local.dat", "w") as file:
		file.write(str(new_music[0]["id"]))

	# 提示用户
	print("下载完成！")
	util.notify("下载完成！")
	print("本次下载音乐%d首，列表如下：" % len(new_music))
	for each in range(len(new_music)):
		print(new_music[each]["name"] + " - " + new_music[each]["artists"][0]["name"])


# ---------------
# ------入口------
# ---------------
if __name__ == "__main__":
	init()
