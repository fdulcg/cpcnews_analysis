# cpcnews_analysis
习大大重要讲话数据收集分析与可视化。（Analysis and visualization of  important speech data of Chairman Xi）

newsclawer.py   -- python clawer, using beautifulsoup4 and lxml to request and locate speech content. Collecting data.

news.py  -- python handle data file. Extract keywords and relations from plain cpcnews data. Format and write to json file so that cosejs can use this data json file

cosejs / cosejs project from http://js.cytoscape.org/

cosejs/code.js    --javascript file import data and style json file

cosejs/data3.json  --Data after processing and write into a json file

cosejs/index.html  -- Main html

cosejs/show.py  -- bottle python file to build this webpage on server.

## Run Server
python ./cosejs/show.py
visit localhost:8080