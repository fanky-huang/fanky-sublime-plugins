# -*- coding: utf-8 -*-
"""
# 查找文中所有中英文相邻之间，没有空格的地方，加上空格间隔
# author: fanky
# date: 10/20/2018
"""

import sublime_plugin

_pattern = r"([0-9A-Za-z][\x{4e00}-\x{9fa5}])|([\x{4e00}-\x{9fa5}][0-9A-Za-z])"

class fanky_space_start_endCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# 前面是汉字，后面是英文
		regions = self.view.find_all(_pattern)
		for region in reversed(regions):
			text = self.view.substr(region)
			self.view.replace(edit, region, text[0] + ' ' + text[1])
