<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

// Configura los datos de tu conexión a la base de datos
$host = '172.20.10.2'; // o el nombre del servidor si no es local
$db = 'gestion_prendas'; // el nombre de la base de datos
$user = 'postgres'; // tu usuario de la base de datos
$pass = '1234'; // tu contraseña de la base de datos

// Crear una conexión a la base de datos
try {
    $pdo = new PDO("pgsql:host=$host;dbname=$db", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Verifica si el formulario fue enviado y si hay archivos
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        // Verifica si se subió la imagen
        if (isset($_FILES['imagen_prenda']) && $_FILES['imagen_prenda']['error'] == 0) {
            // Define la carpeta donde se guardarán las imágenes
            $targetDir = "uploads/";
            $targetFile = $targetDir . basename($_FILES['imagen_prenda']['name']);
            $imageFileType = strtolower(pathinfo($targetFile, PATHINFO_EXTENSION));

            // Verifica que el archivo sea una imagen
            $check = getimagesize($_FILES['imagen_prenda']['tmp_name']);
            if ($check === false) {
                echo json_encode(['error' => 'El archivo no es una imagen']);
                exit;
            }

            // Verifica el tamaño del archivo (por ejemplo, máximo 5MB)
            if ($_FILES['imagen_prenda']['size'] > 5000000) {
                echo json_encode(['error' => 'El archivo es demasiado grande']);
                exit;
            }

            // Permitir ciertos formatos de imagen
            if ($imageFileType != 'jpg' && $imageFileType != 'png' && $imageFileType != 'jpeg' && $imageFileType != 'gif') {
                echo json_encode(['error' => 'Solo se permiten archivos JPG, JPEG, PNG y GIF']);
                exit;
            }

            // Intenta mover el archivo subido a la carpeta de destino
            if (move_uploaded_file($_FILES['imagen_prenda']['tmp_name'], $targetFile)) {
                // Obtiene los otros datos del formulario
                $tipo_prenda = $_POST['tipo_prenda'];
                $propietario = $_POST['propietario'];
                $color = $_POST['color'];
                $material = $_POST['material'];
                $departamento = $_POST['departamento'];
                $id_propietario = $_POST['id_propietario'];
                $codigo_inventario = $_POST['codigo_inventario'];

                // Inserta los datos en la base de datos, incluyendo la ruta de la imagen
                $stmt = $pdo->prepare("INSERT INTO prendas (tipo_prenda, propietario, color, material, departamento, id_propietario, codigo_inventario, imagen_prenda) 
                                       VALUES (?, ?, ?, ?, ?, ?, ?)");
                $stmt->execute([$tipo_prenda, $propietario, $color, $material, $departamento, $id_propietario, $codigo_inventario, $targetFile]);

                echo json_encode(['success' => 'Prenda y imagen guardados con éxito']);
            } else {
                echo json_encode(['error' => 'Hubo un error al subir la imagen']);
            }
        } else {
            echo json_encode(['error' => 'No se subió ninguna imagen']);
        }
    } else {
        try {
            // Si el método no es POST, solo muestra las prendas en formato JSON
            $stmt = $pdo->query("SELECT * FROM prendas");
    
            // Recoge los datos
            $prendas = $stmt->fetchAll(PDO::FETCH_ASSOC);    
            // Convierte la columna 'imagen_prenda' de bytea a Base64
            foreach ($prendas as &$prenda) {
                if (isset($prenda['imagen'])) {
                    // Verifica si la imagen es un recurso y la convierte
                    if (is_resource($prenda['imagen'])) {
                        $prenda['imagen'] = stream_get_contents($prenda['imagen']);
                    }
                    // Convierte los datos binarios a Base64
                    $prenda['imagen'] = base64_encode($prenda['imagen']);
                }
            }
    
            // Devuelve los datos como JSON
            echo json_encode($prendas);
        } catch (PDOException $e) {
            // Si ocurre un error, muestra el mensaje
            echo json_encode(['error' => $e->getMessage()]);
        }
    }
} catch (PDOException $e) {
    // Si ocurre un error, muestra el mensaje
    echo json_encode(['error' => $e->getMessage()]);
}
?>
