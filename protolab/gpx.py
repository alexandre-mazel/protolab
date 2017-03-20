# -*- coding: utf-8 -*-

#
# Handle gpx file (modify, visualize...)
# (c) 2016 A.Mazel
#

import copy
import datetime
import random
import time
import xml.dom.minidom # for xml parsing

#~ def long2km( rLong ):
    #~ """
    #~ convert a longitude to a km (from the 0,0 of the earth)
    #~ """
    #~ return rLong*20000/360

#~ def lat2km( rLat ):
    #~ """
    #~ convert a latitude to a km (from the 0,0 of the earth)
    #~ """
    #~ return rLat*20000/360
    
def distanceCoordLatLong2km( pt1, pt2 ):
    """
    convert 2 coordinates long/lat to a distance in km
    """
    #~ import geometry    
    #~ d = geometry.distance( [lat2km(pt1[0]), long2km(pt1[1])], [lat2km(pt2[0]), long2km(pt2[1])] )
    import math
    if isinstance( pt1, list ):
        la1, lo1 = pt1
        la2, lo2 = pt2
    else:
        la1 = pt1.la
        lo1 = pt1.lo
        la2 = pt2.la
        lo2 = pt2.lo
            
    #~ rDeltaLat= la1 - la2
    #~ rDeltaLon= lo1 - lo2
    #~ rCenterLat= ( la1 + la2) / 2
    #~ rCenterLatEnRadians = rCenterLat
    #~ d = math.sqrt( rDeltaLat*rDeltaLat + math.pow(math.cos( rCenterLatEnRadians )*rDeltaLon, 2) )    

    rlat1 = math.pi * la1 / 180
    rlat2 = math.pi * la2 / 180
    rlon1 = math.pi * lo1 / 180
    rlon2 = math.pi * lo2 / 180
 
    theta = lo1 - lo2
    rtheta = math.pi * theta/180
 
    dist = math.sin(rlat1) * math.sin(rlat2) + math.cos(rlat1) * math.cos(rlat2) * math.cos(rtheta)
    dist = math.acos(dist)
    dist = dist * 180/math.pi
    dist = dist * 60 * 1.1515
 
    dist = dist * 1.609344 # => km
    
    return dist
# distanceCoordLatLong2km - end

print distanceCoordLatLong2km( [48.73021, 9.34456], [48.72473,9.36872] )
    
def floatToStrComplete( f, nLimitToNbrDecimal = -1 ):
    """
    return the minimal string complete representation with at least 1 digit after the "."
    - nLimitToNbrDecimal: limit to n decimal after the comma
    """
    #~ intPart = int(f);
    #~ strOut = "%d." % intPart;
    #~ remaining = f-intPart;
    #~ bFirst = True;
    #~ while( remaining > 0.000001 or bFirst ):
        #~ bFirst = False;
        #~ print( "str: %s, remainging: %f" % (strOut, remaining))
        #~ remaining *=10;
        #~ intPart = int(remaining);
        #~ if( remaining > 0.999999 and remaining < 1. ):
            #~ intPart = 1;
        #~ strOut += "%d" % intPart;
        #~ remaining -= intPart;
    #~ return strOut;
    
    
    strFmt = "%12.9f";
    if( nLimitToNbrDecimal != -1 ):
        strFmt = "%%12.%df" % nLimitToNbrDecimal;
    strOut = strFmt % f;
    while( strOut[-1] == '0' and strOut[-2] != '.' ):
        strOut = strOut[:-1];
    while( strOut[0] == ' ' ):
        strOut = strOut[1:];        
    return strOut;
# floatToStrComplete - end

def timeToGpxTime( timeToConvert = None, bFileWritableFmt = False ):
    """
    convert a python time to a gpx string formated time.
    Return a string eg: "2014-09-02T08:33:01Z" 
    
    Z/UTC time is 2h sooner than paris summer time and perhaps 1h compared to winter time TODO: check it!
    
    - timeToConvert: python floating second time eg: 13123123.34 or None for current time
    """
    if( timeToConvert == None ):
        timeToConvert = time.time();
        
    dt = datetime.datetime.fromtimestamp(timeToConvert) # fromtimestamp: no zone 'naive', utcfromtimestamp: use local timezone and convert to utc
    #~ print( "DBG: timeToGpxTime: dt tz: %s" % dt.tzinfo );
    if( not bFileWritableFmt ):
        strTimeStamp = dt.strftime( "%Y-%m-%dT%H:%M:%SZ" );    
    else:
        strTimeStamp = dt.strftime( "%Y_%m_%d__%H_%M_%S" );    
    #~ print( "DBG: timeToGpxTime: %s => %s" % (timeToConvert,strTimeStamp) );
    return strTimeStamp;
    
