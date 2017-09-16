# FileTransLate_BaiduAPI

## Jstranslate.py
	This a python3 script.I use it to translate the contents of the specified format into other languages.
	If your file content is the following format, and just translate the value, you can use this script.
> key1:value1
> 
> key2:value2
> 
> key3:value3
> 
> or
> 
> key1=value1
> 
> key2=value2
> 
> key3=value3
> 
## How to use
	Run the script at the terminal，follow the prompts to enter the necessary parameters.If you want to test this script, please put two files in the same directory to run.
> 请输入文件格式:
> 
> 1) a:b 2) a=b
> 
> 1
> 
> 请输入源语言:(若不确定，请输入auto)
> 
> auto
> 
> 请输入目标语言:(必须指定，不能输入auto)
> 
> en
## Issue
	The total length of the string that needs to be translated can not exceed 2000 because of some restrictions on the Baidu translation API.Next, I will improve the script so that it supports the simultaneous translation of a file into a multilingual version.
	If you have any questions please contact me
