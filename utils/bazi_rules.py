# ============================================================
# BAZI RULES - Lógica completa de interacciones
# ============================================================

# ------------------------------------------------------------
# ANIMALES - 12 ramas terrenales
# ------------------------------------------------------------
ANIMALES_DESC = {
    "Rata": {
        "nombre_chino": "Zi", "elemento": "agua", "polaridad": "yang",
        "mes": "Diciembre", "horas": "23:00 a 01:00",
        "personalidad": ["Inteligente", "Astuta", "Ambiciosa"],
        "desc": "Tiene una mente ágil y sabe resolver problemas rápidamente. Sabe moverse con discreción y aprovechar las oportunidades. Siempre busca mejorar y alcanzar sus metas."
    },
    "Buey": {
        "nombre_chino": "Chou", "elemento": "tierra", "polaridad": "yin",
        "mes": "Enero", "horas": "01:00 a 03:00",
        "personalidad": ["Confiable", "Paciente", "Trabajador"],
        "desc": "Leal y constante, es alguien en quien se puede confiar. Toma su tiempo, pero es firme y persistente. Valora el esfuerzo y la dedicación."
    },
    "Tigre": {
        "nombre_chino": "Yin", "elemento": "madera", "polaridad": "yang",
        "mes": "Febrero", "horas": "03:00 a 05:00",
        "personalidad": ["Valiente", "Impulsivo", "Líder natural"],
        "desc": "No teme a los desafíos y actúa con determinación. A veces actúa sin pensar demasiado. Inspira a otros con su energía y carisma."
    },
    "Conejo": {
        "nombre_chino": "Mao", "elemento": "madera", "polaridad": "yin",
        "mes": "Marzo", "horas": "05:00 a 07:00",
        "personalidad": ["Amable", "Elegante", "Cauto"],
        "desc": "Cortés, sensible y considerado con los demás. Tiene buen gusto y aprecio por la estética. Prefiere evitar el conflicto y los riesgos innecesarios."
    },
    "Dragón": {
        "nombre_chino": "Chen", "elemento": "tierra", "polaridad": "yang",
        "mes": "Abril", "horas": "07:00 a 09:00",
        "personalidad": ["Carismático", "Seguro de sí mismo", "Idealista"],
        "desc": "Tiene una presencia fuerte y magnética. Confía en sus capacidades. Tiene grandes sueños y ambiciones."
    },
    "Serpiente": {
        "nombre_chino": "Si", "elemento": "fuego", "polaridad": "yin",
        "mes": "Mayo", "horas": "09:00 a 11:00",
        "personalidad": ["Intuitiva", "Reservada", "Sabia"],
        "desc": "Percibe lo que otros no ven fácilmente. No muestra sus cartas fácilmente. Reflexiona y actúa con estrategia."
    },
    "Caballo": {
        "nombre_chino": "Wu", "elemento": "fuego", "polaridad": "yang",
        "mes": "Junio", "horas": "11:00 a 13:00",
        "personalidad": ["Independiente", "Energético", "Sociable"],
        "desc": "Valora su libertad y autonomía. Siempre está en movimiento, lleno de vitalidad. Le encanta estar rodeado de gente y conversar."
    },
    "Cabra": {
        "nombre_chino": "Wei", "elemento": "tierra", "polaridad": "yin",
        "mes": "Julio", "horas": "13:00 a 15:00",
        "personalidad": ["Creativa", "Compasiva", "Tranquila"],
        "desc": "Tiene talento artístico y sensibilidad estética. Se preocupa genuinamente por los demás. Prefiere entornos armoniosos y sin conflictos."
    },
    "Mono": {
        "nombre_chino": "Shen", "elemento": "metal", "polaridad": "yang",
        "mes": "Agosto", "horas": "15:00 a 17:00",
        "personalidad": ["Ingenioso", "Curioso", "Divertido"],
        "desc": "Rápido mentalmente, resuelve problemas con creatividad. Le encanta aprender y explorar cosas nuevas. Tiene buen sentido del humor y sabe entretener."
    },
    "Gallo": {
        "nombre_chino": "You", "elemento": "metal", "polaridad": "yin",
        "mes": "Septiembre", "horas": "17:00 a 19:00",
        "personalidad": ["Meticuloso", "Honesto", "Trabajador"],
        "desc": "Detallista y organizado. Dice las cosas como son, sin rodeos. Le gusta tener objetivos claros y cumplirlos."
    },
    "Perro": {
        "nombre_chino": "Xu", "elemento": "tierra", "polaridad": "yang",
        "mes": "Octubre", "horas": "19:00 a 21:00",
        "personalidad": ["Leal", "Justo", "Protector"],
        "desc": "Fiel a su familia y amigos. Tiene un fuerte sentido de la ética. Defiende lo que considera correcto."
    },
    "Cerdo": {
        "nombre_chino": "Hai", "elemento": "agua", "polaridad": "yin",
        "mes": "Noviembre", "horas": "21:00 a 23:00",
        "personalidad": ["Generoso", "Sincero", "Tolerante"],
        "desc": "Siempre dispuesto a compartir y ayudar. Genuino y honesto en sus intenciones. Acepta a los demás tal como son."
    },
}

