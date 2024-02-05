




var map;

// initialisation des fond de carte OSM et géoportail 
var raster = new ol.layer.Tile({
  source: new ol.source.OSM(),
  // visible: false
});
var ignlayer = new ol.layer.Tile({
  // Preload infinity c'est pour éviter d'avoir des espaces blancs quand tu navigues sur la carte,
  // À la place, tu as des images pixelisés des données (à voir ce que tu préfères, tu peux l'enlever sinon)
  //preload: "Infinity",
  source: new ol.source.WMTS({
      url: "https://wxs.ign.fr/decouverte/geoportail/wmts",
      layer: "GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2",
      matrixSet: "PM",
      format: "image/png",
      style: "normal",
      dimensions: [256, 256],
      requestEncoding: "KVP",
      tileGrid: new ol.tilegrid.WMTS({
          origin: [-20037508, 20037508],
          resolutions: [
              156543.03392804103, 78271.5169640205, 39135.75848201024, 19567.879241005125, 9783.939620502562,
              4891.969810251281, 2445.9849051256406, 1222.9924525628203, 611.4962262814101, 305.74811314070485,
              152.87405657035254, 76.43702828517625, 38.218514142588134, 19.109257071294063, 9.554628535647034,
              4.777314267823517, 2.3886571339117584, 1.1943285669558792, 0.5971642834779396, 0.29858214173896974,
              0.14929107086948493, 0.07464553543474241
          ],
          matrixIds: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"],
      })
  }),
})

/* Déclaration des couches*/
var couches = [ignlayer]; 

map = new ol.Map({
  /* Appel des couches de la carte */

  layers: couches,
  /* Cible de la div map */
  target: 'map',
  /* Caractéristiques de la vue de la carte */
  view: new ol.View({
      center: ol.proj.fromLonLat([2.350260867376038, 48.852893162747485]),
      zoom: 10
  })
});
function controle(){
  var valeur = parseInt(document.getElementById("zoom").value);
  map.getView().setZoom(valeur)
}




  

