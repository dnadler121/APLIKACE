# Občanka Flask aplikace

## Spuštění

```bash
pip install -r requirements.txt
python app.py
```

Pak otevřete:

```text
http://127.0.0.1:5000
```

## Otázky

Otázky jsou v souboru:

```text
data/questions.csv
```

Formát:

```text
id;question;a;b;c;d;correct
```

Ve sloupci `correct` napište správnou možnost: `a`, `b`, `c` nebo `d`.

## Výsledky

Výsledky se ukládají do:

```text
data/results.csv
```

## Posílání e-mailu

V souboru `app.py` změňte:

```python
TEACHER_EMAIL = "dnadler121@gmail.com"
```

Na Linuxu nebo Windows nastavte proměnné prostředí:

```bash
export MAIL_USERNAME="vas_email@gmail.com"
export MAIL_PASSWORD="heslo_aplikace_z_gmailu"
```

U Gmailu je potřeba použít takzvané „heslo aplikace“, ne běžné heslo k účtu.
