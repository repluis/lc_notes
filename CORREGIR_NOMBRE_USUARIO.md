# Cómo Corregir el Nombre de Usuario en los Commits

## Paso 1: Configurar el nombre de usuario local (SOLO para este repositorio)

Ejecuta estos comandos en PowerShell:

```bash
git config user.name "Luis Cedeño"
git config user.email "luis2000.dev@gmail.com"
```

Verifica que se configuró correctamente:

```bash
git config user.name
git config user.email
```

**✅ A partir de ahora, todos los commits nuevos usarán tu nombre correcto.**

---

## Paso 2: Corregir los commits anteriores

Tienes dos opciones dependiendo de si quieres cambiar todos los commits o solo algunos:

### Opción A: Corregir solo los últimos commits en la rama `develop`

Si solo quieres corregir los commits que acabas de hacer en `develop`:

```bash
# Cambiar a la rama develop
git checkout develop

# Corregir los últimos 2 commits (o el número que necesites)
git rebase -i HEAD~2
```

En el editor que se abre, cambia `pick` por `edit` en los commits que quieres corregir, guarda y cierra.

Luego ejecuta:

```bash
git commit --amend --author="Luis Cedeño <luis2000.dev@gmail.com>" --no-edit
git rebase --continue
```

Repite el último comando por cada commit que marcaste como `edit`.

Finalmente, fuerza el push (cuidado, esto reescribe el historial):

```bash
git push --force-with-lease origin develop
```

### Opción B: Corregir automáticamente todos los commits de una rama

Si quieres corregir todos los commits de `jeanpitx` a `Luis Cedeño` en la rama `develop`:

```bash
# Cambiar a la rama develop
git checkout develop

# Corregir todos los commits del autor jeanpitx
git filter-branch --env-filter '
if [ "$GIT_AUTHOR_NAME" = "jeanpitx" ]; then
    export GIT_AUTHOR_NAME="Luis Cedeño"
    export GIT_AUTHOR_EMAIL="luis2000.dev@gmail.com"
fi
if [ "$GIT_COMMITTER_NAME" = "jeanpitx" ]; then
    export GIT_COMMITTER_NAME="Luis Cedeño"
    export GIT_COMMITTER_EMAIL="luis2000.dev@gmail.com"
fi
' --tag-name-filter cat -- --branches --tags
```

Luego fuerza el push:

```bash
git push --force-with-lease origin develop
```

### Opción C: Usar git rebase con exec (más simple)

```bash
# Cambiar a develop
git checkout develop

# Corregir los últimos N commits (cambia 3 por el número que necesites)
git rebase -i HEAD~3 --exec 'git commit --amend --author="Luis Cedeño <luis2000.dev@gmail.com>" --no-edit'

# Forzar push
git push --force-with-lease origin develop
```

---

## Paso 3: Corregir commits en la rama `main`

Si también necesitas corregir commits en `main`:

```bash
# Cambiar a main
git checkout main

# Ver los commits para identificar cuántos corregir
git log --oneline --author="jeanpitx"

# Corregir los commits (ajusta el número según necesites)
git rebase -i HEAD~2 --exec 'git commit --amend --author="Luis Cedeño <luis2000.dev@gmail.com>" --no-edit'

# Forzar push
git push --force-with-lease origin main
```

---

## ⚠️ IMPORTANTE

1. **`--force-with-lease` es más seguro que `--force`**: Previene sobrescribir trabajo de otros
2. **Avisa a tu equipo**: Si trabajas con otros, avísales antes de hacer force push
3. **Backup**: Considera crear una rama de respaldo antes:
   ```bash
   git branch backup-develop develop
   ```

---

## Verificar que funcionó

Después de corregir, verifica:

```bash
git log --oneline --pretty=format:"%h - %an (%ae) : %s" -5
```

Deberías ver `Luis Cedeño (luis2000.dev@gmail.com)` en lugar de `jeanpitx`.

---

## Nota sobre commits ya subidos

Si los commits ya fueron subidos a GitHub/GitLab, necesitarás usar `--force-with-lease` para actualizarlos. Esto reescribe el historial, así que ten cuidado.


