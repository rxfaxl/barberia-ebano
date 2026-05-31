& "$PSScriptRoot\venv\Scripts\Activate.ps1"
Write-Host "Iniciando servidor de Barbería..." -ForegroundColor Green
Write-Host "Admin: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host "Usuario: admin / Contraseña: admin123" -ForegroundColor Cyan
python manage.py runserver 0.0.0.0:8000
