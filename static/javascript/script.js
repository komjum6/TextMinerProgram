function litteShit() {
// lijntjes clickbaar maken - > ajaxrequest -> pubmed artikelen -> artikelen requesten
// nodes clickbaar maken ->  pubmed artikelen 

    var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(100))
	//.force("link", d3.forceLink().id(function (d) {return d.id;}).distance(100).strength(1))
    .force("charge", d3.forceManyBody(100))
    .force("center", d3.forceCenter(width / 2, height / 2));


var abs_url = "http://cytosine.nl/~owe8_pg1/Clickme.wsgi/jsonrequesturl"
var url = abs_url

d3.json(url, function(error, graph) {
  if (error) throw error;

   var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return Math.sqrt(d.value); })
	 .on("click", function(d) { nodeClick(d); } );

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")
    
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

   function ticked() {
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

function nodeClick( linkx ) {
	var x = linkx.source
	var y = linkx.target
	
     //d3.select('h1').text(linkx.source.id + ":reee:"+linkx.target.id)
	 
	 loadDoc(x,y)
	 
    }

	
	
// group1 = Compound
// group2 = Crop
// group3 = Health_benefit	
function loadDoc(node1, node2) {
	
  var abs_url = "http://cytosine.nl/~owe8_pg1/Clickme.wsgi/getPMIDinfo"
	
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      
	  document.getElementById("linkPlace").innerHTML = this.responseText;
	  
	  
    }
  };
  
  if(node1.group == 1){type1 = "Compound"}
  if(node1.group == 2){type1 = "Crop"}
  if(node1.group == 3){type1 = "Health_benefit"}
  
  if(node2.group == 1){type2 = "Compound"}
  if(node2.group == 2){type2 = "Crop"}
  if(node2.group == 3){type2 = "Health_benefit"}
  
  var1 = node1.id
  var2 = node2.id
  
  var var_str = "?"+type1 + "=" + var1  + "&" + type2 +"=" + var2;
  
  
  
  xhttp.open("GET", abs_url+var_str, true);
  
  xhttp.send();
}

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
}
