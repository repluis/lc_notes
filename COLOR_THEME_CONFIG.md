# Configuración de Tema de Colores

Este proyecto utiliza un sistema de colores basado en variables CSS que permite cambiar fácilmente los colores de toda la aplicación modificando un solo archivo.

## Archivo de Configuración

El archivo principal de configuración de colores está en:
```
static/css/theme.css
```

## Cómo Cambiar los Colores

### 1. Colores Primarios

Los colores principales del gradiente y elementos destacados:

```css
--color-primary-1: #667eea;      /* Azul púrpura */
--color-primary-2: #764ba2;      /* Púrpura */
--color-primary-dark: #4c63d2;   /* Azul oscuro */
--color-primary-light: #8b9eff;  /* Azul claro */
```

**Ejemplo:** Para cambiar a un tema verde, modifica:
```css
--color-primary-1: #10b981;
--color-primary-2: #059669;
```

### 2. Colores de Fondo

```css
--color-bg-primary: #0f0f23;      /* Fondo principal (muy oscuro) */
--color-bg-secondary: #1a1a2e;    /* Fondo secundario */
--color-bg-tertiary: #16213e;     /* Fondo terciario */
--color-bg-card: #1e2749;        /* Fondo de tarjetas */
--color-bg-card-hover: #2a3a5f;   /* Fondo de tarjetas al hover */
```

**Ejemplo:** Para un tema más claro, modifica:
```css
--color-bg-primary: #f5f5f5;
--color-bg-card: #ffffff;
```

### 3. Colores de Texto

```css
--color-text-primary: #ffffff;     /* Texto principal (blanco) */
--color-text-secondary: #b8b8d4;   /* Texto secundario */
--color-text-muted: #8a8a9e;       /* Texto deshabilitado */
--color-text-link: #8b9eff;        /* Color de enlaces */
--color-text-link-hover: #a8b7ff;  /* Color de enlaces al hover */
```

### 4. Colores de Estado

```css
--color-success: #10b981;          /* Verde éxito */
--color-error: #ef4444;             /* Rojo error */
--color-warning: #f59e0b;          /* Amarillo advertencia */
--color-info: #3b82f6;              /* Azul información */
```

### 5. Colores de Botones

```css
--color-btn-primary: linear-gradient(135deg, var(--color-primary-1) 0%, var(--color-primary-2) 100%);
--color-btn-danger: #dc3545;        /* Botón de peligro */
```

## Temas Predefinidos

### Tema Dark (Actual)
Paleta oscura con tonos azul-púrpura.

### Tema Light (Ejemplo)
```css
--color-bg-primary: #f5f5f5;
--color-bg-card: #ffffff;
--color-text-primary: #1a1a1a;
--color-text-secondary: #4a4a4a;
```

### Tema Verde (Ejemplo)
```css
--color-primary-1: #10b981;
--color-primary-2: #059669;
```

## Uso en Templates

Los templates usan las variables CSS directamente:

```html
<div style="background: var(--color-bg-card); color: var(--color-text-primary);">
    Contenido
</div>
```

O usando clases de utilidad:

```html
<div class="bg-card text-primary">
    Contenido
</div>
```

## Variables Disponibles

### Espaciado
- `--spacing-xs`: 0.25rem
- `--spacing-sm`: 0.5rem
- `--spacing-md`: 1rem
- `--spacing-lg`: 1.5rem
- `--spacing-xl`: 2rem

### Bordes
- `--border-radius-sm`: 5px
- `--border-radius-md`: 10px
- `--border-radius-lg`: 15px

### Sombras
- `--shadow-sm`: Sombra pequeña
- `--shadow-md`: Sombra media
- `--shadow-lg`: Sombra grande
- `--shadow-xl`: Sombra extra grande

### Transiciones
- `--transition-fast`: 0.15s
- `--transition-normal`: 0.3s
- `--transition-slow`: 0.5s

## Clases de Utilidad

El archivo `theme.css` incluye clases de utilidad:

- `.text-primary`, `.text-secondary`, `.text-muted`, `.text-link`
- `.bg-primary`, `.bg-secondary`, `.bg-card`
- `.border-primary`, `.border-secondary`

## Recomendaciones

1. **Mantén el contraste**: Asegúrate de que el texto sea legible sobre los fondos
2. **Consistencia**: Usa las variables CSS en lugar de colores hardcodeados
3. **Accesibilidad**: Verifica que los colores cumplan con WCAG AA (contraste mínimo 4.5:1)
4. **Testing**: Prueba los cambios en diferentes dispositivos y navegadores

## Herramientas Útiles

- [Coolors](https://coolors.co/) - Generador de paletas de colores
- [Contrast Checker](https://webaim.org/resources/contrastchecker/) - Verificar contraste
- [Material Design Color Tool](https://material.io/resources/color/) - Paletas de Material Design

