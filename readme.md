# DeepSeek CLI

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

## 简介

DeepSeek CLI 是一个基于OpenAI API构建的命令行工具，旨在为用户提供便捷的与AI对话交互方式。用户可以通过简单的命令操作，进行多轮对话、设置系统角色、保存对话内容等。

## 安装

确保您已经安装了Python 3.6或更高版本，并且安装了所需的依赖库。您可以使用pip来安装这些依赖库：

```bash
pip install -r requirements.txt
```


同时，请确保您已获取到有效的API Key，并将其配置在`cliconfig.py`模块中。

## 使用方法

### 启动程序

通过以下命令启动CLI工具：

```bash
python DeepSeekCLI.py
```

### 命令列表

启动后，您可以输入以下命令进行操作：

- `:run` 或 `:r`：提交当前输入的查询文本给AI。
- `:quit` 或 `:q`：退出程序。
- `:new` 或 `:n`：新建会话，清空之前的对话记录。
- `:sysrole`：设置system role，影响AI的行为模式。
- `:save` 或 `:w`：保存回答文本为markdown文件。
- `:savehtml`：保存回答文本为html文件。
- `:help` 或 `:h`：打印帮助信息。

### 多行输入

当您需要输入多行文本时，只需直接输入文本并回车换行即可。当您准备提交请求时，输入`:run`或`:r`。

### 示例对话

```plaintext
chat·new(:run 进行查询)> 您好，我想了解一下今天的天气。
chat·new(:run 进行查询)>:run
...>
今天是晴天，气温适宜。
chat·new(:run 进行查询)> :save
文件名：weather_report.md
```

## 注意事项

1. 在首次运行前，请确保正确配置了`cliconfig`中的API Key和base URL。
2. 保存文件时，默认路径为`out`目录下，如果该目录不存在，程序将自动创建。
3. 如果遇到任何问题，欢迎提交issue或者pull request。