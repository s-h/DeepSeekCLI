#!/usr/bin/env python3
from typing import NoReturn
from openai import OpenAI
from rich.console import Console
from  lib.MarkdownToHTML import MarkdownConverter
import cliconfig
import sys
import os
import re

class OpenAICLI:
    ps_new="\nchat·new(:run 进行查询)> "
    ps_continue="...>"
    ps_bye="bye~"
    def __init__(self):
        # openaisdk client.chat.completions.create 请求参数
        self.messages=[{"role":"system", "content":""}]
        self.markdown=""
        # 构造 client
        self.client = OpenAI(
            api_key=cliconfig.sk,  # 知识引擎原子能力 APIKey
            base_url=cliconfig.baseURL  # 知识引擎原子能力 API 地址  ,
        )
        # 新会话标志
        self.is_new_flag = True
        self.console = Console()
        self.model = cliconfig.model
    @staticmethod
    def print_help() -> None:
        help_msg =""":run     进行查询
:quit       退出程序
:new        新建会话
:sysrole    设置system role
:save       保存回答文本为markdown文件
:savehtml   保存回答文本为html文件
:help       打印帮助"""
        print(help_msg)

    def print_deepseek_logo(self) -> None:
        self.console.print(":rocket::sparkles: DeepSeek CLI", style="bold red")
        self.print_help()

    # openAI对话请求
    def request_chat(self, user_input:str) -> list:
        self.messages.append({"role": "user", "content": user_input})
        chat_completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True, #流式回答
        )
        # 思维链内容
        reasoning_content = ""
        # AI回复内容
        content = ""

        status = self.console.status("...")
        status.start()
        loading_stoped = False
        try:
            for chunk in chat_completion:
                if not loading_stoped:
                    status.stop()
                    loading_stoped = True
                # 打印思维链内容
                if hasattr(chunk.choices[0].delta, 'reasoning_content'):
                        print(f"{chunk.choices[0].delta.reasoning_content}", end="")
                        reasoning_content += chunk.choices[0].delta.reasoning_content
                # 打印模型最终返回的content
                if hasattr(chunk.choices[0].delta, 'content'):
                    if chunk.choices[0].delta.content != None and len(chunk.choices[0].delta.content) != 0:
                        print(chunk.choices[0].delta.content, end="")
                        content += chunk.choices[0].delta.content
            print("\n")
        except KeyboardInterrupt:
            # 终止回答，不记录用户提问 
            self.messages.pop()
            if not loading_stoped:
                status.stop()
            return 
        finally:
            if not loading_stoped:
                status.stop()

        self.messages.append({"role": "assistant", "content": content})
        return 
    def _handle_sysrole(self, _) -> None:
        system_content = input("输入system role:")
        self.messages[0]["content"] = system_content
        print(self.messages[0]["content"])

    def _handle_exit(self, _) -> NoReturn:
        self.console.print(":smiley:" + OpenAICLI.ps_bye)
        sys.exit(0)
    
    def _handle_save_markdown(self, args: str) -> None:
        filename = args.strip()
        if not filename:
            filename = input("文件名：")
        self.save_chat_markdown(os.path.join("out", filename))
    def _handle_save_html(self, args: str) -> None:
        filename = args.strip()
        if not filename:
            filename = input("文件名：")
        self.save_chat_html(os.path.join("out", filename))

    def _handle_new(self, _) -> None:
        print("清空会话")
        self.messages = []
        self.is_new_flag = True

    def _handle_help(self, _) -> None:
        self.print_help()
    # 用户多行输入
    def multi_line_input(self) -> str:
        lines = []
        command_handlers = {
            ':quit': self._handle_exit,
            ':q': self._handle_exit,
            ':save': self._handle_save_markdown,
            ':w': self._handle_save_markdown,
            ':savehtml': self._handle_save_html,
            ':n': self._handle_new,
            'new': self._handle_new,
            ':h': self._handle_help,
            ':help': self._handle_help,
            ':sysrole': self._handle_sysrole
        }
        while True:
            try:
                if self.is_new_flag:
                    ps = OpenAICLI.ps_new
                else:
                    ps = OpenAICLI.ps_continue
                line = input(ps).strip()  # 每次回车输入一行
                cmd_line = line.lower()
                if cmd_line in [":run", ":r"]: # 提交请求
                    if not lines: 
                        print("请输入查询文本")
                        continue
                    return '\n'.join(lines)  # 合并为多行字符串
                if re.match(r'^:', cmd_line):
                    parts = line.split(maxsplit=1)  # 分割命令和参数
                    if len(parts) > 1:
                        cmd, args = parts[0].lower(), parts[1]
                    else:
                        cmd = parts[0].lower()
                        args = ""
                    handler = command_handlers.get(cmd)
                    if handler:
                        handler(args)
                else: # 不是用户指令
                    lines.append(line)
                    self.is_new_flag = False

            except KeyboardInterrupt or EOFError:
                print("清空输入")
                lines = []
                continue

    def update_markdown(self) -> None:
        self.markdown = ""
        line = ""
        # print(self.messages)
        for i in self.messages:
            if i["role"] == "user":
                line = "# " + i["content"].replace("\n", " ").replace("\r", " ")
            elif i["role"] == "assistant":
                line = i["content"] + "\n"
            self.markdown += line
    # 保存会话为markdown文件
    def save_chat_markdown(self, name:str) -> None:
        self.update_markdown()
        with open(name, "w", encoding="utf-8") as f:
            f.write(self.markdown)

    # 保存会话为html文件
    def save_chat_html(self, htmlfile:str) -> None:
        self.update_markdown()
        converter = MarkdownConverter(style='monokai')
        HTML=converter.convert(self.markdown, "DeepSeekCLI")
        with open(htmlfile, "w", encoding="utf-8") as f:
            f.write(HTML)

    def CLI_run(self):
        self.print_deepseek_logo()
        while True:
            user_input = self.multi_line_input()  
            # 发起请求获取AI回复内容
            self.request_chat(user_input)

        
if __name__ == '__main__':
    cli = OpenAICLI()
    cli.CLI_run()