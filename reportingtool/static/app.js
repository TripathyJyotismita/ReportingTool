function load() {
	//alert("Inside js");
	var mydata = JSON.parse(CLIENTDETAILS);
	//alert("Inside js1");
	x = []
	for (i = 0; i < mydata.length; i++) {x.push(mydata[i].CLIENT_NAME);}
	//alert('Inside js');
	var dynamicSelect = document.getElementById("Selector");
	if(dynamicSelect.length == 0){
	x.forEach(function(item){ 
        
                var newOption = document.createElement("option");
                newOption.text = item.toString();//item.whateverProperty

                dynamicSelect.add(newOption);

                //new select items should populated immediately...
        });
	}
	//x = [];
	//return x;
	//alert(mydata[0].name);
	//alert(mydata[0].age);
}