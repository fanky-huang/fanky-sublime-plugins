# fanky-sublime-plugins
sublime text plugins

1、skip_word.py
  plugin "skip_word.py" contains 4 commands:
  1) fanky_move_left_word
    move the cursor to the start of left word
    将光标移动到左边单词的起始处
    
  2) fanky_move_right_word
    move the cursror to the end of right word
    将光标移动到右边单词的结束位置处
  
  3) fanky_del_left_word
    delete the left word of cursor site
    删除光标左边的单词
  
  4) fanky_del_right_word
    delete the right word of cursor site
    删除光标右边的单词
    
  use in shortcut table:	// 跳到光标所在行首和行尾
    { "keys": ["home"], "command": "move_to", "args": {"to": "bol", "extend": false}},
    { "keys": ["end"], "command": "move_to", "args": {"to": "eol", "extend": false} },
    // 跳到光标所在行首和行尾并选中
    { "keys": ["shift+home"], "command": "move_to", "args": {"to": "bol", "extend": true}},
    { "keys": ["shift+end"], "command": "move_to", "args": {"to": "eol", "extend": true} },

    // 跳到文件最顶端和最末端
    { "keys": ["ctrl+home"], "command": "move_to", "args": {"to": "bof", "extend": false} },
    { "keys": ["ctrl+end"], "command": "move_to", "args": {"to": "eof", "extend": false}},
    // 跳到文件最顶端和最末端并选中文本
    { "keys": ["ctrl+shift+home"], "command": "move_to", "args": {"to": "bof", "extend": true} },
    { "keys": ["ctrl+shift+end"], "command": "move_to", "args": {"to": "eof", "extend": true}},

    // 光标位置不动，单行滚屏(一次滚动 2 两行距离)
    { "keys": ["ctrl+up"], "command": "scroll_lines", "args": {"amount": 2.0} },
    { "keys": ["ctrl+down"], "command": "scroll_lines", "args": {"amount": -2.0} },

    // 前跳一个单词（自定义插件）
    { "keys": ["ctrl+left"], "command": "fanky_move_left_word", "args": {"extend": false} },
    { "keys": ["ctrl+right"], "command": "fanky_move_right_word", "args": {"extend": false} },
    { "keys": ["ctrl+shift+left"], "command": "fanky_move_left_word", "args": {"extend": true} },
    { "keys": ["ctrl+shift+right"], "command": "fanky_move_right_word", "args": {"extend": true} },

    // 删除光标所在行
    { "keys":["ctrl+l"],"command": "run_macro_file", "args": {"file": "res://Packages/Default/Delete Line.sublime-macro"} },

    // 删除右边一个单词
    { "keys": ["ctrl+backspace"], "command": "fanky_del_left_word"},
    { "keys": ["ctrl+delete"], "command": "fanky_del_right_word"},
    
2、space_start_end.py
    insert a space to the begin and end of the ascii text.
    在 ASCII 文本的前后插入一个空格，主要用于中英混合的文本中，如果中文后面接着一个英文单词，而且衔接之间并没有空格，则給它插入一个空格（如果有，则不会插入），
    该插件方便看不惯中英之间没有空格隔开的强迫症患者。
    
    use in shortcut table:
      // 在前后为中文的英文单词前后，加上空格（自定义插件）
      {
        "keys": ["ctrl+f12"],
        "command": "fanky_space_start_end",
        "args": {}
      },

 3、tab_command.py
    in sublime default, press tab key to show indent table, some people dosn't like this. now this plugin is use to shield
    the default tab actions.
    
    subliem 默认按下 tab 键会有很多功能，譬如显示补全列表等，而这些功能是很多人不想要的，通过该插件，可以屏蔽掉原来的功能，让 tab 键只输入
    \t。当然，如果 \t 是输入 n 个空格的，也可以修改插件，或者增加插件参数，允许自行设定。这里只为适合我个人用，所以写成硬代码。
    
    use in shortcut table:
    	{ "keys": ["tab"], "command" : "fanky_tab"},
    	{ "keys": ["shift+tab"], "command" : "fanky_shift_tab", "args": {}},
