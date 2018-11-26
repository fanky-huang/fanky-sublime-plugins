# -*- coding: utf-8 -*-
# 让 Tab 键仅仅是输入 \t

import time
import sublime
import sublime_plugin

class fanky_tabCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		region = self.view.sel()[0]
		a, b = region.a, region.b
		if a == b:
			self.view.insert(edit, b, "\t")
			return

		count = 0
		self.view.sel().clear()
		regions = self.view.lines(region)
		for reg in reversed(regions):
			if reg.a == reg.b: continue
			self.view.insert(edit, reg.a, "\t")
			count += 1
		a = regions[0].a
		b = regions[-1].b + count                    # 补加中间插入的 \t 数量
		self.view.sel().add(sublime.Region(a, b))


class fanky_shift_tabCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		region = self.view.sel()[0]
		a, b = region.a, region.b
		if a == b:
			self.view.insert(edit, b, "    ")
			return

		count = 0
		self.view.sel().clear()
		regions = self.view.lines(region)
		for reg in reversed(regions):
			if reg.a == reg.b: continue
			line = self.view.substr(reg)
			if line.startswith("\t"):
				self.view.erase(edit, sublime.Region(reg.a, reg.a+1))
				count += 1
				continue

			spaces = 0
			length = min(4, len(line))
			for i in range(length):
				if (line[i] != ' '): break
				spaces += 1
			if spaces > 0:
				self.view.erase(edit, sublime.Region(reg.a, reg.a+spaces))
				count += spaces

		a = regions[0].a
		b = regions[-1].b - count
		self.view.sel().add(sublime.Region(a, b))