def gpxTimeToDateTime( timeToConvert ):
    """
    convert a GpxTime to a DateTime Object
    - timeToConvert: a string eg: "2014-09-02T08:33:01Z" 
    """    
    dt = datetime.datetime.strptime( timeToConvert, "%Y-%m-%dT%H:%M:%SZ");
    return dt;
    
def gpxTimeToTime( timeToConvert ):
    """
    convert a GpxTime to a time Object
    - timeToConvert: a string eg: "2014-09-02T08:33:01Z" 
    """    
    dt = gpxTimeToDateTime( timeToConvert );
    dt.replace(tzinfo = None);
    t = time.mktime(dt.timetuple()) + dt.microsecond / 1E6 # using utctimetuple or just timetuple
    return t;
    
def timeToStr( t ):
    """
    return a time in sec to a string
    """
    rCent = int( (t - int(t)) * 1000 )
    t = int(t)
    rSec = t % 60
    t = (t - rSec)/60
    rMin = t % 60
    t = (t - rMin)/60    
    rHour = t % 24
    t = (t - rMin)/24
    strOut = ""
    if t > 0:
        strOut += "%dj" % t
    if rHour > 0:
        strOut += "%dh" % rHour
    if rMin > 0:
        strOut += "%dm" % rMin
    if rSec > 0:
        strOut += "%ds" % rSec
    if rCent > 0:
        strOut += "%03d" % rCent
    return strOut
#~ def timeToGpxTime( timeToConvert ):
    #~ """
    #~ convert a time to a Gpx Time
    #~ - timeToConvert: a string eg: "2014-09-02T08:33:01Z" 
    #~ """ 
    
    #~ dt = datetime.fromtimestamp(timeToConvert)
    #~ return 

    
def domNodeTypeToString( nodeType ):
    dicNodeType = {
        xml.dom.minidom.Node.ATTRIBUTE_NODE: "AttributeNode",
        xml.dom.minidom.Node.CDATA_SECTION_NODE: "CDataSectionNode",
        xml.dom.minidom.Node.COMMENT_NODE: "CommentNode",
        xml.dom.minidom.Node.DOCUMENT_FRAGMENT_NODE: "DocumentFragmentNode",
        xml.dom.minidom.Node.DOCUMENT_NODE: "DocumentNode",
        xml.dom.minidom.Node.DOCUMENT_TYPE_NODE: "DocumentTypeNode",
        xml.dom.minidom.Node.ELEMENT_NODE: "ElementNode",
        xml.dom.minidom.Node.ENTITY_NODE: "EntityNode",
        xml.dom.minidom.Node.ENTITY_REFERENCE_NODE: "EntityReferenceNode",
        xml.dom.minidom.Node.NOTATION_NODE: "NotationNode",
        xml.dom.minidom.Node.PROCESSING_INSTRUCTION_NODE: "ProcessingNode",
        xml.dom.minidom.Node.TEXT_NODE: "TextNode",
    };
    try:
        return dicNodeType[nodeType]
    except: pass
    return "Unknow type node";

def domAttributesToString( attributes, nNbrTabToAdd = 0 ):
    """
    return a string describing all attributes of a node
    """
    if( attributes == None ):
        return "None";
    strOut = "%d attribute(s):\n" % attributes.length;
    for i in range(attributes.length):
        attr = attributes.item(i);
        strOut += "%s- %s:'%s'\n" % ("    " * nNbrTabToAdd, attr.name, attr.value );
    return strOut;
# domAttributesToString - end

def domNodeToString( node, nDepth = 0, aListChildParentNum = [], aListChildParentName = [], bRecurse = True ):
    "print a node list to a string" 
    strTab = "    " *  nDepth;
    if( nDepth > 0 ):
        strTab += "| ";
    strOut = strTab + "--------------------\n";
    if( node == None ):
        return strTab + "None!";
    try:
        strOut += strTab + "nodeType: %d (%s)\n" % ( node.nodeType, domNodeTypeToString( node.nodeType ) );
    except BaseException, err:
        print( "WRN: domNodeToString: nodeType: %s" % err );
        
    try:
        strOut += strTab + "localName: '%s'\n" % node.localName;
    except: pass
    
    try:
        strOut += strTab + "nodeName: '%s'\n" % node.nodeName;
    except: pass
    
    try:
        strOut += strTab + "nodeValue: '%s'\n" % node.nodeValue;
    except: pass
    
    try:
        strOut += strTab + "nodeData: '%s'\n" % node.nodeData;
    except: pass
    
    try:
        strOut += strTab + "attr name: '%s'\n" % node.getAttribute( "name" );
    except: pass
    
    try:
        strOut += strTab + "attributes: '%s'\n" % domAttributesToString(node.attributes, nNbrTabToAdd = nDepth+1);
    except BaseException, err:
        print( "WRN: domNodeToString: attributes: %s" % err );
        
    try:
        if( node.prefix != None ):
            strOut += strTab + "prefix: '%s'\n" % node.prefix;
    except: pass

        
