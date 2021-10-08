const canvas = document.querySelector('canvas');
const context = canvas.getContext('2d');


var nodes = [];
var edges = [];




function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.onresize = resize;
resize();

function drawNode(node) {
    context.beginPath();
    context.fillStyle = node.fillStyle;
    context.arc(node.x, node.y, node.radius, 0, Math.PI * 2, true);
    context.strokeStyle = node.strokeStyle;
    context.stroke();
    context.fill();
}

function draw(nodes, edges) {
    // context.clearRect(0, 0, window.innerWidth, window.innerHeight);

    for (let i = 0; i < edges.length; i++) {
        var fromNode = nodes[edges[i].from];
        var toNode = nodes[edges[i].to];
        context.beginPath();
        context.strokeStyle = fromNode.strokeStyle;
        context.moveTo(fromNode.x, fromNode.y);
        context.lineTo(toNode.x, toNode.y);
        context.stroke();
    }

    for (let i = 0; i < nodes.length; i++) {
        context.beginPath();
        let node = nodes[i];
        context.fillStyle = node.fillStyle;
        context.arc(node.x, node.y, node.radius, 0, Math.PI * 2, true);
        context.strokeStyle = node.strokeStyle;
        context.fill();
        context.stroke();
        context.font = "10px Arial";
        context.fillStyle = "black"
        context.fillText(`${node.id}`,node.x-2,node.y+4)
    }
}

function drawCircle(x,y){
    var radius = 5;  
    context.beginPath();
    context.arc(x, y, radius, 0, Math.PI*2, true);
    context.closePath();
    context.fillStyle = 'red';
    context.fill();
    context.lineWidth = 2;
    context.strokeStyle = '#003300';
    context.stroke(); 
}

function drawArrow(p1,p2,progress){
    var pathStarts={ x:p1.x, y:p1.y };
    var pathEnds={ x:p2.x, y:p2.y };
    var dx=pathEnds.x-pathStarts.x;
    var dy=pathEnds.y-pathStarts.y;
    var pathLength=Math.sqrt(dx*dx+dy*dy)-10;
    var pathAngle=Math.atan2(dy,dx);
    var arrowLineLength=10;
    var arrowLength=20;

    var traveled=(pathLength-arrowLineLength)*progress;

    // calculate the new starting point of the arrow-line
    var x0=pathStarts.x+traveled*Math.cos(pathAngle);
    var y0=pathStarts.y+traveled*Math.sin(pathAngle);
    var lineStart={x:x0,y:y0};

    // calculate the new ending point of the arrow-line
    var x1=pathStarts.x+(traveled+arrowLength)*Math.cos(pathAngle);
    var y1=pathStarts.y+(traveled+arrowLength)*Math.sin(pathAngle);
    var lineEnd={x:x1,y:y1};

    drawLineWithArrowhead(lineStart,lineEnd,arrowLineLength)
}
function drawLineWithArrowhead(p0,p1,headLength){

    // constants (could be declared as globals outside this function)
    var PI=Math.PI;
    var degreesInRadians225=225*PI/180;
    var degreesInRadians135=135*PI/180;
  
    // calc the angle of the line
    var dx=p1.x-p0.x;
    var dy=p1.y-p0.y;
    var angle=Math.atan2(dy,dx);
  
    // calc arrowhead points
    var x225=p1.x+headLength*Math.cos(angle+degreesInRadians225);
    var y225=p1.y+headLength*Math.sin(angle+degreesInRadians225);
    var x135=p1.x+headLength*Math.cos(angle+degreesInRadians135);
    var y135=p1.y+headLength*Math.sin(angle+degreesInRadians135);
  
    // draw line plus arrowhead
    context.beginPath();
    // draw the line from p0 to p1
    context.moveTo(p0.x,p0.y);
    context.lineTo(p1.x,p1.y);
    // draw partial arrowhead at 225 degrees
    context.moveTo(p1.x,p1.y);
    context.lineTo(x225,y225);
    // draw partial arrowhead at 135 degrees
    context.moveTo(p1.x,p1.y);
    context.lineTo(x135,y135);
    // stroke the line and arrowhead
    context.lineWidth = 4
    context.strokeStyle = 'black'
    context.stroke();
    context.lineWidth = 2
}


function render (progress,positions,i) {
    // console.log(p1.x)
    // var x = p1.x + progress * (p2.x - p1.x),
    //   y = p1.y + progress * (p2.y - p1.y);

    context.clearRect(0, 0, window.innerWidth, window.innerHeight);
    draw(nodes,edges);
    for(var j=0; j<positions.length; j++){
        var p1 = positions[j].p1
        var p2 = positions[j].p2
        var x = p1.x + progress * (p2.x - p1.x),
        y = p1.y + progress * (p2.y - p1.y);
        // drawCircle(x,y);
        drawArrow(p1,p2,progress)
    }
    context.font = "30px Arial";
    context.fillStyle = "black"
    context.fillText(`Round number ${i}`,500,500)

}


function startAnimation(positions, start, end, i){
     //one second of animation
    //  console.log(edge)
    // positions = []
    // for(var i=0; i<edges.length; i++){
    //     p1 = { x: nodes[edges[i].from].x, y: nodes[edges[i].from].y }, //start coordinates
    //     p2 = { x: nodes[edges[i].to].x, y: nodes[edges[i].to].y }; // end coordinates
    //     final = {p1: p1, p2: p2}
    //     positions.push(final)
    // }
    loop(positions, start, end, i)
}
function loop(positions, start, end, i) {
   
    var now = new Date().getTime(),
        progress = (now - start)/(end - start);
    // console.log(start, end, progress)

    if (progress >= 0 && progress <= 1) {
        render(progress,positions, i);
        window.requestAnimationFrame(function() {
            loop(positions,start, end, i)
        });
    }
    else{
        context.clearRect(0, 0, window.innerWidth, window.innerHeight);
        draw(nodes,edges);
        context.font = "30px Arial";
        context.fillStyle = "black"
        context.fillText(`Round number ${i}`,500,500)
    }
}


var ender
function gettingReadyForAnimation(i){
    positions = []
    for(let j=0; j<edges.length; j++){
        p1 = { x: nodes[edges[j].from].x, y: nodes[edges[j].from].y }, //start coordinates
        p2 = { x: nodes[edges[j].to].x, y: nodes[edges[j].to].y }; // end coordinates
        final = {p1: p1, p2: p2}
        positions.push(final)
    }

    // startAnimation(positions); 
    count = 0
    ender = setInterval(function(){
        var start = new Date().getTime(),
        end = start + 1000;
        if(count < 5){
            startAnimation(positions, start, end, i); 
        }
        if(count == 5){
            console.log(`hello filenumber ${i}`)
            clearInterval(ender)
            main(i+1)
        }
        count+=1
    }, 2000);
    
}

function main(i){

    var xhr = new XMLHttpRequest();
    xhr.open('HEAD', `http://127.0.0.1:8887/JSON/Lifetime_Tree/tree${i}.json`, false); //change file path here to access different trees
    xhr.send();
     
    if (xhr.status == "404") {
        alert("Simulation done")
    } else {
        fetch(`http://127.0.0.1:8887/JSON/Lifetime_Tree/tree${i}.json`) //change file path here to access different trees
        .then(response => {
            return response.json();
        })
        .then(data => {
            // draw(data.nodes,data.edges);
            // loop()
            nodes = data.nodes
            edges = data.edges
            gettingReadyForAnimation(i)
        });
    }

}

main(1)