# ------------------------------------------------------------
# ANIMALES CON ELEMENTO ESPECÍFICO - descripción del pilar exacto
# ------------------------------------------------------------
ANIMALES_ELEMENTO_DESC = {
    ("Rata", "metal"):    "La influencia del metal hace actuar a la rata con imprudencia, especialmente con el dinero. La Rata de Metal es la más emotiva de todas las ratas, le cuesta controlar sus emociones, en el amor se muestra celosa e irascible, con tendencia a dominar.",
    ("Rata", "agua"):     "Sus características más relevantes son su interés en el ámbito cultural y literario. Usa su instinto calculador para rodearse de amistades influyentes. Su actitud comprensiva la hace popular, pero debe tener cuidado con el chismorreo.",
    ("Rata", "madera"):   "Se destacan por su carácter amable, cordial y tendiente al progreso. La Rata de Madera muestra un gran compromiso profesional, es la más flexible de todas las ratas y despierta con los grandes desafíos.",
    ("Rata", "fuego"):    "La más idealista y competitiva de las ratas. Cuenta con la energía para estar en todas las situaciones que le rodean. Trabajadora sin descanso, le pierde su impaciencia.",
    ("Rata", "tierra"):   "La tierra fija las malas cualidades, aumenta la ambición y avaricia de la rata. Por otro lado, destaca su practicidad y la vuelve más precavida. Se muestra protectora con aquellos a los que verdaderamente aprecia.",

    ("Buey", "agua"):     "El más paciente, silencioso e idealista de todos los búfalos. Su mayor virtud es su capacidad de organización. Su mente racional, lógica y metódica le permite concentrarse en varias actividades simultáneas con eficacia.",
    ("Buey", "madera"):   "Representa a los más sociables de los búfalos. La madera le resta rigidez, con motivación puede reaccionar con cierta flexibilidad. Se ve capacidad para colaborar y trabajar en equipo.",
    ("Buey", "fuego"):    "El más apasionado de todos los búfalos, se siente atraído por el poder con obstinación y ambición. El fuego le dota de impaciencia frente a los sentimientos ajenos.",
    ("Buey", "tierra"):   "El Búfalo más paciente, lento y falto de iniciativa, pero con gran sentido del deber. Constante en su búsqueda de seguridad y estabilidad, va paso a paso hacia su meta.",
    ("Buey", "metal"):    "El más inflexible y crítico de todos los Perros — de fuertes convicciones. Idealista, si encuentra un objetivo que siga sus consignas de justicia, se comprometerá con entusiasmo.",

    ("Tigre", "metal"):   "El tigre de Metal es el más decidido y competitivo de todos los Tigres. Todo lo quiere y lo quiere ya, sin demoras. Activo, presuntuoso y optimista.",
    ("Tigre", "agua"):    "El agua otorga al Tigre el don de la flexibilidad, una mente abierta llena de ideas nuevas y cierto sosiego. El Tigre de agua controla sus instintos y sabe ejercer de líder con intuición y realismo.",
    ("Tigre", "madera"):  "El más tolerante de todos los tigres y dispuesto a colaborar. Busca razonar y discutir en lugar de imponer su opinión. Los Tigres de Madera se muestran irresponsables, indisciplinados y superficiales, pero con una gran capacidad creativa.",
    ("Tigre", "fuego"):   "El más teatral e inconformista de los Tigres. Puede saltar de entusiasmo y al segundo siguiente perder el control y estallar. Derrocha optimismo y generosidad, todo lo vive en primera persona.",
    ("Tigre", "tierra"):  "Menos brillante que el resto de los Tigres, pero le sobra constancia y tiene muy claro cuáles son sus objetivos. El elemento Tierra le otorga mayor concentración y le permite actuar con mayor precisión.",

    ("Conejo", "metal"):  "La influencia del Metal hace de la liebre un ser duro y vigoroso; con gran ambición y astucia intelectual para conseguir sus objetivos. Se anticipa a los acontecimientos a través de su poder de observación.",
    ("Conejo", "agua"):   "Emblema de amor y paz, es la liebre más sensible y emotiva. De naturaleza frágil, se deja influenciar con facilidad. Posee muy buena memoria y dones extrasensoriales.",
    ("Conejo", "madera"): "La más flexible de todas las liebres. Exaltan sus cualidades de generosidad y compresión. En el ámbito laboral es ambiciosa, pero frente a la autoridad se siente intimidada.",
    ("Conejo", "fuego"):  "De carácter emotivo y turbulento, es la liebre más demostrativa de afecto y divertida. De todas las liebres, es la más capacitada para ocupar el rol de líder.",
    ("Conejo", "tierra"):  "El elemento Tierra aporta equilibrio, constancia y realismo. La liebre de tierra sabe muy bien lo que quiere, es racional y reflexiva. Materialista, utilizará todos sus recursos para forjarse un bienestar.",

    ("Dragón", "metal"):  "La influencia del Metal está presente en su incansable voluntad para luchar y su integridad. Combativo, irá a por todas con dedicación. Apasionado puede caer en fanatismos.",
    ("Dragón", "agua"):   "Destacan su gran sabiduría para comprender y analizar las distintas situaciones, su flexibilidad para aceptar un rechazo o la derrota. Es menos egoísta y obstinado, no le gusta exhibirse.",
    ("Dragón", "madera"): "Con cualidades creativas, revolucionarias y geniales. Se comprometerá siempre y cuando sea beneficioso para él. Se desenvuelve bien en el ámbito de la investigación.",
    ("Dragón", "fuego"):  "Apunto de estallar en todo momento, tiene condiciones para ser líder que a veces se opacen con una actitud autoritaria. Sus características más sobresalientes son la impaciencia, la exageración y su carácter competitivo.",
    ("Dragón", "tierra"):  "El más sociable de todos los Dragones. El elemento Tierra impregna de realismo, solidez y junto a sus cualidades innatas de fuerza y ambición tendrá la determinación para alcanzar sus metas.",

    ("Serpiente", "metal"):  "Esta serpiente tiene una gran inteligencia y capacidad para el cálculo. Tiene el don innato de la oportunidad. Se mueve en silencio, pero constante. Es la más reservada de todas las serpientes.",
    ("Serpiente", "agua"):   "Cultiva el don de la telepatía, sumada a su fuerte intuición puede alcanzar un gran nivel de concentración. Destaca su agudeza mental para fijarse en su punto de atención sin permitir distracciones. Frente a las ofensas es muy rencorosa.",
    ("Serpiente", "madera"): "El elemento Madera acentúa su sabiduría e intuición, dotándole de creatividad e inventiva. Su mayor capacidad es la facilidad para captar los conocimientos, hacer conjeturas y predecir acontecimientos.",
    ("Serpiente", "fuego"):  "La más carismática, imperiosa y dominante de todas las serpientes. Con firme personalidad, son líderes destacados que desprenden confianza. Luchará por llegar a la cima y se aferrará a la fama y al éxito con orgullo.",
    ("Serpiente", "tierra"):  "Destaca por su espontaneidad y calidez; la más cauta y reflexiva de todas las serpientes. Sus metas son a largo plazo, trazadas en el futuro, con gran visión de conjunto.",

    ("Caballo", "agua"):   "El más intelectual de todos los Caballos, aunque sumamente divertido, alegre e inquieto. Elegante, es un gran conversador, amante de los viajes y los deportes. Incapaz de una planificación en cualquier ámbito de su vida.",
    ("Caballo", "metal"):  "Rebelde sin causa, también ridículo y extravagante en sus apreciaciones. El más valiente, impetuoso y demostrativo de todos los caballos. Tendrá miles de ocupaciones, muchos amores y viajará sin descanso. El trabajo no le entusiasma, no soporta la rutina.",
    ("Caballo", "madera"): "El menos impaciente de todos los caballos, se muestra alegre, amistoso y dinámico. El Caballo de Madera disfruta en el ambiente social, entre gente que le quiera y le estime. También se destaca su optimismo, siempre ve el medio vaso lleno.",
    ("Caballo", "fuego"):  "El elemento Fuego dota de energía desmedida, excitación y pasión descontrolada. De gran magnetismo e inteligencia, pero oscilante entre la inconstancia y la distracción. Anhela emociones fuertes y grandes retos para sentirse vivo.",
    ("Caballo", "tierra"):  "El más lento de todos los Caballos, le falta la vivacidad propia de su animal. El elemento Tierra le hace menos impulsivo y le aporta calma para tomar decisiones. Se desempeña de forma brillante en las inversiones financieras.",

    ("Cabra", "metal"):   "La más segura de sí misma de todas las Cabras u Ovejas, aunque vulnerable y susceptible sabe cómo disimular las ofensas detrás de una máscara. Sus innatos talentos artísticos le convierten en un excelente exponente de belleza.",
    ("Cabra", "agua"):    "Su dulzura, delicadeza y encanto atrae como moscas a la miel. Cabra u Oveja con gran emotividad, sociable y con un innato oportunismo, ve y lee entre líneas. Encierra grandes talentos para la música y la poesía.",
    ("Cabra", "madera"):  "El elemento Madera otorga altruismo, confianza y precaución a esta Cabra. Aunque sentimental, es firme y generosa con altos principios morales. Trabaja muy bien en equipo.",
    ("Cabra", "fuego"):   "La más valiente e innovadora de todas las Cabras u Ovejas. Muy mala administradora, es derrochadora buscando la comodidad personal. Como todas las Cabras sueña con los ojos abiertos.",
    ("Cabra", "tierra"):   "Algo más prudente que las demás Cabras u Ovejas, especialmente en los gastos caprichosos. El elemento Tierra la hace más conservadora y precavida. Le duele la crítica pero esconde sus sentimientos para defenderse.",

    ("Mono", "metal"):    "De espíritu independiente pero luchador y constante para lograr sus objetivos, encierran grandes ambiciones económicas. De naturaleza apasionada, trabajador y práctico.",
    ("Mono", "agua"):     "El parlanchín de todos los Monos, puede contribuir en las metas de los demás, pero siempre será por un interés especulador. El elemento Agua le otorga determinación para poner en marcha sus objetivos.",
    ("Mono", "madera"):   "Tiene excelentes cualidades para llevar el presupuesto familiar, la organización y gestión del hogar. Busca el éxito y el prestigio. Con espíritu insatisfecho y ávido de respuestas.",
    ("Mono", "fuego"):    "El más enérgico de todos los monos; con dotes naturales para el liderazgo. Competidor innato puede perderse en sus propias conjeturas mentales.",
    ("Mono", "tierra"):    "Encontramos un Mono sereno y con moderación. El elemento Tierra aporta calma e introspección, también despierta el interés hacia la cultura, con apertura mental dedicada al estudio y la lectura.",

    ("Gallo", "metal"):   "El Gallo madrugador que trabaja sin descanso. El elemento Metal le hace obstinado con necesidad de adquirir importancia y reconocimiento. Tiene ambición desmedida por obtener riquezas materiales.",
    ("Gallo", "agua"):    "Un gallo con iniciativas intelectuales; se desenvuelve muy bien en ambientes culturales. Es lúcido y práctico capaz de mantener una conversación sin imponer su opinión.",
    ("Gallo", "madera"):  "Menos testarudo y obstinados que los otros gallos, con mentes más abiertas. El elemento Madera acentúa sus cualidades de honestidad e integridad. También poseen un gran sentido de la justicia.",
    ("Gallo", "fuego"):   "El más autoritario y lleno de energía de todos los Gallos, desbordante de pasión, habilidad y precisión. De temperamento explosivo, monta en cólera con celeridad de forma teatral y nerviosa.",
    ("Gallo", "tierra"):   "El Gallo intelectual, gusta de la investigación y el análisis, buscador de la verdad. Brilla por su acertada elocuencia y sus apreciaciones concluyentes.",

    ("Perro", "metal"):   "El más inflexible y crítico de todos los Perros; de fuertes convicciones, no tolera ni el mínimo desliz fuera de la ley. Su grado de responsabilidad y compromiso en todos los ámbitos de su vida es de destacar.",
    ("Perro", "agua"):    "La reflexión y el instinto caracterizan a este Perro. Algo más indulgente que el resto de los Perros. Su personalidad encantadora y elocuente le rodea de un buen número de amigos.",
    ("Perro", "madera"):  "El más entregado y generoso de todos los Perros. El elemento Madera le otorga un temperamento más estable que los demás Perros, honesto y respetuoso.",
    ("Perro", "fuego"):   "Con una personalidad encantadora y atractiva, se muestra alegre y seguro de sí mismo. Su honestidad y sinceridad combinado con su fuerte idealismo y confianza aseguran su éxito.",
    ("Perro", "tierra"):   "Sus características son la resistencia y la voluntad. En el trabajo se desempeña prudentemente y de forma constructiva. Será imparcial repartiendo consejos con gran sentido de justicia.",

    ("Cerdo", "agua"):    "El diplomático de todos los cerdos; tiene el don innato para interpretar los sentimientos de los demás. Disfruta en eventos sociales, se muestra extravertido y amigable. Le encanta el lujo y gasta sin medida.",
    ("Cerdo", "metal"):   "Lo más importante para este Cerdo es su reputación. El elemento de Metal hace de él un animal apasionado y orgulloso que no tiene miedo de decir lo que siente. Sociable y extrovertido disfruta con sus amigos.",
    ("Cerdo", "madera"):  "El más organizado de todos los cerdos, capaz de llevar con habilidad y precisión las actividades. Su amable corazón querrá ayudar a todas las personas que lo necesiten.",
    ("Cerdo", "fuego"):   "Con gran apasionamiento, valentía y obstinación se enfrentará a la vida. Rodeado de buena suerte, es impulsado por su optimismo y confianza en sí mismo; no teme a lo desconocido.",
    ("Cerdo", "tierra"):   "Voluntarioso, sensato y tenaz, conseguirá lo que se proponga. El elemento Tierra sostiene su fuerza de voluntad y su capacidad para soportar las cargas que se impone para lograr su sueño. Su corazón está lleno de bondad.",
}

# ------------------------------------------------------------
# DÍA MAESTRO - descripciones por tronco
# ------------------------------------------------------------
DM_DESC = {
    "Jia":  {"elemento":"madera","polaridad":"yang","titulo":"Madera Yang","perfil":"Líderes decididos, con fuerte ética de trabajo.","desc":"La madera Jia es el primer tallo celestial. El gran árbol, en contacto con el cielo por su altura y con la tierra por sus raíces. Difícil de derribar, no se deja torcer por el viento, ni arrastrar por el agua. Brinda sombra a quien se le acerque. Inspira Protección. Siempre está en crecimiento. El día maestro Jia tiende a ser creativo, benevolente y determinado para mejorar su vida. Tiene una gran fortaleza para tolerar las dificultades; es estoico y terco, renuente a los cambios, con pensamiento rígido. Es protector y leal con sus allegados. Su empuje, perseverancia y capacidad para el trabajo duro, le conducen al éxito."},
    "Yi":   {"elemento":"madera","polaridad":"yin","titulo":"Madera Yin","perfil":"Creativos y flexibles, con talento para resolver problemas.","desc":"La madera Yi es el arbusto de jardín, la planta trepadora, flexible y astuta para subsistir. Siempre encuentra un camino hacia la luz. Es sobreviviente pero delicada. En la práctica BaZi, la madera Yi es sinónimo de belleza y elegancia. El día maestro Yi es atractivo, agradable, sutil, sofisticado y elegante. Tiene una gran facilidad para expresarse. Su naturaleza, flexible y sobreviviente, le permite adaptarse rápidamente a los cambios. Analiza problemas y encuentra soluciones rápidamente."},
    "Bing": {"elemento":"fuego","polaridad":"yang","titulo":"Fuego Yang","perfil":"Carismáticos y comunicativos, ideales para roles sociales.","desc":"El fuego Bing no debe ser visualizado como fuego real, sino como el astro sol. Es imponente, esplendido, exuberante, protector, cálido e indispensable. El día maestro Bing es apasionado, impulsivo, amable, cálido, generoso, compasivo, esplendido, entusiasta, optimista, amigable y extremadamente extrovertido. Como el sol, siempre quiere brillar e iluminar el mundo. Es líder por naturaleza, noble, sincero, leal. Es perseverante, optimista eterno, ve la vida en positivo, siempre va hacia delante."},
    "Ding": {"elemento":"fuego","polaridad":"yin","titulo":"Fuego Yin","perfil":"Inspiradores y entusiastas, con gran creatividad.","desc":"El tallo celestial Ding es el fuego real. Imponente, exuberante, impredecible, volátil, temperamental, cálido y reconfortante. El día maestro Ding es apasionado, impulsivo, amable, cálido, compasivo, esplendido, sentimental y amigable. Es discreto, elegante, de carácter suave, refinado y atractivo. Es detallista extremo; explora todos los ángulos de cualquier situación. Es desconfiado en todos los aspectos de su vida. Adicionalmente, es bastante temperamental; sus emociones son volátiles."},
    "Wu":   {"elemento":"tierra","polaridad":"yang","titulo":"Tierra Yang","perfil":"Estables y confiables, con fuerte sentido familiar.","desc":"La tierra yang Wu es la tierra dura; la visualizamos como las rocas o la imponente y exuberante montaña; mística, reservada, protectora, estable y confiable. El día maestro tierra Wu es considerado, estable y confiable. Por lo general, muestra una personalidad tranquila y reservada; tiende a ser el tipo de persona que inspira confianza inmediata. Posee un gran sentido de la lealtad. Es extremadamente sentimental, resultándole prácticamente imposible separar las emociones de su proceso de pensamiento. Tiene memoria prodigiosa; recuerda todo y no olvida nada."},
    "Ji":   {"elemento":"tierra","polaridad":"yin","titulo":"Tierra Yin","perfil":"Amigables y serviciales, comprometidos con los demás.","desc":"La tierra Ji es la tierra suave y delicada; la madre tierra, lista para el cultivo; fértil, productiva, protectora, estable y confiable. Es por sobre todas las cosas un ser humano productivo. Similar a su hermano Wu, muestra una personalidad tranquila, reservada que inspira confianza inmediata y con un gran sentido de la lealtad. Aunque no tiene la resistencia de Wu, su increíble talento, flexibilidad, intuición y creatividad le permiten sortear adversidades con soluciones ingeniosas. El día maestro Ji es capaz de poseer múltiples habilidades y talentos que permanecen escondidos pero que salen a relucir cuando los necesita."},
    "Geng": {"elemento":"metal","polaridad":"yang","titulo":"Metal Yang","perfil":"Analíticos y metódicos, expertos en los detalles.","desc":"El tallo celestial Geng es el metal fuerte, rustico y perdurable, como el acero, el hierro, el hacha o la espada. Resistencia, coraje, altruismo, autoridad y gran energía, son sus atributos dominantes. El día maestro Geng es inquebrantable; puede soportar adversidades con gran estoicismo y nunca le falta disposición para el trabajo más difícil. Un altruista innato que valora la amistad con fervor. Muy determinado, visualiza su vida como un campo de batalla. La derrota no existe en su vocabulario. Es orgulloso extremo. Se le hace difícil disculparse o admitir errores."},
    "Xin":  {"elemento":"metal","polaridad":"yin","titulo":"Metal Yin","perfil":"Justos y disciplinados, con alta integridad.","desc":"El tallo celestial Xin representa la belleza del metal refinado, delicado, procesado para ser admirado o para cortar con precisión, como la navaja suiza, el bisturí o la tijera afilada. Similar a una hermosa joya, el día maestro Xin es delicado y objeto de admiración. Por lo general, muestra gran sofisticación y tiende a desarrollar una necesidad especial por un estilo de vida glamoroso. Le gusta disfrutar los placeres de la vida. Tiene una mente ágil y especial, capaz de concebir ideas excepcionales para superar obstáculos. Su gran debilidad es que su auto estima depende demasiado de la admiración de terceros."},
    "Ren":  {"elemento":"agua","polaridad":"yang","titulo":"Agua Yang","perfil":"Adaptables e intuitivos, manejan bien los cambios.","desc":"El tallo celestial Ren representa el agua en gran volumen del océano, los lagos y los ríos. Es movimiento, dinamismo e inteligencia. El día maestro Ren es imparable, bravio, activo, incapaz de permanecer quieto por mucho tiempo porque necesita estar en movimiento constante. Por lo general, el día maestro Ren es muy inteligente, con una capacidad de aprendizaje superior. Tiene grandes habilidades de liderazgo. Es extrovertido, buen orador, pero no parlanchín. Ama lo desconocido, es un aventurero con energía ilimitada. Su mayor desventaja: temperamento cambiante."},
    "Gui":  {"elemento":"agua","polaridad":"yin","titulo":"Agua Yin","perfil":"Empáticos y comprensivos, excelentes en relaciones personales.","desc":"El tallo celestial Gui representa el agua suave de la lluvia, la neblina o el rocío. El agua que nutre y desarrolla plantas o cultivos. Mística, creativa, espiritual, inteligente, intuitiva, introvertida, impredecible. El día maestro Gui tiene gran capacidad para guiar e inspirar personas. Su pensamiento es bastante flexible, adaptándose con facilidad a los cambios o situaciones difíciles. Es cariñoso y preocupado por sus allegados; es reservado, profundo, místico, enigmático y difícil de descifrar. Se aburre con rapidez y puede ser inconstante."},
}