#            try:
    if( node.hasChildNodes() ):
            strOut += strTab + "Child(s): %d child(s):\n" % len( node.childNodes );
            if( bRecurse ):            
                nNumChild = 1;
                aListChildParentName.append( node.localName );
                strTotalPath = "";
                for name in aListChildParentName:
                    strTotalPath += "/%s" % name;
                for nodeChild in node.childNodes:
                    strChildNumberParentPrefix = "";
                    for number in aListChildParentNum:
                        strChildNumberParentPrefix += "%d." % number;
                    aListChildParentNum.append( nNumChild );
                    strOut += strTab + "Child " + strChildNumberParentPrefix + str(  nNumChild ) + " (%s):\n" % strTotalPath+ domNodeToString( nodeChild, nDepth + 1, aListChildParentNum, aListChildParentName );
                    aListChildParentNum.pop();
                    nNumChild += 1;
                aListChildParentName.pop();
    strOut += "    " *  nDepth + "--------------------\n";
    return strOut;
# domNodeToString - end
    
    
def findElementByName( node, strName ):
    nodes = [];
    for subnode in node.childNodes:
        if( subnode.nodeName == strName ):
            nodes.append( subnode );
        else:
            nodes.extend( findElementByName( node = subnode, strName = strName ) );
    return nodes;
# findElementByName - end

def domNodeGetFirstValue( node ):
    """
    return the first node with a value, try this one, then child one by one (search depth first)
    return None, if no node with value found
    """
    #~ print( "domNodeGetFirstValue: node.nodeValue: %s" % str(node.nodeValue));
    if( node.nodeValue != None ):
        return node.nodeValue;
    if( node.hasChildNodes() ):
        for nodeChild in node.childNodes:
            strValue = domNodeGetFirstValue( nodeChild )
            if( strValue != None ):
                return strValue;
    return None;
# domNodeGetFirstValue - end

def findFirstValueFromElementByName( nodes, strName, nElementIndex = 0 ):
    """
    find element by name, then in the nth, find the first valid value
    Param:
    - nElementIndex: when element are found by Name, which one to take?
    Return: a string containing the value or None if no element by name OR no nth element or no value in the element
    """
    nodes = findElementByName( nodes, strName );
    if( len(nodes) > nElementIndex ):
        return domNodeGetFirstValue(nodes[nElementIndex]);
    return None;
# findFirstValueFromElementByName - end

def domFindElement( node, strElementName ):
    "find a child by its name"
    if( not node.hasChildNodes() ):
        if(  node.nodeName == strElementName ):
            return node;
    else:
        for nodeChild in node.childNodes:
            if( nodeChild.nodeName == strElementName ):
                return nodeChild;
    return None;
# domFindElement - end

def domFindElementByPath( node, astrElementPathName ):
    """find a child of a child of a child... by its name tree"""
    """eg: ["starting-condition", "condition", "script_type"] """
    element = node;
    for name in astrElementPathName:
        element = domFindElement( element, name );
        if( element == None ):
            print( "WRN: domFindElementByPath: while looking for path: '%s', failure while finding element named '%s'" % (astrElementPathName,name) );
            return None;
    return element;
# domFindElementByPath - end


class Pt:
    def __init__( self, t, la, lo, el ):
        """
        dt, la, lo, el: time object in local area, latitude, longitude, elevation in meter
        """
        self.t = t # the time as a float (python-time style)
        self.la = la
        self.lo = lo
        self.el = el
        
    def __str__( self ):
        strOut = "";
        strOut += "-- t: %s\n" % timeToGpxTime( self.t );
        strOut += "-- la: %s\n" % self.la; # lat: le Y
        strOut += "-- lo: %s\n" % self.lo; # long: le X
        strOut += "-- el: %s\n" % self.el;        
        return strOut;
        
