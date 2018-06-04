function litteShit() {
// lijntjes clickbaar maken - > ajaxrequest -> pubmed artikelen -> artikelen requesten
// nodes clickbaar maken ->  pubmed artikelen 

    var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var simulation = d3.forceSimulation()
    
	 .force("link", d3.forceLink().id(function (d) {return d.id;}))
    .force("charge", d3.forceManyBody().strength(-1000).distanceMin(250))
    .force("center", d3.forceCenter(width / 2, height / 2));

    var linkedByIndex = {};
    

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
      
     
    for (i = 0; i < graph.nodes.length; i++) {
    linkedByIndex[graph.nodes[i].id + "," + graph.nodes[i].id] = 1;
    };
    graph.links.forEach(function (d) {
    linkedByIndex[d.source.id + "," + d.target.id] = 1;
    });

    function neighboring(a, b) {
    return linkedByIndex[a.index + "," + b.index];
    }
    
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

function connTo(node) {
	var g = d3.select("svg").select(".links").selectAll("line");
	var ding = d3.select(".pb-10")
	
	if (selectedNodes.length > 0){
	return 0
	}
	
	selectedNodes = node.id
	
	
	var derp = {}
	derp[node.id] = 1
    
    console.log(linkedByIndex)
    
    
    
    g.each(function(d) {
        
        
    	if (d.source == node && !(derp[d.target])){
        	derp[d.target.id] = 1
        }
        if (d.target == node && !(derp[d.source])){
            derp[d.source.id] = 1
        }
        
    });
    
    d3.select("svg").select(".nodes").selectAll("g").each(function(item,index){
    
        if (!(derp[item.id])){
            
            console.log(item.id)
            console.log(derp)
            d3.select(this).style("visibility", "hidden");
        }    
    
    });
    
    g.each(function(d){   
        
        if (!(derp[d.source.id]) || !(derp[d.target.id])){
        
            d3.select(this).style("visibility","hidden");
        }    
        
    });

}

function linkClick( linkx ) {
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
    
  var1 = node1.id
  var2 = node2.id
  
  var var_str = "?1=" + var1 + "&2=" + var2;
  
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

function lineWidth(i){
    return 2 * (Math.log(i) / Math.log(10)) + 2;

}
var svgtje = document.getElementsByTagName("svg")[0];
svgtje.style.borderStyle = "solid";
}
