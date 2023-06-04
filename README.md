## 1.ASAMMDF的基本使用
* 相关链接：
  * https://canlogger.csselectronics.com/tools-docs/converters/asc/index.html#example-output
  * https://www.csselectronics.com/pages/asammdf-gui-api-mdf4-mf4
## 2. PyQT的基本使用
* 相关链接：
  * https://www.byhy.net/tut/py/gui/proj-prac/
* 配置QT Designer到Pycharm
  * pip3 install pyqt5-tools 
  * 找到QtDesigner的路径(pycharm 里面 按两次shift Files里面搜索即可)、 =>在site-packages文件夹下
  * 找到路径后复制(/x/xx/../designer.exe)，并且在pycharm中找到File>Settings>Tools>External Tools>+,自行添加即可
  * Program选择PyQt安装目录中 designer.exe 的路径
  * Work directory 使用变量 $ProjectFileDir$
* 配置 Pyuic5到Pycharm
  * 找出pyuic5.exe或者pyuic5.bat 并复制其路径 => Scripts文件夹下
  * File>Settings>Tools>External Tools>+
  * Program选择PyQt安装目录中 pyuic5.bat 或者pyuic5.exe的路径
  * Argumens设置为：$FileName$ -o $FileNameWithoutExtension$.py
  * Work directory 设置为 $FileDir$
* 基本使用：
  * 全部配置好后，勾选，然后在 Tools>External Tools就可以调用了
  * 后续到Tools>External Tools里面调用 QtDesigner
  * 到xx.py右击选择External Tools调用 pyuic