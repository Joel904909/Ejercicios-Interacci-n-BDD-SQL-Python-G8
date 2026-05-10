USE DatabaseBDDII_Fase3;
GO

-- 1. Consultar todos los usuarios
CREATE PROCEDURE Operaciones.SP_ConsultarUsuarios 
AS
BEGIN
    SELECT idUsuario, nombreUsuario, emailUsuario, tipoSuscripcion, fechaRegistro
    FROM Operaciones.Usuario;
END;
GO

-- 2. Insertar un nuevo usuario
CREATE PROCEDURE Operaciones.SP_InsertarUsuario
    @ID int, 
    @Nombre varchar(50),  
    @Email varchar(50),  
    @TipoSusc bit,      
    @FechaReg datetime = NULL 
AS
BEGIN
    INSERT INTO Operaciones.Usuario (idUsuario, nombreUsuario, emailUsuario, tipoSuscripcion, fechaRegistro)
    VALUES (@ID, @Nombre, @Email, @TipoSusc, ISNULL(@FechaReg, GETDATE()));
END;
GO

-- 3. Actualizar un usuario existente
CREATE PROCEDURE Operaciones.SP_ActualizarUsuario
    @ID int, 
    @Nombre varchar(50), 
    @Email varchar(50),
    @TipoSusc bit, 
    @FechaReg datetime
AS
BEGIN
    UPDATE Operaciones.Usuario
    SET nombreUsuario = @Nombre, 
        emailUsuario = @Email,
        tipoSuscripcion = @TipoSusc, 
        fechaRegistro = @FechaReg
    WHERE idUsuario = @ID;
END;
GO

-- 4. Eliminar un usuario
CREATE PROCEDURE Operaciones.SP_EliminarUsuario 
    @ID int 
AS
BEGIN
    DELETE FROM Operaciones.Usuario 
    WHERE idUsuario = @ID;
END;
GO


USE DatabaseBDDII_Fase3;
GO

-- 1. Permiso para poder crear procedimientos en la base de datos
GRANT CREATE PROCEDURE TO AppStreamingUserV2;

-- 2. Permiso para poder modificar (ALTER) el esquema Operaciones
-- Sin esto, no te dejará "escribir" dentro de ese esquema
GRANT ALTER ON SCHEMA::Operaciones TO AppStreamingUserV2;
GO

SELECT SUSER_SNAME() AS LoginName, USER_NAME() AS DatabaseUserName;

