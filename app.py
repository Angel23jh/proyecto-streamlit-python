import streamlit as st
import pandas as pd
import numpy as np

from libreria_funciones_proyecto1 import calcular_ticket_promedio
from libreria_clases_proyecto1 import InventarioProducto


# =====================================================
# CONFIGURACION GENERAL
# =====================================================

st.set_page_config(
    page_title="Proyecto Python Fundamentals",
    page_icon="📊",
    layout="wide"
)


# =====================================================
# INICIALIZAR VARIABLES DE SESSION
# =====================================================

if "movimientos" not in st.session_state:
    st.session_state.movimientos = []

if "ventas" not in st.session_state:
    st.session_state.ventas = []

if "historico_funcion" not in st.session_state:
    st.session_state.historico_funcion = []

if "inventario" not in st.session_state:
    st.session_state.inventario = []


# =====================================================
# MENU LATERAL
# =====================================================

st.sidebar.title("Menú principal")

opcion = st.sidebar.selectbox(
    "Seleccione una sección",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)


# =====================================================
# HOME
# =====================================================

if opcion == "Home":
    st.title("Proyecto Aplicado en Streamlit")
    st.subheader("Módulo 1 - Python Fundamentals")

    st.write("Miguel Angel Jimenez Huamani")
    st.write("75447465")

# =====================================================
# EJERCICIO 1 - FLUJO DE CAJA CON LISTAS
# =====================================================

elif opcion == "Ejercicio 1":
    st.title("Ejercicio 1 - Flujo de caja con listas")

    st.markdown("""
    En este ejercicio se registran movimientos de caja utilizando una lista.
    Cada movimiento puede ser un ingreso o un gasto.
    """)

    concepto = st.text_input("Concepto del movimiento")
    tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
    valor = st.number_input("Valor", min_value=0.0, step=10.0)

    if st.button("Agregar movimiento"):
        if concepto != "" and valor > 0:
            movimiento = {
                "Concepto": concepto,
                "Tipo": tipo,
                "Valor": valor
            }

            st.session_state.movimientos.append(movimiento)
            st.success("Movimiento agregado correctamente.")
        else:
            st.error("Debe ingresar un concepto y un valor mayor a cero.")

    if len(st.session_state.movimientos) > 0:
        df_movimientos = pd.DataFrame(st.session_state.movimientos)
        st.dataframe(df_movimientos)

        total_ingresos = df_movimientos[df_movimientos["Tipo"] == "Ingreso"]["Valor"].sum()
        total_gastos = df_movimientos[df_movimientos["Tipo"] == "Gasto"]["Valor"].sum()
        saldo_final = total_ingresos - total_gastos

        col1, col2, col3 = st.columns(3)

        col1.metric("Total ingresos", f"S/ {total_ingresos:.2f}")
        col2.metric("Total gastos", f"S/ {total_gastos:.2f}")
        col3.metric("Saldo final", f"S/ {saldo_final:.2f}")

        if saldo_final >= 0:
            st.success("El flujo de caja está a favor.")
        else:
            st.error("El flujo de caja está en contra.")
    else:
        st.info("Aún no se han registrado movimientos.")


# =====================================================
# EJERCICIO 2 - REGISTRO CON NUMPY Y DATAFRAME
# =====================================================

elif opcion == "Ejercicio 2":
    st.title("Ejercicio 2 - Registro de ventas con NumPy y DataFrame")

    st.markdown("""
    En este ejercicio se registran ventas de productos.
    Los datos se almacenan en una lista, luego se convierten en un arreglo de NumPy
    y finalmente se muestran como DataFrame.
    """)

    producto = st.text_input("Nombre del producto")
    categoria = st.selectbox("Categoría", ["Tecnología", "Oficina", "Limpieza", "Alimentos", "Otros"])
    precio = st.number_input("Precio unitario", min_value=0.0, step=1.0)
    cantidad = st.number_input("Cantidad", min_value=0, step=1)

    if st.button("Agregar venta"):
        if producto != "" and precio > 0 and cantidad > 0:
            total = precio * cantidad

            venta = [producto, categoria, precio, cantidad, total]
            st.session_state.ventas.append(venta)

            st.success("Venta registrada correctamente.")
        else:
            st.error("Debe completar los datos correctamente.")

    if len(st.session_state.ventas) > 0:
        arreglo_ventas = np.array(st.session_state.ventas, dtype=object)

        df_ventas = pd.DataFrame(
            arreglo_ventas,
            columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"]
        )

        st.dataframe(df_ventas)

        total_ventas = df_ventas["Total"].astype(float).sum()
        st.metric("Total de ventas registradas", f"S/ {total_ventas:.2f}")
    else:
        st.info("Aún no se han registrado ventas.")


# =====================================================
# EJERCICIO 3 - FUNCION EXTERNA
# =====================================================

