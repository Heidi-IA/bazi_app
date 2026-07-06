import os
import json
import uuid
import threading
import tempfile
from io import BytesIO
import anthropic
from flask import Flask, render_template, request, jsonify, session, send_file
from flask_session import Session
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    Table, TableStyle, KeepTogether,
)
from utils.bazi_rules import (
    detectar_combinaciones_troncos, detectar_choques_troncos,
    detectar_combinaciones_ramas, detectar_conflictos_ramas,
    detectar_relaciones, detectar_salud_especial,
    analizar_cinco_elementos, calcular_yin_yang,
    calcular_cesta_elementos, get_cesta_desc,
    get_animal_elemento_desc, get_muerte_vacio,
    BLOQUEOS_FINANCIEROS, PILARES_INFO, DM_DESC,
    SALUD_ELEMENTOS, SALUD_DIOSES, CESTA_ELEMENTOS,
    DIOSES_DESC, ANIMALES_DESC, _rama_nombre,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# ============================================================
# SESIÓN DEL LADO DEL SERVIDOR (evita el error de cookie gigante)
# ============================================================
# Por defecto, Flask guarda toda la sesión codificada dentro de la
# cookie del navegador, que tiene un límite de ~4KB. El análisis BaZi
# (combinaciones, conflictos, descripciones, etc.) supera ese límite
# fácilmente, lo que provoca que Heroku devuelva 502 "oversized cookie"
# y la sesión se pierda a mitad de la generación del informe.
# Con Flask-Session, la cookie solo guarda un ID corto y los datos
# reales quedan en archivos dentro de /tmp (visibles para todos los
# workers del mismo dyno, igual que los jobs de informe).
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(tempfile.gettempdir(), "flask_session")
app.config["SESSION_PERMANENT"] = False
os.makedirs(app.config["SESSION_FILE_DIR"], exist_ok=True)
Session(app)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ============================================================
# JOBS DE GENERACIÓN DE INFORME (persistidos en disco)
# ============================================================
# Heroku puede atender cada request con un proceso worker distinto,
# así que un diccionario en memoria de Python no alcanza: un worker
# podría crear el job y otro (que no lo tiene en su memoria) atender
# la consulta de estado, devolviendo 404. Guardamos cada job como un
# archivo JSON en /tmp, que sí es visible para todos los workers del
# mismo dyno.
JOBS_DIR = os.path.join(tempfile.gettempdir(), "informe_jobs")
os.makedirs(JOBS_DIR, exist_ok=True)


def _job_path(job_id):
    return os.path.join(JOBS_DIR, f"{job_id}.json")


def _job_leer(job_id):
    try:
        with open(_job_path(job_id), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _job_escribir(job_id, data):
    # Escritura atómica: escribimos a un archivo temporal y renombramos,
    # para evitar que otro proceso lea un JSON a medio escribir.
    tmp_path = _job_path(job_id) + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    os.replace(tmp_path, _job_path(job_id))


def _job_borrar(job_id):
    try:
        os.remove(_job_path(job_id))
    except FileNotFoundError:
        pass

# ============================================================
# COMBINACIONES DE DIOSES POR PILAR
# ============================================================
COMBO_DIOSES_PILAR = [
    {
        "requiere": ["RD","OD"],
        "excluye": [],
        "desc": "Reconocimiento institucional, ascenso, educación formal.",
    },
    {
        "requiere": ["7M"],
        "excluye": ["RI","RD"],
        "desc": "Presión intensa, autoridad adversa, conflictos legales o de poder.",
    },
    {
        "requiere": ["DD","DC"],
        "excluye": [],
        "desc": "Expansión en negocios, creatividad lucrativa, nuevas fuentes de ingresos.",
    },
    {
        "requiere": ["RR","RI"],
        "excluye": [],
        "desc": "Pérdidas por terceros, pensamientos mágicos, inversiones mal calculadas, traición en relaciones.",
    },
    {
        "requiere": ["RD","DD"],
        "excluye": [],
        "desc": "Estabilidad, logros consistentes, matrimonio, acumulación.",
    },
]

def detectar_combo_dioses(pilar_datos):
    """Detecta combinaciones de dioses dentro de un pilar."""
    dioses_pilar = set()
    dios_t = pilar_datos.get("tronco",{}).get("dios","")
    if dios_t:
        dioses_pilar.add(dios_t)
    for to in pilar_datos.get("troncos_ocultos",[]):
        d = to.get("dios","")
        if d:
            dioses_pilar.add(d)

    resultados = []
    for combo in COMBO_DIOSES_PILAR:
        requiere = set(combo["requiere"])
        excluye  = set(combo["excluye"])
        if requiere.issubset(dioses_pilar):
            if not excluye or not excluye.intersection(dioses_pilar):
                resultados.append(combo["desc"])
    return resultados


# ============================================================
# PROMPT DE EXTRACCIÓN
# ============================================================
EXTRACTION_PROMPT = """Extraé de estas imágenes BAZI todos los datos y respondé ÚNICAMENTE con un JSON válido (sin markdown, sin backticks, sin explicaciones).

Estructura exacta requerida:
{
  "carta_fija": {
    "hora":  {"tronco":{"nombre":"","elemento":"","polaridad":"","dios":""},"rama":{"nombre":"","elemento":"","polaridad":""},"troncos_ocultos":[{"nombre":"","dios":""}]},
    "dia":   {"tronco":{"nombre":"","elemento":"","polaridad":"","dios":""},"rama":{"nombre":"","elemento":"","polaridad":""},"troncos_ocultos":[{"nombre":"","dios":""}]},
    "mes":   {"tronco":{"nombre":"","elemento":"","polaridad":"","dios":""},"rama":{"nombre":"","elemento":"","polaridad":""},"troncos_ocultos":[{"nombre":"","dios":""}]},
    "anio":  {"tronco":{"nombre":"","elemento":"","polaridad":"","dios":""},"rama":{"nombre":"","elemento":"","polaridad":""},"troncos_ocultos":[{"nombre":"","dios":""}]}
  },
  "carta_movil": {
    "pilar_suerte": {"periodo":"","tronco":{"nombre":"","elemento":"","polaridad":"","dios":""},"rama":{"nombre":"","elemento":"","polaridad":""},"troncos_ocultos":[{"nombre":"","dios":""}]},
    "anio_curso":   {"anio":"","tronco":{"nombre":"","elemento":"","polaridad":"","dios":""},"rama":{"nombre":"","elemento":"","polaridad":""},"troncos_ocultos":[{"nombre":"","dios":""}]}
  },
  "dia_maestro":{
    "nombre":"","elemento":"","polaridad":"",
    "hombre_noble":[],"inteligencia":"","caballo_celeste":"",
    "flor_melocoton":"","estrella_vida":""
  },
  "cinco_elementos":{
    "fuego":  {"porcentaje":0,"representa":""},
    "tierra": {"porcentaje":0,"representa":""},
    "metal":  {"porcentaje":0,"representa":""},
    "agua":   {"porcentaje":0,"representa":""},
    "madera": {"porcentaje":0,"representa":""}
  },
  "dioses_presentes": [],
  "dioses_ausentes": []
}

Instrucciones:
- Para cinco_elementos.representa: extraé exactamente la palabra que aparece bajo cada elemento (Recurso, Compañero, Producción, Riqueza o Influencia).
- Para dioses_presentes y dioses_ausentes: analizá el cuadro de 10 aspectos. Los que tienen porcentaje > 0 son presentes, los que tienen 0 son ausentes.
- Para flor_melocoton: extraé el animal que aparece en el cuadro de análisis básico.
- Para hombre_noble: extraé los animales que aparecen como nobles.
- Para inteligencia, caballo_celeste: extraé los animales correspondientes."""


# ============================================================
# RUTAS
# ============================================================

def _expandir_dioses_pilar(datos):
    """Devuelve una copia de los datos de un pilar donde cada código de
    dios (p. ej. "OH", "DD") viene acompañado de su nombre completo
    correcto (p. ej. "Oficial Herido"), tomado de DIOSES_DESC.

    Esto es necesario porque la extracción por imagen sólo captura el
    código de 2-3 letras (como aparece en la carta), y si el modelo que
    redacta el informe solo ve ese código, a veces lo traduce mal por su
    cuenta (p. ej. "Output Honorable" en vez de "Oficial Herido"). Al
    resolver el nombre completo acá, en código, el modelo ya no tiene
    que adivinar ni inventar una traducción.
    """
    nuevo = dict(datos)

    tronco = dict(nuevo.get("tronco", {}))
    dios_t = tronco.get("dios", "")
    if dios_t:
        tronco["dios_nombre"] = DIOSES_DESC.get(dios_t, {}).get("nombre", dios_t)
    nuevo["tronco"] = tronco

    ocultos_nuevos = []
    for to in nuevo.get("troncos_ocultos", []):
        to2 = dict(to)
        dios_o = to2.get("dios", "")
        if dios_o:
            to2["dios_nombre"] = DIOSES_DESC.get(dios_o, {}).get("nombre", dios_o)
        ocultos_nuevos.append(to2)
    nuevo["troncos_ocultos"] = ocultos_nuevos

    return nuevo


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/carta", methods=["POST"])
def carta():
    data = request.get_json()
    session["usuario"] = {
        "nombre": data.get("nombre"),
        "fecha":  data.get("fecha"),
        "hora":   data.get("hora"),
        "sexo":   data.get("sexo"),
        "email":  data.get("email"),
    }
    return jsonify({"ok": True})


@app.route("/extraer", methods=["POST"])
def extraer():
    try:
        imagenes = request.get_json().get("imagenes", [])
        content = []
        for img in imagenes:
            content.append({
                "type": "image",
                "source": {"type":"base64","media_type":img["media_type"],"data":img["data"]}
            })
        content.append({"type":"text","text":EXTRACTION_PROMPT})

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{"role":"user","content":content}]
        )
        raw = response.content[0].text.strip()
        extracted = json.loads(raw)
        session["carta"] = extracted
        return jsonify({"ok":True,"data":extracted})
    except Exception as e:
        return jsonify({"ok":False,"error":str(e)}), 500


