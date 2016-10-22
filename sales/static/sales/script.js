var amountClicks = 1
function add(){
  var div = document.createElement('fieldset');
  div.innerHTML += '<select name="'+'selector' + amountClicks + '" id="'+'row' + amountClicks +'" onchange="changeFunc(value, this.id)"><option value="1">1 Ticket ${{ price1 }}</option><option value="2">3 Ticket Pack $3</option><option value="3">10 Ticket Pack $8</option></select><input name="ticket' + amountClicks.toFixed(1) + '" id="text'+amountClicks+'" placeholder="Ticket Number" type="text"><div id="contentrow'+amountClicks+'"></div>';
  document.getElementById("more").appendChild(div);
  amountClicks +=1;
}



function changeFunc($i, id) {
   if($i == 2){
    var div = document.getElementById("content"+id);
    var rest = id.slice(3);
    div.innerHTML += '<fieldset><input name='+ 'ticket' + rest + '.1' + ' placeholder="Ticket Number" type="text" ><input name='+ 'ticket' + rest + '.2' + ' placeholder="Ticket Number" type="text" >';
  } else if ($i == 1 || $i== 3) {
    var div = document.getElementById("contentrow"+id);
    div.innerHTML = "";
  }
}
