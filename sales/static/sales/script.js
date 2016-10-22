var amountClicks = 1
function add(){
  var div = document.createElement('fieldset');
  div.innerHTML += '<select id="'+'row' + amountClicks +'" onchange="changeFunc(value, this.id)"><option value="1">1 Ticket $2</option><option value="2">3 Ticket Pack $3</option><option value="3">10 Ticket Pack $8</option></select><input id="text'+amountClicks+'" placeholder="Ticket Number" type="text"><div id="contentrow'+amountClicks+'"></div>';
  document.getElementById("more").appendChild(div);
  amountClicks +=1;
}



function changeFunc($i, id) {
   if($i == 2){
    var div = document.getElementById("content"+id);
    div.innerHTML += '<fieldset><input placeholder="Ticket Number" type="text" ><input placeholder="Ticket Number" type="text" >';
  } else if ($i == 1 || $i== 3) {
    var div = document.getElementById("content"+id);
    div.innerHTML = "";
  }
}