@app.route("/validar", methods=["POST"])
def validar():
    try:
        data           = request.get_json()
        carta          = data.get("carta", session.get("carta",{}))
        pilares_extra  = data.get("pilares_adicionales",[])
        usuario        = session.get("usuario",{})
        sexo           = usuario.get("sexo","mujer")

        # Construir todos los pilares
        todos_pilares = {}
        for nombre, datos in carta.get("carta_fija",{}).items():
            todos_pilares[nombre] = datos
        cm = carta.get("carta_movil",{})
        if cm.get("pilar_suerte"):
            todos_pilares["pilar_suerte"] = cm["pilar_suerte"]
        if cm.get("anio_curso"):
            todos_pilares["anio_curso"] = cm["anio_curso"]
        for extra in pilares_extra:
            todos_pilares[extra["nombre"]] = extra

        # Datos del día maestro
        dm          = carta.get("dia_maestro",{})
        dm_tronco   = dm.get("nombre","")
        dm_rama     = carta.get("carta_fija",{}).get("dia",{}).get("rama",{}).get("nombre","")
        dm_info     = DM_DESC.get(dm_tronco,{})

        # Armonía de género
        dm_pol = dm.get("polaridad","").lower()
        if sexo == "mujer":
            armonia_genero = dm_pol == "yin"
        else:
            armonia_genero = dm_pol == "yang"

        armonia_texto = (
            "Energía en armonía con el género. La persona fluye con naturalidad en la vida. Se le presentan oportunidades y personas que ayudan. El flujo de la vida es natural y espontáneo."
            if armonia_genero else
            "Energía opuesta a la naturaleza del consultante. Por lo tanto, le costará más conseguir las oportunidades en la vida y deberá hacer un esfuerzo consciente para abrirse a ellas."
        )

        # Yin/Yang y cesta de elementos
        carta_fija  = carta.get("carta_fija",{})
        yin_yang    = calcular_yin_yang(carta_fija)
        cesta_raw   = calcular_cesta_elementos(carta_fija)
        cesta       = {}
        for elem, cant in cesta_raw.items():
            desc = get_cesta_desc(elem, cant)
            cesta[elem] = {"cantidad": cant, **desc}

        # Descripción específica animal+elemento por pilar
        pilares_con_desc = {}
        for nombre_pilar, datos in carta_fija.items():
            animal   = _rama_nombre(datos)
            tronco_n = datos.get("tronco",{}).get("nombre","")
            desc_esp = get_animal_elemento_desc(animal, tronco_n)
            combos   = detectar_combo_dioses(datos)
            pilares_con_desc[nombre_pilar] = {
                **_expandir_dioses_pilar(datos),
                "desc_especifica": desc_esp,
                "combo_dioses": combos,
            }

        # Hacer lo mismo para carta móvil y extras
        for nombre_pilar, datos in todos_pilares.items():
            if nombre_pilar not in pilares_con_desc:
                animal   = _rama_nombre(datos)
                tronco_n = datos.get("tronco",{}).get("nombre","")
                desc_esp = get_animal_elemento_desc(animal, tronco_n)
                combos   = detectar_combo_dioses(datos)
                pilares_con_desc[nombre_pilar] = {
                    **_expandir_dioses_pilar(datos),
                    "desc_especifica": desc_esp,
                    "combo_dioses": combos,
                }

        # Tronco oculto principal del pilar del Día (rama del Día Maestro,
        # el "palacio del cónyuge"). Es el primero de la lista de troncos
        # ocultos de esa rama, que es el que domina esa energía oculta.
        # Se agrega para que la sección 01 pueda mencionar qué dios
        # representa, ya con el nombre completo resuelto (no solo el código).
        tronco_oculto_principal_dia = None
        _troncos_ocultos_dia = carta_fija.get("dia", {}).get("troncos_ocultos", [])
        if _troncos_ocultos_dia:
            _principal = _troncos_ocultos_dia[0]
            _dios_p = _principal.get("dios", "")
            tronco_oculto_principal_dia = {
                "nombre": _principal.get("nombre", ""),
                "dios": _dios_p,
                "dios_nombre": DIOSES_DESC.get(_dios_p, {}).get("nombre", _dios_p),
                "dios_desc": DIOSES_DESC.get(_dios_p, {}).get("desc", ""),
            }

        # Interacciones
        comb_troncos   = detectar_combinaciones_troncos(todos_pilares)
        choq_troncos   = detectar_choques_troncos(todos_pilares, sexo)
        comb_ramas     = detectar_combinaciones_ramas(todos_pilares)
        conf_ramas     = detectar_conflictos_ramas(todos_pilares, sexo)

        # 5 elementos
        cinco_e        = carta.get("cinco_elementos",{})
        analisis_elem  = analizar_cinco_elementos(cinco_e)
        dioses_ausentes= carta.get("dioses_ausentes",[])
        bloqueos       = [
            {"dios":d,"descripcion":BLOQUEOS_FINANCIEROS[d]}
            for d in dioses_ausentes if d in BLOQUEOS_FINANCIEROS
        ]
        analisis_elem["bloqueos_financieros"] = bloqueos

        # Relaciones
        # Se pasan por separado los pilares fijos (los 4 reales de la carta
        # natal) y los pilares móviles (pilar de suerte, año en curso y
        # cualquier pilar extra agregado por el astrólogo), para que
        # Casamentero y Cámara Roja puedan distinguir si están activos
        # en la carta natal o si se activan por tránsito, y para que
        # "Pilares afines" se calcule únicamente sobre los 4 pilares
        # reales (Año/Mes/Día/Hora).
        pilares_moviles = {}
        if cm.get("pilar_suerte"):
            pilares_moviles["pilar_suerte"] = cm["pilar_suerte"]
        if cm.get("anio_curso"):
            pilares_moviles["anio_curso"] = cm["anio_curso"]
        for extra in pilares_extra:
            pilares_moviles[extra["nombre"]] = extra

        flor_animal = dm.get("flor_melocoton","")
        relaciones  = detectar_relaciones(
            carta_fija, dm_tronco, dm_rama, sexo, flor_animal,
            pilares_moviles=pilares_moviles
        )

        # Salud especial
        salud_especial = detectar_salud_especial(todos_pilares, sexo)

        # Muerte y vacío
        mv = get_muerte_vacio(dm_tronco, dm_rama)

        analisis = {
            "carta":              carta,
            "pilares_adicionales":pilares_extra,
            "todos_pilares":      todos_pilares,
            "pilares_con_desc":   pilares_con_desc,
            "tronco_oculto_principal_dia": tronco_oculto_principal_dia,
            "dm_info":            dm_info,
            "armonia_genero":     armonia_genero,
            "armonia_texto":      armonia_texto,
            "yin_yang":           yin_yang,
            "cesta":              cesta,
            "combinaciones_troncos": comb_troncos,
            "choques_troncos":       choq_troncos,
            "combinaciones_ramas":   comb_ramas,
            "conflictos_ramas":      conf_ramas,
            "cinco_elementos":       analisis_elem,
            "relaciones":            relaciones,
            "salud_especial":        salud_especial,
            "muerte_vacio":          mv,
        }
        session["analisis"] = analisis
        return jsonify({"ok":True,"analisis":analisis})

    except Exception as e:
        return jsonify({"ok":False,"error":str(e)}), 500


