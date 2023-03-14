
// ajouter l'export de l'ordre de passation des sessions


var tab= [];
var tab_desorientation = [];

var etape_suiv;
var interval;
var interval_ajout;
var etape = 0;
var etape_max ;

// récupération des élèment HTML
var but = document.getElementById("but");
var div_im = document.getElementById("div_image");
var enquete;
var liste_im =[];

var session_liste =[1,2,3,4];
numero_session = 0;
const session = session_liste.sort((a, b) => 0.5 - Math.random());
var image;
/*
fonction ajout : permet connaitre l'image à t 
*/
function ajout(valeur){
  let date = Date.now()
  tab.push([date,valeur])
}




/*
fonction fin : création des fichiers d'export 
*/
function fin(){
  clearInterval(interval);
  let csvContent = "data:text/csv;charset=utf-8," +"time,etape\n"
    + tab.map(e => e.join(",")).join("\n");
  var encodedUri = encodeURI(csvContent);
  var link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  let nom = "resultat_enquete_"+enquete+"_session"+session[numero_session]+".csv"
  link.setAttribute("download", nom);
  document.body.appendChild(link); 
  link.click();
  if(numero_session <3){
    var r='<button id="lancement" onclick="lancement()">Session suivante</button>';
    $("#but").append(r);

    numero_session +=1;
    let chemin = "data/"+enquete+"/session_"+session[numero_session]+"/name_im.csv";
    liste_im = [];
    tab = [];
    etape = 0;
    $(document).ready(function() {
      $.ajax({
          type: "GET",
          url: chemin,
          dataType: "text",
          success: function(data) {processData(data);}
       });
    });

  }
  else{
    let csvContent = "data:text/csv;charset=utf-8," + session.join(",")
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    let nom = "ordre_session_"+enquete+".csv"
    link.setAttribute("download", nom);
    document.body.appendChild(link); 
    link.click();
  }
}

/*
fonction etape_suivante : fonction récursive, récupère les donnée de l'etape suivante et met à jour la carte 
*/
function etape_suivante(){
  if(etape < etape_max){

    etape += 1;
    div_im.innerHTML = ''
    image= document.createElement("img");
    image.src = "data/"+enquete+"/session_"+session[numero_session]+"/"+liste_im[etape];

    div_im.appendChild(image)
    // div_im.style.display = "block";
    ajout(liste_im[etape]);
    setTimeout(cache,3000);
  }else{
    fin()
  }
}

function cache(){
  div_im.innerHTML = ''
  // div_im.style.display = "none";
  ajout(false,0,0);

}
function lancement(){
  but.removeChild(document.getElementById("lancement"))
  div_im.innerHTML = ''
  image= document.createElement("img");

  image.src = "data/"+enquete+"/session_"+session[numero_session]+"/"+liste_im[etape];
  div_im.appendChild(image)
  // div_im.style.display = "block";
  setTimeout(cache,3000);
  interval = setInterval(etape_suivante, 4000) ;

  ajout(liste_im[etape]);
}

function debut(value) {
  but.removeChild(document.getElementById("E1"));
  but.removeChild(document.getElementById("E2"));
  var r='<button id="lancement" onclick="lancement()">Commencer</button>';
  $("#but").append(r);

  enquete = value;

  let chemin = "data/"+enquete+"/session_"+session[numero_session]+"/name_im.csv";
  $(document).ready(function() {
    $.ajax({
        type: "GET",
        url: chemin,
        dataType: "text",
        success: function(data) {processData(data);}
     });
  });

}


function processData(allText) {
  liste_im = allText.split(/\r\n|\n/);
  etape_max = liste_im.length-2;
}
  

