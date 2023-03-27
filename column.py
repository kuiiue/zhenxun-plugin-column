import math
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg

__zx_plugin_name__='竖排文字'
__plugin_usage__ = """
usage：
    竖排文字
    指令：
        竖排<文本>
""".strip()

def replace_symbols(text):
    replace_dict={
        ' ':'　', 
        '—':'｜',
        '“':'﹁',
        '”':'﹂',
        '（':'︵',
        '）':'︶',
        '《':'︽',
        '》':'︾',
        '【':'︻',
        '】':'︼',
        '…':'︙',
        '，':'︐',
        '。':'︒',
        '、':'︑',
        '：':'︓',
        '！':'︕',
        '？':'︖',
        '；':'︔',
    }
    result=''
    for t in text:
        if t in replace_dict:
            result+=replace_dict[t]
        else:
            result+=t
    return result

column=on_command('竖排', priority=5, block=True)

@column.handle()
async def _(arg: Message=CommandArg()):
    text=arg.extract_plain_text().strip()
    if not text:
        await column.finish("没有文本啊", at_sender=True)
    await column.finish(f"竖排文本：\n\n{to_column(text)}", at_sender=True)


def get_best_division(length, ratio=1.6):
    width=round(math.sqrt(length/ratio))
    height=math.ceil(length/width)
    return width, height

def to_column(text, height=None, width=None):
    length=len(text)
    if height==None and width==None:
        width, height=get_best_division(length)
    elif height!=None:
        width=math.ceil(length/height)
    elif width!=None:
        height=math.ceil(length/width)
    result=''
    length=width*height
    text=replace_symbols(text)
    for i in range(length):
        w=width-1-i%width
        h=int(i/width)
        c=w*height+h
        try:
            result+=text[c]
        except:
            result+='　'
        if (i+1)%width==0 and i!=length-1:
            result+='\n'
    return result
    
