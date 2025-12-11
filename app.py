import streamlit as st
from fpdf import FPDF
from datetime import date, timedelta

# --- FUNCIÓN PDF DISEÑO MODERNO ---
def crear_pdf(cliente, ruc, direccion, telefono, numero_proforma, f_emision, f_validez, items, subtotal, valor_iva, total):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- COLORES DE MARCA (Personalízalos aquí) ---
    color_primario = (41, 128, 185)   # Azul profesional
    color_fondo_tabla = (232, 246, 243) # Azul muy pálido
    color_texto = (44, 62, 80)        # Gris oscuro (más elegante que negro puro)

    # --- 1. ENCABEZADO ---
    # Logo
    try:
        pdf.image('logo.png', 10, 12, 80) # Logo un poco más pequeño y elegante
    except:
        pass

    # Datos Empresa (Alineados a la derecha)
    pdf.set_y(10) # Regresamos arriba
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(*color_primario) # Desempaquetamos la tupla de color
    pdf.cell(0, 10, 'FILJOB', 0, 1, 'R')
    
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'RUC: 2400090201001', 0, 1, 'R')
    pdf.cell(0, 5, 'Salinas, Santa Elena, Ecuador', 0, 1, 'R')
    pdf.cell(0, 5, 'paulchoez92@gmail.com | +593993739630', 0, 1, 'R')
    
    pdf.ln(15) # Separador visual
    
    # Línea decorativa
    pdf.set_draw_color(*color_primario)
    pdf.set_line_width(1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # --- 2. INFO CLIENTE Y PROFORMA (Diseño en 2 columnas invisibles) ---
    y_antes = pdf.get_y()
    
    # Columna Izquierda: Cliente
    pdf.set_text_color(*color_texto)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(100, 6, "FACTURAR A:", 0, 1)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(100, 5, cliente, 0, 1)
    pdf.cell(100, 5, f"RUC: {ruc}", 0, 1)
    pdf.cell(100, 5, f"Dirección: {direccion}", 0, 1)
    pdf.cell(100, 5, f"Teléfono: {telefono}", 0, 1)

    # Columna Derecha: Datos Proforma (Movemos el cursor)
    pdf.set_xy(120, y_antes) 
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(80, 6, "DETALLES:", 0, 1, 'R')
    
    pdf.set_x(120)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(80, 6, f"N° {numero_proforma}", 0, 1, 'R')
    
    pdf.set_x(120)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, f"Fecha: {f_emision}", 0, 1, 'R')
    
    pdf.set_x(120)
    pdf.set_text_color(200, 0, 0) # Rojo sutil
    pdf.cell(80, 5, f"Vence: {f_validez}", 0, 1, 'R')

    pdf.ln(15)

    # --- 3. TABLA MODERNA (Sin bordes verticales) ---
    # Encabezados
    pdf.set_fill_color(*color_primario)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 10)
    
    # Altura de fila
    h = 10 
    
    pdf.cell(100, h, "  Descripción", 0, 0, 'L', fill=True) # Espacio al inicio para estética
    pdf.cell(20, h, "Cant.", 0, 0, 'C', fill=True)
    pdf.cell(35, h, "Precio Unit.", 0, 0, 'R', fill=True)
    pdf.cell(35, h, "Total  ", 0, 1, 'R', fill=True) # Espacio al final

    # Filas
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*color_texto)
    fill = False
    pdf.set_fill_color(*color_fondo_tabla) # Color cebra suave

    for item in items:
        # Usamos border=0 para quitar líneas, o 'B' para solo línea inferior
        pdf.cell(100, h, f"  {item['desc']}", 'B', 0, 'L', fill=fill)
        pdf.cell(20, h, str(item['cant']), 'B', 0, 'C', fill=fill)
        pdf.cell(35, h, f"${item['precio']:.2f}", 'B', 0, 'R', fill=fill)
        pdf.cell(35, h, f"${item['total']:.2f}  ", 'B', 1, 'R', fill=fill)
        # fill = not fill # Descomenta si quieres efecto cebra (rayado)

    # --- 4. TOTALES (Diseño de tarjeta) ---
    pdf.ln(10)
    
    # Calculamos posición X para que quede a la derecha
    x_totales = 130
    
    pdf.set_x(x_totales)
    pdf.set_text_color(*color_texto)
    pdf.cell(35, 8, "Subtotal:", 0, 0, 'R')
    pdf.cell(35, 8, f"${subtotal:.2f}", 0, 1, 'R')
    
    pdf.set_x(x_totales)
    pdf.cell(35, 8, "IVA (15%):", 0, 0, 'R')
    pdf.cell(35, 8, f"${valor_iva:.2f}", 0, 1, 'R')
    
    # Caja de Total Final
    pdf.ln(2)
    pdf.set_x(x_totales)
    pdf.set_fill_color(*color_primario)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 12)
    # Dibujamos celda rellena
    pdf.cell(70, 12, f"  TOTAL: ${total:.2f}  ", 0, 1, 'R', fill=True)

    # --- 5. PIE DE PÁGINA / GRACIAS ---
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, "Gracias por elegirnos como su solución confiable", 0, 0, 'C')

    return bytes(pdf.output(dest='S'))

