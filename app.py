import streamlit as st
import re
import pandas as pd
from pypdf import PdfReader
import io
import html


# ============================================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Filtro de Notas UGB",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

/* ==============================
   FONDO GENERAL
   ============================== */

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


/* ==============================
   OCULTAR STREAMLIT
   ============================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* ==============================
   TITULO
   ============================== */

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
    margin-bottom: 10px;
}


.brand {
    text-align: center;
    font-size: 14px;
    font-weight: 700;
    color: #7c3aed;
    margin-bottom: 30px;
}


/* ==============================
   CAJA DE CARGA
   ============================== */

.upload-card {
    max-width: 850px;
    margin: 0 auto 20px auto;
    padding: 28px;

    border-radius: 24px;

    background: rgba(255,255,255,0.80);

    border: 1px solid rgba(255,255,255,0.9);

    box-shadow:
        0 20px 50px rgba(31,41,55,0.08),
        0 5px 15px rgba(31,41,55,0.05);

    backdrop-filter: blur(15px);
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


/* ==============================
   UPLOADER
   ============================== */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.75);
    border-radius: 18px;
    padding: 10px;
    border: 2px dashed #8b5cf6;
}


/* ==============================
   CARDS PRINCIPALES
   ============================== */

.cards-container {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 20px;
    margin-top: 30px;
    margin-bottom: 35px;
}


.premium-card {
    min-height: 220px;
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
        0 5px 15px rgba(0,0,0,0.08);

    transition: all .3s ease;
}


.premium-card:hover {
    transform: translateY(-8px);

    box-shadow:
        0 30px 55px rgba(91,33,182,0.35);
}


.card-number {
    position: absolute;
    top: 18px;
    right: 18px;

    width: 38px;
    height: 38px;

    border-radius: 50%;

    border: 1px solid rgba(255,255,255,0.40);

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 12px;

    background: rgba(255,255,255,0.08);
}


.card-icon {
    width: 45px;
    height: 45px;

    border-radius: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 22px;

    margin-bottom: 18px;

    background: rgba(255,255,255,0.10);
}


.card-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    opacity: .85;
    margin-bottom: 6px;
}


.card-title {
    font-size: 20px;
    line-height: 1.15;
    font-weight: 800;
    margin-bottom: 12px;
    word-break: break-word;
}


.card-line {
    width: 42px;
    height: 3px;

    border-radius: 10px;

    background: white;

    margin-bottom: 12px;
}


.card-description {
    font-size: 12px;
    line-height: 1.5;
    opacity: .90;
}


/* ==============================
   RESULTADOS
   ============================== */

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


/* ==============================
   TARJETAS DE ESTUDIANTES
   ============================== */

.students-container {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));

    gap: 20px;

    margin-top: 25px;
    margin-bottom: 35px;
}


.student-card {
    position: relative;

    overflow: hidden;

    min-height: 235px;

    padding: 24px;

    border-radius: 22px;

    color: white;

    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(255,255,255,.18),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed,
            #6d28d9
        );

    box-shadow:
        0 18px 40px rgba(79,70,229,.20),
        0 5px 15px rgba(0,0,0,.08);

    transition: all .3s ease;
}


.student-card:hover {
    transform: translateY(-8px) scale(1.01);

    box-shadow:
        0 30px 55px rgba(79,70,229,.30);
}


.student-number {
    position: absolute;

    top: 16px;
    left: 18px;

    width: 38px;
    height: 38px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background: rgba(255,255,255,.12);

    border: 1px solid rgba(255,255,255,.30);

    font-size: 12px;

    font-weight: 700;
}


.student-grade {
    position: absolute;

    top: 16px;
    right: 18px;

    padding: 8px 14px;

    border-radius: 30px;

    background: rgba(255,255,255,.16);

    border: 1px solid rgba(255,255,255,.30);

    font-size: 18px;

    font-weight: 800;
}


