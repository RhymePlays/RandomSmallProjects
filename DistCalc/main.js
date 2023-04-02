/*\
|--Variables Start--|
\*/
{
    var pointGrid = {}
    var lineGrid = {}
    var currentPointIndex = 0
    var currentLineIndex = 0
    var refreshPerXMiliSec = 1000
    var autoRefreshOn = false
}
/*\
|--Variables End--|
\*/



/*\
|--Rendering Start--|
\*/

{ // Element Creation and Populating
    function renderPointElems(){
        document.getElementById("pointLayer").innerHTML = ""
        for (index in pointGrid){
            let pointElem = document.createElement("div")
            
            pointElem.setAttribute("id", index)
            pointElem.setAttribute("class", "point")
            pointElem.style.backgroundColor = pointGrid[index].color
            pointElem.style.position = "absolute"
            pointElem.style.top = `${pointGrid[index].ypos-6}px`
            pointElem.style.left = `${pointGrid[index].xpos-6}px`

            let pnttxtElem = document.createElement("span")
            pnttxtElem.setAttribute("class", "pnttxt")
            pnttxtElem.style.color = pointGrid[index].color
            pnttxtElem.innerText = `${index}\nx:${pointGrid[index].xpos} y:${pointGrid[index].ypos}`
            pointElem.appendChild(pnttxtElem)
            
            document.getElementById("pointLayer").appendChild(pointElem)
        }
    }

    function renderLineElems(){
        document.getElementById("lineLayer").innerHTML = ""
        for (index in lineGrid){
            let lineElem = document.createElement("div")
            
            lineElem.setAttribute("id", index)
            lineElem.setAttribute("class", "line")
            lineElem.style.backgroundColor = lineGrid[index].color
            lineElem.style.position = "absolute"
            lineElem.style.top = `${((lineGrid[index].points.b.ypos + lineGrid[index].points.a.ypos)/2)-2}px`
            lineElem.style.left = `${((lineGrid[index].points.b.xpos + lineGrid[index].points.a.xpos)/2)-(lineGrid[index].length/2)}px`
            lineElem.style.width = `${lineGrid[index].length}px`
            lineElem.style.rotate = `${lineGrid[index].angle}deg`
            
            document.getElementById("lineLayer").appendChild(lineElem)
        }
    }
}

function renderWindow(){renderPointElems();renderLineElems()}

function autoRefresh(){
    if (autoRefreshOn){
        renderWindow()
    }
    setTimeout(autoRefresh, refreshPerXMiliSec)
}//autoRefresh()
/*\
|--Rendering End--|
\*/



/*\
|--Functions Start--|
\*/

{ // Grid Manipulation

    {
        function addPoint(xpos, ypos, color){
            currentPointIndex = currentPointIndex + 1
            pointGrid[`p${currentPointIndex}`] = {xpos: xpos, ypos: ypos, color: color}
            renderPointElems()
            meshPoints()
        }
        function clearPoints(){pointGrid = {};renderPointElems()}


        function drawLineBetween2Points(pointA, pointB){
            currentLineIndex = currentLineIndex + 1
            
            if ((typeof pointA) == "string"){
                let length = ((pointGrid[pointA].xpos - pointGrid[pointB].xpos)**2 + (pointGrid[pointA].ypos - pointGrid[pointB].ypos)**2)**(1/2)
                let angle = Math.atan((pointGrid[pointB].ypos - pointGrid[pointA].ypos)/(pointGrid[pointB].xpos - pointGrid[pointA].xpos))*(180/Math.PI)
                let points = {
                    a: {xpos: pointGrid[pointA].xpos, ypos: pointGrid[pointA].ypos},
                    b: {xpos: pointGrid[pointB].xpos, ypos: pointGrid[pointB].ypos}
                }
                lineGrid[`l${currentLineIndex}`] = {length, angle, points}

            }else if ((typeof pointA) == "object"){
                let length = ((pointA.xpos - pointB.xpos)**2 + (pointA.ypos - pointB.ypos)**2)**(1/2)
                let angle = Math.atan((pointB.ypos - pointA.ypos)/(pointB.xpos - pointA.xpos))*(180/Math.PI)
                let points = {
                    a: {xpos: pointA.xpos, ypos: pointA.ypos},
                    b: {xpos: pointB.xpos, ypos: pointB.ypos}
                }
                lineGrid[`l${currentLineIndex}`] = {length, angle, points}
            }
            
            renderLineElems()
        }
        function clearLines(){lineGrid = {};renderLineElems()}
    }

    function offsetGrids(offsetBy){
        for (index in pointGrid){
            pointGrid[index].xpos = pointGrid[index].xpos + offsetBy.xpos
            pointGrid[index].ypos = pointGrid[index].ypos + offsetBy.ypos
        }
        for (index in lineGrid){
            lineGrid[index].points.a.xpos = lineGrid[index].points.a.xpos + offsetBy.xpos
            lineGrid[index].points.a.ypos = lineGrid[index].points.a.ypos + offsetBy.ypos
            lineGrid[index].points.b.xpos = lineGrid[index].points.b.xpos + offsetBy.xpos
            lineGrid[index].points.b.ypos = lineGrid[index].points.b.ypos + offsetBy.ypos
        }
        renderWindow()
    }

    function clearWindow(){clearPoints();clearLines()}
}


{ // Input
    document.getElementById("clickable").addEventListener("click", (event)=>{addPoint(event.x, event.y, "white")});

    let mouseOldPos = {x: 0, y: 0}
    let mouseWheelHeld = false
    document.getElementById("clickable").addEventListener("mousedown", (event)=>{
        if (event.button==1){
            mouseOldPos = {x: event.x, y: event.y}
            mouseWheelHeld = true
        }
    });
    document.getElementById("clickable").addEventListener("mouseup", (event)=>{
        if (event.button==1){
            offsetGrids({xpos: event.x-mouseOldPos.x, ypos: event.y-mouseOldPos.y})
            mouseWheelHeld = false
        }
    });

    function uselessButton(){
        meshPoints()
    }
}


{ // Operations
    function calculateShortestDistance(){
        clearLines()
    
        let shortestPath = Infinity
        let shortestPathPoints = []
    
        let  = {a:"", b:""}
        for (index1 in pointGrid){
            for (index2 in pointGrid){
                if (pointGrid[index1] != pointGrid[index2]){
                    let dist = ((pointGrid[index1].xpos-pointGrid[index2].xpos)**2 + (pointGrid[index1].ypos-pointGrid[index2].ypos)**2)**(1/2)
                    if (dist < shortestPath){
                        shortestPath = dist
                        shortestPathPoints = [index1, index2]
                    }
                }
            }
        }
        drawLineBetween2Points(shortestPathPoints[0], shortestPathPoints[1])
    }

    function meshPoints(){
        clearLines()

        let checkedOnes = []
        
        for (index1 in pointGrid){
            for (index2 in pointGrid){
                if (pointGrid[index1]!=pointGrid[index2] && (checkedOnes.includes([index1, index2].sort().toString())==false)){
                    checkedOnes.push([index1, index2].sort().toString())
                    drawLineBetween2Points(index1, index2)
                }
            }
        }
    }
}

/*\
|--Functions End--|
\*/