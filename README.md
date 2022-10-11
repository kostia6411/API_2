# API_future_salary
API_future_salary - это поиск средней зарплаты по вакансиям.

### Как установить

Нужно создать файл .env и занести в него следующие данные: ключ от Superjob.

Получить ключ нужно будет после ригистрации на сайте [Superjob](https://spb.superjob.ru/auth/registration/applicant/?returnUrl=https%3A%2F%2Fapi.superjob.ru%2Fregister%2F&context=hackwork).

Пример файла .env
```
SJ_KEY=v9.r.136978092.c4b964b6fa868b087e8147d891393fvaekab0838.284a07509df56c000cn51baee797b572ec9b016a
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Пример работы скрипта в случае штатной ситуации:

При запуске main.py, скррипт выдаст в терминале таблицы по средней зарплате с сайтов Superjob и hh: 
```
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
