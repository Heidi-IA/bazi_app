import os
import json
import uuid
import threading
import tempfile
import anthropic
from flask import Flask, render_template, request, jsonify, session
from utils.bazi_rules import (
    detectar_combinaciones_troncos, detectar_choques_troncos,
    detectar_combinaciones_ramas, detectar_conflictos_ramas,
    detectar_relaciones, detectar_salud_especial,
    analizar_cinco_elementos, calcular_yin_yang,
    calcular_cesta_elementos, get_cesta_desc,
    get_animal_elemento_desc, get_muerte_vacio,
    BLOQUEOS_FINANCIEROS, PILARES_INFO, DM_DESC,
    SALUD_ELEMENTOS, SALUD_DIOSES, CESTA_ELEMENTOS,
    DIOSES_DESC, ANIMALES_DESC,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
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
            animal   = datos.get("rama",{}).get("nombre","")
            tronco_n = datos.get("tronco",{}).get("nombre","")
            desc_esp = get_animal_elemento_desc(animal, tronco_n)
            combos   = detectar_combo_dioses(datos)
            pilares_con_desc[nombre_pilar] = {
                **datos,
                "desc_especifica": desc_esp,
                "combo_dioses": combos,
            }

        # Hacer lo mismo para carta móvil y extras
        for nombre_pilar, datos in todos_pilares.items():
            if nombre_pilar not in pilares_con_desc:
                animal   = datos.get("rama",{}).get("nombre","")
                tronco_n = datos.get("tronco",{}).get("nombre","")
                desc_esp = get_animal_elemento_desc(animal, tronco_n)
                combos   = detectar_combo_dioses(datos)
                pilares_con_desc[nombre_pilar] = {
                    **datos,
                    "desc_especifica": desc_esp,
                    "combo_dioses": combos,
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
        flor_animal = dm.get("flor_melocoton","")
        relaciones  = detectar_relaciones(
            todos_pilares, dm_tronco, dm_rama, sexo, flor_animal
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
"""


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
Separar en dos bloques:
BLOQUE A — Conflictos de ramas (choques, daños, destrucciones, castigos):
- Para cada uno: tipo, animales, pilares, efecto, aspecto psicológico si existe, personas involucradas según sexo
BLOQUE B — Conflictos de troncos:
- Para cada uno: descripción, efecto, pilares, ámbito, personas involucradas
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
1. Cámara roja: animal, si aparece en algún pilar de la carta
2. Flor de melocotón: animal, elemento, razón de atracción
3. Hombre/Mujer noble: animales y cuándo se activan
4. Relaciones kármicas detectadas: descripción del par y en qué pilares aparece
5. Casamentero detectado: pares y pilares
6. Pilares afines y muerte y vacío: animales de MV ({muerte_vacio}), en qué pilares aparecen y qué puede significar
7. Si algún par es a la vez kármico y casamentero, mencionar la dualidad
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


@app.route("/exportar-pdf", methods=["POST"])
def exportar_pdf():
    # TODO: implementar con ReportLab
    return jsonify({"ok":False,"error":"PDF en construcción"}), 501


@app.route("/enviar-email", methods=["POST"])
def enviar_email():
    # TODO: implementar con smtplib
    return jsonify({"ok":False,"error":"Email en construcción"}), 501


if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port, debug=False)
