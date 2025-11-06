#!/bin/bash
# Script para corregir el autor de los commits

# Desactivar pager
export GIT_PAGER=cat

# Configurar nombre local
git config --local user.name "Luis Cedeño"
git config --local user.email "luis2000.dev@gmail.com"

echo "Configuración aplicada:"
git config user.name
git config user.email

# Cambiar a develop si no estamos ahí
current_branch=$(git branch --show-current)
if [ "$current_branch" != "develop" ]; then
    echo "Cambiando a rama develop..."
    git checkout develop
fi

# Corregir los últimos commits
echo "Corrigiendo commits..."
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

echo "Commits corregidos. Verificando:"
git log --format="%h - %an <%ae> : %s" -3


