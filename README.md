# 测试版app更新工具
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
* 把整个Python工程拷贝或者是clone到自己的android项目里，建议使用git submodule 的方式
* 修改config.yml以适应自己的项目
* 执行start.sh 调试和使用

### 高级玩法
请参考这个demo https://github.com/pokercc/debug_app_updater_demo

欢迎大家批评指正





我最近在研究android 的持续集成，jenkins ,docker ,gradle 等技术，
有兴趣的朋友，可以找我沟通，qq 729368896,email pokercc@sina.com

