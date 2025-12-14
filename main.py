"""
Sistema de Gestion de Inventario - Interfaz Principal
Aplicacion interactiva para gestionar productos de Botica
"""

from src.Mi_Proyecto.models.producto import Categoria, Producto
from src.Mi_Proyecto.repositories.inventario import RepositorioMemoria, Inventario
from src.Mi_Proyecto.services.reportes import GeneradorReportes
from src.Mi_Proyecto.utils.validaciones import Validadores
from src.Mi_Proyecto.utils.formateo import Formateadores

class AplicacionInventario:
    """Aplicacion principal con interfaz de usuario."""

    def __init__(self):
        """Inicializa la aplicacion."""
        self.repositorio = RepositorioMemoria()
        self.inventario = Inventario(self.repositorio)
        self.reportes = GeneradorReportes(self.inventario)

    def mostrar_menu_principal(self) -> str:
        """Muestra el menu principal."""
        print("\n" + "=" * 50)
        print("   SISTEMA DE GESTION DE INVENTARIO (BOTICA)")
        print("=" * 50)
        print("1. Agregar producto")
        print("2. Ver todos los productos")
        print("3. Aumentar stock")
        print("4. Disminuir stock (Venta)")
        print("5. Productos con bajo stock")
        print("6. Ver reporte completo")
        print("7. Salir")
        print("=" * 50)

        return input("Seleccione una opcion: ")

    def agregar_producto_interactivo(self):
        """Permite agregar un producto de forma interactiva."""
        try:
            print("\n--- AGREGAR NUEVO PRODUCTO ---")
            nombre = input("Nombre del producto: ")
            Validadores.validar_nombre_no_vacio(nombre)

            descripcion = input("Descripcion: ")

            precio = float(input("Precio: $"))
            Validadores.validar_precio_positivo(precio)

            cantidad = int(input("Cantidad inicial: "))
            Validadores.validar_cantidad_no_negativa(cantidad)
            
            print("\nCategorias disponibles:")
            for i, cat in enumerate(Categoria):
                print(f" {i+1}. {cat.value}")

            while True:
                cat_input = input("Ingrese el nombre o número de la Categoria: ").strip()
                try:
                    if cat_input.isdigit() and 1 <= int(cat_input) <= len(Categoria):
                        categoria = list(Categoria)[int(cat_input) - 1]
                        break
                    cat_key = cat_input.upper().replace(" ", "_").replace("Ñ", "N") 
                    categoria = Categoria[cat_key]
                    break
                except (ValueError, KeyError):
                    print(f"ERROR: Categoría '{cat_input}' inválida. Intente de nuevo o use un número.")


            producto = self.inventario.agregar_producto(nombre, descripcion, precio, cantidad, categoria)
            print(f"\nOK - Producto agregado: {producto}")

        except (ValueError, KeyError) as e:
            print(f"\nERROR: {e}")

    def ver_todos_productos(self):
        """Muestra todos los productos."""
        productos = self.repositorio.obtener_todos()
        print("\n--- LISTA COMPLETA DE PRODUCTOS ---")
        print(Formateadores.formatear_lista_productos(productos))

    def aumentar_stock_interactivo(self):
        """Aumenta el stock de un producto."""
        try:
            id_prod = int(input("\nID del producto a aumentar: "))
            cantidad = int(input("Cantidad a aumentar: "))
            
            if cantidad <= 0:
                 raise ValueError("La cantidad a aumentar debe ser positiva.")

            self.inventario.aumentar_stock(id_prod, cantidad)
            print("\nOK - Stock aumentado exitosamente.")

        except (ValueError, KeyError) as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"\nERROR al aumentar stock: {e}")

    def disminuir_stock_interactivo(self):
        """Disminuye el stock de un producto (simula venta)."""
        try:
            id_prod = int(input("\nID del producto a vender: "))
            cantidad = int(input("Cantidad vendida: "))

            if cantidad <= 0:
                 raise ValueError("La cantidad vendida debe ser positiva.")

            self.inventario.disminuir_stock(id_prod, cantidad)
            print("\nOK - Venta registrada exitosamente.")

        except (ValueError, KeyError) as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"\nERROR al disminuir stock: {e}")

    def ver_bajo_stock(self):
        """Muestra productos con bajo stock."""
        try:
            limite_input = input("Límite de stock bajo (Ej: 10). Presione Enter para 10: ")
            limite = int(limite_input) if limite_input.strip() else 10
            
            if limite < 0:
                raise ValueError("El límite no puede ser negativo.")

            productos = self.inventario.obtener_productos_bajo_stock(limite)
            print(f"\n--- PRODUCTOS CON STOCK <= {limite} ---")
            print(Formateadores.formatear_lista_productos(productos))
            
        except ValueError as e:
            print(f"\nERROR: Entrada inválida. {e}")
            
    def ver_reporte(self):
        """Muestra el reporte completo."""
        reporte = self.reportes.reporte_completo()
        print(Formateadores.formatear_reporte(reporte))

    def ejecutar(self):
        """Ejecuta la aplicacion principal."""
        self._cargar_datos_prueba()

        while True:
            opcion = self.mostrar_menu_principal()

            if opcion == "1":
                self.agregar_producto_interactivo()
            elif opcion == "2":
                self.ver_todos_productos()
            elif opcion == "3":
                self.aumentar_stock_interactivo()
            elif opcion == "4":
                self.disminuir_stock_interactivo()
            elif opcion == "5":
                self.ver_bajo_stock()
            elif opcion == "6":
                self.ver_reporte()
            elif opcion == "7":
                print("\n¡Gracias por usar el Sistema de Inventario! ¡Hasta luego!")
                break
            else:
                print("\nERROR - Opción inválida. Por favor, seleccione un número del 1 al 7.")

    def _cargar_datos_prueba(self):
        """Carga datos de prueba en el inventario para Botica."""
        productos_prueba = [
            # ID 1001: Bajo stock
            ("Paracetamol 500mg", "Analgésico y antipirético", 4.50, 5, Categoria.MEDICAMENTOS_LIBRE_VENTA), 
            # ID 1002
            ("Amoxicilina 250mg", "Antibiótico (Requiere receta)", 15.90, 50, Categoria.MEDICAMENTOS_CON_RECETA),
            # ID 1003
            ("Vitamina D3", "Suplemento para huesos", 28.00, 15, Categoria.SUPLEMENTOS),
            # ID 1004
            ("Pañales Talla G", "Paquete de pañales para bebés", 45.00, 100, Categoria.BEBES_Y_NINOS),
            # ID 1005: Bajo stock
            ("Curitas Band-Aid", "Caja de 20 unidades", 8.50, 8, Categoria.MATERIAL_CURACION), 
            # ID 1006
            ("Crema Hidratante", "Crema para piel sensible", 19.99, 20, Categoria.CUIDADO_PERSONAL),
            # ID 1007: Bajo stock
            ("Tensiómetro Digital", "Para medir presión arterial", 75.00, 3, Categoria.OTROS),
            # ID 1008
            ("Alcohol 90%", "Botella de 1 litro", 10.00, 12, Categoria.MATERIAL_CURACION),
        ]
        
        for nombre, desc, precio, cantidad, categoria in productos_prueba:
            self.inventario.agregar_producto(nombre, desc, precio, cantidad, categoria)
        
        print("\n[INFO] OK - Datos de prueba de Botica cargados.")
        
if __name__ == "__main__":
    app = AplicacionInventario()
    app.ejecutar()