# ------------------------------------------------------------
# DIOSES - descripción completa
# ------------------------------------------------------------
DIOSES_DESC = {
    "A":   {"nombre":"Amigo","desc":"Tú misma, buen momento para relacionarte con personas afines a ti y crear un grupo y círculo afín. Representa a los amigos íntimos, hermanos si eres hombre y hermanas si eres mujer."},
    "RR":  {"nombre":"Robo de Riqueza","desc":"Genial para ventas, atraes personas y clientes a ti, relaciónate, vende, aunque con precaución porque puedes perder dinero. Para la mujer son sus hermanos, para el hombre son sus hermanas, además de nuestra competencia, rivales."},
    "DC":  {"nombre":"Dios Comiendo","desc":"Nos habla de que tenemos que trabajar en proyectos, metas, ser creativos. Representa las hijas de una mujer."},
    "OH":  {"nombre":"Oficial Herido","desc":"Es el centro de atención, atrae sin ser demasiado llamativo, ideal para comunicarnos, nos atenderán, realizar presentaciones. Para una mujer representa los hijos."},
    "DI":  {"nombre":"Dinero Indirecto","desc":"Atrae dinero indirecto, de ventas, comisiones, herencias, lotería, dinero imprevisto. Para un hombre es su novia o amante, para una mujer representa su padrastro u otra figura paterna que no es de sangre."},
    "DD":  {"nombre":"Dinero Directo","desc":"Es un dinero fijo, un sueldo por trabajar para otro, nómina, alquiler. Para el hombre es su mujer o pareja estable, para una mujer representa su padre."},
    "7M":  {"nombre":"7 Muertes","desc":"Saltarse las reglas, hacer las cosas de forma diferente, sin excederse y cumplir la ley, nos invita a innovar y arriesgarse. Para la mujer representa el novio o amante, para el hombre los hijos."},
    "OD":  {"nombre":"Oficial Directo","desc":"Hacer las cosas según lo establecido, de manera correcta, si eres mujer te trae una pareja ese año, buen momento para planear, ser detallista, siguiendo las reglas. Para la mujer representa el Marido, para el hombre las hijas que tenga."},
    "RI":  {"nombre":"Recurso Indirecto","desc":"Aprendemos mediante la experiencia, autodidacta, ideal para reforzar nuestro Don, inspiración, intuición, terapias espirituales, alternativas, salud, aquello que se sale de lo convencional. Representa la madre para la mujer y la madrastra para el hombre."},
    "RD":  {"nombre":"Recurso Directo","desc":"Ideal para estudiar, formaciones, oposiciones, master, una carrera, etc. Representa la madre del hombre y la madrastra para la mujer, la relación con ella, además de nuestra salud."},
}

# ------------------------------------------------------------
# DIOSES - representación de personas por sexo
# ------------------------------------------------------------
DIOSES_PERSONAS = {
    "hombre": {
        "DD": ["padre","esposa"],
        "DI": ["padre","pareja/amante"],
        "A":  ["hermano"],
        "RR": ["hermana","competencia"],
        "RI": ["madrastra"],
        "RD": ["madre"],
        "OD": ["hija"],
        "7M": ["hijo"],
        "OH": [],
        "DC": [],
    },
    "mujer": {
        "DD": ["padre"],
        "DI": ["padrastro"],
        "RR": ["hermano"],
        "A":  ["hermana"],
        "RI": ["madre"],
        "RD": ["madrastra"],
        "OD": ["esposo"],
        "7M": ["pareja/amante"],
        "DC": ["hija"],
        "OH": ["hijo"],
    }
}

# ------------------------------------------------------------
# PILARES - ámbitos vitales y edades
# ------------------------------------------------------------
PILARES_INFO = {
    "hora":  {"edad": "+60 años",   "ambito": "hijos, proyectos, subordinados, pensamientos, órganos internos, lo íntimo"},
    "dia":   {"edad": "40-60 años", "ambito": "uno mismo y la pareja, órganos internos, lo íntimo"},
    "mes":   {"edad": "20-40 años", "ambito": "padres, hermanos, mundo laboral, órganos externos, lo visible"},
    "anio":  {"edad": "0-20 años",  "ambito": "antepasados, mundo externo, parientes lejanos, sociedad, órganos externos"},
}

# Significado del choque entre pilares específicos
CHOQUE_PILARES = {
    frozenset(["anio","mes"]):            "cambios de país o ciudad de residencia",
    frozenset(["anio","dia"]):            "relaciones no armoniosas con parientes lejanos, niñez difícil",
    frozenset(["anio","hora"]):           "relaciones no armoniosas con hijos o subordinados",
    frozenset(["anio","mes","dia"]):      "agresividad y emociones no estables",
    frozenset(["dia","hora"]):            "problemas con cónyuges e hijos",
    frozenset(["dia","mes"]):             "relaciones problemáticas entre padres y hermanos",
}

# ------------------------------------------------------------
# CINCO ELEMENTOS - descripción completa
# ------------------------------------------------------------
ELEMENTOS_DESC = {
    "recurso": {
        "nombre": "RECURSO (印)",
        "concepto": "Lo que te nutre y sostiene: conocimiento, mentores, credenciales, salud, descanso, seguridad interna.",
        "subtipos": "Recurso Directo: soporte legítimo, títulos, mentoría clara. Recurso Indirecto: intuición, espiritualidad, soluciones poco convencionales.",
        "exceso": "Dependencia, procrastinación, teoría sin acción.",
        "carencia": "Sensación de desamparo, burnout, dificultad para retener o estudiar.",
        "equilibrar": "Rutinas de descanso, estudio estructurado, pedir ayuda de calidad, nutrir cuerpo y mente.",
        "rec_carencia": "Duerme mejor, busca mentores, formación con estructura.",
        "rec_exceso": "Gran capacidad de estudio y recuperación; cuida pasar a la acción (Producción).",
    },
    "compañero": {
        "nombre": "COMPAÑERO (比/劫)",
        "concepto": "Personas iguales a ti: hermanos, colegas, comunidad. Autoafirmación y red de pares.",
        "subtipos": "Amigo: cooperación y apoyo mutuo. Robo Riqueza: competencia fuerte, liderazgo bajo presión.",
        "exceso": "Rivalidades, dispersión por querer hacer todo solo, choques de ego.",
        "carencia": "Falta de red, baja autoestima para emprender o negociar.",
        "equilibrar": "Diseñar alianzas claras, roles definidos, límites sanos.",
        "rec_carencia": "Construye red (2 alianzas clave), pide referidos.",
        "rec_exceso": "Fuerza de red y emprendimiento; cuida acuerdos y foco.",
    },
    "producción": {
        "nombre": "PRODUCCIÓN (食/伤)",
        "concepto": "Lo que expresas y creas: creatividad, comunicación, productos, hijos, contenidos.",
        "subtipos": "DC (Dios Comida): creatividad fluida, docencia, arte. OH (Oficial Herido): innovación disruptiva, desafía normas.",
        "exceso": "Hablar o crear sin entregar, perfeccionismo o rebeldía improductiva.",
        "carencia": "Bloqueo creativo, dificultad para visibilizarte o poner tu voz.",
        "equilibrar": "Rutinas de publicación y entrega, buscar feedback externo.",
        "rec_carencia": "Calendario de entregas, cumple con tus ideas.",
        "rec_exceso": "Alta visibilidad y creatividad; asegura procesos de cobro (Riqueza) y respeto a normas (Influencia).",
    },
    "riqueza": {
        "nombre": "RIQUEZA (财)",
        "concepto": "Todo lo que controlas y administras: dinero, activos, tiempo, operaciones, responsabilidad.",
        "subtipos": "Dinero Directo: salario estable, presupuestos, constancia. Dinero Indirecto: ventas, networking, olfato comercial.",
        "exceso": "Avaricia, fatiga por sobre-trabajo, priorizar dinero sobre salud y valores.",
        "carencia": "Caos financiero, fuga de tiempo, promesas sin cobro.",
        "equilibrar": "Presupuestos, KPI claros, precio/valor, disciplina de cobro y ahorro.",
        "rec_carencia": "Presupuesto 50/30/20, KPI semanales, regla de cobro.",
        "rec_exceso": "Ejecutor confiable; evita sobre-exigencia, delega.",
    },
    "influencia": {
        "nombre": "INFLUENCIA/Autoridad (官/杀)",
        "concepto": "Lo que te controla: normas, jefes, Estado, mercado, reputación.",
        "subtipos": "Oficial Directo: orden, ética, carrera formal. 7 Muertes: presión, riesgo, competición; cataliza coraje.",
        "exceso": "Ansiedad por control externo, miedo a equivocarte, somatización.",
        "carencia": "Falta de límites, incumplimientos, reputación difusa.",
        "equilibrar": "Reglas simples y visibles, gestión de riesgos.",
        "rec_carencia": "Reglas claras, límites horarios, acuerdos por escrito.",
        "rec_exceso": "Marca profesional sólida; evita rigidez y cultiva flexibilidad (Producción/Recurso).",
    },
}

