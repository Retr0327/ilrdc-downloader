# **ILRDC Downloader**
Downloading the data from the website [Indigenous Languages Research and Development Center (ILRDC)](https://ilrdc.tw/grammar/index.php).


## **Documentation**

### 1. Import the package.

``` python
from ilrdc import ILRDC
```
If you don't know which dialect or which part of data you want to download, you can import two additional classes: `ILRDCDialect` and `ILRDCPart`

``` python
from ilrdc import ILRDC, ILRDCDialect, ILRDCPart
```
Use the method `.get_info()` on `ILRDCDialect` and `ILRDCPart` to get all the information:
- To get information of dialects:

    ```python
    ILRDCDialect.get_info()
    ```
    This prints:
    ```python
    ['泰雅語', 
     '邵語', 
     '賽德克語', 
     '布農語', 
     '魯凱語', 
     '噶瑪蘭語', 
     '卑南語', 
     '雅美語', 
     '撒奇萊雅語', 
     '卡那卡那富語']
    ```
- To get information of the parts:

    ```python
    ILRDCPart.get_info()
    ```
    This prints:
    ```python
    ['詞彙與構詞',
     '基本句型及詞序',
     '格謂標記與代名詞系統',
     '焦點與時貌語氣系統',
     '存在句所有句方位句結構',
     '祈使句結構',
     '使動結構',
     '否定句結構',
     '疑問句結構',
     '連動結構',
     '補語結構',
     '修飾結構',
     '並列結構',
     '其他結構',
     '標點符號',
     '基本詞彙',
     '長篇語料']
    ```
    Regarding this list, the first fifteen values refer to the Grammar part; the second to last, to the Vocabulary part; the last, to the Story part. 
    
### 2. Fill in and instantiate `ILRDC` class: 
#### Parameters:
* `dialect_ch`: the chinese name of the dialect  
* `part_type`: the part type that you want to download (i.e. grammar, vocabulary and story)
* `part`: the part you want to specify (optional)

#### Examples:
- Select Grammar Part:

    Pass the string `'grammar'` to the parameter `part_type`:

    ```python
    ILRDC('泰雅語', part_type='grammar')
    ```
    Without specifing the parameter `part`, the class will include all the grammar parts (i.e. from 詞彙與構詞 to 標點符號). On the other hand, if you want to select a particular grammar part, pass one of the grammar part's name as a string to the parameter `part`:

    ```python
    ILRDC('泰雅語', part_type='grammar', part='否定句結構')
    ```
- Select Vocabulary Part:
    
  Pass the string `'vocab'` to the parameter `part_type`:

    ```python
    ILRDC('泰雅語', part_type='vocab')
    ```
    Since there is only one part for Vocabulary, you don't need to pass the string `'基本詞彙'` to the parameter `part`. If you insist, you can still specify:
    
    ```python
    ILRDC('泰雅語', part_type='vocab', part='基本詞彙')
    ```
- Select Story Part:
    
  Pass the string `'story'` to the parameter `part_type`:

    ```python
    ILRDC('泰雅語', part_type='story')
    ```
    Since there is only one part for Story, you don't need to pass the string `'長篇語料'` to the parameter `part`. If you insist, you can still specify:
    
    ```python
    ILRDC('泰雅語', part_type='story', part='長篇語料')
    ```
### 3. Print out the data: 
After filling in and instantiating the `ILRDC` class, you can use `.data` to access the class attribute value. For example:

```python
ILRDC('泰雅語', part_type='grammar', part='基本句型及詞序').data
```
This prints:
```python
{
    '基本句型及詞序': [
        {
            'ID': '(4-1)a.',
            'dialect': 'maniq ngahi’ i Silan.',
            'chinese_translation': 'Silan 吃地瓜。',
            'sound_url': 'https://ilrdc.tw/grammar/sound/2/4-1-1.mp3'},
        }
        ...
    ]
}
```

### 4. Write object to a JSON file: 
After filling in and instantiating the ILRDC class, you can use the method `.to_json()` convert all the data to a JSON file.

```python
ILRDC('泰雅語', part_type='vocab').to_json()
```

### 5. Write object to a CSV file: 
After filling in and instantiating the ILRDC class, you can use the method `.to_csv()` convert all the data to a comma-separated values (CSV) file.

```python
ILRDC('泰雅語', part_type='vocab').to_csv()
```

## Contact Me
If you have any suggestion or question, please do not hesitate to email me at r07142010@g.ntu.edu.tw
