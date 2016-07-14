<?php
require('../includes/query_conf.php');

$data = null;
if (isset($_GET['score'])) {
  $data = $_GET['score'];
}
else if (isset($_GET['CUI'])) {
	$data = $_GET['CUI'];
}
else if (isset($_GET['model_by_riskfactors'])){
	$data = $_GET['model_by_riskfactors'];
}
else if (isset($_GET['model_by_id'])){
	$data = $_GET['model_by_id'];
	$ans['id'] = query("SELECT * FROM models WHERE id = " . (string)$data["id"]);
	echo(json_encode($ans));
	exit();
}
else if (isset($_GET['model_by_DOI'])){
	$data = $_GET['model_by_DOI'];
	
}
else {
	echo json_encode({
		'error' : 'bad request'
	});
}


?>