---
layout: post
title: "Layout чужого сайта под себя"
date: 2016-7-3
categories: experimental
---
Уже пару лет у меня есть вкладочка fixes в Chrom(ium). Идея проста: в моих
тайлах оконного менеджера затисался chromium, который занимает половину экрана.
В нем открыт как правило какой-то сайт с инфой, но верстка на нем
универсальная, резиновая. Еще иногда авторы оставляют сайдбар постоянно, без
возможности скрыть его, как в интерфейсе Jira. Ну что же, я же разраб, почему
бы мне самому все не сделать?  Возьмем к примеру сайтец который вынудил меня
написать данный пост:

![Before](/images/SitesForme_before.png)

Вот зачем это тот сайдбар? Без него намного лучше

![After](/images/SitesForme_after.png)

Сделать такое просто до нельзя, ибо "сырцы" разметки у нас на руках.

{% highlight javascript %}
var sidebar =document.querySelector('.book-summary')
var book = document.querySelector('.book-body')
var visible = (s.style.display!=="none")
if ( visible ) {
  sidebar.style.display="none";
  book.style.left="0px";
} else {
  sidebar.style.display="block";
  book.style.left="300px";
}
{% endhighlight %}

Просто меняем стили того что нам необходимо. И делаем это в режиме toggle - в
зависимости от состояния либо показываем либо скрываем сайдбар. Насчет `book` и
его стиля: ширина блока задается жестко через media queryes, поэтому нужно его
тоже фиксить.

И тут я задумался о том, что хорошо бы иметь на этот случай хоткей.
Первые же поиски привели к [Shortcut Manager](ttps://chrome.google.com/webstore/detail/shortcut-manager/mgjjeipcdnnjhgodgjpfkffcejoljijf).
Данный скрипт втолкнулся в хоткей <kbd>Alt-h</kbd>. А все потому что Vim.
