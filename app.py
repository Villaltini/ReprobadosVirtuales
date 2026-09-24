import streamlit as st
import re
import pandas as pd
from pypdf import PdfReader
import io
import html


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Filtro de Notas UGB",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS - DISEÑO PREMIUM
# ============================================================

st.markdown("""
<style>

/* ============================================================
   FONDO GENERAL
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(124, 58, 237, 0.08),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(79, 70, 229, 0.08),
            transparent 30%
        ),
        #f6f7fb;
}


/* Ocultar menú */
#MainMenu {
    visibility: hidden;
}

/* Ocultar footer */
footer {
    visibility: hidden;
}

/* Ocultar header */
header {
    visibility: hidden;
}


/* ============================================================
   TITULO
   ============================================================ */

.main-title {
    text-align: center;

    font-size: 42px;

    font-weight: 800;

    margin-top: 20px;

    margin-bottom: 5px;

    background:
        linear-gradient(
            90deg,
            #2563eb,
            #7c3aed,
            #4f46e5
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


.subtitle {
    text-align: center;

    color: #6b7280;

    font-size: 16px;

    margin-bottom: 15px;
}


.brand {
    text-align: center;

    font-size: 14px;

    font-weight: 700;

    color: #7c3aed;

    margin-bottom: 30px;
}


/* ============================================================
   TARJETA DE CARGA
   ============================================================ */

.upload-card {
    max-width: 850px;

    margin: 0 auto 20px auto;

    padding: 28px;

    border-radius: 24px;

    background:
        rgba(255,255,255,0.78);

    border:
        1px solid rgba(255,255,255,0.9);

    box-shadow:
        0 20px 50px rgba(31,41,55,0.08),
        0 5px 15px rgba(31,41,55,0.05);

    backdrop-filter:
        blur(15px);
}


.upload-title {
    text-align: center;

    color: #374151;

    font-size: 20px;

    font-weight: 700;

    margin-bottom: 5px;
}


.upload-text {
    text-align: center;

    color: #6b7280;

    font-size: 14px;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {

    background:
        rgba(255,255,255,0.75);

    border-radius: 18px;

    padding: 10px;

    border:
        2px dashed #8b5cf6;

    transition:
        all .3s ease;
}


[data-testid="stFileUploader"]:hover {

    border-color: #6d28d9;

    box-shadow:
        0 10px 30px rgba(124,58,237,.12);
}


/* ============================================================
   CONTENEDOR DE CARDS
   ============================================================ */

.cards-container {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 20px;

    margin-top: 30px;

    margin-bottom: 35px;
}


/* ============================================================
   PREMIUM CARD
   ============================================================ */

.premium-card {

    min-height: 225px;

    padding: 25px;

    box-sizing: border-box;

    border-radius: 22px;

    position: relative;

    overflow: hidden;

    color: white;

    background:
        radial-gradient(
            circle at 85% 15%,
            rgba(255,255,255,0.20),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #8b5cf6,
            #6d28d9,
            #4f46e5
        );

    box-shadow:
        0 20px 40px rgba(91,33,182,0.28),
        0 5px 15px rgba(0,0,0,0.08),
        inset 0 1px 1px rgba(255,255,255,0.30);

    transition:
        transform .35s ease,
        box-shadow .35s ease;
}


/* ============================================================
   EFECTO HOVER
   ============================================================ */

.premium-card:hover {

    transform:
        translateY(-12px)
        rotateX(3deg)
        rotateY(-3deg);

    box-shadow:
        0 35px 60px rgba(91,33,182,0.40),
        0 10px 25px rgba(0,0,0,0.15),
        inset 0 1px 1px rgba(255,255,255,0.35);
}


/* ============================================================
   BRILLO SUPERIOR
   ============================================================ */

.premium-card::before {

    content: "";

    position: absolute;

    width: 180px;

    height: 180px;

    top: -90px;

    right: -60px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.13);

    filter:
        blur(5px);

    pointer-events: none;
}


/* ============================================================
   BRILLO INFERIOR
   ============================================================ */

.premium-card::after {

    content: "";

    position: absolute;

    width: 140px;

    height: 140px;

    bottom: -80px;

    left: -60px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.08);

    filter:
        blur(15px);

    pointer-events: none;
}


/* ============================================================
   ICONO
   ============================================================ */

.card-icon {

    width: 45px;

    height: 45px;

    border-radius: 12px;

    border:
        1px solid rgba(255,255,255,0.45);

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 22px;

    margin-bottom: 18px;

    background:
        rgba(255,255,255,0.08);

    position: relative;

    z-index: 2;
}


/* ============================================================
   NUMERO
   ============================================================ */

.card-number {

    position: absolute;

    top: 18px;

    right: 18px;

    width: 38px;

    height: 38px;

    border-radius: 50%;

    border:
        1px solid rgba(255,255,255,0.40);

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 12px;

    background:
        rgba(255,255,255,0.06);

    z-index: 3;
}


/* ============================================================
   LABEL
   ============================================================ */

.card-label {

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1.2px;

    opacity: .85;

    margin-bottom: 6px;

    position: relative;

    z-index: 2;
}


/* ============================================================
   TITULO DE CARD
   ============================================================ */

.card-title {

    font-size: 20px;

    line-height: 1.15;

    font-weight: 800;

    margin-bottom: 12px;

    word-break: break-word;

    position: relative;

    z-index: 2;
}


/* ============================================================
   LINEA
   ============================================================ */

.card-line {

    width: 42px;

    height: 3px;

    border-radius: 10px;

    background:
        white;

    margin-bottom: 12px;

    position: relative;

    z-index: 2;
}


/* ============================================================
   DESCRIPCIÓN
   ============================================================ */

.card-description {

    font-size: 12px;

    line-height: 1.5;

    opacity: .90;

    position: relative;

    z-index: 2;
}


/* ============================================================
   TITULO RESULTADOS
   ============================================================ */

.results-title {

    font-size: 28px;

    font-weight: 800;

    color: #111827;

    margin-top: 25px;

    margin-bottom: 5px;
}


.results-subtitle {

    color: #6b7280;

    font-size: 14px;

    margin-bottom: 15px;
}


/* ============================================================
   TABLA
   ============================================================ */

[data-testid="stDataFrame"] {

    border-radius: 15px;

    overflow: hidden;

    box-shadow:
        0 10px 30px rgba(0,0,0,.05);
}


/* ============================================================
   BOTON EXCEL
   ============================================================ */

.stDownloadButton > button {

    width: 100%;

    border-radius: 14px;

    border: none;

    padding: 14px;

    font-weight: 700;

    font-size: 15px;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #4f46e5
        );

    color: white;

    box-shadow:
        0 10px 25px rgba(79,70,229,0.25);

    transition:
        all .3s ease;
}


.stDownloadButton > button:hover {

    transform:
        translateY(-3px);

    box-shadow:
        0 15px 30px rgba(79,70,229,0.35);
}


/* ============================================================
   ALERTAS
   ============================================================ */

div[data-testid="stAlert"] {

    border-radius: 14px;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1100px) {

    .cards-container {

        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }
}


@media (max-width: 700px) {

    .main-title {

        font-size: 30px;
    }

    .cards-container {

        grid-template-columns:
            1fr;
    }

    .premium-card {

        min-height: 200px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🎓 Lector y Filtro de Colector UGB
    </div>

    <div class="subtitle">
        Carga tu colector de notas en PDF y obtén automáticamente
        los estudiantes que se encuentran entre 5.0 y 5.9.
    </div>

    <div class="brand">
        🎓 EDUCACIÓN VIRTUAL · UGB
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# AREA DE CARGA
# ============================================================

st.markdown(
    """
    <div class="upload-card">

        <div class="upload-title">
            📄 Cargar colector de notas
        </div>

        <div class="upload-text">
            Arrastra tu archivo PDF o selecciónalo desde tu computadora.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


archivo_pdf = st.file_uploader(
    "Sube tu colector de notas (PDF)",
    type=["pdf"],
    label_visibility="collapsed"
)


# ============================================================
# PROCESAMIENTO DEL PDF
# ============================================================

if archivo_pdf is not None:

    try:

        # ----------------------------------------------------
        # LEER PDF
        # ----------------------------------------------------

        lector = PdfReader(archivo_pdf)

        materia = "Materia no especificada"

        docente = "Docente no especificado"

        ciclo = ""

        regional = ""


        # ----------------------------------------------------
        # EXTRAER INFORMACIÓN DEL ENCABEZADO
        # ----------------------------------------------------

        for i in range(min(2, len(lector.pages))):

            texto = lector.pages[i].extract_text()

            if not texto:
                continue


            for linea in texto.split("\n"):

                linea_limpia = linea.strip()

                linea_lower = linea_limpia.lower()


                # --------------------------------------------
                # MATERIA
                # --------------------------------------------

                if (
                    "materia" in linea_lower
                    or "asignatura" in linea_lower
                ):

                    if ":" in linea_limpia:

                        partes = linea_limpia.split(
                            ":",
                            1
                        )

                        if (
                            len(partes) > 1
                            and len(partes[1].strip()) > 2
                        ):

                            materia = partes[1].strip()


                # --------------------------------------------
                # DOCENTE
                # --------------------------------------------

                if (
                    "catedr" in linea_lower
                    or "docente" in linea_lower
                ):

                    if ":" in linea_limpia:

                        partes = linea_limpia.split(
                            ":",
                            1
                        )

                        if (
                            len(partes) > 1
                            and len(partes[1].strip()) > 2
                        ):

                            docente = partes[1].strip()


                # --------------------------------------------
                # CICLO
                # --------------------------------------------

                if "ciclo:" in linea_lower:

                    partes = re.split(
                        r"ciclo\s*:",
                        linea_limpia,
                        flags=re.IGNORECASE
                    )

                    if len(partes) > 1:

                        ciclo = partes[1].strip()


                # --------------------------------------------
                # REGIONAL
                # --------------------------------------------

                if "regional:" in linea_lower:

                    partes = re.split(
                        r"regional\s*:",
                        linea_limpia,
                        flags=re.IGNORECASE
                    )

                    if len(partes) > 1:

                        regional = partes[1].strip()


        # ====================================================
        # LIMPIAR INFORMACIÓN
        # ====================================================

        # Si la materia contiene información de ciclo,
        # la separamos.

        match_ciclo = re.search(
            r"(.*?)\s+Ciclo\s*:\s*(.+)",
            materia,
            flags=re.IGNORECASE
        )

        if match_ciclo:

            materia = match_ciclo.group(1).strip()

            if not ciclo:

                ciclo = match_ciclo.group(2).strip()


        # Si el docente contiene Regional,
        # lo separamos.

        match_regional = re.search(
            r"(.*?)\s+Regional\s*:\s*(.+)",
            docente,
            flags=re.IGNORECASE
        )

        if match_regional:

            docente = match_regional.group(1).strip()

            if not regional:

                regional = match_regional.group(2).strip()


        # ====================================================
        # EXTRAER ESTUDIANTES
        # ====================================================

        estudiantes = []


        for num_pagina, pagina in enumerate(
            lector.pages,
            start=1
        ):

            texto = pagina.extract_text()

            if not texto:
                continue


            for linea in texto.split("\n"):

                # --------------------------------------------
                # BUSCAR CARNET
                # --------------------------------------------

                match_carnet = re.search(
                    r"\b([A-Z]{2,4}\d{6})\b",
                    linea,
                    re.IGNORECASE
                )


                if not match_carnet:
                    continue


                carnet = match_carnet.group(1).upper()


                # --------------------------------------------
                # BUSCAR NOTAS
                # --------------------------------------------

                numeros = re.findall(
                    r"\b(10(?:\.0{1,2})?|[0-9](?:\.\d{1,2})?)\b",
                    linea
                )


                grados = [
                    float(n)
                    for n in numeros
                    if 0.0 <= float(n) <= 10.0
                ]


                if not grados:
                    continue


                nota_final = grados[-1]


                # --------------------------------------------
                # FILTRAR 5.0 - 5.9
                # --------------------------------------------

                if not (
                    5.0 <= nota_final <= 5.9
                ):

                    continue


                # --------------------------------------------
                # EXTRAER NOMBRE
                # --------------------------------------------

                nombre_limpio = re.sub(
                    r"\b([A-Z]{2,4}\d{6})\b",
                    "",
                    linea
                )


                for g in numeros:

                    nombre_limpio = (
                        nombre_limpio.replace(
                            g,
                            ""
                        )
                    )


                nombre_limpio = re.sub(
                    r"^\d+\s*",
                    "",
                    nombre_limpio
                )


                nombre_limpio = re.sub(
                    r"CARNET|NOMBRE|APELLIDO|ESTUDIANTE|N\.F\.|P\.F\.|TOTAL|ACUMULADO",
                    "",
                    nombre_limpio,
                    flags=re.IGNORECASE
                )


                nombre_limpio = re.sub(
                    r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]",
                    " ",
                    nombre_limpio
                )


                nombre_limpio = " ".join(
                    nombre_limpio.split()
                ).strip()


                # --------------------------------------------
                # AGREGAR ESTUDIANTE
                # --------------------------------------------

                estudiantes.append(
                    {
                        "Materia": materia,
                        "Docente": docente,
                        "Carnet": carnet,
                        "Nombre":
                            nombre_limpio
                            if nombre_limpio
                            else "Estudiante",
                        "Nota Final": nota_final
                    }
                )


        # ====================================================
        # CREAR DATAFRAME
        # ====================================================

        df = pd.DataFrame(estudiantes)


        if not df.empty:

            # Eliminar duplicados
            df = df.drop_duplicates(
                subset=["Carnet"]
            )


            # =================================================
            # ESTADÍSTICAS
            # =================================================

            promedio = df["Nota Final"].mean()

            nota_minima = df["Nota Final"].min()

            nota_maxima = df["Nota Final"].max()

            cantidad = len(df)


            # =================================================
            # MENSAJE DE ÉXITO
            # =================================================

            st.success(
                f"¡Procesado con éxito! "
                f"Se encontraron {cantidad} estudiantes "
                f"en el rango."
            )


            # =================================================
            # ESCAPAR TEXTO PARA HTML
            # =================================================

            materia_html = html.escape(
                materia
            )

            docente_html = html.escape(
                docente
            )


            # =================================================
            # PREMIUM CARDS
            # =================================================

            st.markdown(
                f"""
                <div class="cards-container">

                    <div class="premium-card">

                        <div class="card-number">
                            01
                        </div>

                        <div class="card-icon">
                            📚
                        </div>

                        <div class="card-label">
                            ASIGNATURA
                        </div>

                        <div class="card-title">
                            {materia_html}
                        </div>

                        <div class="card-line"></div>

                        <div class="card-description">
                            Materia encontrada automáticamente
                            en el colector.
                        </div>

                    </div>


                    <div class="premium-card">

                        <div class="card-number">
                            02
                        </div>

                        <div class="card-icon">
                            👨‍🏫
                        </div>

                        <div class="card-label">
                            DOCENTE
                        </div>

                        <div class="card-title">
                            {docente_html}
                        </div>

                        <div class="card-line"></div>

                        <div class="card-description">
                            Docente identificado desde
                            el encabezado del PDF.
                        </div>

                    </div>


                    <div class="premium-card">

                        <div class="card-number">
                            03
                        </div>

                        <div class="card-icon">
                            👨‍🎓
                        </div>

                        <div class="card-label">
                            ESTUDIANTES
                        </div>

                        <div class="card-title">
                            {cantidad}
                        </div>

                        <div class="card-line"></div>

                        <div class="card-description">
                            Estudiantes encontrados con
                            nota entre 5.0 y 5.9.
                        </div>

                    </div>


                    <div class="premium-card">

                        <div class="card-number">
                            04
                        </div>

                        <div class="card-icon">
                            📊
                        </div>

                        <div class="card-label">
                            PROMEDIO
                        </div>

                        <div class="card-title">
                            {promedio:.2f}
                        </div>

                        <div class="card-line"></div>

                        <div class="card-description">
                            Promedio de las notas
                            encontradas en el rango.
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # INFORMACIÓN ADICIONAL
            # =================================================

            if ciclo or regional:

                informacion_extra = ""

                if ciclo:

                    informacion_extra += (
                        f"📅 **Ciclo:** {ciclo}  "
                    )

                if regional:

                    informacion_extra += (
                        f" | 📍 **Regional:** {regional}"
                    )


                st.markdown(
                    informacion_extra
                )


            # =================================================
            # TITULO RESULTADOS
            # =================================================

            st.markdown(
                """
                <div class="results-title">
                    📋 Estudiantes encontrados
                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="results-subtitle">
                    Rango de notas:
                    <strong>{nota_minima:.1f}</strong>
                    –
                    <strong>{nota_maxima:.1f}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # TABLA
            # =================================================

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


            # =================================================
            # GENERAR EXCEL
            # =================================================

            output = io.BytesIO()


            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                df.to_excel(
                    writer,
                    index=False
                )


            excel_data = output.getvalue()


            # =================================================
            # BOTÓN EXCEL
            # =================================================

            st.markdown(
                "<br>",
                unsafe_allow_html=True
            )


            st.download_button(

                label="📥 Descargar Reporte Excel",

                data=excel_data,

                file_name=
                    "reprobados_5.0_a_5.9.xlsx",

                mime=
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


        else:

            st.warning(
                "No se encontraron estudiantes con "
                "Nota Final entre 5.0 y 5.9 en este documento."
            )


    except Exception as e:

        st.error(
            f"Ocurrió un error al procesar el archivo: {str(e)}"
        )