@ECHO OFF

IF EXIST backup.sql DEL backup.sql
SET PGPASSWORD=ilinca

ECHO Realizam procesarea tabelelor

(FOR %%t IN (
    "site_telefonie_produs"
    "site_telefonie_serviciu"
    "site_telefonie_telefon"
    "site_telefonie_categoriepachet"
    "site_telefonie_promotie"
    "site_telefonie_pachet"
) DO (
    ECHO Procesam tabelul %%t
    ECHO Tabelul %%t

    pg_dump --column-inserts --data-only --inserts -h localhost -U ilinca -p 5432 -d dj2025 -t %%t >> backup.sql
))

SET PGPASSWORD=