# CNKI-Crawler-
This is a project which can get basic information of articles from CNKI, including name, authors(contains ID), abstract, keywords, volume and citations. 可以获取知网上的论文基本信息，包括作者（包括ID），摘要，关键词，页数、引文等
basic-info.py用于爬取基本信息（不包括引文），使用前需要人工检查需要爬取的期刊名字缩写（url中），期刊创刊年、1994-1999年是否出现url的filename字段异常，每年发行数量，在代码前更改，如果过去年发刊量较少，后来增加，可以设置变化的年份。也可以统一设置较大值，但会执行一些冗余操作（不影响结果）。

cite.py用于爬取引文，使用前先将basic-info.py的输出结果的作者、filename两列单独建立文件保存在source_csv中，执行后输出结果到cite文件夹下。一次可以接受多个文件输入。