def _construir_datos_carta(usuario, analisis, carta, dm, cinco_e, sexo):
    """Arma el bloque de datos de la carta, compartido por ambas llamadas al informe."""
    return f"""Sos un astrólogo experto en BaZi (astrología china de los 4 pilares).
Estás generando un informe profesional en español para {usuario.get('nombre')},
nacido/a el {usuario.get('fecha')} a las {usuario.get('hora')}, sexo: {sexo}.

═══════════════════════════════════
DATOS COMPLETOS DE LA CARTA
═══════════════════════════════════

CARTA FIJA:
{json.dumps(analisis.get('pilares_con_desc',{}), ensure_ascii=False, indent=2)}

CARTA MÓVIL:
{json.dumps(carta.get('carta_movil',{}), ensure_ascii=False, indent=2)}

DÍA MAESTRO:
{json.dumps(dm, ensure_ascii=False, indent=2)}

INFO DÍA MAESTRO:
{json.dumps(analisis.get('dm_info',{}), ensure_ascii=False, indent=2)}

TRONCO OCULTO PRINCIPAL DEL PILAR DEL DÍA (dentro de la rama del Día Maestro,
el "palacio del cónyuge"): este es el dios de mayor peso oculto en esa rama,
distinto del día maestro mismo, y aporta un matiz importante a la
personalidad y a la vida íntima de la persona:
{json.dumps(analisis.get('tronco_oculto_principal_dia'), ensure_ascii=False, indent=2)}

ARMONÍA DE GÉNERO:
{analisis.get('armonia_texto','')}

YIN/YANG:
{json.dumps(analisis.get('yin_yang',{}), ensure_ascii=False)}

CESTA DE ELEMENTOS:
{json.dumps(analisis.get('cesta',{}), ensure_ascii=False, indent=2)}

5 ELEMENTOS:
{json.dumps(carta.get('cinco_elementos',{}), ensure_ascii=False, indent=2)}

ANÁLISIS 5 ELEMENTOS:
{json.dumps(cinco_e, ensure_ascii=False, indent=2)}

COMBINACIONES DE TRONCOS:
{json.dumps(analisis.get('combinaciones_troncos',[]), ensure_ascii=False)}

CHOQUES DE TRONCOS:
{json.dumps(analisis.get('choques_troncos',[]), ensure_ascii=False)}

COMBINACIONES DE RAMAS:
{json.dumps(analisis.get('combinaciones_ramas',[]), ensure_ascii=False)}

CONFLICTOS DE RAMAS:
{json.dumps(analisis.get('conflictos_ramas',[]), ensure_ascii=False)}

RELACIONES:
{json.dumps(analisis.get('relaciones',{}), ensure_ascii=False, indent=2)}

SALUD ESPECIAL:
{json.dumps(analisis.get('salud_especial',[]), ensure_ascii=False)}

MUERTE Y VACÍO (animales):
{json.dumps(analisis.get('muerte_vacio',[]), ensure_ascii=False)}

{_resumen_conteo_items(analisis)}
"""


