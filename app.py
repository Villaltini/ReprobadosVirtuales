import streamlit as st
import pandas as pd
import re
import io

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Filtro de Notas UGB",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

    /* ==============================
       GENERAL
    ============================== */

    .main {
        padding-top: 1rem;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ==============================
       ENCABEZADO
    ============================== */

    .header {
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 25px;
        background: linear-gradient(
            135deg,
            #0f172a,
            #1e3a8a
        );
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    .header h1 {
        margin: 0;
        font-size: 34px;
        font-weight: 700;
    }

    .header p {
        margin-top: 8px;
        margin-bottom: 0;
        font-size: 16px;
        opacity: 0.85;
    }


    /* ==============================
       TARJETAS
    ============================== */

    .card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        height: 100%;
        min-height: 130px;
    }

    .card-title {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 8px;
    }

    .card-value {
        font-size: 30px;
        font-weight: 700;
        color: #0f172a;
    }

    .card-description {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 5px;
    }


    /* ==============================
       SECCIONES
    ============================== */

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 30px;
        margin-bottom: 15px;
    }


    /* ==============================
       CAJA PDF
    ============================== */

    .upload-box {
        padding: 30px;
        border: 2px dashed #94a3b8;
        border-radius: 18px;
        text-align: center;
        background: #f8fafc;
        margin: 20px 0;
    }

    .upload-box h3 {
        margin-bottom: 5px;
        color: #0f172a;
    }

    .upload-box p {
        color: #64748b;
    }


    /* ==============================
       ESTADOS
    ============================== */

    .estado-aprobado {
        padding: 8px 12px;
        border-radius: 8px;
        background: #dcfce7;
        color: #166534;
        font-weight: 600;
    }

    .estado-riesgo {
        padding: 8px 12px;
        border-radius: 8px;
        background: #fef3c7;
        color: #92400e;
        font-weight: 600;
    }

    .estado-reprobado {
        padding: 8px 12px;
        border-radius: 8px;
        background: #fee2e2;
        color: #991b1b;
        font-weight: 600;
    }


    /* ==============================
       INFORMACIÓN
    ============================== */

    .info-box {
        padding: 18px;
        border-radius: 12px;
        background: #eff6ff;
        border-left: 5px solid #2563eb;
        margin: 15px 0;
    }


    /* ==============================
       BOTONES
    ============================== */

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }


    /* ==============================
       FOOTER
    ============================== */

    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        color: #94a3b8;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES
# ============================================================

def extraer_texto_pdf(archivo):
    """
    Extrae texto de un PDF utilizando pypdf.
    """

    try:
        from pypdf import PdfReader

        archivo.seek(0)

        reader = PdfReader(archivo)

        texto = ""

        for pagina in reader.pages:
            contenido = pagina.extract_text()

            if contenido:
                texto += contenido + "\n"

        return texto

    except Exception as e:
        st.error(f"Error al leer el PDF: {e}")
        return ""


def buscar_notas(texto):
    """
    Intenta detectar líneas que contengan:
    código + nombre + nota.

    Ejemplos que puede reconocer:

    001 Juan Perez 5.4
    002 Ana Lopez 5.8
    """

    registros = []

    lineas = texto.splitlines()

    for linea in lineas:

        linea = linea.strip()

        if not linea:
            continue

        # Buscar una nota entre 0 y 10
        coincidencia_nota = re.search(
            r'(?<!\d)(10(?:\.0)?|[0-9](?:\.[0-9])?)(?!\d)',
            linea
        )

        if not coincidencia_nota:
            continue

        nota = float(coincidencia_nota.group())

        if nota < 0 or nota > 10:
            continue

        parte_izquierda = linea[:coincidencia_nota.start()].strip()

        if not parte_izquierda:
            continue

        # Intentar detectar código al inicio
        codigo = ""

        coincidencia_codigo = re.match(
            r'^([A-Za-z0-9-]+)\s+(.+)$',
            parte_izquierda
        )

        if coincidencia_codigo:

            codigo = coincidencia_codigo.group(1)

            nombre = coincidencia_codigo.group(2)

        else:

            nombre = parte_izquierda

        registros.append({
            "Código": codigo,
            "Estudiante": nombre,
            "Nota": nota
        })

    return pd.DataFrame(registros)


def calcular_estado(nota, aprobacion=6.0):

    if nota >= aprobacion:
        return "Aprobado"

    elif nota >= 5.0:
        return "En riesgo"

    else:
        return "Reprobado"


