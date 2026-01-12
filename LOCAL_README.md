# Lokal Development Təlimatları

## 1. Layihəni İşə Salmaq

### İlk dəfə (build etmək lazımdırsa):
```bash
docker-compose-local.bat up --build
```

### Normal işə salmaq:
```bash
docker-compose-local.bat up
```

### Arxa planda işə salmaq:
```bash
docker-compose-local.bat up -d
```

### Dayandırmaq:
```bash
docker-compose-local.bat down
```

### Logları görmək:
```bash
docker-compose-local.bat logs -f
```

### Yalnız web servisinin logları:
```bash
docker-compose-local.bat logs -f web
```

---

## 2. Migration-ları İcra Etmək

### Bütün migration-ları icra etmək:
```bash
docker-compose-local.bat exec web python temizxali/manage.py migrate
```

### Yeni migration yaratmaq (model dəyişikliyindən sonra):
```bash
docker-compose-local.bat exec web python temizxali/manage.py makemigrations
```

### Sonra migrate etmək:
```bash
docker-compose-local.bat exec web python temizxali/manage.py migrate
```

### Migration statusunu görmək:
```bash
docker-compose-local.bat exec web python temizxali/manage.py showmigrations
```

---

## 3. Admin İstifadəçisi Yaratmaq

### Superuser yaratmaq (interaktiv):
```bash
docker-compose-local.bat exec web python temizxali/manage.py createsuperuser
```

Bu komanda sizdən soruşacaq:
- Username (istifadəçi adı)
- Email (email ünvanı - boş buraxa bilərsiniz)
- Password (şifrə - 2 dəfə daxil etməlisiniz)

### Admin paneline daxil olmaq:
Browser-də açın: `http://localhost:8000/admin/`

---

## 4. Static Files-ları Toplamaq

### Static files-ları toplamaq:
```bash
docker-compose-local.bat exec web python temizxali/manage.py collectstatic --noinput
```

**Qeyd:** Bu adətən avtomatik olaraq container başlananda işləyir, amma bəzən manual olaraq etmək lazım ola bilər.

---

## 5. Django Shell-ə Daxil Olmaq

### Python shell:
```bash
docker-compose-local.bat exec web python temizxali/manage.py shell
```

### Django shell (daha yaxşı):
```bash
docker-compose-local.bat exec web python temizxali/manage.py shell_plus
```

---

## 6. Database-ə Daxil Olmaq (PostgreSQL)

### PostgreSQL shell-ə daxil olmaq:
```bash
docker-compose-local.bat exec db psql -U postgres -d temizxali_local
```

### SQL komandaları:
```sql
-- Bütün cədvəlləri görmək
\dt

-- İstifadəçiləri görmək
SELECT * FROM auth_user;

-- Çıxış
\q
```

---

## 7. Container-lara Daxil Olmaq

### Web container-ə daxil olmaq:
```bash
docker-compose-local.bat exec web bash
```

### Database container-ə daxil olmaq:
```bash
docker-compose-local.bat exec db sh
```

---

## 8. Əsas Komandalar

### Container-ları yenidən başlatmaq:
```bash
docker-compose-local.bat restart
```

### Yalnız web-i yenidən başlatmaq:
```bash
docker-compose-local.bat restart web
```

### Container-ların statusunu görmək:
```bash
docker-compose-local.bat ps
```

### Container-ları tam silmək (database də silinir):
```bash
docker-compose-local.bat down -v
```

---

## 9. İstifadə Ünvanları

- **Ana səhifə:** http://localhost:8000
- **Admin panel:** http://localhost:8000/admin/
- **Database port:** localhost:5433 (host machine-dən)

---

## 10. Problemlər və Həllər

### Container işləmir?
```bash
docker-compose-local.bat logs web
```

### Database bağlantı problemi?
```bash
docker-compose-local.bat restart db
```

### Static files görünmür?
```bash
docker-compose-local.bat exec web python temizxali/manage.py collectstatic --noinput
docker-compose-local.bat restart web
```

### Yeni paket əlavə etmisiniz?
```bash
docker-compose-local.bat build --no-cache web
docker-compose-local.bat up -d
```

---

## Qeyd

Bütün komandalar `docker-compose-local.bat` istifadə edir ki, deploy fayllarına toxunmasın.

Əgər `.bat` faylı işləmirsə, birbaşa istifadə edin:
```bash
docker-compose -f docker-compose-local.yaml [komanda]
```

