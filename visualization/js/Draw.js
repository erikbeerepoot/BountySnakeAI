"use strict";

class Rect {
	constructor(x,y,width,height){
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;	
	}
}

function drawGridInRect(rect,canvas,numRows,numCols){
	if(canvas.width % numCols != 0){
        throw new Error("Width must be evenly visible by number of cols");
	}

	if(canvas.height % numRows != 0){
        throw new Error("Height must be evenly visible by number of rows");
	}	

	var horizontalStride = canvas.width / numCols
	var verticalStride = canvas.height / numRows

	var ctx = canvas.getContext("2d");	
	for(var x = 0; x < canvas.width; x += horizontalStride){
		for(var y = 0; y < canvas.height; y += verticalStride){
			ctx.rect(x, y, horizontalStride, verticalStride);			
		}
	}
	ctx.lineWidth=0.25;
	ctx.stroke();
	
}

