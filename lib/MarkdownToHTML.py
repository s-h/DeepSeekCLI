import markdown
from pygments.formatters import HtmlFormatter

class MarkdownConverter:
    def __init__(self, style='monokai'):
        self.style = style
        self.formatter = HtmlFormatter(style=style)
        self.extensions = ['extra', 'codehilite', 'toc']
        self.extension_configs = {
            'codehilite': {
                'use_pygments': True,
                'css_class': 'codehilite',
                'linenums': False
            }
        }

    def _generate_css(self):
        """生成组合样式表"""
        pygments_css = f"<style>{self.formatter.get_style_defs()}</style>"
        custom_css = """
        <style>
        :root {
            --bg-color: #1a1a1a;
            --text-color: #e0e0e0;
            --border-color: #404040;
        }

        body {
            background: var(--bg-color);
            color: var(--text-color);
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            line-height: 1.6;
        }

        .codehilite {
            background: #2d2d2d !important;
            padding: 1rem;
            border-radius: 4px;
            margin: 1.5rem 0;
            overflow-x: auto;
        }
        </style>
        """
        return pygments_css + custom_css

    def convert(self, md_content, title="Converted Document"):
        """
        将 Markdown 字符串转换为完整 HTML 文档
        :param md_content: Markdown 格式字符串
        :param title: 生成的 HTML 标题
        :return: 完整 HTML 字符串
        """
        html_content = markdown.markdown(
            md_content,
            extensions=self.extensions,
            extension_configs=self.extension_configs
        )

        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    {self._generate_css()}
</head>
<body>
{html_content}
</body>
</html>"""

    def convert_file(self, input_path, output_path, title="Converted Document"):
        """从文件读取 Markdown 并输出 HTML 文件"""
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        html = self.convert(md_content, title)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

if __name__ == "__main__":
    # 使用示例 - 直接转换字符串
    converter = MarkdownConverter()

    # 示例 Markdown 内容
    sample_md = """
    # Hello World
    ```python
    print("Hello Dark Theme!")
    ```
    """

    # 转换并打印结果
    print(converter.convert(sample_md, "Demo Page"))

    # 文件转换用法保持不变
    # converter.convert_file("input.md", "output.html")