class Gpx:
    """
    gpx file store gps walk or tracks.
    This class is to manipulate this kind of file: open/read/save/generate...
    Manipulate gpx file (tracks or gps walk)
    """
    def __init__( self ):
        self.reset();
        
    def getCreatorDefaultName( self ):
        return "ProtoWatch";
        
    def reset( self ):
        self.strCreator = self.getCreatorDefaultName();
        self.strGpxVersion = "1.1";
        self.strns = "http://www.topografix.com/GPX/1/1";
        self.strsxi = "http://www.w3.org/2001/XMLSchema-instance";
        self.strSchemaLocation = "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd";
        self.strName = "(noname)";
        self.time = time.time();        # a python time object converted to local area
        self.listPts = [];  # for each item,  a Pt point
        
    def copy( self, rhs ):
        self.strCreator = rhs.strCreator[:]
        self.strGpxVersion = rhs.strGpxVersion[:]
        self.strns = rhs.strns[:]
        self.strsxi = rhs.strsxi[:]
        self.strSchemaLocation = rhs.strSchemaLocation[:]
        self.strName = rhs.strName[:]
        self.time = rhs.time;
        self.listPts = copy.deepcopy( rhs.listPts );
        
    def __str__( self ):
        strOut = "";
        strOut += "- Creator: %s\n" % self.strCreator;
        strOut += "- Name: %s\n" % self.strName;
        strOut += "- Time: %s\n" % timeToGpxTime( self.time );
        strOut += "- listPts: len: %d\n" % len(self.listPts);
        for i in range(4):
            if( len(self.listPts) > i ):
                strOut += "- pt%d:\n%s\n" % (i,str(self.listPts[i]));
        strOut += "- pt-1:\n%s\n" % (str(self.listPts[-1]));
        return strOut;
        
    def nodeToStr( self, node ):
        #~ print( dir(node))
        strOut = "node: ";
        if( hasattr( node, "nodeValue" ) and node.nodeValue != None ):
            strOut += "value: 0x%x" % ord(node.nodeValue[0]);
        else:
            strOut += "value: None";
        if( hasattr( node, "nodeType" ) ):
            strOut += ", nodeType: %d: %s" % (node.nodeType,domNodeTypeToString( node.nodeType ));
        if( node.nodeType != xml.dom.minidom.Node.TEXT_NODE and node.nodeType != xml.dom.minidom.Node.DOCUMENT_NODE  ):
            if( node.hasAttribute( "name" ) ):
                strOut += ", name: " + node.getAttribute( "name" );
            #strOut += ", attributes: " + str(node.attributes);
            if( node.hasAttribute( "data" ) ):
                strOut += ", data: " + node.data;
        else:
            strOut += ", type: " + "TEXT";
            strOut += ", name: " + node.nodeName;

        
        
        strOut += ", raw: %s" % str(node);
        return strOut;
        
    def read( self, strFilename ):
        gpx = xml.dom.minidom.parse( strFilename );
        #~ print(dir(xml.dom.minidom.Node));        
        #~ print gpx.childNodes[0]
        #~ print(dir(gpx.childNodes[0].childNodes[0]))
        
        self.reset();
        
        #print( "header: %s" % self.nodeToStr(gpx) );
        #print( domNodeToString( gpx, bRecurse=True ))
        #print( dir( gpx))
        strTime = domNodeGetFirstValue( domFindElementByPath( gpx, ["gpx", "metadata","time"] ) );
        self.time = gpxTimeToTime(strTime)
        self.strName = findFirstValueFromElementByName( gpx, "name" ); # or gpx/trk/name
        self.strCreator = gpx.childNodes[0].getAttribute("creator");
        
        track = domFindElementByPath( gpx, ["gpx", "trk"] )
        for segment in track.childNodes:
            if( segment.localName == "trkseg" ):
                print( "INF: importing one track..." );
                #~ print( domNodeToString( segment ) );
                for ptNode in segment.childNodes:
                    if( ptNode.localName == "trkpt" ):
                        la = float( ptNode.getAttribute("lat") );
                        lo = float( ptNode.getAttribute("lon") );
                        el = float( findFirstValueFromElementByName( ptNode, "ele" ) );
                        t = findFirstValueFromElementByName( ptNode, "time" );
                        t = gpxTimeToTime( t );
                        pt = Pt( t, la, lo, el );
                        self.listPts.append( pt );
                    
                print( "INF: gpx.read: found %d pts..." % len(self.listPts) );
                
        #~ for node in gpx.childNodes[0].childNodes:
            #~ print( self.nodeToStr( node ) );

        
    def changeCreator( self, strName = None ):
        if( strName == None ):
            strName = self.getCreatorDefaultName();
        print( "INF: Gpx.changeCreator: changing creator name from '%s' to '%s'" % (self.strCreator, strName) );
        self.strCreator = strName;

    def changeName( self, strName ):
        self.strName = strName;
        
    def modify( self, rRatio = 0.01 ):
        """
        modify the track slightly to looks like "another track" but at quite same speed
        """
        for i in range( len(self.listPts) ):
            if( ( i == 0 or random.random() > 0.5 ) and i != len(self.listPts)-1 ):
                # modify the point in direction to the future
                dx = self.listPts[i+1].la - self.listPts[i].la
                dy = self.listPts[i+1].lo - self.listPts[i].lo
            else:
                # modify the point in direction to the past
                dx = self.listPts[i-1].la - self.listPts[i].la
                dy = self.listPts[i-1].lo - self.listPts[i].lo
            lendiff = random.random() * rRatio;
            x = self.listPts[i].la +dx*lendiff;
            y = self.listPts[i].lo +dy*lendiff;
            self.listPts[i].la = x;
            self.listPts[i].lo = y;            
    # modify - end
    
    def modifySpeed( self, rDurationRatio = 0.5 ):
        """
        modify the duration of a track
        - rDurationRatio: [0.01 to inf] eg: 0.5 => speed * 2
        """
        if( len(self.listPts) < 2 ):
            return;
            
        rDurationRatio = float(rDurationRatio)
        
        if( rDurationRatio < 0.001 ):
            rDurationRatio = 0.001;

            
        newPts = [];
        rDuration = self.listPts[-1].t - self.listPts[0].t;
        nNewDuration = int(rDuration * rDurationRatio);
        print( "INF: Gpx.modifySpeed: rDuration: %f, nNewDuration: %d" % (rDuration,nNewDuration) );
        
        nIdxCurrent = 0; # the first point from which to leave
        newPts.append( self.listPts[0] );
        rSimulatedReplayTime = self.listPts[0].t; # le temps pour relire dans le flux original en interpolant
        for i in range( 1, nNewDuration ):
            rSimulatedReplayTime = self.listPts[0].t + (i/rDurationRatio); # for each second, we should add the ratio
            #~ print( "rSimulatedReplayTime: %5.2f, nIdxCurrent: %d, listPts[nIdxCurrent].t: %f, listPts[nIdxCurrent+1].t: %f" % (rSimulatedReplayTime,nIdxCurrent,self.listPts[nIdxCurrent].t, self.listPts[nIdxCurrent+1].t) );
            # find first check prior to current replay time
            while( rSimulatedReplayTime >= self.listPts[nIdxCurrent+1].t ):
                #~ print( "rSimulatedReplayTime: %5.2f, nIdxCurrent: %d, listPts[nIdxCurrent].t: %f, listPts[nIdxCurrent+1].t: %f" % (rSimulatedReplayTime,nIdxCurrent,self.listPts[nIdxCurrent].t, self.listPts[nIdxCurrent+1].t) );
                nIdxCurrent +=1;
            rRatioInterpolate = ( rSimulatedReplayTime - self.listPts[nIdxCurrent].t ) / ( self.listPts[nIdxCurrent+1].t - self.listPts[nIdxCurrent].t )  
            #~ print( "interpolating %5.2f between index %d and %d" % (rRatioInterpolate,nIdxCurrent,nIdxCurrent+1) );
            t = newPts[0].t + i;
            la = self.listPts[nIdxCurrent].la + (self.listPts[nIdxCurrent+1].la-self.listPts[nIdxCurrent].la) * rRatioInterpolate;
            lo = self.listPts[nIdxCurrent].lo + (self.listPts[nIdxCurrent+1].lo-self.listPts[nIdxCurrent].lo) * rRatioInterpolate;
            el = self.listPts[nIdxCurrent].el + (self.listPts[nIdxCurrent+1].el-self.listPts[nIdxCurrent].el) * rRatioInterpolate;
            p = Pt( t, la, lo, el );
            newPts.append( p );
        p = Pt( newPts[0].t+nNewDuration, self.listPts[-1].la, self.listPts[-1].lo, self.listPts[-1].el );
        newPts.append( p );
        self.listPts = newPts;
    # modifySpeed - end
    
    def computeTotalTime( self ):
        return self.listPts[-1].t - self.listPts[0].t
    
    def computeDistance( self ):
        import geometry
        rDist = 0
        for i in range( 1, len(self.listPts) ):
            #~ dla = self.listPts[i].la - self.listPts[i-1].la
            #~ dlo = self.listPts[i].lo - self.listPts[i-1].lo
            #~ dla = lat2km( dla )
            #~ dlo = lat2km( dlo )
            #~ inc = geometry.distance( [lat2km(self.listPts[i-1].la), long2km(self.listPts[i-1].lo)], [lat2km(self.listPts[i].la), long2km(self.listPts[i].lo)] )
            inc = distanceCoordLatLong2km( self.listPts[i-1], self.listPts[i] )
            rDist += inc
        return rDist
        
    def computeAvgPace( self ):
        """
        return pace in second (how much second to make 1km)
        """
        d = self.computeDistance()
        t = self.computeTotalTime()
        return t/d
    
    def computePaceSplited( self, rLenSplit = 1., bOutputInStr = True ):
        """
        compute avg pace over every segment
        - rLenSplit: change length of a split (default 1km)
        """
        tBegin = self.listPts[0].t
        d = 0.
        tinc = 0 # t incremented from point to point
        bPauseDetected = False
        splits = []
        for i in range( 1, len(self.listPts) ):
            inc = distanceCoordLatLong2km( self.listPts[i-1], self.listPts[i] )
            d += inc
            if( inc > 0.001 ):
                tinc += self.listPts[i].t - self.listPts[i-1].t
            else:
                # pause detected
                #~ print( "pause..." ) # happens very rarely...
                bPauseDetected = True
            
            if( d >= rLenSplit or i == len(self.listPts)-1 ):
                t = self.listPts[i].t - tBegin
                v = t/d
                if bPauseDetected:
                    vWithoutPause = tinc/d
                    print( "DBG: split sans pause: %s" % timeToStr( vWithoutPause ) )
                if bOutputInStr:
                    v = timeToStr( v )
                splits.append(v)
                d = 0
                tinc = 0
                bPauseDetected = False
                tBegin = self.listPts[i].t
        return splits
    # computePaceSplited - end
        
    
    def modifyDate( self, nNbrSecondToAdd = 60*60):
        """
        add a time decay to a full track
        """
        self.time += nNbrSecondToAdd;
        for i in range( len(self.listPts) ):
            self.listPts[i].t += nNbrSecondToAdd;
    # modifyDate - end
        
    def write( self, strFilename ):
        """        
        - strFilename: if it's a folder name (end by /), will generate the name from it's date and name
        Return the name of the filename
        """
        if( strFilename[-1] == '/' ):
            strFilename += timeToGpxTime(self.time, bFileWritableFmt = True ) + "__" + self.strName + ".gpx";
            
        print( "INF: gpx.write: writing to '%s'..." % strFilename );
            
        file = open( strFilename, "wt" )
        file.write( "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" );
        file.write( "<gpx creator=\"%s\" version=\"%s\" xmlns=\"%s\" xmlns:xsi=\"%s\" xsi:schemaLocation=\"%s\">\n" % (self.strCreator, self.strGpxVersion,self.strns,self.strsxi,self.strSchemaLocation) );
        file.write( " <metadata>\n" );
        file.write( "  <time>%s</time>\n" % timeToGpxTime(self.time) );
        file.write( " </metadata>\n" );
        file.write( " <trk>\n");
        file.write( "  <name>%s</name>\n" % self.strName );        
        file.write( "  <trkseg>\n" );
        for pt in self.listPts:
            file.write( "   <trkpt lat=\"%s\" lon=\"%s\">\n" % ( floatToStrComplete(pt.la), floatToStrComplete(pt.lo) ) );
            file.write( "    <ele>%s</ele>\n" % floatToStrComplete(pt.el, nLimitToNbrDecimal=1) );
            file.write( "    <time>%s</time>\n" % timeToGpxTime(pt.t) );
            file.write( "   </trkpt>\n" );

        file.write( "  </trkseg>\n" );
        file.write( " </trk>\n" );
        file.write( "</gpx>\n" );    
        
        file.close();
        
        return strFilename;
    # write - end
    
    def printInfo( self ):
        print( "Total Time: %s" %  timeToStr(self.computeTotalTime()) )
        print( "Total distance: %s" % self.computeDistance() )
        print( "Avg pace: %s" % timeToStr(self.computeAvgPace()) )
        print( "Split: %s" % self.computePaceSplited() )
    # printInfo - end
    
    def render( self, img = None, colorTrace = (255,0,0) ):
        """
        render the track and return a cv2 image
        - img: an image to write in
        """
        import cv2
        import numpy        
        nSizeX = 2048
        nSizeY = 1400
        nMargin = 20
        nRealSizeX = nSizeX - nMargin*2
        nRealSizeY = nSizeY - nMargin*2
        if( img == None ):
            img = numpy.zeros((nSizeY,nSizeX,3), numpy.uint8)
            img[::] = (255,255,255)
        
        # find min & max
        minX = self.listPts[0].lo
        maxX = self.listPts[0].lo
        minY = self.listPts[0].la
        maxY = self.listPts[0].la
        for pt in self.listPts:
            if( pt.lo > maxX ):
                maxX = pt.lo
            if( pt.lo < minX ):
                minX = pt.lo
            if( pt.la > maxY ):
                maxY = pt.la
            if( pt.la < minY ):
                minY = pt.la
                
        px = None
        pY = None
        for pt in self.listPts:
            x = (int)( (pt.lo-minX)*nRealSizeX/(maxX-minX) )+nMargin
            y = nSizeY-1-( (int)( (pt.la-minY)*nRealSizeY/(maxY-minY) )+nMargin )
            
            cv2.circle( img, (x, y), 2, (0,0,0) )
            if( px != None ):
                cv2.line( img, (px, py), (x, y), colorTrace, 1, 1 )
            px = x
            py = y
            
        return img
        
    # render - end
    
    def correctGps( self ):
        for i in range( 1, len(self.listPts)-1 ):
            inc = distanceCoordLatLong2km( self.listPts[i-1], self.listPts[i] )/(self.listPts[i].t-self.listPts[i-1].t)
            # 20km/h => 5.5m /sec
            if inc > 0.005:
                rLissage = 0.8
                if inc > 0.012:
                    rLissage = 0.95
                #~ self.listPts[i].la = self.listPts[i-1].la * rLissage + self.listPts[i].la * (1.-rLissage)
                #~ self.listPts[i].lo = self.listPts[i-1].lo * rLissage + self.listPts[i].lo * (1.-rLissage)
                    
                medla = ( self.listPts[i-1].la+self.listPts[i+1].la) / 2
                medlo = ( self.listPts[i-1].lo+self.listPts[i+1].lo) / 2
                self.listPts[i].la = medla * rLissage + self.listPts[i].la * (1.-rLissage)
                self.listPts[i].lo = medlo * rLissage + self.listPts[i].lo * (1.-rLissage)
        
    
