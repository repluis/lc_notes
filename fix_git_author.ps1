# Script PowerShell para corregir el autor de los commits
$env:GIT_PAGER = 'cat'

Write-Host "=== Configurando nombre de usuario ===" -ForegroundColor Green
git config --local user.name "Luis Cedeño"
git config --local user.email "luis2000.dev@gmail.com"

Write-Host "`nConfiguración aplicada:" -ForegroundColor Yellow
Write-Host "  Nombre: $(git config user.name)" -ForegroundColor Cyan
Write-Host "  Email: $(git config user.email)" -ForegroundColor Cyan

# Verificar rama
$currentBranch = git branch --show-current
Write-Host "`nRama actual: $currentBranch" -ForegroundColor Cyan

if ($currentBranch -ne "develop") {
    Write-Host "Cambiando a rama develop..." -ForegroundColor Yellow
    git checkout develop
}

Write-Host "`n=== Corrigiendo commits anteriores ===" -ForegroundColor Green
Write-Host "Esto corregirá los commits de 'jeanpitx' a 'Luis Cedeño'" -ForegroundColor Yellow

# Usar filter-branch para corregir los commits
git filter-branch -f --env-filter '
if [ "$GIT_AUTHOR_NAME" = "jeanpitx" ]; then
    export GIT_AUTHOR_NAME="Luis Cedeño"
    export GIT_AUTHOR_EMAIL="luis2000.dev@gmail.com"
fi
if [ "$GIT_COMMITTER_NAME" = "jeanpitx" ]; then
    export GIT_COMMITTER_NAME="Luis Cedeño"
    export GIT_COMMITTER_EMAIL="luis2000.dev@gmail.com"
fi
' --tag-name-filter cat HEAD~2..HEAD

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Commits corregidos exitosamente!" -ForegroundColor Green
    Write-Host "`nVerificando cambios:" -ForegroundColor Yellow
    git log --format="%h - %an <%ae> : %s" -3
    
    Write-Host "`nIMPORTANTE: Ahora necesitas hacer force push:" -ForegroundColor Yellow
    Write-Host "  git push --force-with-lease origin develop" -ForegroundColor Cyan
} else {
    Write-Host "`nError al corregir commits." -ForegroundColor Red
}


