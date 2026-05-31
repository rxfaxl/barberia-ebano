@echo off
cd /d "C:\Users\BRAVO15\Desktop\app opencode"

set "PATH=C:\Users\BRAVO15\Desktop\app opencode\venv\Scripts;C:\Users\BRAVO15\AppData\Local\Programs\Python\Python312;%PATH%"

echo ========================================
echo       EBANO - Barberia Premium
echo ========================================
echo.
echo  Abriendo navegador...
start "" http://127.0.0.1:8000/
echo.
echo  Admin:  http://127.0.0.1:8000/admin/
echo  Usuario: admin   Clave: admin123
echo.
echo ========================================
echo.

"C:\Users\BRAVO15\Desktop\app opencode\venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000

echo.
pause