def _resumen_conteo_items(analisis):
    """Arma un resumen explícito, con conteo exacto, de los ítems detectados
    en conflictos y relaciones kármicas. Este bloque existe para que el
    modelo que redacta las secciones 06 y 08 no "pierda" ítems al leer el
    JSON crudo: se le da la cantidad exacta que debe cubrir, uno por uno.
    """
    conf_ramas   = analisis.get("conflictos_ramas", [])
    choq_troncos = analisis.get("choques_troncos", [])
    relaciones   = analisis.get("relaciones", {})
    karmicas     = relaciones.get("karmicas", [])
    karmicas_p   = relaciones.get("karmicas_parciales", [])

    def _linea_conf(i, c):
        return (f"  {i}. {c['tipo'].upper()} ({c.get('subtipo','')}) — "
                f"{' + '.join(c['animales'])} — pilares: {', '.join(c['pilares'])} "
                f"— ámbito: {c.get('ambito','')}")

    def _linea_karmica(i, k):
        estado = k.get("estado", "")
        return (f"  {i}. {' + '.join(k['animales'])} — pilares: {', '.join(k['pilares'])} "
                f"— estado: {estado} — ámbito: {k.get('ambito','')}")

    partes = ["═══════════════════════════════════",
              "RESUMEN DE CONTEO — usar para NO omitir ítems",
              "═══════════════════════════════════"]

    partes.append(f"CONFLICTOS DE RAMAS: hay exactamente {len(conf_ramas)} detectados "
                   f"(cubrir los {len(conf_ramas)}, ni más ni menos):")
    if conf_ramas:
        partes += [_linea_conf(i, c) for i, c in enumerate(conf_ramas, 1)]
    else:
        partes.append("  (ninguno detectado)")

    partes.append(f"\nCHOQUES DE TRONCOS: hay exactamente {len(choq_troncos)} detectados.")

    partes.append(f"\nRELACIONES KÁRMICAS COMPLETAS/ACTIVABLES: hay exactamente "
                   f"{len(karmicas)} detectadas (cubrir las {len(karmicas)}, ni más ni menos):")
    if karmicas:
        partes += [_linea_karmica(i, k) for i, k in enumerate(karmicas, 1)]
    else:
        partes.append("  (ninguna detectada)")

    partes.append(f"\nRELACIONES KÁRMICAS PARCIALES (un solo animal presente): "
                   f"hay exactamente {len(karmicas_p)} detectadas.")

    return "\n".join(partes)