# class Gpx - end

def generateWeek( strMondayDate ):
    """
    Generate a week of commuting based on two reference
    - strMondayDate: monday date well formated eg: "2015-03-19"
    """
    nNbrSecPerDay = 60*60*24;
    nWinterToSummer = 0;
    #~ nWinterToSummer = -2*60*60; # enable this when ref is in winter and week in summer
    for strRefName in ["2015_03_19__Morning_Ride_ref","2015_03_19__Evening_Ride_ref"]:    
        strName = "candi-issy";
        bEvening = "Evening" in strRefName;
        if( bEvening ):
            strName = "issy-candi";
        gpx = Gpx();
        gpx.read( "../data/gpx/%s.gpx" % strRefName );        
        # found nbr different day
        dt = datetime.datetime.strptime( strMondayDate, "%Y-%m-%d");
        tMonday = time.mktime(dt.timetuple()) + dt.microsecond / 1E6 # using utctimetuple or just timetuple
        nNbrDiffDay = 0;
        if( tMonday < gpx.time ):
            nNbrDiffDay = -int(( gpx.time - tMonday ) /nNbrSecPerDay);
        else:
            nNbrDiffDay = int( ( tMonday - gpx.time ) /nNbrSecPerDay );
            nNbrDiffDay += 1; # for partial day
        print( "nNbrDiffDay between ref and monday: %s" % nNbrDiffDay );
        
        for i in range(5):
            gpxNew = Gpx();
            gpxNew.copy( gpx );
            gpxNew.changeCreator();
            gpxNew.changeName( strName );
            if( i == 1 and bEvening ):
                nOffset = -60*60*2; # le mardi je pars 2h plus tot...            
            else:
                nOffset = 0;
            gpxNew.modifyDate( (nNbrDiffDay+i) * nNbrSecPerDay+nOffset+random.random()*600 + nWinterToSummer );
            gpxNew.modifySpeed( 0.9+random.random()*0.21)
            print( gpx );
            print( gpxNew );
            strNewName = gpxNew.write( "/tmp/" );
            gpxNew.reset();
            gpxNew.read( strNewName );      
