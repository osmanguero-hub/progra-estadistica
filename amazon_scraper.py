import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import random

datos_ejemplo = [
    {"nombre": "Laptop HP", "precio": 8999},
    {"nombre": "Mouse", "precio": 1599},
    {"nombre": "Teclado", "precio": 2499},
    {"nombre": "Monitor", "precio": 3299},
    {"nombre": "Audifonos", "precio": 5499},
    {"nombre": "Webcam", "precio": 1399},
    {"nombre": "SSD", "precio": 1899},
    {"nombre": "Mouse pad", "precio": 299},
    {"nombre": "Hub USB", "precio": 799},
    {"nombre": "Microfono", "precio": 2899},
]

def buscar_amazon(producto):
    try:
        url = f"https://www.amazon.com.mx/s?k={producto}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        productos = []
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in items[:10]:
            n = item.find('h2')
            p = item.find('span', class_='a-price-whole')
            if n and p:
                productos.append({
                    'nombre': n.get_text(strip=True)[:50],
                    'precio': float(p.get_text().replace(',', '').replace('$', ''))
                })
        
        if len(productos) >= 10:
            return productos
        else:
            return None
    except:
        return None

st.title("Buscador Amazon")

producto = st.text_input("Producto:")
if st.button("Buscar"):
    datos = buscar_amazon(producto)
    
    if not datos:
        st.warning("No funciono. Usando datos de ejemplo.")
        datos = [{"nombre": d['nombre'], "precio": d['precio'] + random.randint(-200, 200)} for d in datos_ejemplo]
    
    df = pd.DataFrame(datos)
    
    st.subheader("Precios")
    fig = px.bar(df, x='nombre', y='precio', color='precio')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)
    
    st.subheader("Filtrar ofertas")
    umbral = st.slider("Precio maximo:", float(df['precio'].min()), float(df['precio'].max()), float(df['precio'].mean()))
    
    ofertas = df[df['precio'] <= umbral].sort_values('precio')
    st.write(f"{len(ofertas)} productos debajo de ${umbral:.0f}")
    st.dataframe(ofertas, hide_index=True)

