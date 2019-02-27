---
layout: post
title: "PythonPlugins"
date: 2019-2-27
categories: python plugin architecture
---

# Плагинная архитектура в Python

Допустим в проекте мы хотим сделать плагины. С автозагрузкой всех установленных
в определенный каталог, проверкой на корректность самого плагина, с
интерфейсами и пр.

Вот кусок кода с общей идеей:

```python
import typing as t
import importlib
import pkgutil
from collections import defaultdict
from abc import abstractmethod, ABCMeta
# импортируем основной пакет, в котором находятся все 
# расширения. Нужен для правильного определения путей к 
# самим расширениям. Предполагается, что в нем то и лежат все 
# модули
import application.extensions as EXTS_PACKAGE


class IExtension(metaclass=ABCMeta):
  """
  Интерфейс расширения(плагина). Расширение должно 
  унаследовать данный интерфейс в файле extension.py в 
  каталоге самого расширения.
  """
  @abstractmethod
  def get_presenter(self) -> t.Callable[[], dict]:
    """ Do the job """


class NIExtension(IExtension):
  """
  Суть - `raise NotImplementedError()`, но по соглашению 
  расширений. Т.о. мы может делать красивые страницы 
  "Извините, пока не реализовали"
  """
  def get_presenter(self):
    return lambda x: {"error": "Do the job"}


def not_impl_ext():
  return NIExtension()


# Список расширений для использования в runtime
# в других файлам мы импортируем этот словарь и по ключу 
# берем нужное расширение. Если значения нет, будет получен 
# NIExtension
EXTENSIONS = defaultdict(not_impl_ext)
for finder, name, ispkg in pkgutil.iter_modules(EXTS_PACKAGE.__path__):
  module = importlib.import_module(f"{EXTS_PACKAGE.__name__}.{name}.extension")
  EXTENSIONS[name] = module.Extension()
```
