"""
Modulo de Utilidades - Formateadores
Define funciones para formatear y presentar datos
"""

from typing import List, Dict, Any
from ..models.producto import Producto


class Formateadores:
    """Clase con metodos estaticos para formatear datos para la interfaz."""

    @staticmethod
    def formatear_precio(precio: float) -> str:
        """Formatea precio con simbolo de moneda y dos decimales."""
        return f"${precio:,.2f}"

    @staticmethod
    def formatear_producto_tabla(producto: Producto) -> str:
        """Formatea un solo producto para visualizacion en una fila de tabla."""
        precio_formateado = Formateadores.formatear_precio(producto.precio).replace("$", "")
        valor_total_formateado = Formateadores.formatear_precio(producto.calcular_valor_total()).replace("$", "")
        
        return (f"| {producto.id_producto:>6} | {producto.nombre:<20} | "
                f"{precio_formateado:>8} | {producto.cantidad:>6} | "
                f"{valor_total_formateado:>10} |")
    @staticmethod
    def formatear_lista_productos(productos: List[Producto]) -> str:
        """Formatea lista de productos completa con encabezado y separadores."""
        if not productos:
            return "No hay productos para mostrar."
            
        encabezado = "|   ID   |        Nombre          |  Precio  | Stock  | Valor Total  |"
        separador = "-" * 70
        filas = [Formateadores.formatear_producto_tabla(p) for p in productos]
        
        return f"{separador}\n{encabezado}\n{separador}\n" + "\n".join(filas) + f"\n{separador}"
    
    @staticmethod
    def formatear_reporte(reporte: Dict[str, Any]) -> str:
        """Formatea el reporte de inventario para una visualización legible."""
        output = "\n" + "=" * 60 + "\n"
        output += "                        REPORTE DE INVENTARIO\n"
        output += "=" * 60 + "\n"
        output += f"Fecha de Generación: {reporte['fecha_generacion']}\n\n"      
        output += f"Total de Tipos de Productos: {reporte['total_productos']}\n"
        output += f"Total de Unidades en Stock: {reporte['total_items']}\n"
        output += f"Valor Total del Inventario: {Formateadores.formatear_precio(reporte['valor_total'])}\n\n"

        if reporte['producto_mas_caro']:
            output += f"Producto Más Caro: {reporte['producto_mas_caro'].nombre} "
            output += f"({Formateadores.formatear_precio(reporte['producto_mas_caro'].precio)})\n"

        if reporte['producto_mas_barato']:
            output += f"Producto Más Barato: {reporte['producto_mas_barato'].nombre} "
            output += f"({Formateadores.formatear_precio(reporte['producto_mas_barato'].precio)})\n"
            
        output += f"\nProductos Bajo Stock ({len(reporte['productos_bajo_stock'])} items):\n"
        
        if reporte['productos_bajo_stock']:
            output += Formateadores.formatear_lista_productos(reporte['productos_bajo_stock'])
        else:
             output += "No hay productos con stock bajo.\n"
        
        output += "=" * 60 + "\n"
        
        return output