SUPERPODER_FINANCIERO = {
    "fuego":  "OPTIMISMO: será la clave para lograr tus objetivos. Actitud positiva cuando las cosas pintan mal.",
    "tierra": "TENACIDAD y PERSEVERANCIA: trabajar duro y con constancia para conseguir tu objetivo.",
    "agua":   "RESILIENCIA emocional: entrena tu mente para controlar tus emociones.",
    "metal":  "Capacidad de ENFOCARTE y priorizar lo que realmente importa.",
    "madera": "INDEPENDENCIA y autosuficiencia: toma control de tus decisiones financieras.",
}

BLOQUEOS_FINANCIEROS = {
    "DC":  "No le das prioridad a ganar dinero. Puedes desearlo, pero no tienes la compulsión de lograrlo.",
    "OH":  "Careces de habilidades para resolver problemas. Aprende a identificar y solucionar obstáculos.",
    "DD":  "Falta de educación sobre el dinero. No entiendes cómo funciona el dinero. Edúcate a ti mismo.",
    "DI":  "Tienes asociaciones negativas con las personas ricas. No puedes convertirte en algo que no admiras.",
    "RD":  "No aprendiste de tus padres sobre el dinero. Hay muchas experiencias negativas asociadas a él.",
    "RI":  "Dependes solo de un trabajo para ganar dinero. Explora e invierte en nuevos conocimientos. Diversifícate.",
    "RR":  "Eres complaciente con una vida mediocre y equilibrada. Para ser extraordinario debes salir del promedio.",
    "A":   "No te gusta relacionarte (networking), especialmente con personas adineradas.",
    "OD":  "No tomas la responsabilidad de TU futuro financiero. No es el trabajo de tu jefe hacerte rico.",
    "7M":  "Falta de coraje para perseguir y superar obstáculos.",
}

# ------------------------------------------------------------
# CESTA DE ELEMENTOS - descripción por cantidad
# ------------------------------------------------------------
CESTA_ELEMENTOS = {
    "agua": {
        "4+": "Intelecto elevado, sorprendentes actitudes para la comunicación, la investigación, la erudición. Elocuente y aventurero, efusivo en el trato con las personas. Si tiene más de 4 elementos podrías perder todo por no centrarte en tus motivaciones.",
        "2-3": "Buen conversador, brillante y lúcido. Reconocerás las oportunidades que se materialicen y no tendrás problemas en aceptarlas y acostumbrarte a los mejores formas de vida y disfrutar del éxito.",
        "0-1": "Persona reservada que tiende a la timidez. Demuestra cautela en los negocios y prudencia en el ámbito social. Si no eres precavido perderás de vista las oportunidades.",
        "recargar": "Sumergirse por ratos en una bañera, piscina o mar sin asolearse demasiado.",
    },
    "metal": {
        "4+": "Carencia de sentimientos y emoción. Tiendes a ser tímido y a encubrir tu timidez con modales bruscos. Competitivo, directo en el trato con las personas. Si superas los 4 elementos tu agresividad podría transformarse en un problema.",
        "2-3": "Posees las mismas cualidades positivas del metal pero en menor medida. Tienes más probabilidades de éxito con voluntad. Sabes cuando ser obstinado y cuando ceder.",
        "0-1": "Falta de sentimentalismo y tendencia a la indecisión.",
        "recargar": "Meditar en soledad, practicar la justicia en las decisiones, escuchar música de piano y usar prendas de metal.",
    },
    "tierra": {
        "4+": "Persona decidida hasta el punto de resultar obstinada. Rara vez serás el centro de la fiesta. Tu respuesta a las oportunidades será planificada y calculada. Lo que hace que las oportunidades se escapen entre tus dedos.",
        "2-3": "Eres práctico y realista, de confianza. Con la ayuda de la presencia de fuego en igual medida sacarás muy buen provecho de cualquier situación.",
        "0-1": "Persona menos realista, probablemente imprudente y quizás poco fiable.",
        "recargar": "Caminar descalzo en tierra o arena.",
    },
    "fuego": {
        "4+": "Personalidad extravagante y vivaz. Carismático, destila energía y vitalidad. Inteligente, agudo e incisivo. Cuando superas los 4 elementos acabarás por extinguirte a ti mismo.",
        "2-3": "Persona enérgica y activa. Respondes con entusiasmo pero también experimentas la influencia tranquilizadora de otros elementos. Harás buen uso de las oportunidades que se te presenten.",
        "0-1": "Personalidad tranquila y hogareña. Te perderás de oportunidades importantes por tu carácter ingenuo. No verás las oportunidades, es como que llevaras anteojos.",
        "recargar": "Asolearse en las primeras horas de la mañana con cierta frecuencia.",
    },
    "madera": {
        "4+": "Individuo extremadamente creativo. Dotado de una sorprendente visión y previsión. Sus ambiciones superan su aptitud. Si supera 4 te estarás extralimitando con la ambición.",
        "2-3": "Cuentas con creatividad e inclinaciones artísticas. Tu reacción frente a las oportunidades será más medida y analizada. Te permites aprovechar el aporte de otros elementos.",
        "0-1": "La imaginación y creatividad no estarán presentes. Las personas soñadoras te molestan. Rara vez podrás aprovechar las oportunidades de la vida.",
        "recargar": "Pasear por bosques, parques o espacios donde haya mucha vegetación.",
    },
}

# ------------------------------------------------------------
# CÁMARA ROJA - tronco DM → animal
# ------------------------------------------------------------
CAMARA_ROJA = {
    "Jia":  "Caballo",
    "Bing": "Tigre",
    "Wu":   "Dragón",
    "Geng": "Perro",
    "Ren":  "Rata",
    "Yi":   "Mono",
    "Ding": "Cabra",
    "Ji":   "Dragón",
    "Xin":  "Gallo",
    "Gui":  "Mono",
}

# ------------------------------------------------------------
# FLOR DE MELOCOTÓN - elemento → razón de atracción
# ------------------------------------------------------------
FLOR_MELOCOTON = {
    "madera": "tu crecimiento y progreso",
    "fuego":  "tu energía y felicidad",
    "tierra": "tu estabilidad",
    "metal":  "tu determinación y liderazgo",
    "agua":   "tu inteligencia e intuición",
}

# ------------------------------------------------------------
# RELACIONES KÁRMICAS - pares fijos con descripción
# ------------------------------------------------------------
RELACIONES_KARMICAS = [
    {
        "animales": ["Caballo", "Gallo"],
        "desc": "Energías difíciles, ya que la agitación del Gallo puede llevar al Caballo a sentirse tenso y nervioso. El Caballo admira al Gallo, pero debe aprender a establecer límites ante sus críticas verbales. Esta es una pareja que es encantadora o totalmente insoportable. La actitud parece ser el principal problema entre estas dos almas. Hacen una mejor pareja pública que privada.",
        "es_tambien_casamentero": True,
    },
    {
        "animales": ["Tigre", "Serpiente"],
        "desc": "El Tigre rápidamente se exaspera con las lentas deliberaciones de la Serpiente. Los Tigres se mueven rápido, piensan rápido. A la Serpiente le gusta calcular y ponderar el significado de la vida, lo cual aburre al Tigre. La Serpiente a menudo se siente presionada, mientras el Tigre se siente frustrado. Hay problemas de control que necesitan ser resueltos.",
        "es_tambien_casamentero": False,
    },
    {
        "animales": ["Cabra", "Perro"],
        "desc": "Una lucha de poder kármico. Ambos tienden a ver el lado negativo de la vida y son propensos a esperar lo peor. El Perro arrea a la Cabra a lugares en los que no desea estar. Las expectativas mutuas llevan a decepciones. Hay problemas de autoridad y control que deben resolverse.",
        "es_tambien_casamentero": False,
    },
    {
        "animales": ["Mono", "Cerdo"],
        "desc": "Solo son familiares, no compatibles. Las discusiones debido a prioridades diferentes con respecto a la casa y el corazón pueden ser problemáticas. El Mono tiene su propia agenda. Las infidelidades del Mono amenazan con derrocar el mundo optimista del Cerdo. El engañoso Mono no puede resistir desorientar al ingenuo Cerdo.",
        "es_tambien_casamentero": False,
    },
    {
        "animales": ["Buey", "Dragón"],
        "desc": "Un choque de voluntades podría desbaratar esta relación. Ambos necesitan admiración. La inclinación del Dragón para las aventuras amorosas es el principal problema. La infidelidad en cualquier forma es imperdonable para el Buey. El Dragón puede fácilmente sentirse atrapado por el terrestre y desapasionado Buey.",
        "es_tambien_casamentero": False,
    },
    {
        "animales": ["Rata", "Conejo"],
        "desc": "La Rata no puede vivir sin conversación íntima, y el reservado Conejo puede dejar a la Rata sintiéndose encerrada. El Conejo no invierte en la relación como su pareja Rata. El Conejo también es percibido como no disponible emocionalmente. Ambos comparten el amor a las artes finas y a la socialización; sin embargo, hacen mejores amigos que amantes.",
        "es_tambien_casamentero": True,
    },
]

# ------------------------------------------------------------
# CASAMENTERO - estrella de matrimonio/uniones duraderas
# Al igual que la Cámara Roja, el Casamentero se determina a partir
# de la RAMA del Día Maestro (no de pares buscados en cualquier
# combinación de pilares). Cada animal tiene un único "casamentero"
# fijo, según los 6 pares de Armonía (Liu He).
# ------------------------------------------------------------
CASAMENTERO = [
    {"animales": ["Rata",     "Conejo"],    "es_tambien_karmico": True},
    {"animales": ["Dragón",   "Cerdo"],     "es_tambien_karmico": False},
    {"animales": ["Serpiente","Perro"],     "es_tambien_karmico": False},
    {"animales": ["Caballo",  "Gallo"],     "es_tambien_karmico": True},
    {"animales": ["Mono",     "Cabra"],     "es_tambien_karmico": False},
    {"animales": ["Tigre",    "Buey"],      "es_tambien_karmico": False},
]

# Mapa bidireccional animal del día maestro → animal casamentero
CASAMENTERO_POR_RAMA = {}
for _par in CASAMENTERO:
    _a1, _a2 = _par["animales"]
    CASAMENTERO_POR_RAMA[_a1] = {"animal": _a2, "es_tambien_karmico": _par["es_tambien_karmico"]}
    CASAMENTERO_POR_RAMA[_a2] = {"animal": _a1, "es_tambien_karmico": _par["es_tambien_karmico"]}

