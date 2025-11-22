@echo off
echo ========================================
echo   PREPARATION POUR GITHUB ET DEPLOIEMENT
echo ========================================
echo.

echo [1/5] Verification de Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Git n'est pas installe. Installez-le depuis https://git-scm.com
    pause
    exit /b 1
)
echo [OK] Git est installe

echo.
echo [2/5] Initialisation du repository Git...
if not exist .git (
    git init
    echo [OK] Repository Git initialise
) else (
    echo [OK] Repository Git deja initialise
)

echo.
echo [3/5] Ajout des fichiers...
git add .
echo [OK] Fichiers ajoutes

echo.
echo [4/5] Creation du commit initial...
git commit -m "Initial commit - Detection Poubelles App" >nul 2>&1
echo [OK] Commit cree

echo.
echo [5/5] Instructions pour GitHub:
echo.
echo ========================================
echo   PROCHAINES ETAPES
echo ========================================
echo.
echo 1. Allez sur https://github.com/new
echo 2. Creez un nouveau repository nomme: detection-poubelles
echo 3. NE cochez PAS "Initialize with README"
echo 4. Copiez l'URL de votre repository
echo.
echo 5. Executez ces commandes (remplacez VOTRE_USERNAME):
echo.
echo    git remote add origin https://github.com/VOTRE_USERNAME/detection-poubelles.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 6. Consultez DEPLOIEMENT.md pour deployer votre app!
echo.
echo ========================================
pause
