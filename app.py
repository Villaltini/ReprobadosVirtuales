import streamlit as st
import re
import pandas as pd
from pypdf import PdfReader
import io

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

/* ==========================================================
   FONDO GENERAL
   ========================================================== */

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

/* Ocultar menú y footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* ==========================================================
   TITULO PRINCIPAL
   ========================================================== */

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 5px;

    background: linear-gradient(
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
    margin-bottom: 35px;
}

.brand {
    text-align: center;
    font-size: 14px;
    font-weight: 600;
    color: #7c3aed;
    margin-bottom: 25px;
}

/* ==========================================================
   TARJETA PRINCIPAL DE CARGA
   ========================================================== */

.upload-card {
    max-width: 850px;
    margin: auto;

    padding: 35px;

    border-radius: 24px;

    background: rgba(255,255,255,0.75);

    border: 1px solid rgba(255,255,255,0.8);

    box-shadow:
        0 20px 50px rgba(31, 41, 55, 0.08),
        0 5px 15px rgba(31, 41, 55, 0.05);

    backdrop-filter: blur(15px);

    margin-bottom: 35px;
}

/* ==========================================================
   CONTENEDOR DE TARJETAS
   ========================================================== */

.cards-container {
    display: flex;
    gap: 22px;
    justify-content: center;
    flex-wrap: wrap;

    margin-top: 30px;
    margin-bottom: 35px;
}

/* ==========================================================
   PREMIUM CARD
   ========================================================== */

.premium-card {

    width: 260px;
    min-height: 205px;

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
        0 20px 40px rgba(91, 33, 182, 0.28),
        0 5px 15px rgba(0,0,0,0.08),

        inset 0 1px 1px rgba(255,255,255,0.3);

    transition:
        transform 0.35s ease,
        box-shadow 0.35s ease;
}

/* ==========================================================
   HOVER
   ========================================================== */

.premium-card:hover {

    transform:
        translateY(-12px)
        rotateX(3deg)
        rotateY(-3deg);

    box-shadow:
        0 35px 60px rgba(91,33,182,0.38),
        0 10px 25px rgba(0,0,0,0.15);
}

/* ==========================================================
   BRILLO SUPERIOR
   ========================================================== */

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

    filter: blur(5px);
}

/* ==========================================================
   BRILLO INFERIOR
   ========================================================== */

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

    filter: blur(15px);
}

/* ==========================================================
   ICONO
   ========================================================== */

.card-icon {

    width: 45px;
    height: 45px;

    border-radius: 12px;

    border: 1px solid rgba(255,255,255,0.45);

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 22px;

    margin-bottom: 20px;

    background:
        rgba(255,255,255,0.08);
}

/* ==========================================================
   ETIQUETA
   ========================================================== */

.card-label {

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1.2px;

    opacity: 0.85;

    margin-bottom: 5px;
}

/* ==========================================================
   TITULO CARD
   ========================================================== */

.card-title {

    font-size: 21px;

    line-height: 1.15;

    font-weight: 800;

    margin-bottom: 12px;
}

/* ==========================================================
   LINEA
   ========================================================== */

.card-line {

    width: 42px;
    height: 3px;

    border-radius: 10px;

    background: white;

    margin-bottom: 12px;
}

/* ==========================================================
   DESCRIPCIÓN
   ========================================================== */

.card-description {

    font-size: 12px;

    line-height: 1.5;

    opacity: 0.9;
}

/* ==========================================================
   NUMERO
   ========================================================== */

.card-number {

    position: absolute;

    top: 18px;
    right: 18px;

    width: 38px;
    height: 38px;

    border-radius: 50%;

    border: 1px solid rgba(255,255,255,0.4);

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 12px;

    background:
        rgba(255,255,255,0.06);
}

/* ==========================================================
   SECCION DE RESULTADOS
   ========================================================== */

.results-title {

    font-size: 27px;

    font-weight: 800;

    color: #111827;

    margin-top: 35px;

    margin-bottom: 15px;
}

/* ==========================================================
   TABLA
   ========================================================== */

.dataframe {

    border-radius: 15px !important;

    overflow: hidden !important;
}

/* ==========================================================
   BOTON EXCEL
   ========================================================== */

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

    transition: all .3s ease;
}

.stDownloadButton > button:hover {

    transform: translateY(-3px);

    box-shadow:
        0 15px 30px rgba(79,70,229,0.35);
}

/* ==========================================================
   FILE UPLOADER
   ========================================================== */

[data-testid="stFileUploader"] {

    background: rgba(255,255,255,0.65);

    border-radius: 18px;

    padding: 10px;

    border: 2px dashed #8b5cf6;
}

/* ==========================================================
   MENSAJES
   ========================================================== */

div[data-testid="stAlert"] {

    border-radius: 14px;
}

/* ==========================================================
   RESPONSIVE
   ========================================================== */

