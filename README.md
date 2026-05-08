# Pruebas Automatizadas Desafio Opencart

Suite de automatización de pruebas funcionales sobre [https://opencart.abstracta.us/](https://opencart.abstracta.us/) construida con **Python + Playwright + Behave (BDD)**, siguiendo el patrón **Page Object Model**.

---

## 1. Justificación de los casos de prueba seleccionados

Se eligieron tres flujos representativos de un ecommerce, con alta cobertura funcional y valor de negocio:

| # | Flujo | Justificación |
|---|-------|---------------|
| 1 | **Registro de nuevo usuario** | Es el punto de entrada al ecommerce. Valida formularios, validaciones de campo, política de privacidad y la creación efectiva de la cuenta. |
| 2 | **Búsqueda de producto y agregado al carrito** | Funcionalidad central del catálogo. Cubre buscador, listado de resultados, navegación al detalle del producto y persistencia en el carrito. |
| 3 | **Checkout como invitado (guest checkout)** | Flujo de mayor impacto comercial. Integra dirección de facturación, método de envío, método de pago y confirmación de orden. |

Estos tres casos juntos recorren las páginas críticas del sitio (home, búsqueda, detalle, carrito, registro y checkout completo) y permiten detectar regresiones con alto retorno de inversión.

---

## 2. Stack y justificación

- **Python 3.11+** — lenguaje versátil y popular en QA.
- **Playwright** — auto-waits robustos, soporte nativo cross-browser (Chromium, Firefox, WebKit), screenshots y trace integrados.
- **Behave** — BDD en Gherkin, tests legibles por stakeholders y usuarios no tecnicos.
- **Faker** — datos dinámicos por ejecución (emails, nombres únicos), tests idempotentes.
- **behave-html-formatter** — reporte HTML único, fácil de compartir.
- **Page Object Model** — desacopla los selectores de la lógica de prueba.

---

## 3. Estructura del proyecto

```
opencart_desafioQA/
├── features/
│   ├── environment.py          # Hooks de ciclo de vida (Playwright + screenshots)
│   ├── register.feature        # Feature: registro
│   ├── search.feature          # Feature: búsqueda + carrito
│   ├── checkout.feature        # Feature: guest checkout
│   └── steps/                  # Step definitions 
├── pages/                      # Page Objects (selectores encapsulados por página)
├── utils/                      # config, data_factory (Faker), logger
├── reports/
│   ├── report.html             # Reporte HTML generado tras cada ejecución
│   └── screenshots/            # Capturas automáticas en escenarios fallidos
├── behave.ini                  # Configuración de Behave (formatter HTML)
├── requirements.txt
└── README.md
```

---

## 4. Pre-requisitos

- Python 3.11 o superior
- pip
- Conexión a internet
- Clonar repositorio: git clone https://github.com/GonzaloArevaloT/opencart-desafio-qa.git

---

## 5. Instalación

### 5.1. Crear y activar el entorno virtual

```bash
# Crear el entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux / Mac)
source venv/bin/activate
```

### 5.2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5.3. Instalar los navegadores de Playwright

```bash
playwright install
```

> Esto descarga las versiones de Chromium, Firefox y WebKit necesarias para la ejecución cross-browser.

---

## 6. Variables de entorno

Se leen del sistema operativo.

| Variable | Valores | Default | Descripción |
|----------|---------|---------|-------------|
| `BROWSER` | `chromium`, `firefox`, `webkit` | `chromium` | Navegador a utilizar |
| `HEADLESS` | `true`, `false` | `true` | Modo headless |
| `BASE_URL` | URL | `https://opencart.abstracta.us/` | URL base del sitio |
| `DEFAULT_TIMEOUT` | número (ms) | `15000` | Timeout por defecto de Playwright |

### Cómo definirlas

**Windows (PowerShell):**
```powershell
$env:BROWSER="firefox"
$env:HEADLESS="false"
behave
```

**Windows (CMD):**
```cmd
set BROWSER=firefox
set HEADLESS=false
behave
```

**Linux / Mac:**
```bash
BROWSER=firefox HEADLESS=false behave
```

---

## 7. Ejecución de las pruebas

> **Importante:** todos los comandos deben ejecutarse con el entorno virtual activado.

### 7.1. Ejecutar toda la suite

```bash
behave
```

### 7.2. Ejecutar un feature individual

```bash
behave features/register.feature
behave features/search.feature
behave features/checkout.feature
```

### 7.3. Ejecutar por tag

```bash
behave --tags=@register
behave --tags=@search
behave --tags=@checkout
behave --tags=@smoke
```

### 7.4. Ejecutar en otro navegador

```powershell
# PowerShell
$env:BROWSER="firefox"; behave
$env:BROWSER="webkit"; behave
```

### 7.5. Ejecutar en modo visible (no headless)

```powershell
$env:HEADLESS="false"; behave
```

---

## 8. Reportes

Tras cada ejecución se genera automáticamente un reporte HTML en:

```
reports/report.html
```

Ábrelo con cualquier navegador para revisar:

- Escenarios pasados / fallidos
- Duración total y por escenario
- Pasos ejecutados con su detalle
- Mensajes de error en caso de fallo

### Screenshots de fallos

Si un escenario falla, Playwright captura automáticamente una imagen de la página y la guarda en:

```
reports/screenshots/<nombre_escenario>_<timestamp>.png
```

---

## 9. Buenas prácticas aplicadas

- **Page Object Model** — cada página encapsula sus selectores y acciones.
- **Datos dinámicos con Faker** — emails únicos por ejecución, tests idempotentes.
- **Scenario Outlines** — parametrización nativa de Gherkin.
- **Hooks de Behave** — aislamiento por escenario, navegador limpio en cada test.
- **Tags** para ejecución selectiva.
- **Logging estructurado** en lugar de prints.
- **Configuración externalizada** vía variables de entorno del SO.
- **Codigo comentado.**

---

## 10. Resolución de algunos problemas

- **`playwright: command not found`** → activar el entorno virtual antes de ejecutar.
- **Error al lanzar el navegador** → ejecutar `playwright install` para descargar los navegadores.
- **Tests fallan en headless pero pasan visibles** → revisar timeouts o aumentar `DEFAULT_TIMEOUT`.
- **El sitio público está caído** → la suite depende de `https://opencart.abstracta.us/`. Verificar disponibilidad.
