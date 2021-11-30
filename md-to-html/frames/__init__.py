import xml.etree.ElementTree as etree
from re import sub

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor

"""
Github式<h>
"""
class AddHref(Postprocessor):
    def run(self, text):
        return sub(r'<h(\d) id=([\'"])(.*?)\2>(.*?)</h\1>', r"<h\1 id='\3'><a href='#\3'>\4</a></h\1>", text)

class AddHrefExt(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(AddHref(), 'add_href', 175)

"""
<del>
"""
class DelTag(InlineProcessor):
    def handleMatch(self, m, data):
        if m.group(1) == '\\':
            return '~~'+m.group(2)+'~~', m.start(), m.end()
        p = etree.Element('del')
        p.text = m.group(2)
        return p, m.start(1)+len(m.group(1)), m.end()

class DelTagExt(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(DelTag(r"(^|.)\~\~(.*?)\~\~"), 'del_tag', 70)


"""
自定义字体大小
"""
class LargeFont(InlineProcessor):
    def handleMatch(self, m, data):
        p = etree.Element('span')
        p.set('style', f'font-size: {m.group(2)}rem')
        p.text = m.group(3)
        return p, m.start(), m.end()

class LargeFontExt(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(LargeFont(r"(\$([\d.]*)\$)(.*?)\1"), 'large_font', 175)

"""
target=_blank
"""
class BlankLink(InlineProcessor):
    def handleMatch(self, m, data):
        p = etree.Element('a')
        p.set('href', m.group(2))
        p.set('target', '_blank')
        p.text = m.group(1)
        return p, m.start(), m.end()

class BlankLinkExt(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(BlankLink(r"#\[(.*?)\]\((.*?)\)"), 'blank_link', 165)

all_ext = [AddHrefExt(), LargeFontExt(), DelTagExt(), BlankLinkExt()]