elif opcion == "Ejercicio 3":
    st.title("Ejercicio 3 - Uso de función desde librería externa")

    st.markdown("""
    En este ejercicio se utiliza una función externa llamada
    `calcular_ticket_promedio`, importada desde el archivo
    `libreria_funciones_proyecto1.py`.

    La función calcula el ticket promedio dividiendo las ventas totales
    entre el número de clientes.
    """)

    ventas_totales = st.number_input("Ventas totales", min_value=0.0, step=100.0)
    numero_clientes = st.number_input("Número de clientes", min_value=1, step=1)

    if st.button("Calcular ticket promedio"):
        try:
            resultado = calcular_ticket_promedio(ventas_totales, numero_clientes)

            ticket = resultado["ticket_promedio"]

            st.success("Cálculo realizado correctamente.")
            st.metric("Ticket promedio", f"S/ {ticket:.2f}")

            registro = {
                "Ventas totales": ventas_totales,
                "Número de clientes": numero_clientes,
                "Ticket promedio": ticket
            }

            st.session_state.historico_funcion.append(registro)

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

    if len(st.session_state.historico_funcion) > 0:
        st.subheader("Histórico de resultados")
        df_historico = pd.DataFrame(st.session_state.historico_funcion)
        st.dataframe(df_historico)
    else:
        st.info("Aún no hay cálculos registrados.")


# =====================================================
# EJERCICIO 4 - CLASE EXTERNA Y CRUD
# =====================================================

elif opcion == "Ejercicio 4":
    st.title("Ejercicio 4 - CRUD con clase InventarioProducto")

    st.markdown("""
    En este ejercicio se utiliza la clase `InventarioProducto`, importada desde
    el archivo `libreria_clases_proyecto1.py`.

    Se implementan operaciones básicas CRUD:
    crear, leer, actualizar y eliminar productos.
    """)

    tab1, tab2, tab3, tab4 = st.tabs(["Crear", "Leer", "Actualizar", "Eliminar"])

    # -----------------------------
    # CREAR
    # -----------------------------
    with tab1:
        st.subheader("Crear producto")

        nombre = st.text_input("Nombre del producto")
        costo_unitario = st.number_input("Costo unitario", min_value=0.0, step=1.0)
        precio_unitario = st.number_input("Precio unitario", min_value=0.0, step=1.0)
        stock_actual = st.number_input("Stock actual", min_value=0, step=1)
        stock_minimo = st.number_input("Stock mínimo", min_value=0, step=1)

        if st.button("Guardar producto"):
            try:
                producto_objeto = InventarioProducto(
                    nombre,
                    costo_unitario,
                    precio_unitario,
                    stock_actual,
                    stock_minimo
                )

                resumen = producto_objeto.resumen()
                st.session_state.inventario.append(resumen)

                st.success("Producto creado correctamente.")

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

    # -----------------------------
    # LEER
    # -----------------------------
    with tab2:
        st.subheader("Lista de productos")

        if len(st.session_state.inventario) > 0:
            df_inventario = pd.DataFrame(st.session_state.inventario)
            st.dataframe(df_inventario)
        else:
            st.info("No hay productos registrados.")

    # -----------------------------
    # ACTUALIZAR
    # -----------------------------
    with tab3:
        st.subheader("Actualizar producto")

        if len(st.session_state.inventario) > 0:
            nombres_productos = [item["producto"] for item in st.session_state.inventario]

            producto_seleccionado = st.selectbox(
                "Seleccione producto a actualizar",
                nombres_productos
            )

            nuevo_stock = st.number_input("Nuevo stock actual", min_value=0, step=1)
            nuevo_stock_minimo = st.number_input("Nuevo stock mínimo", min_value=0, step=1)

            if st.button("Actualizar producto"):
                for item in st.session_state.inventario:
                    if item["producto"] == producto_seleccionado:
                        item["stock_actual"] = nuevo_stock
                        item["necesita_reposicion"] = nuevo_stock <= nuevo_stock_minimo

                st.success("Producto actualizado correctamente.")
        else:
            st.info("No hay productos para actualizar.")

    # -----------------------------
    # ELIMINAR
    # -----------------------------
    with tab4:
        st.subheader("Eliminar producto")

        if len(st.session_state.inventario) > 0:
            nombres_productos_eliminar = [item["producto"] for item in st.session_state.inventario]

            producto_eliminar = st.selectbox(
                "Seleccione producto a eliminar",
                nombres_productos_eliminar
            )

            if st.button("Eliminar producto"):
                st.session_state.inventario = [
                    item for item in st.session_state.inventario
                    if item["producto"] != producto_eliminar
                ]

                st.success("Producto eliminado correctamente.")
        else:
            st.info("No hay productos para eliminar.")
