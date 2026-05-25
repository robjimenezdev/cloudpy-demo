# Cloudpy Demo — Git Workflow (dev → staging → prod)

Mini API Flask para demostrar el flujo Git de tres entornos.

## Estructura

```
cloudpy-demo/
├── src/
│   └── app.py                     # API Flask
├── tests/
│   └── test_app.py                # Tests con pytest
├── .github/
│   └── workflows/
│       ├── deploy-dev.yml         # Push a dev → deploy DEV
│       ├── deploy-staging.yml     # Push a staging → deploy STAGING
│       └── deploy-prod.yml        # Push a main → aprobación → deploy PROD
└── requirements.txt
```

## Endpoints

| Endpoint | Descripción |
|---|---|
| `GET /` | Estado del servicio y entorno activo |
| `GET /plan?llamadas=150` | Plan recomendado para N llamadas |
| `GET /planes` | Lista todos los planes |

## Ejecutar en local

```bash
pip install -r requirements.txt
APP_ENV=DEV python src/app.py
```

## Tests

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=term-missing
```

## Flujo Git

```
feature/xxx  →  dev  →  staging  →  main
                 ↓          ↓          ↓
               DEV      STAGING      PROD
            (auto)      (auto)    (aprobación manual)
```

## Configurar en GitHub

1. Crear el repo y subir este código
2. Crear las ramas: `dev`, `staging`, `main`
3. Settings → Branches → añadir reglas de protección
4. Settings → Environments → crear `dev`, `staging`, `prod`
   - En `prod`: añadir Required reviewers
5. Settings → Secrets → añadir `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY`
