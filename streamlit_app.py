# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Importamos las bibliotecas necesarias
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Cargar datos
df_data = pd.read_csv("data.csv")
df_data['Date'] = pd.to_datetime(df_data['Date'])

st.title("📊 Dashboard Interactivo de Ventas y Clientes")
st.markdown("Este dashboard presenta un análisis interactivo de las ventas, ingresos, tipos de clientes y métodos de pago. Usa los filtros para explorar distintas perspectivas del negocio.")

# Filtros interactividad
branches = st.sidebar.multiselect("Seleccionar Sucursal:", df_data['Branch'].unique(), default=df_data['Branch'].unique())
products = st.sidebar.multiselect("Seleccionar Línea de Producto:", df_data['Product line'].unique(), default=df_data['Product line'].unique())
customer_types = st.sidebar.multiselect("Tipo de Cliente:", df_data['Customer type'].unique(), default=df_data['Customer type'].unique())

filtered_df = df_data[
    (df_data['Branch'].isin(branches)) &
    (df_data['Product line'].isin(products)) &
    (df_data['Customer type'].isin(customer_types))
]

# Layout
col1, col2 = st.columns(2)

# Evolución de ventas en el tiempo
with col1:
    st.subheader("🕒 Evolución de las Ventas Totales")
    sales_by_date = filtered_df.groupby('Date')['Total'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(data=sales_by_date, x='Date', y='Total', marker='o', ax=ax)
    ax.set_ylabel("Total de Ventas")
    ax.set_xlabel("Fecha")
    ax.set_title("Ventas Totales por Fecha")
    st.pyplot(fig)

# Ingresos por línea de producto
with col2:
    st.subheader("🌿 Ingresos por Línea de Producto")
    income_by_product = filtered_df.groupby('Product line')['Total'].sum().sort_values().plot(kind='barh', color='skyblue')
    plt.title("Total de Ventas por Línea de Producto")
    st.pyplot(plt.gcf())

# Distribución de la calificación
st.subheader("📈 Distribución de Calificaciones de Clientes")
fig, ax = plt.subplots()
sns.histplot(filtered_df['Rating'], bins=10, kde=True, color='lightgreen', ax=ax)
ax.set_title("Distribución de Rating de Clientes")
ax.set_xlabel("Rating")
st.pyplot(fig)

# Gasto por tipo de cliente
st.subheader("🧳 Comparación del Gasto por Tipo de Cliente")
fig, ax = plt.subplots()
sns.violinplot(x='Customer type', y='Total', data=filtered_df, palette='pastel', ax=ax)
ax.set_title("Distribución del Gasto Total por Tipo de Cliente")
st.pyplot(fig)

# Relación entre Costo y Ganancia
st.subheader("💲 Relación entre Costo y Ganancia Bruta")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x='cogs', y='gross income', hue='Branch', ax=ax)
ax.set_title("COGS vs Ganancia Bruta")
st.pyplot(fig)

# Métodos de pago
st.subheader("💳 Métodos de Pago Preferidos")
payment_counts = filtered_df['Payment'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, figsize=(6,6))
plt.ylabel("")
plt.title("Distribución de Métodos de Pago")
st.pyplot(plt.gcf())

# Ingreso bruto por sucursal y línea de producto
st.subheader("🏪 Ingreso Bruto por Sucursal y Línea de Producto")
gross_by_branch_product = filtered_df.groupby(['Branch', 'Product line'])['gross income'].sum().unstack()
gross_by_branch_product.plot(kind='bar', stacked=True, colormap='viridis')
plt.title("Ingreso Bruto por Sucursal y Producto")
plt.xlabel("Sucursal")
plt.ylabel("Ingreso Bruto")
st.pyplot(plt.gcf())


