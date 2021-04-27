def lang_phrases(lang, num):
    if lang == 0:
        phrases = ['Оқушының жеке  🆔 енгізіңіз. Егер сіз оқушының  🆔 білмесеңіз, тәлімгеріңізден(куратордан) сұрап біле аласыз.',  # 0
                   'Біздің жүйеде тіркелген нөміріңізді мына форматта енгізіңіз 87***** : 📱',  # 1
                   'Сіздің нөміріңіз дерекқорда табылмады, қайтадан көріңіз ↲',  # 2
                   'Оқушының аты-жөні👤 : {0}. Дұрыс па?',  # 3
                   'Иә',  # 4
                   'Жоқ',  # 5
                   'Пайдаланушы табылмады 👤',  # 6
                   'Қайтадан көріңіз ↑',  # 7
                   'Сіз қайтадан көре аласыз 😊',  # 8
                   'Біз отчетты қалыптастырамыз...⌛',  # 9
                   'Tesla Educaton оқу орталығының автоматты жүйесіне қош келдіңіз.\n'
                   'Интерфейс тілін таңдаңыз.\n Добро пожаловать в автоматическую систему'
                   ' образовательного центра Tesla Education.\n Выберите язык интерфейса.',  # 10
                   'Сіз оқушының үлгерімі жайлы хабарландыруға сәтті тіркелдіңіз. ✅',  # 11
                   'Қайырлы күн, құрметті ата-ана! 🧔👩 \n '
                   '{0}\n'
                   'Сізге өткізілген сабақтар жөнінде хабарлаймыз.\n'
                   'Күні: {1}\n'
                   'Пән: {2}\n'
                   'Сабақтың тақырыбы: {3}\n'
                   'ҮЙ ТАПСЫРМАСЫ\n\n'
                   'Үй тапсырмасын бағалау (орындаудың ең жоғары пайызы: 100%): {4}\n'
                   'Үй және сынып жұмысы үшін берілген Бонус(TED) (максималды балл - 20 балл): {5}\n'
                   'Мұғалімнің ескертуі: {6}\n',  # 12
                   'Сіз оқушының үлгерімі жайлы хабарландыруға сәтті тіркелдіңіз. ✅',  # 13
                   'Қазіргі уақытта оқушының білімін бағалау бойынша ақпарат жоқ',  # 14
                   'Выберите от кого отписаться',  # 15
                   ]
        return phrases[num]
    elif lang == 1:
        phrases = ['Укажите 🆔 ребенка в электронной базе. Если вы не знаете 🆔 своего ребенка,'
                   ' можете запросить у вашего куратора.',  # 0
                   'Введите зарегистрированный в нашей системе номер телефона в формате 87********* 📱',  # 1
                   'Ваш номер не обнаружен в базе данных, попробуйте заново ↲ ',  # 2
                   'ФИ ученика 👤 : {0}. Верно?',  # 3
                   'Да',  # 4
                   'Нет',  # 5
                   'Пользователь не найден 👤',  # 6
                   'Попробовать снова ↑',  # 7
                   'Можете попробовать снова 😊',  # 8
                   'Мы формируем отчет...⌛',  # 9
                   'Tesla Educaton оқу орталығының автоматты жүйесіне қош келдіңіз. '
                   'Интерфейс тілін таңдаңыз.\n Добро пожаловать в автоматическую систему'
                   ' образовательного центра Tesla Education. Выберите язык интерфейса.',  # 10
                   'Вы успешно зарегистрировались на рассылку успеваемости ученика. ✅',  # 11
                   'Доброго времени суток, дорогой родитель!🧔👩\n '
                   '{0}\n'
                   'Сообщаем Вам о проведенных занятиях.\n'
                   'Дата:  {1}\n'
                   'Предмет: {2}\n'
                   'Тема урока: {3}\n\n'
                   'ДОМАШНЕЕ ЗАДАНИЕ\n'
                   'Оценка домашнего задания (максимальный процент выполнения: 100%): {4}\n'
                   'Бонус(TED) за домашнюю и классную работу(максимально 20 баллов): {5}\n'
                   'Примечание от преподавателя: {6}\n',  # 12
                   'Вы успешно зарегистрировались на рассылку успеваемости ученика. ✅',  # 13
                   'В данный момент оценок нет',  # 14
                   'Выберите от кого отписаться',  # 15
                   ]
        return phrases[num]



# print(lang_phrases(1, 2))
