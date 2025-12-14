"""
Modulo de Utilidades - Validadores
Define funciones para validar entrada de datos
"""
from typing import List
from ..models.producto import Categoria 

class Validadores:
    """Clase con metodos estaticos para validaciones de datos."""

    @staticmethod
    def validar_precio_positivo(precio: float) -> bool:
        """Valida que el precio sea un número positivo."""
        if not isinstance(precio, (int, float)):
            # Permite 0, pero no negativo.
            raise ValueError("El precio debe ser un numero (entero o decimal)")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        return True
    
    @staticmethod
    def validar_cantidad_no_negativa(cantidad: int) -> bool:
        """Valida que la cantidad sea un entero no negativo."""
        if not isinstance(cantidad, int):
            raise ValueError("La cantidad debe ser un numero entero")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        return True

    @staticmethod
    def validar_nombre_no_vacio(nombre: str) -> bool:
        """Valida que el nombre sea una cadena de texto no vacía."""
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser texto")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacio")
        return True
    
    @staticmethod
    def validar_categoria_valida(categoria: str, categorias_validas: List[str]) -> bool:
        """Valida que la categoria ingresada exista en la lista de categorías permitidas."""
        if categoria not in categorias_validas:
            raise ValueError(f"Categoria invalida. Validas: {', '.join(categorias_validas)}")
        return True
    