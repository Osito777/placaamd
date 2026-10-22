"""Juego de la placa base MSI A88XM-E35 V2 (Streamlit).

Juego 1: componentes de la placa. Juego 2: elementos del panel trasero.
Modos: "Relacionar todo" y "¿Qué número es?".
"""
import random
from pathlib import Path

import streamlit as st

BASE = Path(__file__).parent

st.set_page_config(page_title="Juego: placa base", page_icon="🧩", layout="wide")


def it(num, name, silk, desc):
    return {"num": num, "name": name, "silk": silk, "desc": desc}


MSI_GAMES = {
    "juego1": {
        "title": "Juego 1 · Componentes de la placa",
        "image": "assets/msi_componentes.png",
        "items": [
            it(1, "Zócalo del procesador (Socket FM2+)", "—", "Aloja el procesador/APU AMD (socket FM2+)."),
            it(2, "Anclaje del disipador", "—", "Sujeta con tornillos el disipador y el ventilador de la CPU."),
            it(3, "Ranuras de RAM DDR3", "DIMM1, DIMM2", "Alojan la memoria DDR3 (2 ranuras, dual channel, hasta 32 GB)."),
            it(4, "Conector ATX de 24 pines", "JPWR1", "Recibe de la fuente la corriente (3,3 V, 5 V y 12 V) para toda la placa."),
            it(5, "Conector ATX12V de 4 pines", "JPWR2", "Lleva 12 V de la fuente a los reguladores del procesador."),
            it(6, "VRM (MOSFET, bobinas y condensadores)", "—", "Convierte y estabiliza los 12 V en la tensión baja que necesita la CPU."),
            it(7, "Chipset AMD A88X con disipador azul", "—", "Comunica la CPU con SATA, USB, PCI, audio, etc."),
            it(8, "Conectores SATA III", "SATA1 – SATA6", "Conectan discos duros, SSD y unidades ópticas (6 puertos, RAID 0/1/5/10)."),
            it(9, "Ranura PCI Express 3.0 x16", "PCI_E1", "Para la tarjeta gráfica dedicada (PCIe 3.0 solo con CPU FM2+)."),
            it(10, "Ranura PCI Express 2.0 x1", "PCI_E2", "Para tarjetas pequeñas: red, sonido, USB adicional…"),
            it(11, "Ranura PCI", "PCI1", "Ranura clásica para tarjetas antiguas."),
            it(12, "Pila CR2032", "BAT1", "Alimenta el reloj (RTC) y la memoria CMOS de la BIOS."),
            it(13, "Condensador electrolítico", "—", "Almacena y filtra la corriente para estabilizar las tensiones."),
            it(14, "Chip Super I/O (Fintek F71878AD)", "—", "Gestiona PS/2, puertos heredados, ventiladores y sensores."),
            it(15, "Conectores USB 2.0 internos", "JUSB1, JUSB2", "Para los USB 2.0 frontales de la caja (2 puertos cada uno)."),
            it(16, "Conector USB 3.0 interno", "JUSB3", "Para los USB 3.0 frontales de la caja (2 puertos)."),
            it(17, "Conector del panel frontal (System Panel)", "JFP1", "Botón de encendido, reset y LEDs de la caja."),
            it(18, "Conector de audio frontal", "JAUD1", "Audio HD del frontal de la caja (auriculares y micrófono)."),
            it(19, "Conector del puerto paralelo (LPT)", "JLPT1", "Permite añadir un puerto paralelo (impresoras antiguas)."),
            it(20, "Conector del puerto serie (COM)", "JCOM1", "Permite añadir un puerto serie RS-232."),
            it(21, "Conector de ventilador de la caja", "SYSFAN2", "Alimenta y controla un ventilador del chasis."),
            it(22, "Puerto de red Gigabit LAN (RJ45)", "—", "Red Ethernet 10/100/1000 Mb/s (Realtek RTL8111G)."),
        ],
    },
    "juego2": {
        "title": "Juego 2 · Panel trasero",
        "image": "assets/msi_trasero.png",
        "items": [
            it(1, "PS/2 ratón (verde)", "—", "Conecta un ratón PS/2."),
            it(2, "PS/2 teclado (púrpura)", "—", "Conecta un teclado PS/2."),
            it(3, "USB 2.0 (4 puertos)", "—", "Periféricos USB de velocidad media (480 Mb/s)."),
            it(4, "VGA (D-Sub 15 pines)", "—", "Salida de vídeo analógica, hasta 1920×1200."),
            it(5, "DVI-D", "—", "Salida de vídeo digital, hasta 2560×1600. Sin audio."),
            it(6, "HDMI", "HDMI", "Salida digital de vídeo y audio."),
            it(7, "LAN (RJ45)", "—", "Red Ethernet Gigabit."),
            it(8, "USB 3.0 (azules)", "—", "Dos puertos USB de hasta 5 Gb/s."),
            it(9, "Line-In (azul)", "—", "Entrada de audio analógica estéreo."),
            it(10, "Line-Out (verde)", "—", "Salida de audio hacia altavoces o auriculares."),
            it(11, "Micrófono (rosa)", "—", "Entrada de micrófono."),
            it(12, "Conector ATX12V de 4 pines (JPWR2)", "JPWR2", "Alimenta la CPU (referencia: no es de panel trasero)."),
            it(13, "Zócalo de CPU (Socket FM2+)", "—", "Aloja el procesador (referencia: no es de panel trasero)."),
        ],
    },
}

