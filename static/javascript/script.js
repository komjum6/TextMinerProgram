function litteShit() {

    var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var simulation = d3.forceSimulation()
    
	 .force("link", d3.forceLink().id(function (d) {return d.id;}))
    .force("charge", d3.forceManyBody().strength(-1000).distanceMin(250))
    .force("center", d3.forceCenter(width / 2, height / 2));

    var linkedByIndex = {};
    
    //hardcoded de url van de json, omdat het berekenen van de inhoud hiervan cytosine intens belast
    var abs_url = "http://cytosine.nl/~owe8_pg1/static/javascript/data.json"
    
d3.json(abs_url, function(error, graph) {
  if (error) throw error;

   var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return lineWidth(d.value); })
	 .on("click", function(d) { linkClick(d); } );

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")
    .on("click", function(d) { connTo(d); } )
    
  var circles = node.append("circle")
      .attr("r", 10)
      .attr("fill", function(d) { return color(d.group); })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));	  

  var lables = node.append("text")
      .text(function(d) {
        return d.id;
      })
      .attr('x', 6)
      .attr('y', 3);

  node.append("title")
      .text(function(d) { return d.id; });

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

 simulation.force("link")
      .links(graph.links);
      
    // het aanmaken van een dictionary set achtig object om te bepalen of nodes buren van elkaar zijn.
    for (i = 0; i < graph.nodes.length; i++) {
    linkedByIndex[graph.nodes[i].id + "," + graph.nodes[i].id] = 1;
    };
    graph.links.forEach(function (d) {
    linkedByIndex[d.source.id + "," + d.target.id] = 1;
    });

    function neighboring(a, b) {
    return linkedByIndex[a.index + "," + b.index];
    }
    
   function ticked() { //functie voor het verplaatsen van nodes
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
        })
  }
});

//Functie voor het verbergen van alle nodes die geen verbinding hebben met de node die geselecteerd is
//Dit als een soort pseudo filtering die niet CPU intensief is, ook al is deze niet volledig correct volgens set-theorie
//Maar over het algemeen kan hier toch nuttige informatie uit gewonnen worden omdat bij datasets van dit formaat
//het alleen bij zeer obscure situaties optreed dat er niet minimaal 1 artikel bestaat waarin alle 3 de termen zitten
function connTo(node) {
	var g = d3.select("svg").select(".links").selectAll("line");
	var pb10 = d3.select(".pb-10")
	
	if (selectedNodes.length > 0){
	return 0
	}
	
	selectedNodes = node.id
	
	var nodeDic = {}
   
    g.each(function(d) { //loopen over alle lines om te bepalen welke verbonden aan welke zijn
        
    	if (d.source == node && !(nodeDic[d.target])){
        	nodeDic[d.target.id] = 1
        }
        if (d.target == node && !(nodeDic[d.source])){
            nodeDic[d.source.id] = 1
        }
        
    });
    
    d3.select("svg").select(".nodes").selectAll("g").each(function(item,index){ //loopen over alle nodes
    
        if (!(nodeDic[item.id])){

            d3.select(this).style("visibility", "hidden");
        }    
    
    });
    
    g.each(function(d){ //nogmaals lopen over alle lines om verbindingen potentieel weg te halen
        
        if (!(nodeDic[d.source.id]) || !(nodeDic[d.target.id])){
        
            d3.select(this).style("visibility","hidden");
        }    
        
    });

}
//Functie voor het klikken op linkjes als actionlistener om de source en target te bepalen
function linkClick( linkx ) {
	var x = linkx.source
	var y = linkx.target
	 
	 loadDoc(x,y)
	 
    }

//Functie voor het generen van een link naar pubmed met daarin de artikelen die relateren aan deze termen,
//Pubmed is bekend voor de bioloog en bevat een zeer goede mogelijkheid tot het sorteren van artikelen.
function loadDoc(lijst) {
	
  var abs_url = "http://cytosine.nl/~owe8_pg1/Clickme.wsgi/getPMIDinfo"
	
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      
	  document.getElementById("linkPlace").innerHTML = this.responseText;
	  
	  
    }
  };
    
    var arrayLength = lijst.length;
    
    var var_str = "?0=" + lijst[0].id; 
    
    for (var i = 1; i < arrayLength; i++) {
        var_str += "&" + i + "=" + lijst[i].id
    }  
 
  xhttp.open("GET", abs_url+var_str, true);
  xhttp.send();
}

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fx = Math.max(0, d.fx);
  d.fx = Math.min(945, d.fx);
  d.fy = d.y;
  d.fy = Math.max(0, d.fy);
  d.fy = Math.min(595, d.fy);
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fx = Math.max(0, d.fx);
  d.fx = Math.min(945, d.fx);
  d.fy = d3.event.y;
  d.fy = Math.max(0, d.fy);
  d.fy = Math.min(595, d.fy);
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = d3.event.x;
  d.fx = Math.max(0, d.fx);
  d.fx = Math.min(945, d.fx);
  d.fy = d3.event.y;
  d.fy = Math.max(0, d.fy);
  d.fy = Math.min(595, d.fy);
}
//Functie voor het bepalen van de dikte van de lijnen
function lineWidth(i){
    return 2 * (Math.log(i) / Math.log(10)) + 2;

}
var svgtje = document.getElementsByTagName("svg")[0];
svgtje.style.borderStyle = "solid";

//functie voor het herstellen van de grafiek naar de originele variant door alles weer zichtbaar te maken
function restore(){

selectedNodes = [];
var linez = d3.select("svg").select(".links").selectAll("line");
var nodez = d3.select("svg").select(".nodes").selectAll("g");

nodez.each(function(d){ 
    
    d3.select(this).style("visibility", "visible");
    
 });
 
linez.each(function(d){ 
    
    d3.select(this).style("visibility", "visible");
    
 });

}

window.onload = function() {
    document.getElementById("returnButton").onclick = function fun() {
        restore(); 
    }
}
}