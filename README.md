# This is Data Augmentation for Chinese text for Python3

## Usage
### you have two func for Chinese text Data Augmentation 

### Install textda
pip install:

```bash
pip install textda
```

1. you can expansion data use **data_expansion**
```python
from textda.data_expansion import *
print(data_expansion('生活里的惬意，无需等到春暖花开')) 

```
output:

```python
['生活里面的惬意，无需等到春暖花开', 
'生活里的等到春暖花开',
'生活里无需惬意，的等到春暖花开', 
'生活里的惬意，无需等到春暖花开', 
'生活里的惬意，并不需要等到春暖花开', 
'生活无需的惬意，里等到春暖花开', 
'生活里的惬意，等到无需春暖花开']

```

param explain：

    :param sentence: input sentence text
    :param alpha_sr: Replace synonym control param. bigger means more words are Replace
    :param alpha_ri: Random insert. bigger means more words are Insert
    :param alpha_rs: Random swap. bigger means more words are swap
    :param p_rd: Random delete. bigger means more words are deleted
    :param num_aug: How many times do you repeat each method

- you can use parameters alpha_sr, alpha_ri, alpha_rs, p_rd, num_aug can control ouput.

    if you set alpha_ri and alpha_rs is 0 that means use **linear classifier** for it, and insensitive to word location
    
    like this:
  ```python
    
  from textda.data_expansion import *

  print(data_expansion('生活里的惬意，无需等到春暖花开', alpha_ri=0, alpha_rs=0))
  
  ```
  output:
    
  ```python
  ['生活里的惬意，无需等到春暖花开', 
      '，无需春暖花开', 
      '生活里面的惬意，无需等到春暖花开', 
      '生活里的惬意，需等到春暖花开']
    
  ```
     


2. you can use **translate_batch** like this:

```python
from textda.youdao_translate import *
dir = './data'
translate_batch(os.path.join(dir, 'insurance_train'), batch_num=30)

```

```
# translate results:  chinese->english and english -> chinese

颜色碰掉了一个角不延迟,但事情或他们不赠送,或发送,眉笔打开已经破碎,磨山楂,也不打破一只手,轻轻刷掉,持久性不长,
这个用户没有填写评价内容
颜色非常不喜欢它
不说话,缓慢的新领域
不太容易染好骑吗
不是很好我喜欢!
没有颜色的眼影
应该有大礼物盒眼影,礼物不礼物盒,没有一起破碎粉碎好的眼影不买礼物清洁剂脏就像商品是压力
没有生产日期,我不知道是否真实,总是觉得有点奇怪
是一个小飞粉吗
但是一些混合的颜色
有几次,现在这个东西,笔是空的
眼影有点小,少一点。
不好的颜色,粉红色
明星不想买,坏了,不容易,不要在乎太多!
一开始我已经联系快递,快递一直拖,说他将返回将联系快递服务
画不是,是不好的
物理和照片有很大的区别
不要把眼影刷不是很方便
感觉好干,颜色更暗
打破了在运输途中,有点太脆弱…
盒子有点坏了,还没有发送。

```

param explain：

    :param file_path: src file path
    :param batch_num: default 30
    :param reWrite: default True. means you can rewrite file , False means you can append data after this file.
    :param suffix: new file suffix



## Reference:

https://github.com/jasonwei20/eda_nlp

Code for the ICLR 2019 Workshop paper: Easy data augmentation techniques for boosting performance on text classification tasks. https://arxiv.org/abs/1901.11196


## License

[MIT](./LICENSE)
