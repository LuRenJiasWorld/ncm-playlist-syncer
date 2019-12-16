import os
import requests
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3, APIC, TPE1, TIT2, TALB, TSO2, TRCK, TYER, error
from PIL import Image
import platform


class NetEaseMusicAssistant:

	# 下载指定文件，重命名为指定文件名到指定目录
	def download_file(self, url, file_path):
		try:	
			os.system("wget -q \"{}\" -O \"{}\"".format(url, file_path))
			print("\t -> {}下载成功".format(file_path))
			return "success"
		except Exception:
			print("\t -> {}下载失败".format(file_path))
			return "fail"

	# 对图片进行压缩（主要解决Sony Walkman不识别太大封面文件的情况，反正Walkman分辨率也就那样，小图片无所谓的）
	def image_resize(self, file_path, max_size=(640, 640), quality=30):
		try:
			img_obj = Image.open(file_path)
		except IOError:
			return "fail"

		if img_obj.size[0] > max_size[0] or img_obj.size[1] > max_size[1]:
			img_obj.thumbnail(max_size, Image.ANTIALIAS)
			try:
				img_obj.save(file_path, quality=quality)
				return "success"
			except IOError:
				return "fail"

	# 为MP3文件附加元信息
	def id3_metadata_append(self, file_path, cover_path, title, artist, album, album_artist, track_num_current, year):
		# 检测文件是否有效
		try:
			audio_obj = MP3(file_path, ID3=ID3)
		except HeaderNotFoundError:
			print("不是有效的MP3文件")
			return "fail"

		# 如果音乐内没有ID3信息，新建ID3信息
		if audio_obj.tags is None:
			try:
				audio_obj.add_tags()
				audio_obj.save()
			except error as e:
				print("无法写入ID3信息，错误信息：" + str(e))
				return "fail"

		# 修改ID3标签
		id3_info = ID3(file_path)

		# 删除已有的APIC帧，避免重复写入
		if id3_info.getall("APIC"):
			id3_info.delall("APIC")

		# 添加封面
		id3_info.add(
			APIC(
				encoding=0,			 # LATIN1编码
				mime="image/jpeg",	   # jpeg格式
				type=3,				 # 封面图像
				data=open(cover_path, "rb").read()
			)
		)

		# 添加歌曲名
		id3_info.add(
			TIT2(
				encoding=3,			 # UTF8编码
				text=title
			)
		)

		# 添加歌手名
		id3_info.add(
			TPE1(
				encoding=3,
				text=artist
			)
		)

		# 添加专辑名
		id3_info.add(
			TALB(
				encoding=3,
				text=album
			)
		)

		# 添加唱片集艺术家
		id3_info.add(
			TSO2(
				encoding=3,
				text=album_artist
			)
		)

		# 添加当前音轨
		id3_info.add(
			TRCK(
				encoding=3,
				text=track_num_current
			)
		)

		# 添加年份
		id3_info.add(
			TYER(
				encoding=3,
				text=year
			)
		)

		# 保存文件(v2.3格式)
		id3_info.save(v2_version=3)


class Util:

	# MacOS下实现通知
	def __notify_command_osx(self, msg, msg_type, t=None):
		command = '/usr/bin/osascript -e "display notification \\\"{}\\\" {} with title \\\"Netease Cloud Music Playlist Syncer\\\""'
		sound = 'sound name \\\"/System/Library/Sounds/Ping.aiff\\\"' if msg_type else ''
		return command.format(msg, sound)

	# Linux下实现通知
	def __notify_command_linux(self, msg, t=None):
		command = '/usr/bin/notify-send "' + msg + '"'
		if t:
			command += ' -t ' + str(t)
		command += ' -h int:transient:1'
		return command

	# 通知方法
	def notify(self, msg, msg_type=0, t=None):
		if platform.system() == 'Darwin':
			command = self.__notify_command_osx(msg, msg_type, t)
		else:
			command = self.__notify_command_linux(msg, t)
		os.system(command.encode('utf-8'))