PAUTAS_GENERALES = """
═══════════════════════════════════
PAUTAS GENERALES
═══════════════════════════════════
- Cada sección: texto fluido y profesional, párrafos bien desarrollados
- Tono: cálido, profesional, orientado al crecimiento personal
- Sexo del consultante: {sexo} — usar pronombres correctos
- NO incluir tablas en el JSON, solo texto fluido
- Respondé ÚNICAMENTE con el JSON, sin markdown ni explicaciones previas, en este formato exacto:

{{
  "secciones": [
    {{"numero": "01", "titulo": "...", "texto": "..."}},
    ...
  ]
}}
"""

INSTRUCCIONES_SECCION_01 = """
═══════════════════════════════════
INSTRUCCIONES — SECCIÓN 01: El día maestro
═══════════════════════════════════
Generá EXACTAMENTE 1 sección (numero "01", titulo "El día maestro"):
- Descripción del día maestro (elemento, polaridad, personalidad según dm_info)
- Armonía de género con su implicancia práctica
- Resumen del balance Yin/Yang
- Cesta de elementos: para cada elemento indicar cantidad, descripción del nivel y recomendación de recarga si corresponde
- Tronco oculto principal del pilar del Día: usá el bloque "TRONCO OCULTO PRINCIPAL DEL
  PILAR DEL DÍA" de los datos de la carta. Mencioná qué dios representa (usando SIEMPRE
  el campo "dios_nombre", nunca inventes ni traduzcas el código vos mismo) y qué matiz
  aporta a la vida íntima/personalidad de la persona según su descripción.
IMPORTANTE sobre los 10 dioses en TODA la sección: cuando menciones un dios (de un tronco
o de un tronco oculto), usá siempre el campo "dios_nombre" ya resuelto en los datos (p. ej.
"Oficial Herido"), nunca el código de 2-3 letras solo (p. ej. "OH") ni una traducción propia
inventada. Los 10 nombres correctos son: A (Amigo), RR (Robo de Riqueza), DC (Dios Comiendo),
OH (Oficial Herido), DI (Dinero Indirecto), DD (Dinero Directo), 7M (7 Muertes),
OD (Oficial Directo), RI (Recurso Indirecto), RD (Recurso Directo).
"""

INSTRUCCIONES_SECCION_02 = """
═══════════════════════════════════
INSTRUCCIONES — SECCIÓN 02: Análisis de los 4 pilares (carta fija)
═══════════════════════════════════
Generá EXACTAMENTE 1 sección (numero "02", titulo "Análisis de los 4 pilares"):
Para cada pilar (Año, Mes, Día, Hora):
- Indicar edad y ámbito
- Analizar tronco (dios y lo que representa), rama (animal y energía emocional), troncos ocultos (inconsciente)
- Incluir descripción específica animal+elemento (desc_especifica) si existe
- Incluir combo_dioses si hay combinaciones detectadas
- Un párrafo fluido por pilar
IMPORTANTE sobre los 10 dioses: para nombrar el dios de un tronco o de un tronco oculto,
usá SIEMPRE el campo "dios_nombre" ya resuelto en los datos (p. ej. "Oficial Herido"),
nunca el código de 2-3 letras solo (p. ej. "OH") ni una traducción propia inventada. Los
10 nombres correctos son: A (Amigo), RR (Robo de Riqueza), DC (Dios Comiendo),
OH (Oficial Herido), DI (Dinero Indirecto), DD (Dinero Directo), 7M (7 Muertes),
OD (Oficial Directo), RI (Recurso Indirecto), RD (Recurso Directo).
"""

INSTRUCCIONES_SECCION_03 = """
═══════════════════════════════════
INSTRUCCIONES — SECCIÓN 03: Carta móvil (pilares transitorios)
═══════════════════════════════════
Generá EXACTAMENTE 1 sección (numero "03", titulo "Carta móvil"):
- Analizar pilar de suerte y año en curso
- Aclarar SIEMPRE que son transitorios
- Incluir descripción específica animal+elemento si existe
"""

INSTRUCCIONES_SECCION_04 = """
═══════════════════════════════════
INSTRUCCIONES — SECCIÓN 04: Los 5 elementos — balance y finanzas
═══════════════════════════════════
Generá EXACTAMENTE 1 sección (numero "04", titulo "Los 5 elementos — balance y finanzas"):
1. Tabla/descripción de cada elemento: porcentaje, qué representa en esta carta, estado (exceso/equilibrio/carencia)
2. Descripción del exceso y carencia con sus implicancias
3. Superpoder financiero
4. Qué te impide avanzar financieramente (bloqueos por dioses ausentes)
5. Recomendaciones de equilibrio
"""

INSTRUCCIONES_SECCION_05 = """
═══════════════════════════════════
INSTRUCCIONES — SECCIÓN 05: Combinaciones
═══════════════════════════════════
Generá EXACTAMENTE 1 sección (numero "05", titulo "Combinaciones"):
- SOLO combinaciones positivas (troncos y ramas)
- Indicar tipo (direccional/estacional/elemental), animales, pilares involucrados, elemento que genera
- Si no hay combinaciones, mencionarlo y explicar qué significa energéticamente
"""

