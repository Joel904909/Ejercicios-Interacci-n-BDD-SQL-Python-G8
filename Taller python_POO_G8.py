import pyodbc
import json

# ============================================================
# CLASE: GestorUsuarios (Encapsulamiento solicitado)
# ============================================================
class GestorUsuarios:
    def __init__(self):
        """Inicializa la conexión desde el archivo TallerConfig.json"""
        try:
            # Se agrega encoding='utf-8' para evitar el error de charmap
            with open('TallerConfig.json', 'r', encoding='utf-8') as archivo_config:
                config = json.load(archivo_config)

            # Construcción de la cadena de conexión
            self.connection_string = (
                f"DRIVER={config['controlador_odbc']};"
                f"SERVER={config['name_server']};"
                f"DATABASE={config['database']};"
                f"UID={config['username']};"
                f"PWD={config['password']}"
            )

            self.conexion = pyodbc.connect(self.connection_string)
            print("\n\t[OK] Conexión establecida correctamente.")

        except FileNotFoundError:
            print("\n\t[ERROR] No se encontró el archivo 'TallerConfig.json'.")
            raise
        except Exception as e:
            print("\n\t[ERROR] Al inicializar la conexión:", e)
            raise

    # ----------------------------------------------------------
    # MÉTODOS CRUD (Llamada a Stored Procedures)
    # ----------------------------------------------------------
    def consultar_usuarios(self):
        """Llama al Stored Procedure de consulta (READ)"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("EXEC Operaciones.SP_ConsultarUsuarios")
            records = cursor.fetchall()

            if not records:
                print("\tNo hay registros.")
            else:
                print(f"\n\t{'ID':<5} {'Nombre':<20} {'Email':<30}")
                print("\t" + "-" * 60)
                for r in records:
                    # Acceso a los campos por nombre de columna
                    print(f"\t{r.idUsuario:<5} {r.nombreUsuario:<20} {r.emailUsuario:<30}")
        except Exception as e:
            print("\tError en la consulta:", e)

    def insertar_usuario(self):
        """Llama al Stored Procedure de inserción (CREATE)"""
        try:
            print("\n\t--- Registrar Nuevo Usuario ---")
            # Parámetros ingresados con INPUT según la consigna
            id_u = input("\tID: ")
            nom  = input("\tNombre: ")
            em   = input("\tEmail: ")
            tipo = input("\tTipo (0: Normal, 1: Premium): ")
            fec  = input("\tFecha (YYYY-MM-DD): ")

            cursor = self.conexion.cursor()
            cursor.execute("EXEC Operaciones.SP_InsertarUsuario ?, ?, ?, ?, ?", 
                           (id_u, nom, em, tipo, fec))
            self.conexion.commit()
            print("\tRegistro insertado con éxito.")
        except Exception as e:
            self.conexion.rollback()
            print("\tError al insertar:", e)

    def actualizar_usuario(self):
        """Llama al Stored Procedure de actualización (UPDATE)"""
        try:
            print("\n\t--- Actualizar Usuario ---")
            id_u = input("\tID a modificar: ")
            nom  = input("\tNuevo Nombre: ")
            em   = input("\tNuevo Email: ")
            tipo = input("\tNuevo Tipo: ")
            fec  = input("\tNueva Fecha: ")

            cursor = self.conexion.cursor()
            cursor.execute("EXEC Operaciones.SP_ActualizarUsuario ?, ?, ?, ?, ?", 
                           (id_u, nom, em, tipo, fec))
            self.conexion.commit()
            print(f"\tUsuario {id_u} actualizado.")
        except Exception as e:
            self.conexion.rollback()
            print("\tError al actualizar:", e)

    def eliminar_usuario(self):
        """Llama al Stored Procedure de eliminación (DELETE)"""
        try:
            print("\n\t--- Eliminar Usuario ---")
            id_u = input("\tIngrese el ID a eliminar: ")
            
            cursor = self.conexion.cursor()
            cursor.execute("EXEC Operaciones.SP_EliminarUsuario ?", (id_u,))
            self.conexion.commit()
            print(f"\tUsuario {id_u} eliminado.")
        except Exception as e:
            self.conexion.rollback()
            print("\tError al eliminar:", e)

    # ----------------------------------------------------------
    # MENÚ PRINCIPAL
    # ----------------------------------------------------------
    def ejecutar_menu(self):
        """Gestiona el menú principal del sistema CRUD"""
        while True:
            print("\n\t** SISTEMA CRUD - PROYECTO INTEGRADOR **")
            print("\t1. Crear registro")
            print("\t2. Consultar registros")
            print("\t3. Actualizar registro")
            print("\t4. Eliminar registro")
            print("\t5. Salir")
            
            opcion = input("\n\tSeleccione una opción: ")
            if opcion == '1': self.insertar_usuario()
            elif opcion == '2': self.consultar_usuarios()
            elif opcion == '3': self.actualizar_usuario()
            elif opcion == '4': self.eliminar_usuario()
            elif opcion == '5': break
            else: print("\tOpción no válida.")

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos de forma segura"""
        if hasattr(self, 'conexion'):
            self.conexion.close()

# ============================================================
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    gestor = None
    try:
        gestor = GestorUsuarios()
        gestor.ejecutar_menu()
    except Exception as e:
        print("\n\t[ERROR] El programa terminó con error:", e)
    finally:
        if gestor:
            gestor.cerrar_conexion()