BOARDS = {
    "MSI A88XM-E35 V2": {"id": "msi", "games": MSI_GAMES, "caption": "Socket FM2+ · chipset AMD A88X · Micro-ATX"},
}


# ------------------------------------------------------------------ utilidades
def reset_game(gkey):
    for k in list(st.session_state.keys()):
        if k.endswith(f"_{gkey}") or f"_{gkey}_" in k:
            del st.session_state[k]


def show_image(game):
    path = BASE / game["image"]
    if path.exists():
        try:
            st.image(str(path), width="stretch")  # Streamlit reciente
        except TypeError:
            st.image(str(path), use_container_width=True)  # Streamlit antiguo
    else:
        st.error(f"No se encuentra la imagen: {game['image']}")


# --------------------------------------------------------------- modo relacionar
def mode_match(gkey, game, show_hint):
    items = game["items"]
    names = [i["name"] for i in items]

    order_key = f"order_{gkey}"
    if order_key not in st.session_state:
        shuffled = names[:]
        random.shuffle(shuffled)
        st.session_state[order_key] = shuffled
    options = st.session_state[order_key]

    col_img, col_form = st.columns([3, 2], gap="large")
    with col_img:
        show_image(game)
    with col_form:
        st.markdown("**Elige el nombre que corresponde a cada número:**")
        box = st.container(height=640)
        with box:
            for i in items:
                label = f"Nº {i['num']}"
                if show_hint:
                    label += f"  (serigrafía: {i['silk']})"
                st.selectbox(label, options, index=None, placeholder="Elige…",
                             key=f"sel_{gkey}_{i['num']}")

    b1, b2, _ = st.columns([1, 1, 4])
    if b1.button("✅ Comprobar", type="primary", key=f"check_btn_{gkey}"):
        st.session_state[f"checked_{gkey}"] = True
    if b2.button("🔄 Reiniciar", key=f"reset_btn_{gkey}"):
        reset_game(gkey)
        st.rerun()

    if st.session_state.get(f"checked_{gkey}"):
        answers = {i["num"]: st.session_state.get(f"sel_{gkey}_{i['num']}") for i in items}
        unanswered = [n for n, a in answers.items() if a is None]
        used = [a for a in answers.values() if a is not None]
        correct = sum(1 for i in items if answers[i["num"]] == i["name"])

        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("Aciertos", f"{correct} / {len(items)}")
        c2.metric("Nota sobre 10", f"{correct / len(items) * 10:.1f}")
        if correct == len(items):
            st.balloons()
            st.success("¡Perfecto! Has relacionado todo correctamente.")
        if unanswered:
            st.warning("Sin responder: " + ", ".join(f"Nº {n}" for n in unanswered))
        if len(used) != len(set(used)):
            st.info("Has usado algún nombre más de una vez; revisa tus respuestas.")

        with st.expander("Ver resultados detallados", expanded=True):
            for i in items:
                a = answers[i["num"]]
                if a == i["name"]:
                    st.markdown(f"✅ **Nº {i['num']}** · {i['name']}")
                else:
                    st.markdown(
                        f"❌ **Nº {i['num']}** · Tu respuesta: *{a or 'sin responder'}* → "
                        f"Correcto: **{i['name']}**  \n&nbsp;&nbsp;&nbsp;&nbsp;{i['desc']}"
                    )


