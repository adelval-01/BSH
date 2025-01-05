<?php
header("Content-Type: application/json");

// Configuración de la base de datos
$db_host = "172.20.10.2";
$db_name = "gestion_prendas";
$db_user = "postgres";
$db_password = "1234";

// Conectar a la base de datos
try {
    $conn = new PDO("pgsql:host=$db_host;dbname=$db_name", $db_user, $db_password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo json_encode(["error" => "Error de conexión a la base de datos: " . $e->getMessage()]);
    exit();
}

// Leer los EPCs enviados desde el frontend
$input = json_decode(file_get_contents("php://input"), true);
$epcs = $input['epcs'] ?? [];

if (empty($epcs)) {
    echo json_encode(["error" => "No se proporcionaron EPCs."]);
    exit();
}

try {
    // Consulta para obtener los nombres de las prendas asociadas
    $placeholders = implode(",", array_fill(0, count($epcs), "?"));
    $sql = "SELECT codigo_inventario FROM prendas WHERE rfcid IN ($placeholders)";
    $stmt = $conn->prepare($sql);
    $stmt->execute($epcs);

    // Obtener los resultados
    $prendas = $stmt->fetchAll(PDO::FETCH_COLUMN);

    echo json_encode(["prendas" => $prendas]);
} catch (PDOException $e) {
    echo json_encode(["error" => "Error al consultar la base de datos: " . $e->getMessage()]);
}

// Cerrar la conexión
$conn = null;
?>
