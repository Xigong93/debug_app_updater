# 测试版app发布工具
## 用途
开发人员每天打包给测试，自动发包的程序。
支持特性
* pgyer
* 自动化脚步
* 读取git 提交记录作为更新日志
* 钉钉通知

## 为什么要分享这个工具
这是我自己工作中写的一个帮助自己开发的脚本，因为在面试一些开发同学的时候，有人觉得这个还不错，所以想分享出来，希望对大家有所帮助。

## 为什么不是用java写 或者gradle 插件，而是python 脚本
因为我觉得python 写一些小工具，非常方便，后面如果大家觉得有必要写成gradle 插件，我会努力。

## 怎么使用?
### 简单步骤
* 把整个Python工程下载或使用git submodule 方式集成到自己的安卓项目中
* 复制config_temp.yml 文件命名为config.yml,并修改其中的参数配置，以适应自己的项目(注意config.yml 被添加到了.gitignore 文件中)
* 执行start.sh 调试和使用


### 工程文件介绍
* tests 单元测试
* Pipfile和Pipfile.lock python 虚拟环境的配置文件，类似java的依赖配置文件 pom.xml 或者是build.gradle
* start.sh 启动脚本
* upload.py 主要的脚本
* config_temp.yml 配置文件的模板

### 相关技术点
* python3
* pipenv python3 的虚拟环境库
* 简单的shell 语法
* yaml 配置文件(比json,xml,properties 更适合作为配置文件)
* gradle 打包命令
* git log --since 命令

**建议不要去理会其中的技术点，直接用起来,玩玩看**

### 高级玩法
请参考这个demo https://github.com/pokercc/debug_app_updater_demo


我最近在研究android 的持续集成，jenkins ,docker ,gradle 等技术，
有兴趣的朋友，可以一起沟通探讨，qq 729368896,email pokercc@sina.com

