function fileSelected() {
	document.getElementById('btn_upload').src = '/static/img/btn_uploadmore.png';

	//alert(oFile.value)
	var u = document.getElementById ("status_upload");
	var x = document.getElementById('file-input');
	var txt = "";
	if ('files' in x) {
		if (x.files.length == 0) {
			txt = "Select one or more files.";
		} else {
			if (x.files.length == 1) {
				document.getElementById ("msg_upload").innerHTML = x.files.length + ' file is selected.' 
			} else {
				document.getElementById ("msg_upload").innerHTML = x.files.length + ' files are selected.' 
			}
			for (var i = 0; i < x.files.length; i++) {
				var file = x.files[i];
				var textnode = document.createTextNode(file.name);
				var br = document.createElement("br");
				u.appendChild(textnode);
				u.appendChild(br);

//				txt += "<br><strong>" + (i+1) + ". file</strong><br>";
//				if ('name' in file) {
//					txt += "name: " + file.name + "<br>";
//				}
//				if ('size' in file) {
//					txt += "size: " + file.size + " bytes <br>";
//				}
			}
		}
	} 
}
