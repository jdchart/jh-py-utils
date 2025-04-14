import copy
import networkx as nx
from PIL import Image, ImageDraw
import math

def network_to_image(graph, out_path, **kwargs) -> dict:

    gCopy = copy.copy(graph)
    pos = _apply_layout(gCopy, kwargs.get("pos_algo", "spring"))

    print("pos:")
    print(pos)

    imgWidth = kwargs.get("width", 1000)
    imgHeight = kwargs.get("height", 1000)
    sizeMinMax = kwargs.get("size_min_max", [int(math.floor(imgWidth / 200)), int(math.floor(imgWidth / 50))])
    bgCol = kwargs.get("bgCol", (250,250,250,0))
    edgeWidth = kwargs.get("edge_width", int(math.floor(imgWidth / 1000)))
    edgeCol = kwargs.get("edge_col", (185, 187, 189))
    nodeCol = kwargs.get("node_col", (124, 187, 217))
    nodeOutlineCol = kwargs.get("node_outline_col", (142, 146, 148))
    
    finalImg = Image.new('RGBA',(imgWidth, imgHeight), bgCol)
    draw = ImageDraw.Draw(finalImg)

    minMaxX = [None, None]
    minMaxY = [None, None]
    minMaxSize = [None, None]
    nodeInfo = {}

    # Process minMax for x y and collect neighbours.
    _parseMinMaxAndNeighbors(gCopy, pos, minMaxX, minMaxY, minMaxSize, nodeInfo)

    print("nodeinfo:")
    print(nodeInfo)

    # Rescale data and prepare return dict.
    outData = {"meta" : {"width" : imgWidth, "height" : imgHeight, "fileformat" : "png"}}    
    _rescaleData(pos, minMaxX, minMaxY, minMaxSize, nodeInfo, sizeMinMax, imgWidth, imgHeight, outData)

    # Draw edges:

    for source_id, target_id in G.edges():
        sourceInfo = outData[source_id]
        targetInfo = outData[target_id]
        draw.line(
            (
                sourceInfo["x"] + (sourceInfo["size"] * 0.5), 
                sourceInfo["y"] + (sourceInfo["size"] * 0.5), 
                targetInfo["x"] + (targetInfo["size"] * 0.5), 
                targetInfo["y"] + (targetInfo["size"] * 0.5)
            ),
            fill = edgeCol,
            width = edgeWidth
        )

    # Draw nodes:
    for item in pos:
        draw.ellipse(
            (outData[item]["x"], outData[item]["y"], outData[item]["x"] + outData[item]["size"], outData[item]["y"] + outData[item]["size"]),
            fill=nodeCol,
            outline=nodeOutlineCol,
            width = edgeWidth
        )
    
    finalImg.save(out_path,"PNG")

    return outData

def rescale(val, oldMin, oldMax, a, b):
    return a + (((val - oldMin) * (b - a)) / (oldMax - oldMin))

def _apply_layout(graph: nx.Graph, algo: str) -> dict:
    if algo == "spring":
        pos = nx.spring_layout(graph, seed=3068)
    elif algo == "circular":
        pos = nx.circular_layout(graph)
    elif algo == "fr":
        pos = nx.fruchterman_reingold_layout(graph)
    elif algo == "spectral":
        pos = nx.spectral_layout(graph)
    elif algo == "random":
        pos = nx.random_layout(graph)
    else:
        pos = nx.spring_layout(graph, seed=3068)
    return pos

def _parseMinMaxAndNeighbors(gr: nx.Graph, nodePositions: dict, mmX: list, mmY: list, mmSize: list, nodeInfoDict: dict) -> None:
    """Parse position data to get minMax's for x, y and size, and collect the number of neighbours."""

    for item in nodePositions:
        if mmX[0] == None:
            mmX[0] = nodePositions[item][0]
            mmX[1] = nodePositions[item][0]
            mmY[0] = nodePositions[item][1]
            mmY[1] = nodePositions[item][1]
            mmSize[0] = len(list(gr.neighbors(item)))
            mmSize[1] = len(list(gr.neighbors(item)))
        else:
            if nodePositions[item][0] < mmX[0]:
                mmX[0] = nodePositions[item][0]
            if nodePositions[item][0] > mmX[1]:
                mmX[1] = nodePositions[item][0]
            if nodePositions[item][1] < mmY[0]:
                mmY[0] = nodePositions[item][1]
            if nodePositions[item][1] > mmY[1]:
                mmY[1] = nodePositions[item][1]
            if len(list(gr.neighbors(item))) < mmSize[0]:
                mmSize[0] = len(list(gr.neighbors(item)))
            if len(list(gr.neighbors(item))) > mmSize[1]:
                mmSize[1] = len(list(gr.neighbors(item)))
        
        nodeInfoEntry = {
            "numNeighbours" : gr.degree[item],
            "label" : item
        }

        nodeInfoDict[item] = nodeInfoEntry

def _rescaleData(nodePositions: dict, mmX: list, mmY: list, mmSize: list, nodeInfoDict: dict, mmImgSize: list, imgW: int, imgH: int, outDataDict: dict) -> None:
    """Rescale data according to draw parameters"""
    
    for item in nodePositions:
        nodeSize = rescale(
            nodeInfoDict[item]["numNeighbours"], 
            mmSize[0], 
            mmSize[1],
            mmImgSize[0],
            mmImgSize[1]
        )
        nodeX = rescale(
            nodePositions[item][0],
            mmX[0],
            mmX[1],
            mmImgSize[1], imgW - mmImgSize[1]
        )
        nodeY = rescale(
            nodePositions[item][1],
            mmY[0],
            mmY[1],
            mmImgSize[1], imgH - mmImgSize[1]
        )

        outDataEntry = {
            "x" : nodeX,
            "y" : nodeY,
            "size" : nodeSize
        }
        outDataDict[item] = outDataEntry