# --- 2. INTERFAZ WEB ---
st.set_page_config(page_title="Proformas Pro", page_icon="💼")
st.title("Generador de Proformas FILJOB 💼")

# Datos Generales
with st.container(border=True):
    st.subheader("Configuración")
    c1, c2, c3 = st.columns(3)
    numero_proforma = c1.text_input("N° Proforma", "001-001-00001")
    f_emision = c2.date_input("Fecha Emisión", date.today())
    
    # 🔴 EL INTERRUPTOR MAGICO
    aplicar_iva = c3.checkbox("Cobrar IVA (15%)", value=False) 
    
    f_validez = f_emision + timedelta(days=10)

# Datos Cliente
with st.container(border=True):
    st.subheader("Datos del Cliente")
    col1, col2 = st.columns(2)
    nombre = col1.text_input("Cliente / Razón Social")
    ruc = col2.text_input("RUC o Cédula")
    c_dir, c_tel = st.columns([2, 1])
    direccion = c_dir.text_input("Dirección")
    telefono = c_tel.text_input("Teléfono")

# Productos
st.subheader("Detalle de Productos")
if 'num_productos' not in st.session_state:
    st.session_state.num_productos = 1

def agregar_fila(): st.session_state.num_productos += 1
def quitar_fila(): 
    if st.session_state.num_productos > 1: st.session_state.num_productos -= 1

b1, b2 = st.columns([1, 4])
b1.button("➕ Agregar Item", on_click=agregar_fila)
b2.button("➖ Quitar Item", on_click=quitar_fila)

items = []
subtotal_acumulado = 0 # Usamos esto para sumar

for i in range(st.session_state.num_productos):
    c1, c2, c3 = st.columns([3, 1, 1])
    desc = c1.text_input(f"Item {i+1}", key=f"d{i}")
    cant = c2.number_input("Cant.", 1, key=f"c{i}")
    precio = c3.number_input("Precio", 0.0, key=f"p{i}")
    
    if desc:
        total_item = cant * precio
        items.append({"desc": desc, "cant": cant, "precio": precio, "total": total_item})
        subtotal_acumulado += total_item

st.divider()

# --- CÁLCULOS INTELIGENTES ---
# Si la cajita está marcada, calculamos 0.15. Si no, es 0.
if aplicar_iva:
    valor_iva = subtotal_acumulado * 0.15
else:
    valor_iva = 0.0

total_final = subtotal_acumulado + valor_iva

# Mostramos el resumen en pantalla
c1, c2, c3 = st.columns(3)
c1.metric("Subtotal", f"${subtotal_acumulado:.2f}")
c2.metric("IVA (15%)", f"${valor_iva:.2f}")
c3.metric("TOTAL", f"${total_final:.2f}")

# Botón
if st.button("Generar PDF", type="primary", use_container_width=True):
    if nombre and items:
        # Pasamos todos los valores calculados al PDF
        pdf_bytes = crear_pdf(nombre, ruc, direccion, telefono, numero_proforma, f_emision, f_validez, items, subtotal_acumulado, valor_iva, total_final)
        
        st.success("✅ ¡Listo!")
        st.download_button("⬇️ Descargar PDF", data=pdf_bytes, file_name=f"Proforma_{numero_proforma}.pdf", mime="application/pdf")
    else:

        st.error("⚠️ Faltan datos.")
