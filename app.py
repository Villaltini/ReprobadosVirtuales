import streamlit as st
import re
import pandas as pd
from pypdf import PdfReader
import io

# Configuración de la página web
st.set_page_config(page_title="Filtro de Notas UGB", page_icon="📚", layout="centered")

st.title("🎓 Lector y Filtro de Colector UGB")
st.write("Arrastra o selecciona tu archivo PDF de notas para extraer automáticamente la información y filtrar las notas de **5.0 a 5.9**.")
st.title("🎓 Educación Virtual")


# Componente para arrastrar y soltar el PDF
archivo_pdf = st.file_uploader("Sube tu colector de notas (PDF)", type=["pdf"])

if archivo_pdf is not None:
    try:
        # Leer el PDF directamente desde la memoria
        lector = PdfReader(archivo_pdf)
        
        materia = "Materia no especificada"
        docente = "Docente no especificado"
        
        # Extraer Materia y Docente del encabezado
        for i in range(min(2, len(lector.pages))):
            texto = lector.pages[i].extract_text()
            if not texto:
                continue
            for linea in texto.split('\n'):
                linea_limpia = linea.strip()
                if "catedr" in linea_limpia.lower() or "docente" in linea_limpia.lower():
                    if ":" in linea_limpia:
                        partes = linea_limpia.split(":", 1)
                        if len(partes) > 1 and len(partes[1].strip()) > 2:
                            docente = partes[1].strip()
                if "materia" in linea_limpia.lower() or "asignatura" in linea_limpia.lower():
                    if ":" in linea_limpia:
                        partes = linea_limpia.split(":", 1)
                        if len(partes) > 1 and len(partes[1].strip()) > 2:
                            materia = partes[1].strip()

        estudiantes = []
        for num_pagina, pagina in enumerate(lector.pages, start=1):
            texto = pagina.extract_text()
            if not texto:
                continue

            for linea in texto.split('\n'):
                match_carnet = re.search(r'\b([A-Z]{2,4}\d{6})\b', linea, re.IGNORECASE)
                if match_carnet:
                    carnet = match_carnet.group(1).upper()
                    numeros = re.findall(r'\b(10(?:\.0{1,2})?|[0-9](?:\.\d{1,2})?)\b', linea)
                    grados = [float(n) for n in numeros if 0.0 <= float(n) <= 10.0]

                    if grados:
                        nota_final = grados[-1]
                        if not (5.0 <= nota_final <= 5.9):
                            continue

                        nombre_limpio = re.sub(r'\b([A-Z]{2,4}\d{6})\b', '', linea)
                        for g in numeros:
                            nombre_limpio = nombre_limpio.replace(g, '')
                        
                        nombre_limpio = re.sub(r'^\d+\s*', '', nombre_limpio)
                        nombre_limpio = re.sub(r'CARNET|NOMBRE|APELLIDO|ESTUDIANTE|N\.F\.|P\.F\.|TOTAL|ACUMULADO', '', nombre_limpio, flags=re.IGNORECASE)
                        nombre_limpio = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', ' ', nombre_limpio)
                        nombre_limpio = " ".join(nombre_limpio.split()).strip()

                        estudiantes.append({
                            'Materia': materia,
                            'Docente': docente,
                            'Carnet': carnet,
                            'Nombre': nombre_limpio if nombre_limpio else "Estudiante",
                            'Nota Final': nota_final
                        })

        df = pd.DataFrame(estudiantes)
        if not df.empty:
            df = df.drop_duplicates(subset=['Carnet'])
            
            st.success(f"¡Procesado con éxito! Se encontraron {len(df)} estudiantes en el rango.")
            st.info(f"📚 **Materia:** {materia}\n\n👨‍🏫 **Docente:** {docente}")
            
            # Mostrar vista previa en la web
            st.dataframe(df)

            # Botón para descargar el Excel generado
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            excel_data = output.getvalue()

            st.download_button(
                label="📥 Descargar Reporte Excel",
                data=excel_data,
                file_name="reprobados_5.0_a_5.9.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No se encontraron estudiantes con Nota Final entre 5.0 y 5.9 en este documento.")

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {str(e)}")