INSTRUCCIONES_SECCION_06 = """
═══════════════════════════════════
INSTRUCCIONES — SECCIÓN 06: Conflictos
═══════════════════════════════════
Generá EXACTAMENTE 1 sección (numero "06", titulo "Conflictos"):
IMPORTANTE: revisá el bloque "RESUMEN DE CONTEO" al final de los datos de la carta.
Ahí figura la cantidad EXACTA de conflictos de ramas y de choques de troncos detectados.
Tu texto debe cubrir esa cantidad exacta, uno por uno — ni omitir ninguno de la lista
ni inventar conflictos que no estén en CONFLICTOS DE RAMAS / CHOQUES DE TRONCOS.
Si el resumen dice "0 detectados" para un bloque, decilo explícitamente en el texto
en vez de omitir el bloque.
Separar en dos bloques:
BLOQUE A — Conflictos de ramas (choques, daños, destrucciones, castigos):
- Para cada uno de los ítems listados en CONFLICTOS DE RAMAS: tipo, animales, pilares,
  efecto, aspecto psicológico si existe, personas involucradas según sexo
- Si el mismo animal repite pilar (p. ej. la misma rama aparece en Mes y en Día), vas a
  ver dos entradas separadas para esa combinación: tratalas como conflictos distintos,
  no las fusiones en una sola mención.
BLOQUE B — Conflictos de troncos:
- Para cada uno de los ítems listados en CHOQUES DE TRONCOS: descripción, efecto,
  pilares, ámbito, personas involucradas
- Separar CLARAMENTE combinaciones de conflictos
"""

INSTRUCCIONES_SECCION_07 = """
═══════════════════════════════════
INSTRUCCIONES — SECCIÓN 07: Salud
═══════════════════════════════════
Generá EXACTAMENTE 1 sección (numero "07", titulo "Salud"):
- Elementos en exceso y carencia con órganos afectados y emoción negativa asociada
- Conflictos detectados y su impacto en salud (por dioses involucrados)
- Combinaciones especiales de salud si existen
"""

INSTRUCCIONES_SECCION_08 = """
═══════════════════════════════════
INSTRUCCIONES — SECCIÓN 08: Relaciones
═══════════════════════════════════
Generá EXACTAMENTE 1 sección (numero "08", titulo "Relaciones"):
1. Cámara roja: en RELACIONES.camara_roja tenés {{"animal":..., "pilares_natal":[...], "pilares_transito":[...], "activo": true/false}}.
   Si "activo" es false, explicar que no está encendida en este momento y en qué tipo de ciclo (año, mes o
   pilar de suerte) con ese animal podría activarse. Si "pilares_natal" tiene elementos, está en la carta fija;
   si solo "pilares_transito" tiene elementos, está activa por tránsito actual.
2. Flor de melocotón: animal, elemento, razón de atracción.
3. Hombre/Mujer noble: animales y cuándo se activan.
4. Relaciones kármicas: revisá el bloque "RESUMEN DE CONTEO" al final de los datos de la carta, que indica
   la cantidad EXACTA de kármicas completas/activables y de kármicas parciales. NUNCA digas "no se detectan
   relaciones kármicas completas" si ese conteo es mayor a 0 — en ese caso están en RELACIONES.karmicas,
   con su descripción y pilares, y hay que desarrollarlas todas (si el mismo par de animales aparece en más
   de una combinación de pilares, por repetirse un animal en dos pilares, tratar cada combinación por
   separado). En RELACIONES.karmicas_parciales están los pares con un solo animal presente y sin completar:
   mencionar cuál animal falta y que podría completarse si ese animal llega por año, mes o pilar de suerte.
5. Casamentero: SE DETERMINA POR EL DÍA MAESTRO (igual que la cámara roja, no es un par libre). En
   RELACIONES.casamentero tenés {{"animal":..., "pilares_natal":[...], "pilares_transito":[...], "activo":...,
   "es_tambien_karmico":...}}. Explicar cuál es el animal Casamentero de esta persona, si está o no presente
   en su carta natal, y si se activa por el pilar de suerte o el año en curso. NUNCA omitir esta sección aunque
   "activo" sea false: en ese caso explicar qué significa no tenerlo activo y qué animal, año o ciclo lo activaría.
6. Pilares afines: en RELACIONES.pilares_afines hay una entrada por cada pilar fijo (hora/dia/mes/anio) con
   {{"pilar": "Tronco Rama", "afines": [...9 pilares...], "muerte_vacio_columna": [...]}}. Para cada uno de los
   4 pilares, mencionar sus pilares afines (personas o ciclos con esos pilares tienden a la compatibilidad y
   comprensión mutua) y aclarar que los animales de "muerte_vacio_columna" NO pertenecen a esa columna.
7. Muerte y vacío del día maestro: animales de MV ({muerte_vacio}), en qué pilares de la carta natal aparecen
   (ver RELACIONES.muerte_vacio) y qué puede significar en cada uno.
8. Si algún par es a la vez kármico y casamentero, mencionar la dualidad.
"""

INSTRUCCIONES_SECCION_09 = """
═══════════════════════════════════
INSTRUCCIONES — SECCIÓN 09: Pilares de la suerte
═══════════════════════════════════
Generá EXACTAMENTE 1 sección (numero "09", titulo "Pilares de la suerte"):
Para cada ciclo decenal disponible:
- Período, tronco con dios, rama con animal
- Descripción específica animal+elemento del pilar de suerte
- Qué energía activa ese ciclo y qué puede esperarse
"""

INSTRUCCIONES_SECCION_10 = """
═══════════════════════════════════
INSTRUCCIONES — SECCIÓN 10: Recomendaciones finales
═══════════════════════════════════
Generá EXACTAMENTE 1 sección (numero "10", titulo "Recomendaciones finales"):
- Mínimo 6 recomendaciones concretas y prácticas
- Basadas en todo el análisis anterior
- Tono cálido, orientado al crecimiento personal
"""


def _llamar_claude_secciones(prompt, max_tokens=4000):
    """Llama a Claude y devuelve la lista de secciones (parseada de JSON)."""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        if response.stop_reason == "max_tokens":
            raise Exception(
                "La respuesta de Claude se cortó por el límite de tokens "
                "antes de completar el JSON. Subí max_tokens en "
                "_llamar_claude_secciones o dividí el prompt en partes más chicas."
            ) from e
        raise
    return data.get("secciones", [])