# generateWeek  - end
            
                

def duplicateOne( strRefFile, strDay, nTimeOffset = 0, strName = "" ):
    """
    Take a reference run, and replay it another day, with an optionnal time offset (time in the day)
    """
    nNbrSecPerDay = 60*60*24;
    nWinterToSummer = 0;
    nWinterToSummer = -1*60*60; # enable this when ref is in winter and week in summer
    
    gpx = Gpx();
    gpx.read( strRefFile );
    gpxNew = Gpx();
    gpxNew.copy( gpx );
    gpxNew.changeCreator();
    if( strName != "" ):
        gpxNew.changeName(strName);
        
    dt = datetime.datetime.strptime( strDay, "%Y-%m-%d");
    tDay = time.mktime(dt.timetuple()) + dt.microsecond / 1E6 # using utctimetuple or just timetuple
    nNbrDiffDay = 0;
    nNbrDiffDay = int( ( tDay - gpx.time ) /nNbrSecPerDay );
    nNbrDiffDay += 1; # for partial day
    gpxNew.modifyDate( nNbrDiffDay * nNbrSecPerDay+nWinterToSummer+nTimeOffset );
        
    

    print( gpx );
    print( gpxNew );
    
    strNewName = gpxNew.write( "/tmp/" );
# duplicateOne - end

