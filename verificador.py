import streamlit as st
import pandas as pd
from thefuzz import process, fuzz

st.set_page_config(page_title="Validador Inteligente", page_icon="🧠")
st.title("🧠 Buscador Semántico de Materiales")

@st.cache_data
def cargar_datos():
    # Asegúrate de que este es tu archivo real
    return pd.read_excel('catalogo.xlsx')

df = cargar_datos()
col_desc = 'Texto breve material'
col_cod = 'Material'

input_desc = st.text_input("Escribe el nombre del material (con abreviaciones o palabras desordenadas):")

if input_desc:
    # 1. Obtenemos la lista de descripciones del Excel
    lista_descripciones = df[col_desc].astype(str).tolist()
    
    # 2. Buscamos coincidencias inteligentes
    # token_sort_ratio ignora el orden de las palabras (ej: "tubería 2 pulgada" = "2 pulgada tubería")
    resultados = process.extract(input_desc, lista_descripciones, scorer=fuzz.token_sort_ratio, limit=5)
    
    # 3. Filtramos los que tengan al menos un 50% de similitud (ajustable)
    coincidencias = [res for res in resultados if res[1] >= 50]
    
    if coincidencias:
        st.write(f"✅ He encontrado {len(coincidencias)} materiales que podrían ser lo mismo:")
        
        # Preparamos una tabla para mostrar los resultados
        data_resultado = []
        for desc, score in coincidencias:
            fila = df[df[col_desc] == desc].iloc[0]
            data_resultado.append({
                "Similitud (%)": f"{score}%",
                "Código": fila[col_cod],
                "Descripción en Excel": desc
            })
            
        st.table(pd.DataFrame(data_resultado))
        st.info("⚠️ Si ves tu material aquí, ¡es un posible duplicado!")
    else:
        st.success("✅ No encontré nada parecido. El material parece ser realmente nuevo.")