def _generar_seccion_con_reintento(datos_carta, instrucciones, pautas, numero, titulo):
    """Genera una sección individual. Si se corta por límite de tokens,
    reintenta una vez con más margen. Si igual falla, devuelve un
    placeholder en vez de tirar abajo todo el informe."""
    prompt = datos_carta + instrucciones + pautas
    for intento, tokens in enumerate([4096, 6000], start=1):
        try:
            return _llamar_claude_secciones(prompt, max_tokens=tokens)
        except Exception as e:
            if intento == 2:
                return [{
                    "numero": numero,
                    "titulo": titulo,
                    "texto": (
                        "⚠️ Esta sección no pudo generarse automáticamente "
                        f"(motivo: {e}). Usá el botón para regenerarla o "
                        "editá este texto manualmente."
                    ),
                }]
    return []


def _generar_informe_en_background(job_id, usuario, analisis, carta, dm, cinco_e, sexo):
    """Corre en un hilo aparte: llama a Claude una vez por cada una de las
    10 secciones (lo más chico posible, mínimo riesgo de corte por límite
    de tokens) y va actualizando el progreso en disco para que el
    frontend pueda consultarlo. Si una sección puntual falla, se reemplaza
    por un placeholder en vez de abortar la generación completa."""
    try:
        datos_carta = _construir_datos_carta(usuario, analisis, carta, dm, cinco_e, sexo)
        pautas = PAUTAS_GENERALES.format(sexo=sexo)
        muerte_vacio = analisis.get('muerte_vacio', [])

        secciones_instrucciones = [
            ("01", "El día maestro", INSTRUCCIONES_SECCION_01),
            ("02", "Análisis de los 4 pilares", INSTRUCCIONES_SECCION_02),
            ("03", "Carta móvil", INSTRUCCIONES_SECCION_03),
            ("04", "Los 5 elementos — balance y finanzas", INSTRUCCIONES_SECCION_04),
            ("05", "Combinaciones", INSTRUCCIONES_SECCION_05),
            ("06", "Conflictos", INSTRUCCIONES_SECCION_06),
            ("07", "Salud", INSTRUCCIONES_SECCION_07),
            ("08", "Relaciones", INSTRUCCIONES_SECCION_08.format(muerte_vacio=muerte_vacio)),
            ("09", "Pilares de la suerte", INSTRUCCIONES_SECCION_09),
            ("10", "Recomendaciones finales", INSTRUCCIONES_SECCION_10),
        ]

        secciones_acumuladas = []
        total = len(secciones_instrucciones)
        for i, (numero, titulo, instrucciones) in enumerate(secciones_instrucciones, start=1):
            secciones = _generar_seccion_con_reintento(datos_carta, instrucciones, pautas, numero, titulo)
            secciones_acumuladas += secciones
            _job_escribir(job_id, {
                "status": "running", "secciones": secciones_acumuladas,
                "progreso": f"sección {i} de {total} lista", "error": None,
            })

        _job_escribir(job_id, {
            "status": "done", "secciones": secciones_acumuladas,
            "progreso": "completo", "error": None,
        })

    except Exception as e:
        _job_escribir(job_id, {
            "status": "error", "secciones": [],
            "progreso": "", "error": str(e),
        })


@app.route("/generar-informe/iniciar", methods=["POST"])
def iniciar_informe():
    usuario  = session.get("usuario",{})
    analisis = session.get("analisis",{})
    carta    = analisis.get("carta",{})
    dm       = carta.get("dia_maestro",{})
    cinco_e  = analisis.get("cinco_elementos",{})
    sexo     = usuario.get("sexo","mujer")

    job_id = str(uuid.uuid4())
    _job_escribir(job_id, {
        "status": "running", "secciones": [],
        "progreso": "iniciando", "error": None,
    })

    hilo = threading.Thread(
        target=_generar_informe_en_background,
        args=(job_id, usuario, analisis, carta, dm, cinco_e, sexo),
        daemon=True,
    )
    hilo.start()

    return jsonify({"ok": True, "job_id": job_id})


@app.route("/generar-informe/estado/<job_id>", methods=["GET"])
def estado_informe(job_id):
    job = _job_leer(job_id)
    if not job:
        return jsonify({"ok": False, "error": "No se encontró ese trabajo de generación."}), 404

    if job["status"] == "error":
        return jsonify({"ok": False, "error": job["error"]})

    informe = {"secciones": job["secciones"]}
    if job["status"] == "done":
        session["informe"] = informe
        _job_borrar(job_id)

    return jsonify({
        "ok": True,
        "status": job["status"],
        "progreso": job.get("progreso", ""),
        "informe": informe,
    })


@app.route("/guardar-informe", methods=["POST"])
def guardar_informe():
    data = request.get_json()
    session["informe"] = data.get("informe")
    return jsonify({"ok":True})