# ------------------------------------------------------------
# MUERTE Y VACÍO - por columna de 60 pilares
# ------------------------------------------------------------
MUERTE_VACIO = {
    # Col 1: Jia Yin  →  Muerte y Vacío: Rata, Buey
    "Jia Yin":  ["Rata","Buey"], "Yi Mao":   ["Rata","Buey"],
    "Bing Chen":["Rata","Buey"], "Ding Si":  ["Rata","Buey"],
    "Wu Wu":    ["Rata","Buey"], "Ji Wei":   ["Rata","Buey"],
    "Geng Shen":["Rata","Buey"], "Xin You":  ["Rata","Buey"],
    "Ren Xu":   ["Rata","Buey"], "Gui Hai":  ["Rata","Buey"],
    # Col 2: Jia Chen  →  Muerte y Vacío: Tigre, Conejo
    "Jia Chen": ["Tigre","Conejo"], "Yi Si":   ["Tigre","Conejo"],
    "Bing Wu":  ["Tigre","Conejo"], "Ding Wei": ["Tigre","Conejo"],
    "Wu Shen":  ["Tigre","Conejo"], "Ji You":   ["Tigre","Conejo"],
    "Geng Xu":  ["Tigre","Conejo"], "Xin Hai":  ["Tigre","Conejo"],
    "Ren Zi":   ["Tigre","Conejo"], "Gui Chou": ["Tigre","Conejo"],
    # Col 3: Jia Wu  →  Muerte y Vacío: Dragón, Serpiente
    "Jia Wu":   ["Dragón","Serpiente"], "Yi Wei":   ["Dragón","Serpiente"],
    "Bing Shen":["Dragón","Serpiente"], "Ding You": ["Dragón","Serpiente"],
    "Wu Xu":    ["Dragón","Serpiente"], "Ji Hai":   ["Dragón","Serpiente"],
    "Geng Zi":  ["Dragón","Serpiente"], "Xin Chou": ["Dragón","Serpiente"],
    "Ren Yin":  ["Dragón","Serpiente"], "Gui Mao":  ["Dragón","Serpiente"],
    # Col 4: Jia Shen  →  Muerte y Vacío: Caballo, Cabra
    "Jia Shen": ["Caballo","Cabra"], "Yi You":  ["Caballo","Cabra"],
    "Bing Xu":  ["Caballo","Cabra"], "Ding Hai":["Caballo","Cabra"],
    "Wu Zi":    ["Caballo","Cabra"], "Ji Chou": ["Caballo","Cabra"],
    "Geng Yin": ["Caballo","Cabra"], "Xin Mao":["Caballo","Cabra"],
    "Ren Chen": ["Caballo","Cabra"], "Gui Si":  ["Caballo","Cabra"],
    # Col 5: Jia Xu  →  Muerte y Vacío: Mono, Gallo
    "Jia Xu":   ["Mono","Gallo"], "Yi Hai":  ["Mono","Gallo"],
    "Bing Zi":  ["Mono","Gallo"], "Ding Chou":["Mono","Gallo"],
    "Wu Yin":   ["Mono","Gallo"], "Ji Mao":  ["Mono","Gallo"],
    "Geng Chen":["Mono","Gallo"], "Xin Si":  ["Mono","Gallo"],
    "Ren Wu":   ["Mono","Gallo"], "Gui Wei": ["Mono","Gallo"],
    # Col 6: Jia Zi  →  Muerte y Vacío: Perro, Cerdo
    "Jia Zi":   ["Perro","Cerdo"], "Yi Chou":  ["Perro","Cerdo"],
    "Bing Yin": ["Perro","Cerdo"], "Ding Mao": ["Perro","Cerdo"],
    "Wu Chen":  ["Perro","Cerdo"], "Ji Si":    ["Perro","Cerdo"],
    "Geng Wu":  ["Perro","Cerdo"], "Xin Wei":  ["Perro","Cerdo"],
    "Ren Shen": ["Perro","Cerdo"], "Gui You":  ["Perro","Cerdo"],
}

# ------------------------------------------------------------
# PILARES AFINES - columnas de los 60 pilares (xun)
# Cada columna agrupa 10 pilares que resuenan entre sí. Los "afines"
# de un pilar son los otros 9 miembros de su misma columna. Los 2
# animales de Muerte y Vacío de esa columna nunca son miembros de
# ella (son las 2 ramas que quedan fuera del ciclo de 10 de ese xun).
# ------------------------------------------------------------
PILARES_COLUMNAS = [
    ["Jia Yin","Yi Mao","Bing Chen","Ding Si","Wu Wu","Ji Wei","Geng Shen","Xin You","Ren Xu","Gui Hai"],
    ["Jia Chen","Yi Si","Bing Wu","Ding Wei","Wu Shen","Ji You","Geng Xu","Xin Hai","Ren Zi","Gui Chou"],
    ["Jia Wu","Yi Wei","Bing Shen","Ding You","Wu Xu","Ji Hai","Geng Zi","Xin Chou","Ren Yin","Gui Mao"],
    ["Jia Shen","Yi You","Bing Xu","Ding Hai","Wu Zi","Ji Chou","Geng Yin","Xin Mao","Ren Chen","Gui Si"],
    ["Jia Xu","Yi Hai","Bing Zi","Ding Chou","Wu Yin","Ji Mao","Geng Chen","Xin Si","Ren Wu","Gui Wei"],
    ["Jia Zi","Yi Chou","Bing Yin","Ding Mao","Wu Chen","Ji Si","Geng Wu","Xin Wei","Ren Shen","Gui You"],
]

# Mapa directo pilar → columna completa (lista de 10 miembros)
PILAR_A_COLUMNA = {}
for _col in PILARES_COLUMNAS:
    for _p in _col:
        PILAR_A_COLUMNA[_p] = _col

MUERTE_VACIO_PILARES = {
    "hora": [
        "Dificultad para concebir",
        "Soledad en la vejez",
        "Los hijos no cuidarán en la vejez",
        "También puede significar que los hijos y proyectos simplemente no son una prioridad central en esta vida.",
    ],
    "dia": [
        "Dificultad para concebir",
        "Falta de satisfacción consigo mismo o con las parejas",
        "También puede significar que la pareja y la vida íntima no son una prioridad central en esta vida.",
    ],
    "mes": [
        "Falta de habilidad para encontrar el propósito en la vida",
        "Falta de satisfacción en el trabajo",
        "Poca afinidad con hermanos",
        "También puede significar que el trabajo y los hermanos no son una prioridad central en esta vida.",
    ],
    "anio": [
        "Posible mudanza de la ciudad natal de joven",
        "Niñez difícil y sin cuidados paternos",
        "Poca afinidad con padres y abuelos",
        "También puede significar que la infancia y los vínculos ancestrales no son una prioridad central en esta vida.",
    ],
}

# ------------------------------------------------------------
# SALUD - elementos y órganos
# ------------------------------------------------------------
SALUD_ELEMENTOS = {
    "madera": {
        "organos": "dedos, tendones, hígado, vesícula, nervios, manos, piernas, caderas, crecimiento",
        "yin": "hígado", "yang": "vesícula",
        "emocion_pos": "progreso", "emocion_neg": "ira",
        "correspondencias": "Este, primavera, verde, viento, sabor ácido",
        "virtud": "bondad, creatividad",
    },
    "fuego": {
        "organos": "corazón, ojos, sangre, órgano reproductivo femenino, menstruación",
        "yin": "corazón", "yang": "intestino delgado",
        "emocion_pos": "felicidad", "emocion_neg": "arrogancia",
        "correspondencias": "Sur, verano, rojo, sabor amargo",
        "virtud": "pasión, motivación",
    },
    "tierra": {
        "organos": "músculos, estómago, espalda, aumento de peso, piel",
        "yin": "bazo", "yang": "estómago",
        "emocion_pos": "estabilidad", "emocion_neg": "ansiedad",
        "correspondencias": "Centro, amarillo, humedad, sabor dulce",
        "virtud": "seguridad, tolerancia",
    },
    "metal": {
        "organos": "piel, pulmones, dientes, boca, voz",
        "yin": "pulmón", "yang": "intestino grueso",
        "emocion_pos": "liderazgo", "emocion_neg": "melancolía",
        "correspondencias": "Oeste, otoño, blanco, sequedad, sabor picante",
        "virtud": "estructura, poder",
    },
    "agua": {
        "organos": "alergias, oído, riñones, vejiga, genitales masculinos, uretra, sangre",
        "yin": "riñones", "yang": "vejiga",
        "emocion_pos": "intuición", "emocion_neg": "miedo",
        "correspondencias": "Norte, invierno, negro, frío, sabor salado",
        "virtud": "inteligencia, movimiento",
    },
}

SALUD_DIOSES = {
    "OH": "adicciones, problemas de comunicación",
    "7M": "sangrado, dolor, accidentes",
    "DC": "desorden alimenticio, sistema urinario",
    "RD": "enfermedad mental, autoinmune, sistema respiratorio",
    "DD": "insomnio, cansancio",
    "RI": "problemas emocionales",
    "DI": "estrés, adicciones",
    "RR": "enfermedad crónica, problemas de extremidades",
    "OD": "desorden con alimentos",
    "A":  "sistema linfático, nervios, arterias",
}

SALUD_COMBINACIONES_ESPECIALES = [
    {
        "animales": ["Conejo","Dragón"],
        "condicion": "siempre",
        "efecto": "problemas en la columna vertebral",
    },
    {
        "animales": ["Buey","Perro"],
        "condicion": "siempre",
        "efecto": "tumores, cáncer, encapsulamientos",
    },
    {
        "animales": ["Conejo","Gallo"],
        "condicion": "mujer + pilares dia y hora",
        "efecto": "complicaciones en el embarazo. También aplica si tiene muerte y vacío entre el día maestro y la hora, o si tiene RI como dios.",
    },
]

# ------------------------------------------------------------
# COMBINACIONES DE TRONCOS CELESTES (5)
# ------------------------------------------------------------
COMBINACIONES_TRONCOS = [
    {"tronco1":"Jia","elemento1":"madera","polaridad1":"yang","tronco2":"Ji","elemento2":"tierra","polaridad2":"yin","genera":"tierra","descripcion":"Madera Yang con Tierra Yin — genera Tierra."},
    {"tronco1":"Yi","elemento1":"madera","polaridad1":"yin","tronco2":"Geng","elemento2":"metal","polaridad2":"yang","genera":"metal","descripcion":"Madera Yin con Metal Yang — genera Metal."},
    {"tronco1":"Bing","elemento1":"fuego","polaridad1":"yang","tronco2":"Xin","elemento2":"metal","polaridad2":"yin","genera":"agua","descripcion":"Fuego Yang con Metal Yin — genera Agua."},
    {"tronco1":"Ding","elemento1":"fuego","polaridad1":"yin","tronco2":"Ren","elemento2":"agua","polaridad2":"yang","genera":"madera","descripcion":"Fuego Yin con Agua Yang — genera Madera."},
    {"tronco1":"Wu","elemento1":"tierra","polaridad1":"yang","tronco2":"Gui","elemento2":"agua","polaridad2":"yin","genera":"fuego","descripcion":"Tierra Yang con Agua Yin — genera Fuego."},
]

# ------------------------------------------------------------
# CHOQUES DE TRONCOS CELESTES (10)
# ------------------------------------------------------------
CHOQUES_TRONCOS = [
    {"troncos":["Geng","Jia"],"elem1":"metal","pol1":"yang","elem2":"madera","pol2":"yang","descripcion":"Metal Yang choca con Madera Yang","efecto":"Se generan lesiones, cortes, fracturas. Cambios físicos abruptos."},
    {"troncos":["Xin","Yi"],"elem1":"metal","pol1":"yin","elem2":"madera","pol2":"yin","descripcion":"Metal Yin choca con Madera Yin","efecto":"Lesiones menores, posibles traiciones. Conflictos sutiles pero duraderos."},
    {"troncos":["Ren","Bing"],"elem1":"agua","pol1":"yang","elem2":"fuego","pol2":"yang","descripcion":"Agua Yang choca con Fuego Yang","efecto":"Desafíos de los que tienes que aprender. Situaciones que exigen crecimiento."},
    {"troncos":["Gui","Ding"],"elem1":"agua","pol1":"yin","elem2":"fuego","pol2":"yin","descripcion":"Agua Yin choca con Fuego Yin","efecto":"Contratiempos de corta duración. Dificultades pasajeras."},
    {"troncos":["Jia","Wu"],"elem1":"madera","pol1":"yang","elem2":"tierra","pol2":"yang","descripcion":"Madera Yang choca con Tierra Yang","efecto":"Situaciones que no estaban previstas y se salen de control."},
    {"troncos":["Ji","Yi"],"elem1":"tierra","pol1":"yin","elem2":"madera","pol2":"yin","descripcion":"Tierra Yin choca con Madera Yin","efecto":"Experiencias que te fortalecen como persona. Te sacan de la zona de confort."},
    {"troncos":["Bing","Geng"],"elem1":"fuego","pol1":"yang","elem2":"metal","pol2":"yang","descripcion":"Fuego Yang choca con Metal Yang","efecto":"Choque agresivo. Obstáculos. Desidia, olvido, descuido."},
    {"troncos":["Ding","Xin"],"elem1":"fuego","pol1":"yin","elem2":"metal","pol2":"yin","descripcion":"Fuego Yin choca con Metal Yin","efecto":"Situaciones que te moldean y transforman en la persona que eres en realidad."},
    {"troncos":["Wu","Ren"],"elem1":"tierra","pol1":"yang","elem2":"agua","pol2":"yang","descripcion":"Tierra Yang choca con Agua Yang","efecto":"Obstáculos que te controlan. La montaña te pone límites para que avances por donde debes."},
    {"troncos":["Ji","Gui"],"elem1":"tierra","pol1":"yin","elem2":"agua","pol2":"yin","descripcion":"Tierra Yin choca con Agua Yin","efecto":"Falta de claridad y concentración. El lodo no permite ver más allá de lo obvio."},
]