.student-icon {
    margin-top: 45px;

    font-size: 30px;

    margin-bottom: 8px;
}


.student-label {
    font-size: 10px;

    letter-spacing: 1.5px;

    font-weight: 700;

    opacity: .75;

    margin-bottom: 5px;
}


.student-code {
    font-size: 16px;

    font-weight: 700;

    margin-bottom: 8px;

    letter-spacing: .5px;
}


.student-name {
    font-size: 18px;

    line-height: 1.2;

    font-weight: 800;

    word-break: break-word;

    margin-bottom: 15px;
}


.student-line {
    width: 40px;

    height: 3px;

    border-radius: 10px;

    background: white;

    margin-bottom: 10px;
}


.student-note-label {
    font-size: 10px;

    opacity: .75;

    letter-spacing: 1px;
}


/* ==============================
   TABLA
   ============================== */

[data-testid="stDataFrame"] {
    border-radius: 15px;

    overflow: hidden;

    box-shadow:
        0 10px 30px rgba(0,0,0,.05);
}


/* ==============================
   BOTON EXCEL
   ============================== */

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
}


.stDownloadButton > button:hover {
    transform: translateY(-3px);
}


/* ==============================
   RESPONSIVE
   ============================== */

@media (max-width: 1200px) {

    .cards-container {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .students-container {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

}


@media (max-width: 700px) {

    .main-title {
        font-size: 30px;
    }

    .cards-container {
        grid-template-columns: 1fr;
    }

    .students-container {
        grid-template-columns: 1fr;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# ENCABEZADO
# ============================================================

st.html("""
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
""")


# ============================================================
# CARGAR PDF
# ============================================================

st.markdown(
    "### 📄 Cargar colector de notas"
)

st.caption(
    "Arrastra tu archivo PDF o selecciónalo desde tu computadora."
)

archivo_pdf = st.file_uploader(
    "Selecciona el archivo PDF",
    type=["pdf"]
)


# ============================================================
# PROCESAR PDF
# ============================================================

if archivo_pdf is not None:

    try:

        lector = PdfReader(archivo_pdf)

        materia = "Materia no especificada"
        docente = "Docente no especificado"
        ciclo = ""
        regional = ""

        estudiantes = []


        # ====================================================
        # LEER ENCABEZADO
        # ====================================================

        for pagina in lector.pages[:2]:

            texto = pagina.extract_text()

            if not texto:
                continue

            for linea in texto.splitlines():

                linea_limpia = linea.strip()
                linea_lower = linea_limpia.lower()


                # =================================================
                # MATERIA
                # =================================================

                if (
                    "materia" in linea_lower
                    or "asignatura" in linea_lower
                ):

                    if ":" in linea_limpia:

                        partes = linea_limpia.split(
                            ":",
                            1
                        )

                        if len(partes) > 1:

                            valor = partes[1].strip()

                            if len(valor) > 2:
                                materia = valor


                # =================================================
                # DOCENTE
                # =================================================

                if (
                    "docente" in linea_lower
                    or "catedr" in linea_lower
                ):

                    if ":" in linea_limpia:

                        partes = linea_limpia.split(
                            ":",
                            1
                        )

                        if len(partes) > 1:

                            valor = partes[1].strip()

                            if len(valor) > 2:
                                docente = valor


                # =================================================
                # CICLO
                # =================================================

                match = re.search(
                    r"ciclo\s*:\s*(.+)",
                    linea_limpia,
                    re.IGNORECASE
                )

                if match:

                    ciclo = match.group(1).strip()


                # =================================================
                # REGIONAL
                # =================================================

                match = re.search(
                    r"regional\s*:\s*(.+)",
                    linea_limpia,
                    re.IGNORECASE
                )

                if match:

                    regional = match.group(1).strip()


        # =========================================================
        # LIMPIAR MATERIA
        # =========================================================

        match = re.search(
            r"(.*?)\s+Ciclo\s*:\s*(.+)",
            materia,
            re.IGNORECASE
        )

        if match:

            materia = match.group(1).strip()

            if not ciclo:
                ciclo = match.group(2).strip()


        # =========================================================
        # LIMPIAR DOCENTE
        # =========================================================

        match = re.search(
            r"(.*?)\s+Regional\s*:\s*(.+)",
            docente,
            re.IGNORECASE
        )

        if match:

            docente = match.group(1).strip()

            if not regional:
                regional = match.group(2).strip()


        # =========================================================
        # BUSCAR ESTUDIANTES
        # =========================================================

        for pagina in lector.pages:

            texto = pagina.extract_text()

            if not texto:
                continue


            for linea in texto.splitlines():

                # =================================================
                # BUSCAR CARNET
                # =================================================

                match_carnet = re.search(
                    r"\b([A-Z]{2,4}\d{6})\b",
                    linea,
                    re.IGNORECASE
                )

                if not match_carnet:
                    continue


                carnet = match_carnet.group(1).upper()


                # =================================================
                # BUSCAR NOTAS
                # =================================================

                numeros = re.findall(
                    r"\b(10(?:\.0{1,2})?|[0-9](?:\.\d{1,2})?)\b",
                    linea
                )


                notas = []

                for numero in numeros:

                    try:

                        valor = float(numero)

                        if 0 <= valor <= 10:
                            notas.append(valor)

                    except:

                        pass


                if not notas:
                    continue


                # =================================================
                # ÚLTIMA NOTA = NOTA FINAL
                # =================================================

                nota_final = notas[-1]


                # =================================================
                # FILTRAR 5.0 - 5.9
                # =================================================

                if not 5.0 <= nota_final <= 5.9:
                    continue


                # =================================================
                # EXTRAER NOMBRE
                # =================================================

                nombre = re.sub(
                    r"\b([A-Z]{2,4}\d{6})\b",
                    "",
                    linea,
                    flags=re.IGNORECASE
                )


                # =================================================
                # QUITAR NÚMEROS
                # =================================================

                for numero in numeros:

                    nombre = nombre.replace(
                        numero,
                        ""
                    )


                # =================================================
                # QUITAR NÚMERO INICIAL
                # =================================================

                nombre = re.sub(
                    r"^\d+\s*",
                    "",
                    nombre
                )


                # =================================================
                # QUITAR ENCABEZADOS
                # =================================================

                nombre = re.sub(
                    r"CARNET|NOMBRE|APELLIDO|ESTUDIANTE|N\.F\.|P\.F\.|TOTAL|ACUMULADO",
                    "",
                    nombre,
                    flags=re.IGNORECASE
                )


                # =================================================
                # QUITAR CARACTERES EXTRAÑOS
                # =================================================

                nombre = re.sub(
                    r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]",
                    " ",
                    nombre
                )


                # =================================================
                # LIMPIAR ESPACIOS
                # =================================================

                nombre = " ".join(
                    nombre.split()
                ).strip()


                if not nombre:

                    nombre = "Estudiante"


                estudiantes.append({
                    "Materia": materia,
                    "Docente": docente,
                    "Carnet": carnet,
                    "Nombre": nombre,
                    "Nota Final": nota_final
                })


        # =========================================================
        # CREAR DATAFRAME
        # =========================================================

        df = pd.DataFrame(estudiantes)


        # =========================================================
        # RESULTADOS
        # =========================================================

        if df.empty:

            st.warning(
                "⚠️ No se encontraron estudiantes "
                "con Nota Final entre 5.0 y 5.9."
            )

        else:

            # =====================================================
            # QUITAR DUPLICADOS
            # =====================================================

            df = df.drop_duplicates(
                subset=["Carnet"]
            )


            # =====================================================
            # ESTADÍSTICAS
            # =====================================================

            cantidad = len(df)

            promedio = df["Nota Final"].mean()

            nota_minima = df["Nota Final"].min()

            nota_maxima = df["Nota Final"].max()


            # =====================================================
            # MENSAJE
            # =====================================================

            st.success(
                f"✅ Procesado con éxito. "
                f"Se encontraron {cantidad} estudiantes."
            )


            # =====================================================
            # PROTEGER HTML
            # =====================================================

            materia_html = html.escape(
                str(materia)
            )

            docente_html = html.escape(
                str(docente)
            )


            # =====================================================
            # CARDS PRINCIPALES
            # =====================================================

            cards_html = f"""
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
            encontradas.
        </div>

    </div>

</div>
"""


            # =====================================================
            # RENDERIZAR HTML DIRECTAMENTE
            # =====================================================

            st.html(cards_html)


            # =====================================================
            # CICLO Y REGIONAL
            # =====================================================

            if ciclo or regional:

                info = ""

                if ciclo:

                    info += (
                        f"📅 <strong>Ciclo:</strong> "
                        f"{html.escape(ciclo)}"
                    )

                if ciclo and regional:

                    info += " &nbsp; | &nbsp; "

                if regional:

                    info += (
                        f"📍 <strong>Regional:</strong> "
                        f"{html.escape(regional)}"
                    )


                st.html(
                    f"""
                    <div style="
                        text-align:center;
                        margin:10px 0 25px 0;
                        color:#6b7280;
                    ">
                        {info}
                    </div>
                    """
                )


            # =====================================================
            # TITULO
            # =====================================================

            st.html("""
                <div class="results-title">
                    📋 Estudiantes encontrados
                </div>
            """)


            # =====================================================
            # SUBTITULO
            # =====================================================

            st.html(
                f"""
                <div class="results-subtitle">
                    Se encontraron
                    <strong>{cantidad}</strong>
                    estudiantes con notas entre
                    <strong>5.0</strong>
                    y
                    <strong>5.9</strong>.
                </div>
                """
            )


            # =====================================================
            # TARJETAS DE ESTUDIANTES
            # =====================================================

            students_html = """
<div class="students-container">
"""


            for posicion, (_, estudiante) in enumerate(
                df.iterrows(),
                start=1
            ):

                carnet = html.escape(
                    str(estudiante["Carnet"])
                )

                nombre = html.escape(
                    str(estudiante["Nombre"])
                )

                nota = float(
                    estudiante["Nota Final"]
                )


                students_html += f"""
    <div class="student-card">

        <div class="student-number">
            {posicion:02d}
        </div>

        <div class="student-grade">
            {nota:.1f}
        </div>

        <div class="student-icon">
            🎓
        </div>

        <div class="student-label">
            CARNET
        </div>

        <div class="student-code">
            {carnet}
        </div>

        <div class="student-name">
            {nombre}
        </div>

        <div class="student-line"></div>

        <div class="student-note-label">
            NOTA FINAL
        </div>

    </div>
"""


            students_html += """
</div>
"""


            # =====================================================
            # RENDERIZAR TARJETAS DIRECTAMENTE
            # =====================================================

            st.html(students_html)


            # =====================================================
            # TABLA
            # =====================================================

            st.html("""
                <div class="results-title">
                    📊 Tabla detallada
                </div>
            """)


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


            # =====================================================
            # EXCEL
            # =====================================================

            output = io.BytesIO()


            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Estudiantes"
                )


            excel_data = output.getvalue()


            # =====================================================
            # DESCARGAR
            # =====================================================

            st.download_button(
                label="📥 Descargar Reporte Excel",

                data=excel_data,

                file_name="estudiantes_5.0_a_5.9.xlsx",

                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )


    # ========================================================
    # MOSTRAR ERROR REAL
    # ========================================================

    except Exception as e:

        st.error(
            "❌ Ocurrió un error al procesar el PDF."
        )

        st.exception(e)