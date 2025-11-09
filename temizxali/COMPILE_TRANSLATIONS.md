# Tərcümələri Kompilyasiya Etmək

Statik mətnlərin tərcümə olunması üçün tərcümə fayllarını kompilyasiya etmək lazımdır.

## Komanda:

```bash
cd temizxali
python manage.py compilemessages
```

Bu komanda `locale/ru/LC_MESSAGES/django.mo` faylını yaradacaq və statik mətnlər tərcümə olunacaq.

## Qeyd:

Əgər Django quraşdırılmamışdırsa, virtual environment aktivləşdirin və ya Django quraşdırın:

```bash
pip install django
python manage.py compilemessages
```

