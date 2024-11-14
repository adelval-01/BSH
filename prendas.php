<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
// Configura los datos de tu conexión a la base de datos
$host = 'localhost'; // o el nombre del servidor si no es local
$db = 'gestion_prendas'; // el nombre de la base de datos
$user = 'postgres'; // tu usuario de la base de datos
$pass = '1234'; // tu contraseña de la base de datos

// Crear una conexión a la base de datos
try {
    $pdo = new PDO("pgsql:host=$host;dbname=$db", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Ejecuta la consulta para obtener todas las prendas
    $stmt = $pdo->query("SELECT * FROM prendas");

    // Recoge los datos
    $prendas = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Devuelve los datos como JSON
    echo json_encode($prendas);

} catch (PDOException $e) {
    // Si ocurre un error, muestra el mensaje
    echo json_encode(['error' => $e->getMessage()]);
}
?>
