<?php
// Datos de conexión a la base de datos
header('Content-Type: application/json');
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
$host = "localhost";
$dbname = "gestion_prendas";
$user = "postgres";
$password = "1234";

// Conexión a la base de datos
try {
    $pdo = new PDO("pgsql:host=$host;dbname=$dbname", $user, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Verificar si los datos fueron enviados
    if ($_SERVER["REQUEST_METHOD"] === "POST") {
        // Obtener los datos del formulario
        $rfcid = $_POST["epc"];
        $tipo_prenda = $_POST["tipo_prenda"];
        $propietario = $_POST["propietario"];
        $color = $_POST["color"];
        $material = $_POST["material"];
        $departamento = $_POST["departamento"];
        $id_propietario = $_POST["id_propietario"];
        $codigo_inventario = $_POST["codigo_inventario"];

        // Manejar la imagen subida
        if (isset($_FILES['imagen']) && $_FILES['imagen']['error'] === UPLOAD_ERR_OK) {
            // Leer el contenido del archivo
            $imagen = file_get_contents($_FILES['imagen']['tmp_name']);
        } else {
            $imagen = null; // En caso de que no se suba ninguna imagen
        }

        // Insertar la prenda en la base de datos
        $query = "INSERT INTO prendas (tipo_prenda, propietario, color, material, departamento, id_propietario, codigo_inventario, rfcid, imagen)
                  VALUES (:tipo_prenda, :propietario, :color, :material, :departamento, :id_propietario, :codigo_inventario, :rfcid, :imagen)";
        $stmt = $pdo->prepare($query);
        $stmt->bindParam(":tipo_prenda", $tipo_prenda);
        $stmt->bindParam(":propietario", $propietario);
        $stmt->bindParam(":color", $color);
        $stmt->bindParam(":material", $material);
        $stmt->bindParam(":departamento", $departamento);
        $stmt->bindParam(":id_propietario", $id_propietario);
        $stmt->bindParam(":codigo_inventario", $codigo_inventario);
        $stmt->bindParam(":rfcid", $rfcid);
        $stmt->bindParam(":imagen", $imagen, PDO::PARAM_LOB);

        if ($stmt->execute()) {
            echo "Prenda añadida con éxito.";
            header("Location: inventario.html"); // Redirigir de vuelta a la página principal
            exit;
        } else {
            echo "Error al añadir la prenda.";
        }
    }
} catch (PDOException $e) {
    echo "Error de conexión: " . $e->getMessage();
}
?>
