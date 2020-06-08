# 懒投资回款数据（2019，2020）

今年懒投资回款异常缓慢，不过每天都或多或少有些回款，然而自己在去年已到期的投资只回了不到1%，所以我想抓取今年的回款数据看看是不是有风险，不料把去年的回款数据也拿到了，对比之下，差别很大。

## 直接看结果

[https://dawncold.github.io/lantouzi/](https://dawncold.github.io/lantouzi/)

## 安装

```console
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 抓取

```console
python main.py
```

## 结果

会在`posts`目录下生成一堆文件，只需要使用`stats-year-2019.csv`和`stats-year-2020.csv`

## 说明

通过抓取公告，解析日期和回款金额，大致准确，得益于最近公告模版统一。

祝大家早日得到投资本息！