# ------------------------------------------------------------
# COMBINACIONES DE RAMAS
# ------------------------------------------------------------
COMBINACIONES_RAMAS_DIRECCIONALES = [
    {"animales":["Rata","Buey"],          "genera":"tierra"},
    {"animales":["Tigre","Cerdo"],        "genera":"madera"},
    {"animales":["Conejo","Perro"],       "genera":"metal"},
    {"animales":["Dragón","Gallo"],       "genera":"metal"},
    {"animales":["Serpiente","Mono"],     "genera":"agua"},
    {"animales":["Caballo","Cabra"],      "genera":"tierra"},
]

COMBINACIONES_RAMAS_ESTACIONALES = [
    {"animales":["Cerdo","Rata","Buey"],          "genera":"agua",  "estacion":"Invierno"},
    {"animales":["Serpiente","Caballo","Cabra"],   "genera":"fuego", "estacion":"Verano"},
    {"animales":["Tigre","Conejo","Dragón"],       "genera":"madera","estacion":"Primavera"},
    {"animales":["Mono","Gallo","Perro"],          "genera":"metal", "estacion":"Otoño"},
]

COMBINACIONES_RAMAS_ELEMENTALES = [
    {"animales":["Mono","Rata","Dragón"],         "genera":"agua"},
    {"animales":["Tigre","Perro","Caballo"],      "genera":"fuego"},
    {"animales":["Cerdo","Rata","Cabra"],         "genera":"madera"},
    {"animales":["Serpiente","Gallo","Buey"],     "genera":"metal"},
]

# ------------------------------------------------------------
# CONFLICTOS DE RAMAS
# ------------------------------------------------------------
CHOQUES_RAMAS = [
    {"animales":["Rata","Caballo"],    "efecto":"Altibajos, choques no pacíficos que pueden afectar el corazón."},
    {"animales":["Buey","Cabra"],      "efecto":"Obstáculos y problemas de pareja que afectarán tu salud."},
    {"animales":["Tigre","Mono"],      "efecto":"Choque emocional. Accidentes en viajes. Es el más fuerte."},
    {"animales":["Conejo","Gallo"],    "efecto":"Traición, pérdida de confianza en parientes y amigos. Es de los más fuertes."},
    {"animales":["Dragón","Perro"],    "efecto":"Fuertes conflictos y choque de personalidades. La comunicación es difícil."},
    {"animales":["Serpiente","Cerdo"], "efecto":"Interferencia de personas que provocan problemas."},
]

DANOS_RAMAS = [
    {"animales":["Conejo","Dragón"],   "efecto":"Tendencia a problemas de tipo legal por interferencias de otras personas.", "psicologico":"Dificultad para poner límites. El miedo al rechazo te domina. Trabaja en ello."},
    {"animales":["Gallo","Perro"],     "efecto":"Traiciones por exceso de confianza, en especial en seres queridos.", "psicologico":"Estar a la defensiva, con gran temor al fracaso. Se torna antisocial. Trabajar la autoestima y la confianza."},
    {"animales":["Mono","Cerdo"],      "efecto":"Pensamiento de que las personas están en tu contra. Genera conflictos frecuentes.", "psicologico":"Pesimista y dramático. Deja el drama, aprende a dejar ir lo que no te hace bien."},
    {"animales":["Rata","Cabra"],      "efecto":"Produce confusión emocional que puede hacer que tomes decisiones incorrectas.", "psicologico":"Indecisión. No sabe hacia dónde ir, qué decisiones tomar. Tomar decisiones desde el corazón."},
    {"animales":["Buey","Caballo"],    "efecto":"Pérdida de oportunidades, evita que otras personas interfieran en tu vida.", "psicologico":"Inhabilidad para expresar emociones. ¿Alguna vez pudiste expresar tus emociones? Trabaja en ello."},
    {"animales":["Tigre","Serpiente"], "efecto":"Contratiempos en viajes y todo tipo de movimientos.", "psicologico":"Sentimientos de culpa. Dificultades para recibir, no se siente merecedor. Autoaceptación y autocuidado."},
]

DESTRUCCIONES_RAMAS = [
    {"animales":["Conejo","Caballo"],  "efecto":"Pérdida de confianza con seres queridos por abusos.", "psicologico":"Persona descuidada."},
    {"animales":["Cabra","Perro"],     "efecto":"Afecta la estabilidad de la persona, interfiriendo la familia con el trabajo.", "psicologico":"Exceso de pensamientos, que le generan parálisis."},
    {"animales":["Serpiente","Mono"],  "efecto":"Situaciones que pueden cambiar de positivas a muy negativas.", "psicologico":"Estancado en relaciones de 'hoy te amo, mañana te odio'."},
    {"animales":["Rata","Gallo"],      "efecto":"Aislamiento por excesos: comida, drogas, alcohol, conductas sexuales inapropiadas.", "psicologico":"Difícil aceptar las opiniones de otros."},
    {"animales":["Buey","Dragón"],     "efecto":"Afecta la estabilidad de la persona con su familia y trabajo.", "psicologico":"Guardas emociones."},
    {"animales":["Tigre","Cerdo"],     "efecto":"Situaciones que pueden cambiar de positivas a muy negativas.", "psicologico":"Vulnerable a ser engañado fácilmente."},
]

CASTIGOS_RAMAS = [
    {
        "tipo": "Castigo Ingrato",
        "animales": ["Tigre","Serpiente","Mono"],
        "efecto": "La persona ofrece ayuda o apoyo sin esperar nada a cambio, pero el resultado final es negativo. En lugar de recibir agradecimiento recibirá críticas o se meterá en problemas. Tendencia a ser engañada, defraudada o estafada. Esta condición puede llegar a producir depresión y aislamiento.",
        "psicologico_pares": {
            "Tigre-Serpiente": "Te sientes no valorado.",
            "Serpiente-Mono": "Tu visión, opinión no son reconocidas.",
            "Mono-Tigre": "Sentirte responsable de todo.",
        }
    },
    {
        "tipo": "Castigo Intimidante",
        "animales": ["Buey","Cabra","Perro"],
        "efecto": "Similar al bullying, es un abuso a la persona, donde se sentirá indefensa o incapaz de defenderse a sí misma. La culpa es normalmente de la misma persona por descuido o actuar impulsivamente, estará pagando por un error cometido en el pasado. La persona se verá envuelta en situaciones desventajosas o en contra de su voluntad.",
        "psicologico_pares": {
            "Cabra-Buey": "Desvalorización total de la persona.",
            "Buey-Perro": "Sientes que las personas se aprovechan de ti.",
            "Perro-Cabra": "Estrés extremo, sentirse sin recursos. Intimidación.",
        }
    },
    {
        "tipo": "Castigo Incivilizado",
        "animales": ["Rata","Conejo"],
        "efecto": "Incivilizado significa falta de amabilidad, de educación, de valores, de lealtad. Las personas con este tipo de castigo usualmente son mal habladas, agresivas. La persona es emocionalmente inestable, se siente superior a los demás y puede presentar deseos sexuales incontrolables.",
        "psicologico": "Sentir que no eres fiel a las personas que te aman.",
    },
    {
        "tipo": "Auto-Castigo — Dragón",
        "animales": ["Dragón","Dragón"],
        "efecto": "La persona tiende a vivir sola, no le gusta que le toquen sus cosas. Es obstinada, tiene principios, no le gusta que los demás la estorben, le gusta ser independiente. Tipo depresivo.",
        "psicologico": "Contradicción interna.",
    },
    {
        "tipo": "Auto-Castigo — Caballo",
        "animales": ["Caballo","Caballo"],
        "efecto": "A la persona le gusta siempre ganar, no escucha críticas. Su personalidad es extrema con cambios drásticos de humor, impaciente y negligente.",
        "psicologico": "Intensa culpa por acciones realizadas de forma arbitraria.",
    },
    {
        "tipo": "Auto-Castigo — Gallo",
        "animales": ["Gallo","Gallo"],
        "efecto": "La persona quiere sobresalir a costa de lo que sea, pero puede no llegar a tener reconocimiento. La vanidad es fuerte. Tendencia a la melancolía.",
        "psicologico": "Tendencia a tener mucha lástima de sí mismo.",
    },
    {
        "tipo": "Auto-Castigo — Cerdo",
        "animales": ["Cerdo","Cerdo"],
        "efecto": "Inteligente, listo, comprensivo, guarda las cosas muy adentro, pero es tipo depresivo con tendencia al suicidio si el Agua es un elemento desfavorable para el mapa.",
        "psicologico": "Intensos arrepentimientos por lo hecho o lo no hecho.",
    },
]

# ------------------------------------------------------------
# FUNCIONES DE DETECCIÓN
# ------------------------------------------------------------

def get_animal_elemento_desc(animal, tronco_nombre):
    """Obtiene la descripción específica del animal+elemento del tronco."""
    dm = DM_DESC.get(tronco_nombre, {})
    elemento = dm.get("elemento", "")
    key = (animal, elemento)
    return ANIMALES_ELEMENTO_DESC.get(key, "")


RAMA_A_PINYIN = {
    "Rata":"Zi","Buey":"Chou","Tigre":"Yin","Conejo":"Mao","Dragón":"Chen",
    "Serpiente":"Si","Caballo":"Wu","Cabra":"Wei","Mono":"Shen","Gallo":"You",
    "Perro":"Xu","Cerdo":"Hai"
}

def get_muerte_vacio(dm_tronco, dm_rama):
    """Obtiene los animales de muerte y vacío para un pilar del día maestro."""
    rama_pinyin = RAMA_A_PINYIN.get(dm_rama, dm_rama)
    pilar_key = f"{dm_tronco} {rama_pinyin}"
    return MUERTE_VACIO.get(pilar_key, [])


def get_pilares_afines(tronco, rama):
    """Obtiene los 9 pilares afines (misma columna/xun de los 60 pilares)
    de un pilar dado, excluyendo al propio pilar. Devuelve lista vacía
    si el pilar no se encuentra en la tabla de columnas."""
    rama_pinyin = RAMA_A_PINYIN.get(rama, rama)
    pilar_key = f"{tronco} {rama_pinyin}"
    columna = PILAR_A_COLUMNA.get(pilar_key, [])
    return [p for p in columna if p != pilar_key]


def get_camara_roja(dm_tronco):
    """Obtiene el animal de cámara roja según el tronco del día maestro."""
    return CAMARA_ROJA.get(dm_tronco, "")


def get_casamentero(dm_rama):
    """Obtiene el animal Casamentero según la rama (animal) del día
    maestro. Devuelve dict {"animal": ..., "es_tambien_karmico": ...}
    o dict vacío si no se encuentra."""
    return CASAMENTERO_POR_RAMA.get(dm_rama, {})


