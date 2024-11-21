<?php
// Datos de conexión a la base de datos
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
        $tipo_prenda = $_POST["tipo_prenda"];
        $propietario = $_POST["propietario"];
        $color_material = $_POST["color_material"];
        $departamento = $_POST["departamento"];
        $id_propietario = $_POST["id_propietario"];
        $codigo_inventario = $_POST["codigo_inventario"];
        // Añadir el resto de los campos necesarios

        // Insertar la prenda en la base de datos
        $query = "INSERT INTO prendas (tipo_prenda, propietario, color_material, departamento, id_propietario, codigo_inventario)
                  VALUES (:tipo_prenda, :propietario, :color_material, :departamento, :id_propietario, :codigo_inventario)";
        $stmt = $pdo->prepare($query);
        $stmt->bindParam(":tipo_prenda", $tipo_prenda);
        $stmt->bindParam(":propietario", $propietario);
        $stmt->bindParam(":color_material", $color_material);
        $stmt->bindParam(":departamento", $departamento);
        $stmt->bindParam(":id_propietario", $id_propietario);
        $stmt->bindParam(":codigo_inventario", $codigo_inventario);

        if ($stmt->execute()) {
            echo "Prenda añadida con éxito.";
            header("Location: prendas_iri_1.html"); // Redirigir de vuelta a la página principal
            exit;
        } else {
            echo "Error al añadir la prenda.";
        }
    }
} catch (PDOException $e) {
    echo "Error de conexión: " . $e->getMessage();
}
?>
