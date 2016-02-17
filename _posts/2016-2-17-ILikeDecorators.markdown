---
layout: post
title: "Мне нравятся декораторы"
date: 2016-2-17
categories: python, FP
---

## Декораторы
Да, в питоне это весьма прикольная вещица как декоратор, которорая упрощает
композицию функций.
В ходе тестов, я начал выплевывать огромные количества данных: потому что хз
что не так.
И этот вывод начинает смешиваться с выводом тест-фреймворка, так еще и сами
тесты между собой(хоть и идут друг за другом). Ах да, и конечно принты в самом
коде.  В общем получаю не читаемую пелену.
Не долго думая вставил в начале и конце функции каждого теста про принту
границы:

    ============== RUN test_calculations
    // code code code
    ============== END test_calculations

Да, просто печатаю таких милашек. Имя теста поначалу вшивал и сразу бесился.
А тут еще напечатать список транзакций в колоночку охота, но заполнять тесты
`for...in...` что уж совсем перебор.
И тут я вспоминаю про декоратор.

## Границы списка

{% highlight python %}
def print_borders(fn, header="=================", footer="================="):
    def wrap(*args, **kwargs):
        print("======%s=======" % header)
        fn(*args, **kwargs)
        print("======%s=======" % footer)
    return wrap
{% endhighlight %}

`args`, `kwargs` это мы транслируем аргументы переданные функции-wrapper'у в
непосредственно функцию-исполнителя.

{% highlight python %}
@print_borders
def print_list(l, header=None):
    """Show list with header + footer """
    if header:
        print(header)
    for e in l:
        print(e)
{% endhighlight %}

Здесь, `args` содержит `l`, а `kwargs` - `header`.

Дальше все как обычно:

{% highlight python %}
print_list([1,2,3,4])
{% endhighlight %}

    =============================
    1
    2
    3
    4
    =============================


## Тырим имя функции
Мета доступ и все как класс, это конечно очень круто.

{% highlight python %}
def print_fn_bord(fn):
    h = " RUN %s " % fn.__name__
    f = " END %s " % fn.__name__

    def wrap(*args, **kwargs):
        fn(*args, **kwargs)
    return print_borders(fn=wrap, header=h, footer=f)
{% endhighlight %}


Функцию теста я теперь создаю так:

{% highlight python %}
@print_fn_bord
def test_calcs(self):
	pass
{% endhighlight %}


Здесь, `args` содержит тот самый `self`. Были бы еще параметры у функции
`test_calcs` - они бы были "распакованы" в параметры функции `wrap`.

При запуске этой функции выплевывается

    ======= RUN %func_name% =======
    // prints
    ======= END %func_name% =======