def calcular_yin_yang(carta_fija):
    """Calcula el balance Yin/Yang de los troncos de los 4 pilares fijos."""
    yang_count = 0
    yin_count = 0
    for pilar in ["hora","dia","mes","anio"]:
        pol = carta_fija.get(pilar,{}).get("tronco",{}).get("polaridad","")
        if pol.lower() == "yang":
            yang_count += 1
        elif pol.lower() == "yin":
            yin_count += 1
    total = yang_count + yin_count
    if total == 0:
        return {"yang": 0, "yin": 0, "equilibrio": True}
    return {
        "yang": round(yang_count/total*100),
        "yin":  round(yin_count/total*100),
        "equilibrio": yang_count == yin_count,
    }


def calcular_cesta_elementos(carta_fija):
    """Cuenta elementos en troncos + ramas de los 4 pilares fijos."""
    conteo = {"madera":0,"fuego":0,"tierra":0,"metal":0,"agua":0}
    for pilar in ["hora","dia","mes","anio"]:
        datos = carta_fija.get(pilar, {})
        elem_t = datos.get("tronco",{}).get("elemento","").lower()
        elem_r = datos.get("rama",{}).get("elemento","").lower()
        if elem_t in conteo:
            conteo[elem_t] += 1
        if elem_r in conteo:
            conteo[elem_r] += 1
    return conteo


def get_cesta_desc(elemento, cantidad):
    """Retorna la descripción de la cesta según elemento y cantidad."""
    desc_elem = CESTA_ELEMENTOS.get(elemento, {})
    if cantidad >= 4:
        nivel = "4+"
    elif cantidad >= 2:
        nivel = "2-3"
    else:
        nivel = "0-1"
    return {
        "nivel": nivel,
        "desc": desc_elem.get(nivel, ""),
        "recargar": desc_elem.get("recargar","") if cantidad <= 1 else "",
    }


def detectar_combinaciones_troncos(pilares):
    """Detecta combinaciones entre troncos celestes en todos los pilares."""
    resultados = []
    nombres = list(pilares.keys())
    for i, p1 in enumerate(nombres):
        for p2 in nombres[i+1:]:
            t1 = pilares[p1].get("tronco",{})
            t2 = pilares[p2].get("tronco",{})
            if not t1 or not t2:
                continue
            for combo in COMBINACIONES_TRONCOS:
                if (set([t1.get("nombre"),t2.get("nombre")]) ==
                    set([combo["tronco1"],combo["tronco2"]])):
                    resultados.append({
                        "tipo": "combinacion_troncos",
                        "pilares": [p1,p2],
                        "troncos": [t1.get("nombre"),t2.get("nombre")],
                        "genera": combo["genera"],
                        "descripcion": combo["descripcion"],
                    })
    return resultados


def detectar_choques_troncos(pilares, sexo):
    """Detecta choques entre troncos celestes."""
    resultados = []
    nombres = list(pilares.keys())
    tabla = DIOSES_PERSONAS.get(sexo, {})
    for i, p1 in enumerate(nombres):
        for p2 in nombres[i+1:]:
            t1 = pilares[p1].get("tronco",{})
            t2 = pilares[p2].get("tronco",{})
            if not t1 or not t2:
                continue
            for choque in CHOQUES_TRONCOS:
                if set([t1.get("nombre"),t2.get("nombre")]) == set(choque["troncos"]):
                    dioses = ([t1.get("dios","")] +
                              [to.get("dios","") for to in pilares[p1].get("troncos_ocultos",[])] +
                              [t2.get("dios","")] +
                              [to.get("dios","") for to in pilares[p2].get("troncos_ocultos",[])])
                    personas = []
                    for d in set(dioses):
                        personas.extend(tabla.get(d,[]))
                    clave = frozenset([p1,p2])
                    ambito = CHOQUE_PILARES.get(clave, f"interacción entre pilar {p1} y pilar {p2}")
                    resultados.append({
                        "tipo": "choque_troncos",
                        "pilares": [p1,p2],
                        "troncos": [t1.get("nombre"),t2.get("nombre")],
                        "descripcion": choque["descripcion"],
                        "efecto": choque["efecto"],
                        "ambito": ambito,
                        "personas": list(set(personas)),
                    })
    return resultados


def detectar_combinaciones_ramas(pilares):
    """Detecta combinaciones de ramas (direccionales, estacionales, elementales)."""
    resultados = []
    animales_en_carta = {}
    for nombre_pilar, datos in pilares.items():
        animal = datos.get("rama",{}).get("nombre","")
        if animal:
            animales_en_carta[animal] = nombre_pilar

    def check(lista, tipo):
        for combo in lista:
            match = [animales_en_carta.get(a) for a in combo["animales"]]
            if all(match):
                info = {
                    "tipo": tipo,
                    "animales": combo["animales"],
                    "pilares": match,
                    "genera": combo["genera"],
                }
                if "estacion" in combo:
                    info["estacion"] = combo["estacion"]
                resultados.append(info)

    check(COMBINACIONES_RAMAS_DIRECCIONALES, "direccional")
    check(COMBINACIONES_RAMAS_ESTACIONALES,  "estacional")
    check(COMBINACIONES_RAMAS_ELEMENTALES,   "elemental")
    return resultados


NATAL_KEYS = {"anio", "mes", "dia", "hora"}


def detectar_conflictos_ramas(pilares, sexo):
    """Detecta choques, daños, destrucciones y castigos entre ramas.

    `pilares` puede incluir tanto los 4 pilares fijos (claves "anio","mes",
    "dia","hora") como pilares móviles (p. ej. "pilar_suerte","anio_curso")
    y pilares extra agregados por el astrólogo.

    Reglas de detección:
    - Conflictos de 2 animales distintos (choques, daños, destrucciones,
      Castigo Incivilizado): se detectan si ambos animales están presentes
      en cualquier combinación de pilares (natal y/o móvil).
    - Castigos de 3 animales (Ingrato, Intimidante): se detectan solo si
      están los 3 presentes. Si los 3 están en la carta natal, se marca
      como "natal". Si 2 están en la carta natal y el tercero llega por
      el Pilar de Suerte o el Año en Curso, se marca como "temporal_transito"
      y se aclara que es una activación temporal.
    - Auto-castigos (mismo animal repetido: Dragón, Caballo, Gallo, Cerdo):
      se detectan solo si ese animal aparece en DOS pilares distintos
      (natal y/o móvil) — una sola aparición no activa el auto-castigo.
    """
    resultados = []
    animales_multi = {}
    for nombre_pilar, datos in pilares.items():
        animal = datos.get("rama", {}).get("nombre", "")
        if animal:
            animales_multi.setdefault(animal, []).append(nombre_pilar)

    tabla = DIOSES_PERSONAS.get(sexo, {})

    def es_natal(pilar_nombre):
        return pilar_nombre in NATAL_KEYS

    def get_personas(pilar_nombre):
        datos = pilares.get(pilar_nombre, {})
        dioses = ([datos.get("tronco", {}).get("dios", "")] +
                  [to.get("dios", "") for to in datos.get("troncos_ocultos", [])])
        personas = []
        for d in set(dioses):
            personas.extend(tabla.get(d, []))
        return list(set(personas))

    def personas_de(pilares_list):
        personas = []
        for p in pilares_list:
            if p:
                personas.extend(get_personas(p))
        return list(set(personas))

    def ambito_de(match):
        """Área de vida involucrada. Prioriza la combinación específica de
        CHOQUE_PILARES (solo definida entre pilares fijos); si no existe
        —por ejemplo cuando uno de los pilares es móvil (Pilar de Suerte
        o Año en Curso)— arma el área a partir del/los pilar(es) fijo(s)
        involucrados, usando PILARES_INFO."""
        clave = frozenset(match)
        ambito = CHOQUE_PILARES.get(clave, "")
        if ambito:
            return ambito
        partes = []
        for p in match:
            if p in PILARES_INFO:
                partes.append(f"{p.capitalize()}: {PILARES_INFO[p]['ambito']}")
        return " / ".join(partes)

    def check_par(lista, tipo):
        """Conflictos de 2 animales distintos.

        Reporta TODAS las combinaciones de pilares que activan el
        conflicto, no solo la primera: si un animal se repite en más
        de un pilar (p. ej. la Serpiente en Mes y en Día), cada
        combinación con el otro animal del par se reporta por
        separado, con su propio ámbito y personas involucradas.
        """
        for item in lista:
            a1, a2 = item["animales"]
            p1_list = animales_multi.get(a1, [])
            p2_list = animales_multi.get(a2, [])
            if not (p1_list and p2_list):
                continue
            for p1 in p1_list:
                for p2 in p2_list:
                    if p1 == p2:
                        continue
                    match = [p1, p2]
                    res = {
                        "tipo": tipo,
                        "subtipo": item.get("tipo", tipo),
                        "animales": item["animales"],
                        "pilares": match,
                        "efecto": item["efecto"],
                        "ambito": ambito_de(match),
                        "personas": personas_de(match),
                    }
                    if "psicologico" in item:
                        res["psicologico"] = item["psicologico"]
                    resultados.append(res)

    def check_castigo_triple(item):
        """Castigos de 3 animales: completo en natal, o activable por tránsito."""
        animales_item = item["animales"]
        presentes = {}
        for a in animales_item:
            lst = animales_multi.get(a, [])
            if lst:
                natal_p = next((p for p in lst if es_natal(p)), None)
                presentes[a] = natal_p if natal_p else lst[0]
        if len(presentes) < 3:
            return
        match = [presentes[a] for a in animales_item]
        transito = [a for a in animales_item if not es_natal(presentes[a])]
        res = {
            "tipo": "castigo",
            "subtipo": item["tipo"],
            "animales": animales_item,
            "pilares": match,
            "efecto": item["efecto"],
            "ambito": ambito_de(match[:2]),
            "personas": personas_de(match),
            "activacion": "temporal_transito" if transito else "natal",
        }
        if "psicologico_pares" in item:
            res["psicologico_pares"] = item["psicologico_pares"]
        if transito:
            res["animal_transito"] = transito
            res["nota"] = (
                f"Activación temporal: {', '.join(transito)} completa este castigo "
                "desde el Pilar de Suerte o el Año en Curso, no desde la carta natal."
            )
        resultados.append(res)

    def check_autocastigo(item):
        """Auto-castigo: requiere el mismo animal en 2 pilares distintos."""
        animal = item["animales"][0]
        pilares_animal = animales_multi.get(animal, [])
        if len(pilares_animal) >= 2:
            match = pilares_animal[:2]
            res = {
                "tipo": "castigo",
                "subtipo": item["tipo"],
                "animales": item["animales"],
                "pilares": match,
                "efecto": item["efecto"],
                "ambito": ambito_de(match),
                "personas": personas_de(match),
            }
            if "psicologico" in item:
                res["psicologico"] = item["psicologico"]
            resultados.append(res)

    check_par(CHOQUES_RAMAS, "choque")
    check_par(DANOS_RAMAS, "daño")
    check_par(DESTRUCCIONES_RAMAS, "destrucción")

    for item in CASTIGOS_RAMAS:
        animales_item = item["animales"]
        if len(animales_item) == 3:
            check_castigo_triple(item)
        elif len(animales_item) == 2 and animales_item[0] == animales_item[1]:
            check_autocastigo(item)
        elif len(animales_item) == 2:
            check_par([item], "castigo")

    return resultados


def _animales_de_pilares(pilares_dict):
    """Helper: mapea animal -> nombre_pilar a partir de un dict de pilares."""
    animales = {}
    for nombre_pilar, datos in (pilares_dict or {}).items():
        animal = datos.get("rama", {}).get("nombre", "")
        if animal:
            animales[animal] = nombre_pilar
    return animales


