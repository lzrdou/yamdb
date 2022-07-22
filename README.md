
# api_yamdb
***Новейший сервис формирования рейтинга книг, фильмов и музыки.***  
***Оценивайте, комментируйте, находите для себя лучшее!*** 
## Авторы
Проект разработан Артемием Бутырином, Матвеем Козловым и Фроликовым Сергеем при участии Yandex.Practikum.  
## Лицензия
Данное программное обучение создается в учебных целях. Лицензия не объявлялась.  
  
## Описание
Проект представляет собой базу призведений книг, фильмов и музыки в целях формирования их рейтинга.  
Реализованы следующие возможности:  
	* Возможность оценивать произведения и оставлять собстенные уникальные отзывы.  
 * Просмотр чужих отзывов и комментирование их.  
 * Формирование общего рейтинга произведений на основе отзывов пользователей.
	* Система модерации и администратирования.
	* Создание собственного пользователя.    
	* API.
    
**Внимание!** Проект находится в разработке, функционал доробатывается.
### Технологии проекта:
Django 4.0.6 
djangorestframework 3.12.4  
djangorestframework-simplejwt 4.7.2   
PyJWT 2.1.0  
Django-filter 22.1 
Python 3.8  
pre-commit
  
  
## Установка
### Как запустить проект:
1. Клонировать репозиторий и перейти в него в командной строке:
    * ```git clone https://github.com/lzrdou/api_yamdb.git```
	* ```cd api_yamdb/```
2. Cоздать и активировать виртуальное окружение:
	* ```python -m venv env```
	* ```source venv/Scripts/activate```
	* ```python -m pip install --upgrade pip```
3. Установить зависимости из файла requirements.txt:
	* ```pip install -r requirements.txt```
4. Выполнить миграции:
	* ```python manage.py migrate```
6. Запустить проект:
	* ```python manage.py runserver```
## Тестирование
### Как запустить тесты:
1. Запустить тесты следующей командой:
    * ```python manage.py test ```  
**Внимание!** В данной версии этот  
вариант тестирования не производится.
2. Перейти в корневую директорию:
    * ```cd ..```
3. Запустить тесты Yandex.Practikum следующей командой:
    * ```pytest ```
 
## Примеры  
###Endpoints:
* http://127.0.0.1:8000/api/v1/categories/  
 	```
 	[
  		{
  		 	"count": 0,
  			"next": "string",
  			"previous": "string",
   		 	"results": [
    	 	{
     			"name": "string",
    	    	"slug": "string"
    	 	}
    	 	]
  	    }
 	]
  ```
* http://127.0.0.1:8000/api/v1/genres/  
 	```
 	[
  		{
  		 	"count": 0,
  			"next": "string",
  			"previous": "string",
   		 	"results": [
    	 	{
     			"name": "string",
    	    	"slug": "string"
    	 	}
    	 	]
  	    }
 	]
  ```
* http://127.0.0.1:8000/api/v1/titles/  
  ```
	[
	  {
    	"count": 0,
    	"next": "string",
    	"previous": "string",
   	    "results": [
      	{
        	"id": 0,
        	"name": "string",
       	    "year": 0,
        	"rating": 0,
        	"description": "string",
        	"genre": [
          	{
            	"name": "string",
            	"slug": "string"
          	}
        	],
        	"category": {
          		"name": "string",
          		"slug": "string"
        	}
      	}
   	    ]
  	   }
	  ]
  ```
* http://127.0.0.1:8000/api/v1/titles/{titles_id}/  
   ```
	{
  		"id": 0,
  		"name": "string",
  		"year": 0,
  		"rating": 0,
  		"description": "string",
  		"genre": [
    	{
      		"name": "string",
      		"slug": "string"
    	}
  		],
  		"category": {
    	"name": "string",
    	"slug": "string"
  		}
	}
   ```
* http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/  
	``` 
	[
  		{
   	 		"count": 0,
    		"next": "string",
    		"previous": "string",
    		"results": [
      		{
        		"id": 0,
        		"text": "string",
        		"author": "string",
        		"score": 1,
        		"pub_date": "2019-08-24T14:15:22Z"
      		}
    		]
  		}
	] 
   ```
* http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/  
	```
	{
  		"id": 0,
  		"text": "string",
  		"author": "string",
  		"score": 1,
  		"pub_date": "2019-08-24T14:15:22Z"
	}
	```
* http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
	```
	[
  		{
    		"count": 0,
    		"next": "string",
    		"previous": "string",
    		"results": [
      		{
        		"id": 0,
        		"text": "string",
        		"author": "string",
        		"pub_date": "2019-08-24T14:15:22Z"
      		}
    		]
  		}
	]
  ```  
 * http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
	```
	{
  		"id": 0,
  		"text": "string",
  		"author": "string",
  		"pub_date": "2019-08-24T14:15:22Z"
	}
  	``` 
* http://127.0.0.1:8000/api/v1/auth/signup/  
	```
    {
      "email": "string",
      "username": "string"  
    }
    ```