def accelerateOne( strRefFile, rDurationRatio ):
    """
    Take a reference run, change the speed then save it
    """
    gpx = Gpx();
    gpx.read( strRefFile );
    gpxNew = Gpx();
    gpxNew.copy( gpx );
    gpxNew.changeCreator();
    gpxNew.modifySpeed( rDurationRatio );

    print( gpx );
    print( gpxNew );
    
    strNewName = gpxNew.write( "/tmp/" );
# accelerateOne - end

def duplicateOneSlightChange( strRefFile, rSlightChangeRatio = 0.01 ):
    """
    Take a reference run, change the speed then save it
    """
    gpx = Gpx();
    gpx.read( strRefFile );
    gpxNew = Gpx();
    gpxNew.copy( gpx );
    gpxNew.changeCreator();
    gpxNew.modify( rSlightChangeRatio );
    print( gpx );
    print( gpxNew );
    strNewName = gpxNew.write( "/tmp/" );
# duplicateOneSlightChange - end
    
def render( strFilename, img = None ):
    import cv2
    gpx = Gpx();
    gpx.read( strFilename );
    gpx.printInfo()
    img = gpx.render(img)
    print( "----- lissage ---- " )
    for i in range(10):
        gpx.correctGps()
    gpx.printInfo()
    img = gpx.render(img, (0,255,0) )
    strWindowName = "track"
    cv2.namedWindow( strWindowName, 0 )
    cv2.moveWindow( strWindowName, 0,0 )
    cv2.resizeWindow( strWindowName, img.shape[1]/2,img.shape[0]/2 )
    cv2.imshow( strWindowName, img )
    cv2.waitKey(0)
    return img

        
        
