
# 1. Importar libreria
import pyodbc


# 2. Declarar variables de Conexion
name_server = 'GWTC71427'
database ='UDEMYTEST1'
username ='pythonconsultor'
password = 'UDLA'
controlador_odbc='SQL Server'

# 3. Crear Cadena de Conexion
connection_string = f'DRIVER={controlador_odbc};SERVER={name_server};DATABASE={database};UID={username};PWD={password}'



# ============================================================
# FUNCIONES CRUD
# ============================================================

def mostrar_opciones_crud():
    print("\n\t**********")
    print("\t**  SISTEMA CRUD - CURSOS  **")
    print("\t**********")
    print("\tOpciones CRUD:\n")
    print("\t1. Crear / Insertar curso")
    print("\t2. Consultar cursos")
    print("\t3. Actualizar curso")
    print("\t4. Eliminar curso")
    print("\t5. Salir\n")


# Funcion consultar registros
def consultar_registros(conexion):
    try:
        print("\n\t\tCONSULTA CURSOS:\n")

        SQL_QUERY = """
            SELECT IDCurso, NombreCurso, Descripcion, PrecioxHora, TipoCurso
            FROM Cursos
        """
        cursor = conexion.cursor()
        cursor.execute(SQL_QUERY)
        records = cursor.fetchall()

        if not records:
            print("\t(No hay registros)")
        else:
            print(f"\t{'ID':<5} {'Nombre':<25} {'Descripcion':<30} {'Precio/H':<10} {'Tipo'}")
            print("\t" + "-" * 80)
            for r in records:
                print(f"\t{r.IDCurso:<5} {r.NombreCurso:<25} "
                      f"{r.Descripcion:<30} {r.PrecioxHora:<10} {r.TipoCurso}")

    except Exception as e:
        print("\n\tOcurrio un error al consultar SQL Server:\n", e)

    finally:
        print("\n\tProceso Consulta Finalizado.\n")


# Funcion insertar registros
def insertar_registros(conexion):
    try:
        print("\n\t\tINSERTAR CURSO:\n")

        id_curso    = input("\tID Curso      : ").strip()
        nombre      = input("\tNombre Curso  : ").strip()
        descripcion = input("\tDescripcion   : ").strip()
        precio      = input("\tPrecio x Hora : ").strip()
        tipo        = input("\tTipo Curso    : ").strip()

        SQL_INSERT = """
            INSERT INTO Cursos (IDCurso, NombreCurso, Descripcion, PrecioxHora, TipoCurso)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = conexion.cursor()
        cursor.execute(SQL_INSERT, (id_curso, nombre, descripcion, precio, tipo))
        conexion.commit()

        print("\n\tRegistro insertado correctamente.")

    except Exception as e:
        print("\n\tOcurrio un error al insertar en SQL Server:\n", e)
        conexion.rollback()

    finally:
        print("\n\tProceso Insercion Finalizado.\n")


# Funcion actualizar registros
def actualizar_registros(conexion):
    try:
        print("\n\t\tACTUALIZAR CURSO:\n")

        id_curso    = input("\tID del curso a actualizar : ").strip()
        nombre      = input("\tNuevo Nombre Curso        : ").strip()
        descripcion = input("\tNueva Descripcion         : ").strip()
        precio      = input("\tNuevo Precio x Hora       : ").strip()
        tipo        = input("\tNuevo Tipo Curso          : ").strip()

        SQL_UPDATE = """
            UPDATE Cursos
            SET NombreCurso  = ?,
                Descripcion  = ?,
                PrecioxHora  = ?,
                TipoCurso    = ?
            WHERE IDCurso = ?
        """
        cursor = conexion.cursor()
        cursor.execute(SQL_UPDATE, (nombre, descripcion, precio, tipo, id_curso))
        conexion.commit()

        if cursor.rowcount == 0:
            print(f"\n\tNo se encontro ningun curso con ID {id_curso}.")
        else:
            print("\n\tRegistro actualizado correctamente.")

    except Exception as e:
        print("\n\tOcurrio un error al actualizar en SQL Server:\n", e)
        conexion.rollback()

    finally:
        print("\n\tProceso Actualizacion Finalizado.\n")


# Funcion eliminar registros
def eliminar_registros(conexion):
    try:
        print("\n\t\tELIMINAR CURSO:\n")

        id_curso  = input("\tID del curso a eliminar: ").strip()
        confirmar = input(f"\tConfirma eliminar el curso con ID {id_curso}? (s/n): ").strip().lower()

        if confirmar != 's':
            print("\n\tOperacion cancelada.")
            return

        SQL_DELETE = "DELETE FROM Cursos WHERE IDCurso = ?"
        cursor = conexion.cursor()
        cursor.execute(SQL_DELETE, (id_curso,))
        conexion.commit()

        if cursor.rowcount == 0:
            print(f"\n\tNo se encontro ningun curso con ID {id_curso}.")
        else:
            print("\n\tRegistro eliminado correctamente.")

    except Exception as e:
        print("\n\tOcurrio un error al eliminar en SQL Server:\n", e)
        conexion.rollback()

    finally:
        print("\n\tProceso Eliminacion Finalizado.\n")



conexion = None

try:
    # 4. Establece la conexion
    conexion = pyodbc.connect(connection_string)
    print("\n\tConexion establecida correctamente.")

    # Bucle principal del menu
    while True:
        mostrar_opciones_crud()
        opcion = input("\tSeleccione una opcion (1-5):\t").strip()

        if opcion == '1':
            insertar_registros(conexion)
        elif opcion == '2':
            consultar_registros(conexion)
        elif opcion == '3':
            actualizar_registros(conexion)
        elif opcion == '4':
            eliminar_registros(conexion)
        elif opcion == '5':
            print("\n\tSaliendo del programa...\n")
            break
        else:
            print("\n\tOpcion no valida. Intente de nuevo.")

except Exception as e:
    print("\n\tOcurrio un error:\n\n", e)

finally:
    if conexion:
        conexion.close()
    print("\tConexion Cerrada.\n")