"use strict";

class BoxyPathDrawer {
    //parameters define bounding box + gridsize
    constructor(x,y,width,height,gridWidth,gridHeight,parentElement){
        this.x = x
        this.y = y
        this.width = width
        this.height = height
        this.gridWidth = gridWidth
        this.gridHeight = gridHeight
        this.pathElements = []
        this.parentElement = parentElement 
    }
    
    updatePath(path){
        this.erasePath()
        this.drawPath(path)
    }

    erasePath(){
        for(var element in this.pathElements) {
            this.parentElement.removeChild(element)
        }
        this.pathElements = []
    }

    drawPath(path){
        for(var coord in path){
            var element = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            element.setAttribute('x',this.x + path[coord].x * this.gridWidth)
            element.setAttribute('y',this.y + path[coord].y * this.gridHeight)
            element.setAttribute('width',this.gridWidth)
            element.setAttribute('height',this.gridHeight)
            element.setAttribute('class','path')
            this.pathElements.push(element)
            this.parentElement.appendChild(element)
        }
    }
}