@media (max-width: 768px) {

    .main-title {
        font-size: 30px;
    }

    .premium-card {
        width: 100%;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<div class="main-title">🎓 Lector y Filtro de Colector UGB</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Carga tu colector de notas en PDF y obtén automáticamente '
    'los estudiantes que se encuentran entre 5.0 y 5.9.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="brand">🎓 EDUCACIÓN VIRTUAL · UGB</div>',
    unsafe_allow_html=True
)


# ============================================================
# TARJETA DE CARGA
# ============================================================

st.markdown("""
<div class="upload-card">

<h3 style="text-align:center; color:#374151;">
📄 Cargar colector de notas
</h3>

<p style="text-align:center; color:#6b7280;">
Arrastra tu archivo PDF o selecciónalo desde tu computadora.
</p>

</div>
""", unsafe_allow_html=True)


archivo_pdf = st.file_uploader(
    "Sube tu colector de notas (PDF)",
    type=["pdf"],
    label_visibility="collapsed"
)


# ============================================================
# PROCESAMIENTO
# ============================================================

if archivo_pdf is not None:

    try:

        lector = PdfReader(archivo_pdf)

        materia = "Materia no especificada"
        docente = "Docente no especificado"

        # ====================================================
        # EXTRAER MATERIA Y DOCENTE
        # ====================================================

        for i in range(min(2, len(lector.pages))):

            texto = lector.pages[i].extract_text()

            if not texto:
                continue

            for linea in texto.split('\n'):

                linea_limpia = linea.strip()

                if (
                    "catedr" in linea_limpia.lower()
                    or "docente" in linea_limpia.lower()
                ):

                    if ":" in linea_limpia:

                        partes = linea_limpia.split(":", 1)

                        if (
                            len(partes) > 1
                            and len(partes[1].strip()) > 2
                        ):

                            docente = partes[1].strip()

                if (
                    "materia" in linea_limpia.lower()
                    or "asignatura" in linea_limpia.lower()
                ):

                    if ":" in linea_limpia:

                        partes = linea_limpia.split(":", 1)

                        if (
                            len(partes) > 1
                            and len(partes[1].strip()) > 2
                        ):

                            materia = partes[1].strip()


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

            for linea in texto.split('\n'):

                match_carnet = re.search(
                    r'\b([A-Z]{2,4}\d{6})\b',
                    linea,
                    re.IGNORECASE
                )

                if match_carnet:

                    carnet = match_carnet.group(1).upper()

                    numeros = re.findall(
                        r'\b(10(?:\.0{1,2})?|[0-9](?:\.\d{1,2})?)\b',
                        linea
                    )

                    grados = [
                        float(n)
                        for n in numeros
                        if 0.0 <= float(n) <= 10.0
                    ]

                    if grados:

                        nota_final = grados[-1]

                        if not (
                            5.0 <= nota_final <= 5.9
                        ):
                            continue

                        nombre_limpio = re.sub(
                            r'\b([A-Z]{2,4}\d{6})\b',
                            '',
                            linea
                        )

                        for g in numeros:
                            nombre_limpio = nombre_limpio.replace(
                                g,
                                ''
                            )

                        nombre_limpio = re.sub(
                            r'^\d+\s*',
                            '',
                            nombre_limpio
                        )

                        nombre_limpio = re.sub(
                            r'CARNET|NOMBRE|APELLIDO|ESTUDIANTE|N\.F\.|P\.F\.|TOTAL|ACUMULADO',
                            '',
                            nombre_limpio,
                            flags=re.IGNORECASE
                        )

                        nombre_limpio = re.sub(
                            r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]',
                            ' ',
                            nombre_limpio
                        )

                        nombre_limpio = " ".join(
                            nombre_limpio.split()
                        ).strip()

                        estudiantes.append({

                            'Materia': materia,

                            'Docente': docente,

                            'Carnet': carnet,

                            'Nombre':
                                nombre_limpio
                                if nombre_limpio
                                else "Estudiante",

                            'Nota Final':
                                nota_final
                        })


        # ====================================================
        # DATAFRAME
        # ====================================================

        df = pd.DataFrame(estudiantes)


        if not df.empty:

            df = df.drop_duplicates(
                subset=['Carnet']
            )


            # =================================================
            # MENSAJE DE ÉXITO
            # =================================================

            st.success(
                f"¡Procesado con éxito! "
                f"Se encontraron {len(df)} estudiantes en el rango."
            )


            # =================================================
            # PREMIUM CARDS
            # =================================================

            promedio = df["Nota Final"].mean()

            nota_minima = df["Nota Final"].min()

            nota_maxima = df["Nota Final"].max()

            cantidad = len(df)


            st.markdown(f"""

            <div class="cards-container">

                <!-- CARD MATERIA -->

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
                        {materia}
                    </div>

                    <div class="card-line"></div>

                    <div class="card-description">
                        Materia encontrada automáticamente
                        en el colector.
                    </div>

                </div>


                <!-- CARD DOCENTE -->

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
                        {docente}
                    </div>

                    <div class="card-line"></div>

                    <div class="card-description">
                        Docente identificado desde
                        el encabezado del PDF.
                    </div>

                </div>


                <!-- CARD ESTUDIANTES -->

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


                <!-- CARD PROMEDIO -->

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

            """, unsafe_allow_html=True)


            # =================================================
            # INFORMACIÓN DEL RANGO
            # =================================================

            st.markdown(
                '<div class="results-title">'
                '📋 Estudiantes encontrados'
                '</div>',
                unsafe_allow_html=True
            )


            st.caption(
                f"Rango de notas: "
                f"{nota_minima:.1f} – {nota_maxima:.1f}"
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
            # EXCEL
            # =================================================

            output = io.BytesIO()

            with pd.ExcelWriter(
                output,
                engine='openpyxl'
            ) as writer:

                df.to_excel(
                    writer,
                    index=False
                )

            excel_data = output.getvalue()


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