# ----------------------------------------------------------------- modo pregunta
def mode_quiz(gkey, game, show_hint):
    items = game["items"]
    qk = f"quiz_{gkey}"
    if qk not in st.session_state:
        order = items[:]
        random.shuffle(order)
        st.session_state[qk] = {"order": order, "i": 0, "score": 0, "answered": False, "ok": None}
    s = st.session_state[qk]
    total = len(s["order"])

    col_img, col_q = st.columns([3, 2], gap="large")
    with col_img:
        show_image(game)
    with col_q:
        if s["i"] >= total:
            st.markdown("### 🏁 ¡Terminado!")
            st.metric("Aciertos", f"{s['score']} / {total}")
            st.metric("Nota sobre 10", f"{s['score'] / total * 10:.1f}")
            if s["score"] == total:
                st.balloons()
            if st.button("🔄 Jugar otra vez", type="primary", key=f"again_{gkey}"):
                reset_game(gkey)
                st.rerun()
            return

        item = s["order"][s["i"]]
        st.progress(s["i"] / total, text=f"Pregunta {s['i'] + 1} de {total} · Aciertos: {s['score']}")
        st.markdown(f"### ¿Qué número es…?\n## {item['name']}")
        if show_hint:
            st.caption(f"Pista, serigrafía: {item['silk']}")

        nums = sorted(i["num"] for i in items)
        choice = st.selectbox("Número de la foto", nums, index=None, placeholder="Elige un número…",
                              key=f"choice_{gkey}_{s['i']}", disabled=s["answered"])

        if not s["answered"]:
            if st.button("Responder", type="primary", disabled=choice is None, key=f"answer_{gkey}_{s['i']}"):
                s["answered"] = True
                s["ok"] = choice == item["num"]
                if s["ok"]:
                    s["score"] += 1
                st.rerun()
        else:
            if s["ok"]:
                st.success(f"✅ ¡Correcto! Es el nº {item['num']}.")
            else:
                st.error(f"❌ No. Es el nº {item['num']}.")
            st.info(item["desc"])
            label = "Siguiente ➜" if s["i"] + 1 < total else "Ver resultado"
            if st.button(label, type="primary", key=f"next_{gkey}_{s['i']}"):
                s["i"] += 1
                s["answered"] = False
                s["ok"] = None
                st.rerun()

        if st.button("🔄 Reiniciar", key=f"quiz_reset_{gkey}"):
            reset_game(gkey)
            st.rerun()


# ------------------------------------------------------------------------ main
st.title("🧩 Juego: conoce la placa base")

with st.sidebar:
    st.header("Configuración")
    board_label = list(BOARDS.keys())[0]
    board = BOARDS[board_label]
    game_label = st.radio("Juego", [g["title"] for g in board["games"].values()])
    mode = st.radio("Modo", ["Relacionar todo", "¿Qué número es?"])
    hint = st.checkbox("Mostrar pista (serigrafía)", value=False)
    st.divider()
    st.markdown("**Cómo se juega**\n\n- *Relacionar todo*: asigna un nombre a cada número y pulsa Comprobar.\n"
                "- *¿Qué número es?*: te dicen un componente y eliges su número en la foto.")

st.caption(f"{board_label} · {board['caption']}")
gid = next(k for k, g in board["games"].items() if g["title"] == game_label)
game = board["games"][gid]
gkey = f"{board['id']}_{gid}"
st.subheader(game["title"])

if mode == "Relacionar todo":
    mode_match(gkey, game, hint)
else:
    mode_quiz(gkey, game, hint)
