<?php
$allowed =  array("doc", "pdf", "xls", "docx", "zip", "rar", "apk");
$uploaddir = 'docs/';
if(isset($_FILES['testname']['name'])){
	$uploadfile = $uploaddir . basename($_FILES['testname']['name']);
	$ext = pathinfo($uploadfile, PATHINFO_EXTENSION);
	if(!in_array($ext,$allowed) ) {
	    echo 'error';
	}else{
		if(move_uploaded_file($_FILES['testname']['tmp_name'], $uploadfile)){
			echo "Uploaded";
		}
	}
}else{
    echo "Not uploaded";
}

?>