def _detectar_karmicas(pilares, pilares_moviles, sexo):
    """Detecta relaciones kármicas reportando TODAS las combinaciones de
    pilares que las completan — si un animal se repite en más de un pilar
    (p. ej. la Serpiente en Mes y en Día), se reportan ambas conexiones
    por separado, cada una con su propia área de vida y personas
    involucradas. También detecta activación por tránsito."""
    animales_natal = {}
    for nombre_pilar, datos in pilares.items():
        animal = datos.get("rama", {}).get("nombre", "")
        if animal:
            animales_natal.setdefault(animal, []).append(nombre_pilar)
    animales_mov = {}
    for nombre_pilar, datos in (pilares_moviles or {}).items():
        animal = datos.get("rama", {}).get("nombre", "")
        if animal:
            animales_mov.setdefault(animal, []).append(nombre_pilar)

    tabla = DIOSES_PERSONAS.get(sexo, {})
    todos_los_pilares = {**pilares, **(pilares_moviles or {})}

    def get_personas(pilar_nombre):
        datos = todos_los_pilares.get(pilar_nombre, {})
        dioses = ([datos.get("tronco", {}).get("dios", "")] +
                  [to.get("dios", "") for to in datos.get("troncos_ocultos", [])])
        personas = []
        for d in set(dioses):
            personas.extend(tabla.get(d, []))
        return list(set(personas))

    def ambito_de(match):
        clave = frozenset(match)
        ambito = CHOQUE_PILARES.get(clave, "")
        if ambito:
            return ambito
        partes = []
        for p in match:
            if p in PILARES_INFO:
                partes.append(f"{p.capitalize()}: {PILARES_INFO[p]['ambito']}")
        return " / ".join(partes)

    completos = []
    parciales = []
    for rel in RELACIONES_KARMICAS:
        a1, a2 = rel["animales"]
        p1_natal = animales_natal.get(a1, [])
        p2_natal = animales_natal.get(a2, [])
        combos_reportados = set()

        def _agregar(p1, p2, estado, transito_info=None):
            clave_combo = frozenset([p1, p2])
            if clave_combo in combos_reportados:
                return
            combos_reportados.add(clave_combo)
            entry = {
                "animales": rel["animales"],
                "pilares": [p1, p2],
                "estado": estado,
                "ambito": ambito_de([p1, p2]),
                "personas": list(set(get_personas(p1) + get_personas(p2))),
                "desc": rel["desc"],
                "es_tambien_casamentero": rel.get("es_tambien_casamentero", False),
            }
            if transito_info:
                entry.update(transito_info)
            completos.append(entry)

        for p1 in p1_natal:
            for p2 in p2_natal:
                _agregar(p1, p2, "completo_natal")

        if not p1_natal:
            for p1 in animales_mov.get(a1, []):
                for p2 in p2_natal:
                    _agregar(p1, p2, "activable_transito",
                             {"animal_transito": [a1], "pilar_transito": [p1]})
        if not p2_natal:
            for p2 in animales_mov.get(a2, []):
                for p1 in p1_natal:
                    _agregar(p1, p2, "activable_transito",
                             {"animal_transito": [a2], "pilar_transito": [p2]})

        if p1_natal and not p2_natal and not animales_mov.get(a2):
            parciales.append({
                "animales": rel["animales"], "animal_presente": a1,
                "pilar_presente": p1_natal[0], "animal_faltante": [a2],
            })
        elif p2_natal and not p1_natal and not animales_mov.get(a1):
            parciales.append({
                "animales": rel["animales"], "animal_presente": a2,
                "pilar_presente": p2_natal[0], "animal_faltante": [a1],
            })

    return completos, parciales


def _detectar_par_animal(lista_pares, animales_natal, animales_moviles, clave_extra_natal, clave_extra_movil):
    """Detecta pares de 2 animales (kármicos o casamentero) contra la carta
    natal y, si se proveen, contra los pilares móviles (suerte / año en
    curso). Devuelve dos listas: completos (o activables por tránsito) y
    parciales (un solo animal presente, sin completar)."""
    completos = []
    parciales = []
    for rel in lista_pares:
        animales = rel["animales"]
        presentes_natal = {a: animales_natal.get(a) for a in animales if animales_natal.get(a)}
        faltantes = [a for a in animales if a not in presentes_natal]

        if not faltantes:
            completos.append({
                "animales": animales,
                "pilares": [presentes_natal[a] for a in animales],
                "estado": "completo_natal",
                clave_extra_natal: rel.get(clave_extra_natal, False),
            })
            continue

        if animales_moviles:
            faltan_en_moviles = [a for a in faltantes if a not in animales_moviles]
            if not faltan_en_moviles:
                pilares_combinados = [presentes_natal.get(a) or animales_moviles.get(a) for a in animales]
                completos.append({
                    "animales": animales,
                    "pilares": pilares_combinados,
                    "estado": "activable_transito",
                    "animal_transito": faltantes,
                    "pilar_transito": [animales_moviles[a] for a in faltantes],
                    clave_extra_natal: rel.get(clave_extra_natal, False),
                })
                continue

        if presentes_natal:
            animal_presente = list(presentes_natal.keys())[0]
            parciales.append({
                "animales": animales,
                "animal_presente": animal_presente,
                "pilar_presente": presentes_natal[animal_presente],
                "animal_faltante": faltantes,
            })

    return completos, parciales


def detectar_relaciones(pilares, dm_tronco, dm_rama, sexo, flor_melocoton_animal="", pilares_moviles=None):
    """Detecta cámara roja, relaciones kármicas, casamentero, muerte y
    vacío y pilares afines por columna.

    `pilares_moviles` es opcional: un dict con los pilares de suerte y/o
    año en curso (misma estructura que `pilares`), usado para detectar
    pares kármicos o casamenteros que se completan por tránsito aunque
    no estén completos en la carta natal.
    """
    animales_en_carta = _animales_de_pilares(pilares)
    animales_moviles = _animales_de_pilares(pilares_moviles) if pilares_moviles else {}

    # Cámara roja: mismo criterio que Casamentero (se determina por el
    # Día Maestro, con tronco en este caso) y también puede activarse
    # por tránsito (año, mes o ciclo de suerte con ese animal).
    camara_roja_animal = get_camara_roja(dm_tronco)
    camara_roja_pilares_natal = [p for a, p in animales_en_carta.items() if a == camara_roja_animal]
    camara_roja_pilares_transito = [p for a, p in animales_moviles.items() if a == camara_roja_animal]
    camara_roja = {
        "animal": camara_roja_animal,
        "pilares_natal": camara_roja_pilares_natal,
        "pilares_transito": camara_roja_pilares_transito,
        "activo": bool(camara_roja_pilares_natal or camara_roja_pilares_transito),
    }

    # Flor de melocotón
    flor_elem = ""
    for p, datos in pilares.items():
        if datos.get("rama",{}).get("nombre","") == flor_melocoton_animal:
            flor_elem = datos.get("rama",{}).get("elemento","")
            break
    flor_desc = FLOR_MELOCOTON.get(flor_elem,"")

    # Relaciones kármicas: se reportan TODAS las conexiones de pilares que
    # las completan (natal y/o por tránsito), incluyendo casos donde un
    # mismo animal se repite en más de un pilar.
    karmicas_completas, karmicas_parciales = _detectar_karmicas(
        pilares, pilares_moviles, sexo
    )

    # Casamentero: se determina por la RAMA del Día Maestro (igual que la
    # Cámara Roja), no por búsqueda de pares en cualquier pilar.
    casamentero_info = get_casamentero(dm_rama)
    casamentero_animal = casamentero_info.get("animal", "")
    casamentero_pilares_natal = [p for a, p in animales_en_carta.items() if a == casamentero_animal]
    casamentero_pilares_transito = [p for a, p in animales_moviles.items() if a == casamentero_animal]
    casamentero = {
        "animal": casamentero_animal,
        "es_tambien_karmico": casamentero_info.get("es_tambien_karmico", False),
        "pilares_natal": casamentero_pilares_natal,
        "pilares_transito": casamentero_pilares_transito,
        "activo": bool(casamentero_pilares_natal or casamentero_pilares_transito),
    }

    # Muerte y vacío (del día maestro, sobre los 4 pilares fijos)
    mv_animales = get_muerte_vacio(dm_tronco, dm_rama)
    mv_detectado = []
    for animal in mv_animales:
        pilar = animales_en_carta.get(animal)
        if pilar:
            mv_detectado.append({
                "animal": animal,
                "pilar": pilar,
                "significados": MUERTE_VACIO_PILARES.get(pilar, []),
            })

    # Pilares afines por columna: uno por cada pilar fijo presente en la carta
    pilares_afines = {}
    for nombre_pilar, datos in pilares.items():
        tronco_nombre = datos.get("tronco", {}).get("nombre", "")
        rama_nombre = datos.get("rama", {}).get("nombre", "")
        if not tronco_nombre or not rama_nombre:
            continue
        rama_pinyin = RAMA_A_PINYIN.get(rama_nombre, rama_nombre)
        pilar_key = f"{tronco_nombre} {rama_pinyin}"
        afines = get_pilares_afines(tronco_nombre, rama_nombre)
        mv_columna = MUERTE_VACIO.get(pilar_key, [])
        pilares_afines[nombre_pilar] = {
            "pilar": pilar_key,
            "afines": afines,
            "muerte_vacio_columna": mv_columna,
        }

    return {
        "camara_roja": camara_roja,
        "flor_melocoton": {"animal": flor_melocoton_animal, "elemento": flor_elem, "desc": flor_desc},
        "karmicas": karmicas_completas,
        "karmicas_parciales": karmicas_parciales,
        "casamentero": casamentero,
        "muerte_vacio": mv_detectado,
        "pilares_afines": pilares_afines,
    }


def analizar_cinco_elementos(cinco_elementos):
    """Analiza balance, carencias, excesos y genera recomendaciones."""
    resultado = {"exceso":[], "equilibrio":[], "carencia":[], "superpoder":None}
    dominante = max(cinco_elementos, key=lambda e: cinco_elementos[e].get("porcentaje",0))
    resultado["superpoder"] = {
        "elemento": dominante,
        "descripcion": SUPERPODER_FINANCIERO.get(dominante,""),
    }
    for elemento, datos in cinco_elementos.items():
        pct = datos.get("porcentaje",0)
        representa = datos.get("representa","").lower()
        desc = ELEMENTOS_DESC.get(representa,{})
        if pct > 30:
            resultado["exceso"].append({"elemento":elemento,"porcentaje":pct,"representa":representa,"rec":desc.get("rec_exceso","")})
        elif pct < 10:
            resultado["carencia"].append({"elemento":elemento,"porcentaje":pct,"representa":representa,"rec":desc.get("rec_carencia","")})
        else:
            resultado["equilibrio"].append({"elemento":elemento,"porcentaje":pct,"representa":representa})
    return resultado


def detectar_salud_especial(pilares, sexo):
    """Detecta combinaciones especiales de salud."""
    animales_en_carta = {}
    for nombre_pilar, datos in pilares.items():
        animal = datos.get("rama",{}).get("nombre","")
        if animal:
            animales_en_carta[animal] = nombre_pilar

    resultados = []
    for comb in SALUD_COMBINACIONES_ESPECIALES:
        match = [animales_en_carta.get(a) for a in comb["animales"]]
        if all(match):
            if comb["condicion"] == "siempre":
                resultados.append({
                    "animales": comb["animales"],
                    "pilares": match,
                    "efecto": comb["efecto"],
                })
            elif comb["condicion"] == "mujer + pilares dia y hora" and sexo == "mujer":
                if set(match) == {"dia","hora"}:
                    resultados.append({
                        "animales": comb["animales"],
                        "pilares": match,
                        "efecto": comb["efecto"],
                    })
    return resultados
