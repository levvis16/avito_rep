# QA  для Avito 

Автоматизированное тестирование микросервиса объявлений Avito QA Internship.

## Требования
- Python 3.8+
- pip
- virtualenv 

## Установка

```powershell
git clone https://github.com/levvis16/avito_rep

python -m venv venv
venv\Scripts\activate         

pip install -r requirements.txt
pytest -v
```

## Alure лежит в allure-report

## Настройка линтера и форматтера для тестового кода

```powershell
pylint *.py utils/            
black .                       
isort . 
```

# Задание 1 лежит в файле TASK_1.md