def autoTest():
    current_time_utc = timeToGpxTime();
    print( "Current Time UTC: %s" % current_time_utc );
    current_time_utc2 = timeToGpxTime(gpxTimeToTime(timeToGpxTime()));
    print( "Current Time UTC: %s" % current_time_utc2 );
    assert( current_time_utc == current_time_utc2 );
    gpx = Gpx();
    gpx.read( "/tmp2/Morning Ride.gpx" );
    print( "original file:\n%s" % str(gpx) );    
    gpx.changeCreator();
    #gpx.modify();
    gpx.modifySpeed(0.75);
    gpx.modifyDate(60*60*24);
    print( "final file:\n%s" % str(gpx) );    
    gpx.write( "/tmp/new.gpx" );
    
    
if __name__ == "__main__":
    #autoTest();
    #generateWeek( "2015-03-16" );\
    #~ generateWeek( "2015-11-30" );
    #~ duplicateOne( "../data/gpx/2015_01_21__Afternoon Ride aldeb-chateau_ref.gpx", "2015-04-02", 4*60*60+20*60, "Aldeb-Paris" );
    #~ duplicateOne( "../data/gpx/2015_01_21__Afternoon Ride chateau-candi_ref.gpx", "2015-04-02", 8*60*60, "RetourDodo" );
    #~ accelerateOne( "/tmp/a.gpx", 0.9 );
    img = None
    #~ img = render( "../data/gpx/2015_03_19__Morning_Ride_ref.gpx" )
    #img = render( "../data/gpx/Lunch_Run_bug_gps.gpx", img )
    #~ img = render( "../data/gpx/Lunch_Run_bug_gps2.gpx" )    
    #~ render( "../data/gpx/2015_03_19__Evening_Ride_ref.gpx", img )
    #~ img = render( "../data/gpx/2016-09-23_-_Morning_Run_13.5km__5.28kmh__1h13m58.gpx", img )
    duplicateOneSlightChange( "/tmp/Balade_tahitienne_chaud_et_humide.gpx" )
    
    
    