def calcular_necesita(nota, aprobacion=6.0):

    diferencia = aprobacion - nota

    if diferencia <= 0:
        return 0.0

    return round(diferencia, 1)


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown("""
<div class="header">

    <h1>🎓 Filtro de Notas UGB</h1>

    <p>
        Lector, análisis y seguimiento de calificaciones académicas
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CONFIGURACIÓN ACADÉMICA
# ============================================================

st.markdown("""
<div class="section-title">
⚙️ Configuración académica
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:

    nota_aprobacion = st.number_input(
        "Nota mínima para aprobar",
        min_value=0.0,
        max_value=10.0,
        value=6.0,
        step=0.1
    )

with col2:

    nota_minima_filtro = st.number_input(
        "Nota mínima del filtro",
        min_value=0.0,
        max_value=10.0,
        value=5.0,
        step=0.1
    )

with col3:

    nota_maxima_filtro = st.number_input(
        "Nota máxima del filtro",
        min_value=0.0,
        max_value=10.0,
        value=5.9,
        step=0.1
    )


# ============================================================
# CARGAR PDF
# ============================================================

st.markdown("""
<div class="section-title">
📄 Cargar colector de notas
</div>

<div class="upload-box">

    <h3>📚 Selecciona el archivo PDF</h3>

    <p>
        El sistema analizará las calificaciones automáticamente.
    </p>

</div>
""", unsafe_allow_html=True)


archivo = st.file_uploader(
    "Seleccionar PDF",
    type=["pdf"],
    label_visibility="collapsed"
)


# ============================================================
# PROCESAMIENTO
# ============================================================

if archivo:

    st.success(f"📄 Archivo cargado: **{archivo.name}**")

    with st.spinner("Analizando el PDF..."):

        texto = extraer_texto_pdf(archivo)

    if texto:

        df = buscar_notas(texto)

        # ================================================
        # SI ENCUENTRA DATOS
        # ================================================

        if not df.empty:

            # Eliminar posibles duplicados
            df = df.drop_duplicates()

            # Estado
            df["Estado"] = df["Nota"].apply(
                lambda x: calcular_estado(
                    x,
                    nota_aprobacion
                )
            )

            # Cuánto necesita
            df["Necesita"] = df["Nota"].apply(
                lambda x: calcular_necesita(
                    x,
                    nota_aprobacion
                )
            )

            # ============================================
            # ESTADÍSTICAS
            # ============================================

            total = len(df)

            aprobados = len(
                df[df["Nota"] >= nota_aprobacion]
            )

            riesgo = len(
                df[
                    (df["Nota"] >= nota_minima_filtro)
                    &
                    (df["Nota"] < nota_aprobacion)
                ]
            )

            reprobados = len(
                df[df["Nota"] < nota_minima_filtro]
            )

            promedio = df["Nota"].mean()


            # ============================================
            # TARJETAS
            # ============================================

            st.markdown("""
            <div class="section-title">
            📊 Resumen académico
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.markdown(f"""
                <div class="card">

                    <div class="card-title">
                        👥 Estudiantes
                    </div>

                    <div class="card-value">
                        {total}
                    </div>

                    <div class="card-description">
                        Total encontrados
                    </div>

                </div>
                """, unsafe_allow_html=True)


            with col2:

                st.markdown(f"""
                <div class="card">

                    <div class="card-title">
                        ✅ Aprobados
                    </div>

                    <div class="card-value">
                        {aprobados}
                    </div>

                    <div class="card-description">
                        Nota ≥ {nota_aprobacion:.1f}
                    </div>

                </div>
                """, unsafe_allow_html=True)


            with col3:

                st.markdown(f"""
                <div class="card">

                    <div class="card-title">
                        ⚠️ En riesgo
                    </div>

                    <div class="card-value">
                        {riesgo}
                    </div>

                    <div class="card-description">
                        Entre {nota_minima_filtro:.1f} y {nota_aprobacion:.1f}
                    </div>

                </div>
                """, unsafe_allow_html=True)


            with col4:

                st.markdown(f"""
                <div class="card">

                    <div class="card-title">
                        📊 Promedio
                    </div>

                    <div class="card-value">
                        {promedio:.2f}
                    </div>

                    <div class="card-description">
                        Promedio general
                    </div>

                </div>
                """, unsafe_allow_html=True)


            # ============================================
            # FILTROS
            # ============================================

            st.markdown("""
            <div class="section-title">
            🔎 Filtrar estudiantes
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:

                buscar = st.text_input(
                    "🔍 Buscar estudiante",
                    placeholder="Nombre o código..."
                )

            with col2:

                estados = st.multiselect(
                    "Estado",
                    [
                        "Aprobado",
                        "En riesgo",
                        "Reprobado"
                    ],
                    default=[
                        "Aprobado",
                        "En riesgo",
                        "Reprobado"
                    ]
                )

            with col3:

                mostrar_rango = st.checkbox(
                    f"Mostrar solamente notas de "
                    f"{nota_minima_filtro:.1f} a "
                    f"{nota_maxima_filtro:.1f}"
                )


            # ============================================
            # APLICAR FILTROS
            # ============================================

            df_filtrado = df.copy()

            if buscar:

                texto_busqueda = buscar.lower()

                df_filtrado = df_filtrado[
                    df_filtrado["Estudiante"]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        texto_busqueda,
                        na=False
                    )
                    |
                    df_filtrado["Código"]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        texto_busqueda,
                        na=False
                    )
                ]


            if estados:

                df_filtrado = df_filtrado[
                    df_filtrado["Estado"].isin(estados)
                ]


            if mostrar_rango:

                df_filtrado = df_filtrado[
                    (df_filtrado["Nota"] >= nota_minima_filtro)
                    &
                    (df_filtrado["Nota"] <= nota_maxima_filtro)
                ]


            # ============================================
            # RESULTADOS
            # ============================================

            st.markdown("""
            <div class="section-title">
            🧑‍🎓 Resultados
            </div>
            """, unsafe_allow_html=True)


            st.info(
                f"Se encontraron **{len(df_filtrado)} "
                f"estudiantes** con los filtros actuales."
            )


            # ============================================
            # TABLA
            # ============================================

            if not df_filtrado.empty:

                df_mostrar = df_filtrado.copy()

                df_mostrar["Nota"] = df_mostrar["Nota"].round(1)

                df_mostrar["Necesita"] = df_mostrar[
                    "Necesita"
                ].apply(
                    lambda x: (
                        "Ya aprobó"
                        if x <= 0
                        else f"{x:.1f} puntos"
                    )
                )

                df_mostrar = df_mostrar[
                    [
                        "Código",
                        "Estudiante",
                        "Nota",
                        "Estado",
                        "Necesita"
                    ]
                ]

                st.dataframe(
                    df_mostrar,
                    use_container_width=True,
                    hide_index=True
                )


                # ========================================
                # DESCARGAR CSV
                # ========================================

                csv = df_filtrado.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="⬇️ Descargar resultados CSV",
                    data=csv,
                    file_name="resultados_notas_ugb.csv",
                    mime="text/csv"
                )


            else:

                st.warning(
                    "No hay estudiantes que coincidan "
                    "con los filtros seleccionados."
                )


            # ============================================
            # ESTUDIANTES EN RIESGO
            # ============================================

            df_riesgo = df[
                (df["Nota"] >= nota_minima_filtro)
                &
                (df["Nota"] < nota_aprobacion)
            ].copy()


            if not df_riesgo.empty:

                st.markdown("""
                <div class="section-title">
                ⚠️ Estudiantes que necesitan mejorar
                </div>
                """, unsafe_allow_html=True)


                for _, estudiante in df_riesgo.iterrows():

                    necesita = calcular_necesita(
                        estudiante["Nota"],
                        nota_aprobacion
                    )

                    st.markdown(f"""
                    <div class="info-box">

                        <strong>
                        {estudiante["Estudiante"]}
                        </strong>

                        — Nota actual:
                        <strong>{estudiante["Nota"]:.1f}</strong>

                        <br>

                        ⚠️ Necesita:
                        <strong>{necesita:.1f}</strong>
                        puntos para alcanzar
                        <strong>{nota_aprobacion:.1f}</strong>.

                    </div>
                    """, unsafe_allow_html=True)


            # ============================================
            # GRÁFICAS
            # ============================================

            st.markdown("""
            <div class="section-title">
            📈 Análisis de calificaciones
            </div>
            """, unsafe_allow_html=True)


            col1, col2 = st.columns(2)


            with col1:

                st.write("### Distribución de estados")

                datos_estado = df[
                    "Estado"
                ].value_counts()

                st.bar_chart(datos_estado)


            with col2:

                st.write("### Distribución de notas")

                histograma = pd.cut(
                    df["Nota"],
                    bins=[
                        0,
                        2,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10
                    ],
                    include_lowest=True
                ).value_counts().sort_index()

                st.bar_chart(histograma)


            # ============================================
            # INFORMACIÓN DEL PDF
            # ============================================

            with st.expander("📄 Ver texto extraído del PDF"):

                st.text_area(
                    "Texto",
                    texto,
                    height=300
                )


        else:

            st.warning(
                "⚠️ No pude identificar registros de estudiantes "
                "y notas en este PDF."
            )

            st.info(
                "El formato del colector puede ser diferente. "
                "Si compartes el PDF, puedo adaptar el extractor "
                "a sus columnas reales."
            )


# ============================================================
# SIN ARCHIVO
# ============================================================

else:

    st.markdown("""
    <div class="info-box">

        <strong>👋 Bienvenido al Filtro de Notas UGB</strong>

        <br><br>

        Carga un colector de notas en formato PDF para comenzar.

        <br><br>

        El sistema puede ayudarte a:

        <br>
        📄 Leer el PDF
        <br>
        🔎 Filtrar estudiantes
        <br>
        📊 Analizar calificaciones
        <br>
        ⚠️ Detectar estudiantes en riesgo
        <br>
        🧮 Calcular cuánto necesitan para aprobar
        <br>
        ⬇️ Exportar resultados

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    🎓 Educación Virtual · UGB

    <br>

    Sistema de análisis de calificaciones académicas

</div>
""", unsafe_allow_html=True)