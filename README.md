## Project Name

该项目用于完成latex公式的归一化，对于同一种形式的省略写法，尽量将其补全使得解析上统一。


## Environment

* python版本要求: python >= 3.5


## File Structure
```
├── .gitignore     
├── normalize.py
├── utils.py
├── README.md
├── requirements.txt
├── componenets
├── exceptions
├── stream
└── tests
```
* components: latex各个模块的定义
* exceptions: 异常类的定义
* tests: 单元测试文件
* stream: 字节流处理


## Example

* latex公式输出的归一化
    ```python
    >>> from xizi_latex_normalizer import normalize_latex_expression
    >>> normalize_latex_expression('\\frac12')
    '\\frac{1}{2}'
    ```
* 中文公式混合句子的归一化
    ```python
    >>> from xizi_latex_normalizer import normalize_latex_in_sentence
    >>> normalize_latex_in_sentence("包含中文$\\frac12$的公式测试")
    '包含中文$\\frac{1}{2}$的公式测试'
    ```

## Usage

该仓库需要打包通过`pip`安装的方式进行使用，使用方式有4种:
1. 运行命令`python setup.py sdist bdist_wheel`完成代码的打包处理，之后在`dist`目录下找到`xizi-latex-normalizer.tar.gz`压缩包，使用`pip install xizi-latex-normalizer.tar.gz`进行安装即可
2. 运行命令`python setup.py install --force`进行直接安装，其中`--force`是必须的，否则新版本不会覆盖掉老版本
3. 直接找到相应的发行版下载`tar.gz`文件进行安装，发行版查看的地址为：`https://gitee.com/xizi_ai/dashboard/projects/xizhi-aied/xizi_latex_normalizer/releases/v1.0.0`

在进行打包前，需要先执行`python setup.py test`以确定目前的代码是否可全部通过单元测试。

