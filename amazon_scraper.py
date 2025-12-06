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
        url = f"https://www.amazon.com.mx/s?k={producto.replace(' ', '+')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code != 200:
            return None
            
        soup = BeautifulSoup(r.content, 'html.parser')
        productos = []
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in items:
            try:
                nombre_elem = item.find('h2', class_='a-size-mini')
                if not nombre_elem:
                    nombre_elem = item.find('span', class_='a-size-medium')
                if not nombre_elem:
                    nombre_elem = item.find('span', class_='a-size-base-plus')
                if not nombre_elem:
                    nombre_elem = item.find('h2')
                
                precio_elem = item.find('span', class_='a-price-whole')
                
                if nombre_elem and precio_elem:
                    nombre = nombre_elem.get_text(strip=True)[:60]
                    precio_texto = precio_elem.get_text(strip=True).replace(',', '').replace('$', '').replace('.', '')
                    precio = float(precio_texto)
                    
                    productos.append({'nombre': nombre, 'precio': precio})
                    
                    if len(productos) >= 10:
                        break
            except:
                continue
        
        return productos if len(productos) >= 10 else None
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