def _escapar_html(texto):
    """ReportLab's Paragraph interpreta un subconjunto de HTML; escapamos
    los caracteres especiales del texto generado por Claude para que no
    rompan el parseo (por ejemplo si el texto contiene < o &)."""
    return (texto or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _construir_pdf_informe(usuario, informe, carta_data):
    """Arma el PDF del informe BaZi con el mismo estilo visual (oscuro,
    minimalista) que la página de resultados, usando ReportLab."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=LETTER,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
    )

    color_texto   = colors.HexColor("#1A1A18")
    color_texto2  = colors.HexColor("#5C5A54")
    color_texto3  = colors.HexColor("#9A9790")
    color_accent  = colors.HexColor("#2C2C2A")
    color_fondo2  = colors.HexColor("#F4F3EF")
    color_borde   = colors.HexColor("#E0DDD5")

    styles = getSampleStyleSheet()
    marca_style = ParagraphStyle(
        "Marca", parent=styles["Normal"], fontSize=9, textColor=color_texto3,
        alignment=TA_CENTER, spaceAfter=10, tracking=1,
    )
    titulo_style = ParagraphStyle(
        "TituloPrincipal", parent=styles["Title"], fontSize=22,
        textColor=color_accent, alignment=TA_CENTER, spaceAfter=4,
    )
    subtitulo_style = ParagraphStyle(
        "Subtitulo", parent=styles["Normal"], fontSize=11, textColor=color_texto2,
        alignment=TA_CENTER, spaceAfter=18,
    )
    seccion_titulo_style = ParagraphStyle(
        "SeccionTitulo", parent=styles["Heading2"], fontSize=14,
        textColor=color_accent, spaceBefore=16, spaceAfter=8,
    )
    cuerpo_style = ParagraphStyle(
        "Cuerpo", parent=styles["Normal"], fontSize=10.5, leading=16,
        textColor=color_texto, alignment=TA_JUSTIFY, spaceAfter=8,
    )
    meta_label_style = ParagraphStyle(
        "MetaLabel", parent=styles["Normal"], fontSize=7.5,
        textColor=color_texto3, spaceAfter=2,
    )
    meta_val_style = ParagraphStyle(
        "MetaVal", parent=styles["Normal"], fontSize=10.5,
        textColor=color_texto, fontName="Helvetica-Bold",
    )

    elementos = []

    # --- Logo (si existe) ---
    logo_path = os.path.join(app.root_path, "static", "logo.png")
    if os.path.exists(logo_path):
        try:
            img = RLImage(logo_path, width=2.2 * cm, height=2.2 * cm)
            img.hAlign = "CENTER"
            elementos.append(img)
            elementos.append(Spacer(1, 0.3 * cm))
        except Exception:
            pass

    elementos.append(Paragraph("AZ-CONSULTORÍA &nbsp;·&nbsp; ASTROLOGÍA CHINA", marca_style))
    elementos.append(Paragraph(_escapar_html(usuario.get("nombre", "—")), titulo_style))
    sub = f"{usuario.get('fecha','')} &nbsp;·&nbsp; {usuario.get('hora','')} &nbsp;·&nbsp; {usuario.get('sexo','')}"
    elementos.append(Paragraph(sub, subtitulo_style))

    # --- Caja de metadatos (día maestro / elemento dominante / estrella) ---
    dm = (carta_data or {}).get("dia_maestro", {})
    el = (carta_data or {}).get("cinco_elementos", {})
    dominante = None
    if el:
        try:
            dominante = max(el.items(), key=lambda kv: kv[1].get("porcentaje", 0))
        except (ValueError, AttributeError):
            dominante = None
    dominante_txt = (
        f"{dominante[0].capitalize()} {dominante[1].get('porcentaje', 0)}%"
        if dominante else "—"
    )

    meta_data = [[
        Paragraph("DÍA MAESTRO", meta_label_style),
        Paragraph("ELEMENTO DOMINANTE", meta_label_style),
        Paragraph("ESTRELLA DE VIDA (GUA)", meta_label_style),
    ], [
        Paragraph(_escapar_html(f"{dm.get('nombre','—')} — {dm.get('elemento','')} {dm.get('polaridad','')}"), meta_val_style),
        Paragraph(_escapar_html(dominante_txt), meta_val_style),
        Paragraph(_escapar_html(str(dm.get("estrella_vida", "—"))), meta_val_style),
    ]]
    meta_table = Table(meta_data, colWidths=[5.1 * cm] * 3)
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color_fondo2),
        ("BOX", (0, 0), (-1, -1), 0.75, color_borde),
        ("INNERGRID", (0, 0), (-1, -1), 0.75, color_borde),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elementos.append(meta_table)
    elementos.append(Spacer(1, 1 * cm))

    # --- Secciones del informe ---
    for sec in informe.get("secciones", []):
        numero = _escapar_html(sec.get("numero", ""))
        titulo = _escapar_html(sec.get("titulo", ""))
        texto = sec.get("texto", "") or ""

        bloque = [Paragraph(f"{numero} — {titulo}", seccion_titulo_style)]
        for parrafo in texto.split("\n"):
            parrafo = parrafo.strip()
            if parrafo:
                bloque.append(Paragraph(_escapar_html(parrafo), cuerpo_style))

        # KeepTogether evita que un título quede solo al final de una página
        elementos.append(KeepTogether(bloque[:2] if len(bloque) > 1 else bloque))
        elementos.extend(bloque[2:])

    doc.build(elementos)
    buffer.seek(0)
    return buffer


@app.route("/exportar-pdf", methods=["GET"])
def exportar_pdf():
    usuario  = session.get("usuario", {})
    informe  = session.get("informe", {})
    analisis = session.get("analisis", {})
    carta_data = analisis.get("carta", {})

    if not informe or not informe.get("secciones"):
        return jsonify({"ok": False, "error": "Todavía no hay un informe generado para exportar."}), 400

    try:
        buffer = _construir_pdf_informe(usuario, informe, carta_data)
    except Exception as e:
        return jsonify({"ok": False, "error": f"Error generando el PDF: {e}"}), 500

    nombre_base = (usuario.get("nombre") or "consultante").strip().replace(" ", "_")
    nombre_archivo = f"informe_bazi_{nombre_base}.pdf"

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=nombre_archivo,
    )


@app.route("/enviar-email", methods=["POST"])
def enviar_email():
    # TODO: implementar con smtplib
    return jsonify({"ok":False,"error":"Email en construcción"}), 501


if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port, debug=False)
