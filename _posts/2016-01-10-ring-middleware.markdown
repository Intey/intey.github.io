---
layout: post
title:  "Middleware для REST API"
date:   2016-01-10
categories: Clojure
---

Почти день был потрачен на проблему с запросом PUT к зародышу API. Они роняли
сервак, ничего не возвращали, но самое сложное: сервер возращает корректный
body (JSON), на хводе корректный JSON, а на серваке - `jetty.server.HttpInput`
и хоть ты тресни.

Сначала я все грешил на некоректный вход, Исправил. Потом, начал смотреть весь
запрос целиком и увидел

    Content-Type: application/x-www-form-urlencoded

Ок, вроде бы понятно: мы присылаем запрос, говоря что это форма, там куда инфы.
Jetty умен, кэширует это дело и не показывает кому попало. Что бы его зачитать,
надо прям JAVA'скими методами прочитать байты из потока, конвертануть и собрать
в строку. Но блин, я же JSON шлю!  Через JQuery:

{% highlight javascript %}
    $.ajax({url:"/api/events/555",
            type:'PUT',
            data:JSON.stringify({value:23}),
            dataType:'application/json',
            success: function(data, d, xrh) { console.log(data) }});
{% endhighlight %}

Оказалось, что надо не `dataType` а `contentType`.

XMLHttpRequest:

{% highlight javascript %}
var req = new XMLHttpRequest();
req.open("PUT", "/api/events/12", true);
req.send(JSON.stringify({value:123}));
{% endhighlight %}

Тоже были проблемы, пока перед отправкой запроса не выполнил

{% highlight javascript %}
    req.setRequestHeader('Content-Type', 'application/json');
{% endhighlight %}

И все заработало.

Ладно, с этим разобрались. Mock-API есть, надо бы тесты наклепать: все-таки
API, к тому же отказ от `noir-validation` шел на пользу. А тем ведь BDD, ммм...
Тут же вспомнилась либа, которая висела в dependencies профиля dev -
`ring-mock`. Нашел, поправил, начал смотреть что это и сразу как стало ясно.
На самом деле, про mock я читал статью в сфере С++. Там mock это заглушка
компонента, который должен вызываться целевым компонентом, который мы
тестируем. Штучка для интеграционных тестов. Мы просто мокаем что-то жирное, а
в тестах указываем, что вот этот тестируемый метод, должен 3 раза вызвать метод
"мокнутого" компонента.

Ring mock, больше напоминает мне мои наработки хелперов тестов: упрощение
обращения к ассетам, факторки сложных данных... собственно Ring mock это и
делает: упрощает создание запроса.  Вместо написания всего запроса целиком,
этого жирного гада, мы одной строчкой:

{% highlight clojure %}
(mock/request :get "/api/events/123")
{% endhighlight %}

Дальше кормим этот запрос серверному обработчику и сравниваем полученный
response с ожиданиями. И тут то кульминация: у ответа
`Content-Type: "text/html; charset=utf-8"`. Стерва. Ведь висит же middleware
`wrap-json-response`.  Ну думаю, сейчас я тебя...под middleware засуну!

{% highlight clojure %}
(defn wrap-content-json [handler]
    (fn [req] (update-in (handler req) [:headers "Content-Type"]
        (fn [_] "application/json"))))
{% endhighlight %}

Мимолетом прогуглил как сделать просто замену: не нашел - сам запилил. Конечно
все делается проще:

{% highlight clojure %}
(defn wrap-content-json [handler]
    (fn [req] (assoc-in (handler req) [:headers "Content-Type"]
        "application/json"))
{% endhighlight %}

Эх... Но не пригодился он мне. Оказывается надо возвращать Clojure'ские
объекты, а не строки и тогда будет сам устанавливаться `Content-Type`.
