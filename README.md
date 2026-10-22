# 🧩 Juego de la placa base (MSI A88XM-E35 V2)

Juego interactivo hecho con [Streamlit](https://streamlit.io) para aprender los componentes de una placa base.

- **Juego 1:** 22 componentes de la placa MSI A88XM-E35 V2.
- **Juego 2:** 13 elementos del panel trasero.
- **Modos:** *Relacionar todo* (asignar nombre a cada número) y *¿Qué número es?* (pregunta a pregunta).

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar gratis

1. Sube esta carpeta a un repositorio de GitHub.
2. Entra en <https://share.streamlit.io>, pulsa **New app**, elige el repositorio y `app.py`.

## Estructura

```
app.py
requirements.txt
assets/
  msi_componentes.png
  msi_trasero.png
```

Para cambiar nombres o explicaciones, edita el diccionario `GAMES` de `app.py`.
