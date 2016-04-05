---
layout: post
title: "toonicetoforget"
date: 2016-4-5
categories: experimental
---
# Vim tips
Я люблю колонки.
Вот такие например

{% highlight python %}
url(r'^$',           views.index,      name="index'),
url(r'^events/',     views.events,     name='events'),
url(r'^api/events/', api.views.events, name='events-api')
{% endhighlight %}

Но бывает, когда нужно внести изменения в первую колонку. Места вроде бы
достаточно, но сделал ввод...

{% highlight python %}
url(r'^index/$',           views.index,      name="index'),
url(r'^events/',     views.events,     name='events'),
url(r'^api/events/', api.views.events, name='events-api')
{% endhighlight %}

Больно. Однако в Vim'е есть режим замены.

## Replace mode

> `R`

Аналогично функциональности `Insert` - вводимые символы будут переписывать
существующие.

Поэтому делаем так:

1. Встаем на место, после "^" перед "index"
2. Жмем `dt ` - с пробелом вконце
3. Теперь `R` и вводим все что нужно
4. Когда закончили ввод - `<ESC>p` - 2 клавиши

Конечно, если места нету, придется по старинке, т.к. придется сдвинуть колонки
других строк. В этом мне помогает плагин Tabular.

1. Выполняем вставку, ломая колонки
2. Выделяем всю "таблицу"
3. `:'<,'>s/\s\+/ /g`
4. `:Tabularize /\s\+/l0`


Готово. Хорошо бы это одной кнопкой, да и между строками будут комменты,
которые нужно игнорить. На все это есть функциональность Tabular'а: у него
имеется встроенная команда `AddTabularPipeline`. Подробнее в доках.
