# -*- coding: utf-8 -*-
"""
# 查找文中所有中英文相邻之间，没有空格的地方，加上空格间隔
# author: fanky
# date: 10/26/2018
"""

import sublime
import sublime_plugin

# 中文符号（全部都是一次只跳一个）
_cnSymbos = set("·～！＃￥％……＆×（）－——＋＝【】｛｝｜＼《》，。？、：；”“＇")

# 英文符号（排在一起的符号，光标一次性跨过）
_enSymbos = set(chr(ch) for ch in range(ord('!'), ord('0')))
_enSymbos = _enSymbos.union(chr(ch) for ch in range(ord(':'), ord('A')))
_enSymbos = _enSymbos.union(chr(ch) for ch in range(ord('['), ord('a')))
_enSymbos = _enSymbos.union(chr(ch) for ch in range(ord('{'), ord('`') + 1))
_enSymbos.add('~')

# 下划线通常属于变量的合法字符，所以不将下划线归为英文符号
_enSymbos.remove('_')


# -----------------------------------------------------------------------------
# 单词边界确立
# -----------------------------------------------------------------------------
# 是否是英文字符
def _isEnChar(ch):
	return ('A' <= ch <='Z') or ('a' <= ch <= 'z') or \
		(ch == '_') or (ch.isdigit())

# 是否是英文符号
def _isEnSymbo(ch):
	return ch in _enSymbos

# 是否是空白字符（空格和 tab）
def _isEmptyChar(ch):
	return ch == ' ' or ch == '\t'

# 是否是中文字符
# 注意：这里认为所有码值大于 127 的字符都是中文字符
def _isCnChar(ch):
	return not _isEnChar(ch) and \
		not _isEmptyChar(ch) and \
		not _isEnSymbo(ch) and \
		not _isCnSymbo(ch) and \
		not _isNewline(ch)

# 是否是中文符号
def _isCnSymbo(ch):
	return ch in _cnSymbos

# 是否是换行符
def _isNewline(ch):
	return ch == '\r' or ch == '\n'


# -------------------------------------------------------------------
# LeftWordStart
# -------------------------------------------------------------------
class LeftWordStart(object):
	def __init__(self, view):
		self.view = view

	# 往回跳一组空白字符
	def __skipEmptyChars(self, site):
		while site > 0:
			ch = self.view.substr(site - 1)
			if _isEmptyChar(ch):
				site -= 1
			elif _isNewline(ch):
				break
			else:
				site = self.__getWordStart(site - 1)
				break
		return site

	# 往回跳一组英文符号
	def __skipEnSymbos(self, site):
		while site > 0:
			ch = self.view.substr(site - 1)
			if _isEnSymbo(ch):
				site -= 1
			else:
				break
		return site

	# 回跳一个英语单词
	def __skipEnWord(self, site):
		while site > 0:
			ch = self.view.substr(site - 1)
			if _isEnChar(ch):
				site -= 1
			else:
				break
		return site

	# 往回跳一串中文
	def __skipCnWord(self, site):
		while site > 0:
			ch = self.view.substr(site - 1)
			if _isCnChar(ch):
				site -= 1
			else:
				break
		return site

	# 往回跳一个换行
	def __skipNewLine(self, site):
		ch = self.view.substr(site - 1)
		if ch == '\r': site -= 1
		return site

	# -----------------------------------------------------
	# 获取光标左边单词起始位置
	def __getWordStart(self, site):
		ch = self.view.substr(site)
		if _isCnSymbo(ch):                          # 中文符号只跳一个
			return site

		if _isNewline(ch):                          # 换行
			site = self.__skipNewLine(site)
		elif _isEmptyChar(ch):                      # 空白字符
			site = self.__skipEmptyChars(site)
		elif _isEnSymbo(ch):                        # 英文符号
			site = self.__skipEnSymbos(site)
		elif _isEnChar(ch):                         # 英文单词
			site = self.__skipEnWord(site)
		else:                                       # 其他文本
			site = self.__skipCnWord(site)
		return 0 if site < 0 else site

	def getSite(self, site):
		return self.__getWordStart(site - 1)        # 获取左边单词的起始位置


