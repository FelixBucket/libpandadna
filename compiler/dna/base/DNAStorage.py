from dna.base.DNAPacker import *
from dna.components.DNASuitEdge import DNASuitEdge


class DNAStorage:
    def __init__(self):
        self.catalogCodes = {}        # {root: [code]}
        self.textures = {}            # {code: filename}
        self.fonts = {}               # {code: filename}
        self.nodes = {}               # {code: (filename, search)}
        self.hoodNodes = {}           # {code: (filename, search)}
        self.placeNodes = {}          # {code: (filename, search)}
        self.blockNumbers = []        # [blockNumber]
        self.blockZones = {}          # {blockNumber: zoneId}
        self.blockTitles = {}         # {blockNumber: title}
        self.blockArticles = {}       # {blockNumber: article}
        self.blockBuildingTypes = {}  # {blockNumber: buildingType}
        self.suitPoints = []          # [DNASuitPoint]
        self.suitPointMap = {}        # {DNASuitPoint.index: DNASuitPoint}
        self.suitEdges = {}           # {startPointIndex: [DNASuitEdge]}
        self.battleCells = []         # [DNABattleCell]

    def storeCatalogCode(self, root, code):
        self.catalogCodes.setdefault(root, []).append(code)

    def storeTexture(self, code, filename):
        self.textures[code] = filename

    def storeFont(self, font, code):
        self.fonts[code] = font
        
    def getFont(self, code):
        if not code in self.fonts:
            raise DNAError('no such font: %s' % code)
            
        return loader.loadFont(self.fonts.get(code))

    def storeNode(self, code, filename, search):
        self.nodes[code] = (filename, search)

    def storeHoodNode(self, code, filename, search):
        self.hoodNodes[code] = (filename, search)

    def storePlaceNode(self, code, filename, search):
        self.placeNodes[code] = (filename, search)

    def storeBlockNumber(self, blockNumber):
        self.blockNumbers.append(blockNumber)

    def storeBlockZone(self, blockNumber, zoneId):
        self.blockZones[blockNumber] = zoneId

    def storeBlockTitle(self, blockNumber, title):
        self.blockTitles[blockNumber] = title

    def storeBlockArticle(self, blockNumber, article):
        self.blockArticles[blockNumber] = article

    def storeBlockBuildingType(self, blockNumber, buildingType):
        self.blockBuildingTypes[blockNumber] = buildingType

    def storeSuitPoint(self, point):
        self.suitPoints.append(point)
        self.suitPointMap[point.index] = point

    def storeSuitEdge(self, startPointIndex, endPointIndex, zoneId):
        startPoint = self.suitPointMap[startPointIndex]
        endPoint = self.suitPointMap[endPointIndex]
        edge = DNASuitEdge(startPoint, endPoint, zoneId)
        self.suitEdges.setdefault(startPointIndex, []).append(edge)
        return edge

    def storeBattleCell(self, cell):
        self.battleCells.append(cell)

    def getBlock(self, name):
        return name[2:name.find(':')]

    def dump(self, verbose=False):
        packer = DNAPacker(name='DNAStorage', verbose=verbose)

        # Catalog codes...
        packer.pack('catalog code root count', len(self.catalogCodes), UINT16)
        for root, codes in self.catalogCodes.items():
            packer.pack('root', root, SHORT_STRING)
            packer.pack('root code count', len(codes), UINT8)
            for code in codes:
                packer.pack('code', code, SHORT_STRING)

        # Textures...
        packer.pack('texture count', len(self.textures), UINT16)
        for code, filename in self.textures.items():
            packer.pack('code', code, SHORT_STRING)
            packer.pack('filename', filename, SHORT_STRING)

        # Fonts are not packed since we don't need them (#12)
        packer.pack('font count', 0, UINT16)

        # Nodes...
        packer.pack('node count', len(self.nodes), UINT16)
        for code, (filename, search) in self.nodes.items():
            packer.pack('code', code, SHORT_STRING)
            packer.pack('filename', filename, SHORT_STRING)
            packer.pack('search', search, SHORT_STRING)

        # Hood nodes...
        packer.pack('hood node count', len(self.hoodNodes), UINT16)
        for code, (filename, search) in self.hoodNodes.items():
            packer.pack('code', code, SHORT_STRING)
            packer.pack('filename', filename, SHORT_STRING)
            packer.pack('search', search, SHORT_STRING)

        # Place nodes...
        packer.pack('place node count', len(self.placeNodes), UINT16)
        for code, (filename, search) in self.placeNodes.items():
            packer.pack('code', code, SHORT_STRING)
            packer.pack('filename', filename, SHORT_STRING)
            packer.pack('search', search, SHORT_STRING)

        # Blocks...
        packer.pack('block number count', len(self.blockNumbers), UINT16)
        for blockNumber in self.blockNumbers:
            packer.pack('number', blockNumber, UINT8)
            packer.pack('zone ID', self.blockZones[blockNumber], UINT16)
            title = self.blockTitles.get(blockNumber, '')
            packer.pack('title', title, SHORT_STRING)
            article = self.blockArticles.get(blockNumber, '')
            packer.pack('article', article, SHORT_STRING)
            buildingType = self.blockBuildingTypes.get(blockNumber, '')
            packer.pack('building type', buildingType, SHORT_STRING)

        # Suit points...
        packer.pack('suit point count', len(self.suitPoints), UINT16)
        for point in self.suitPoints:
            packer.pack('index', point.index, UINT16)
            packer.pack('type', point.pointType, UINT8)
            for component in point.pos:
                packer.pack('position', int(component * 100), INT32)
            packer.pack('landmark building index',
                        point.landmarkBuildingIndex, INT8)

        # Suit edges...
        packer.pack('suit edge count', len(self.suitEdges), UINT16)
        for startPointIndex, edges in self.suitEdges.items():
            packer.pack('start point index', startPointIndex, UINT16)
            packer.pack('edge count', len(edges), UINT16)
            for edge in edges:
                packer.pack('end point', edge.endPoint.index, UINT16)
                packer.pack('zone ID', edge.zoneId, UINT16)

        # Battle cells...
        packer.pack('battle cell count', len(self.battleCells), UINT16)
        for cell in self.battleCells:
            packer.pack('width', cell.width, UINT8)
            packer.pack('height', cell.height, UINT8)
            for component in cell.pos:
                packer.pack('position', int(component * 100), INT32)

        return packer
