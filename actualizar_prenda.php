<?php
header('Content-Type: application/json');

$response = array('success' => false, 'message' => ''); // Por defecto, éxito como falso

$host = '172.20.10.2'; // o el nombre del servidor si no es local
$db = 'gestion_prendas'; // el nombre de la base de datos
$user = 'postgres'; // tu usuario de la base de datos
$pass = '1234'; // tu contraseña de la base de datos

// Obtener los datos de la solicitud
$inputData = json_decode(file_get_contents('php://input'), true);

// Verificar que todos los campos necesarios estén presentes
if (isset($inputData['id'])) {
    // Realizar la conexión a la base de datos y la actualización
    $id = $inputData['id'];
    $tipo_prenda = $inputData['tipo_prenda'];
    $propietario = $inputData['propietario'];
    $color = $inputData['color'];
    $material = $inputData['material'];
    $departamento = $inputData['departamento'];
    $alertas = $inputData['alertas'];
    $ciclo_preferido = $inputData['ciclo_preferido'];
    $restricciones = $inputData['restricciones'];
    $temperatura = $inputData['temperatura'];
    $ciclos_realizados = $inputData['ciclos_realizados'];
    $fecha_ultimo_lavado = $inputData['fecha_ultimo_lavado'];
    $tipo_ciclo = $inputData['tipo_ciclo'];
    $nivel_desgaste = $inputData['nivel_desgaste'];
    $id_usuario = $inputData['id_usuario'];
    $preferencias_lavado = $inputData['preferencias_lavado'];
    $tipo_detergente = $inputData['tipo_detergente'];
    $alergias = $inputData['alergias'];
    $ubicacion = $inputData['ubicacion'];
    $datos_desinfeccion = $inputData['datos_desinfeccion'];
    $certificacion_limpieza = $inputData['certificacion_limpieza'];

    try {
        // Establecer la conexión a la base de datos con PDO
        $conn = new PDO("pgsql:host=$host;dbname=$db", $user, $pass);
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Preparar y ejecutar la consulta SQL de actualización
        $sql = "UPDATE prendas 
                SET tipo_prenda=:tipo_prenda, propietario=:propietario, color=:color, material=:material, 
                    departamento=:departamento, alertas=:alertas, ciclo_preferido=:ciclo_preferido, 
                    restricciones=:restricciones, temperatura=:temperatura, ciclos_realizados=:ciclos_realizados, 
                    fecha_ultimo_lavado=:fecha_ultimo_lavado, tipo_ciclo=:tipo_ciclo, nivel_desgaste=:nivel_desgaste, 
                    id_usuario=:id_usuario, preferencias_lavado=:preferencias_lavado, tipo_detergente=:tipo_detergente, 
                    alergias=:alergias, ubicacion=:ubicacion, datos_desinfeccion=:datos_desinfeccion, 
                    certificacion_limpieza=:certificacion_limpieza 
                WHERE id=:id";
        
        $stmt = $conn->prepare($sql);

        // Asociar los valores a la consulta
        $stmt->bindParam(':tipo_prenda', $tipo_prenda);
        $stmt->bindParam(':propietario', $propietario);
        $stmt->bindParam(':color', $color);
        $stmt->bindParam(':material', $material);
        $stmt->bindParam(':departamento', $departamento);
        $stmt->bindParam(':alertas', $alertas);
        $stmt->bindParam(':ciclo_preferido', $ciclo_preferido);
        $stmt->bindParam(':restricciones', $restricciones);
        $stmt->bindParam(':temperatura', $temperatura);
        $stmt->bindParam(':ciclos_realizados', $ciclos_realizados, PDO::PARAM_INT);
        $stmt->bindParam(':fecha_ultimo_lavado', $fecha_ultimo_lavado);
        $stmt->bindParam(':tipo_ciclo', $tipo_ciclo);
        $stmt->bindParam(':nivel_desgaste', $nivel_desgaste);
        $stmt->bindParam(':id_usuario', $id_usuario);
        $stmt->bindParam(':preferencias_lavado', $preferencias_lavado);
        $stmt->bindParam(':tipo_detergente', $tipo_detergente);
        $stmt->bindParam(':alergias', $alergias);
        $stmt->bindParam(':ubicacion', $ubicacion);
        $stmt->bindParam(':datos_desinfeccion', $datos_desinfeccion);
        $stmt->bindParam(':certificacion_limpieza', $certificacion_limpieza);
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);

        // Ejecutar la consulta
        if ($stmt->execute()) {
            $response['success'] = true;
            $response['message'] = 'Prenda actualizada correctamente';
        } else {
            $response['message'] = 'Error al actualizar la prenda';
        }

    } catch (PDOException $e) {
        // En caso de error, capturar el mensaje de la excepción
        $response['message'] = 'Error en la base de datos: ' . $e->getMessage();
    }
} else {
    $response['message'] = 'Faltan datos en la solicitud';
}

// Devolver la respuesta en formato JSON
echo json_encode($response);
?>