# -------------------------------------------------------------------
# RightWordEnd
# -------------------------------------------------------------------
class RightWordEnd(object):
	def __init__(self, view):
		self.view = view

	# 往后面跳一组空白字符
	def __skipEmptyChars(self, maxIndex, site):
		while site < maxIndex:
			site += 1
			ch = self.view.substr(site)
			if _isEmptyChar(ch):
				continue
			else:
				break
		return site

	# 往后面跳一组英文符号
	def __skipEnSymbos(self, maxIndex, site):
		while site < maxIndex:
			site += 1
			ch = self.view.substr(site)
			if _isEnSymbo(ch):
				continue
			elif _isEmptyChar(ch):
				site = self.__skipEmptyChars(maxIndex, site)
			break
		return site

	# 回跳一个英语单词
	def __skipEnWord(self, maxIndex, site):
		while site < maxIndex:
			site += 1
			ch = self.view.substr(site)
			if _isEnChar(ch):
				continue
			elif _isEmptyChar(ch):
				site = self.__skipEmptyChars(maxIndex, site)
			break
		return site

	# 往后面跳一个其他文字组
	def __skipCnWord(self, maxIndex, site):
		while site < maxIndex:
			site += 1
			ch = self.view.substr(site)
			if _isCnChar(ch):
				continue
			elif _isEmptyChar(ch):
				site = self.__skipEmptyChars(maxIndex, site)
			break
		return site

	# 往回跳一个退格和换行
	def __skipNewLine(self, maxIndex, site):
		ch = self.view.substr(site)
		site += 1
		if ch == '\r':
			site += 1
		return site

	# -----------------------------------------------------
	# 获取光标左边单词起始位置
	def __getWordEnd(self, maxIndex, site):
		ch = self.view.substr(site)
		if _isCnSymbo(ch):                                  # 中文符号只跳一个
			return site + 1

		if _isNewline(ch):                                  # 换行
			site = self.__skipNewLine(maxIndex, site)
		elif _isEmptyChar(ch):                              # 空白字符
			site = self.__skipEmptyChars(maxIndex, site)
		elif _isEnSymbo(ch):                                # 英文符号
			site = self.__skipEnSymbos(maxIndex, site)
		elif _isEnChar(ch):                                 # 英文单词
			site = self.__skipEnWord(maxIndex, site)
		else:                                               # 其他文本
			site = self.__skipCnWord(maxIndex, site)
		return maxIndex if site > maxIndex else site

	def getSite(self, site):
		maxIndex = self.view.size()
		return self.__getWordEnd(maxIndex, site)            # 获取左边单词的起始位置


# -----------------------------------------------------------------------------
# commands
# 提示：
# 	习惯上，我并不会对类名采用下划线方式命名，这里之所以对命令类名采用下划线命名方式，主要目的是
#	sublime 会主动将驼峰式命名转化为下划线方式，所以为了命令与类名保持一致性，这里类名也采用下
#	划线方式命名，以方便在快捷键设置文件中搜索。
# -----------------------------------------------------------------------------
# -------------------------------------------------------------------
# 左移一个单词
# -------------------------------------------------------------------
class fanky_move_left_wordCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		extend = args.get("extend", False)                # 是否选中文本
		sel = self.view.sel()
		a, b = sel[0].a, sel[0].b                         # 之前选区位置

		getter = LeftWordStart(self.view)
		site = getter.getSite(b)                          # 光标前一个单词的起始位置

		sel.clear()                                       # 清除旧选区
		if extend:
			sel.add(sublime.Region(a, site))              # 设置光标位置
		else:
			sel.add(sublime.Region(site, site))           # 设置光标位置

# -------------------------------------------------------------------
# 右移一个单词
# -------------------------------------------------------------------
class fanky_move_right_wordCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		extend = args.get("extend", False)                # 是否选中文本
		sel = self.view.sel()
		a, b = sel[0].a, sel[0].b                         # 之前选区位置

		getter = RightWordEnd(self.view)
		site = getter.getSite(b)                          # 光标后一个单词的结束位置

		sel.clear()                                       # 清除旧选区
		if extend:
			sel.add(sublime.Region(a, site))              # 设置光标位置
		else:
			sel.add(sublime.Region(site, site))           # 设置光标位置

# -------------------------------------------------------------------
# 删除左边一个单词
# -------------------------------------------------------------------
class fanky_del_left_wordCommand(sublime_plugin.TextCommand):
	# 如果左边是一组空格，则只删除这组空格，不删除空格前面的单词
	def __leftSpaceStart(self, site):
		ch = self.view.substr(site - 1)
		if not _isEmptyChar(ch):
			return -1

		site -= 1
		while site > 0:
			ch = self.view.substr(site - 1)
			if _isEmptyChar(ch):
				site -= 1
			else:
				break
		return 0 if site < 0 else site


	def run(self, edit):
		sel = self.view.sel()
		a, b = sel[0].a, sel[0].b                            # 之前选区位置
		if a != b:                                           # 如果有选区，则只删除选区
			self.view.erase(edit, sel[0])
			return

		# 如果光标前是一组空白字符，将仅仅删除这组空白符，这与光标向左移动一个单词，有点区别
		site = self.__leftSpaceStart(b)
		if site < 0:                                         # 光标前不是空白字符
			getter = LeftWordStart(self.view)
			site = getter.getSite(b)                         # 光标前一个单词的起始位置
		self.view.erase(edit, sublime.Region(a, site))

# -------------------------------------------------------------------
# 删除右边一个单词
# -------------------------------------------------------------------
class fanky_del_right_wordCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sel = self.view.sel()
		a, b = sel[0].a, sel[0].b                            # 之前选区位置
		if a != b:                                           # 如果有选区，则只删除选区
			self.view.erase(edit, sel[0])
		else:
			getter = RightWordEnd(self.view)
			site = getter.getSite(b)                         # 光标后一个单词的结束位置
			self.view.erase(edit, sublime.Region(a, site))
