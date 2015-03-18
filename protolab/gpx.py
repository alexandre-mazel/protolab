import datetime
import random
import time
import xml.dom.minidom # for xml parsing

def floatToStrComplete( f ):
    """
    return the minimal string complete representation with at least 1 digit after the "."
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
    
    strOut = "%12.9f" % f;
    while( strOut[-1] == '0' and strOut[-2] != '.' ):
        strOut = strOut[:-1];
    return strOut;
# floatToStrComplete - end

def timeToGpxTime( timeToConvert = None ):
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
    strTimeStamp = dt.strftime( "%Y-%m-%dT%H:%M:%SZ" );    
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
        self.t = t
        self.la = la
        self.lo = lo
        self.el = el
        
    def __str__( self ):
        strOut = "";
        strOut += "-- t: %s\n" % timeToGpxTime( self.t );
        strOut += "-- la: %s\n" % self.la;
        strOut += "-- lo: %s\n" % self.lo;
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

    def __str__( self ):
        strOut = "";
        strOut += "- Creator: %s\n" % self.strCreator;
        strOut += "- Name: %s\n" % self.strName;
        strOut += "- Time: %s\n" % timeToGpxTime( self.time );
        strOut += "- listPts: len: %d\n" % len(self.listPts);
        for i in range(4):
            if( len(self.listPts) > i ):
                strOut += "- pt%d:\n%s\n" % (i,str(self.listPts[i]));
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
            print( "rSimulatedReplayTime: %5.2f, nIdxCurrent: %d, listPts[nIdxCurrent].t: %f, listPts[nIdxCurrent+1].t: %f" % (rSimulatedReplayTime,nIdxCurrent,self.listPts[nIdxCurrent].t, self.listPts[nIdxCurrent+1].t) );
            # find first check prior to current replay time
            while( rSimulatedReplayTime >= self.listPts[nIdxCurrent+1].t ):
                print( "rSimulatedReplayTime: %5.2f, nIdxCurrent: %d, listPts[nIdxCurrent].t: %f, listPts[nIdxCurrent+1].t: %f" % (rSimulatedReplayTime,nIdxCurrent,self.listPts[nIdxCurrent].t, self.listPts[nIdxCurrent+1].t) );
                nIdxCurrent +=1;
            rRatioInterpolate = ( rSimulatedReplayTime - self.listPts[nIdxCurrent].t ) / ( self.listPts[nIdxCurrent+1].t - self.listPts[nIdxCurrent].t )  
            print( "interpolating %5.2f between index %d and %d" % (rRatioInterpolate,nIdxCurrent,nIdxCurrent+1) );
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
    
    def modifyDate( self, nNbrSecondToAdd = 60*60):
        """
        add a time decay to a full track
        """
        self.time += nNbrSecondToAdd;
        for i in range( len(self.listPts) ):
            self.listPts[i].t += nNbrSecondToAdd;
    # modifyDate - end
        
    def write( self, strFilename ):
        file = open( strFilename, "wt" )
        file.write( "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" );
        file.write( "<gpx creator=\"%s\" version=\"%s\" xmlns=\"%s\" xmlns:xsi=\"%s\ xsi:schemaLocation=\"%s\">\n" % (self.strCreator, self.strGpxVersion,self.strns,self.strsxi,self.strSchemaLocation) );
        file.write( " <metadata>\n" );
        file.write( "  <time>%s</time>\n" % timeToGpxTime(self.time) );
        file.write( " </metadata>\n" );
        file.write( " <trk>\n");
        file.write( "  <name>%s</name>\n" % self.strName );        
        file.write( "  <trkseg>\n" );
        for pt in self.listPts:
            file.write( "   <trkpt lat=\"%s\" lon=\"%s\">\n" % ( floatToStrComplete(pt.la), floatToStrComplete(pt.lo) ) );
            file.write( "    <ele>%s</ele>\n" % floatToStrComplete(pt.el) );
            file.write( "    <time>%s</time>\n" % timeToGpxTime(pt.t) );
            file.write( "   </trkpt>\n" );

        file.write( "  </trkseg>\n" );
        file.write( " </trk>\n" );
        file.write( "</gpx>\n" );    
        
        file.close();
    # write - end
    
    
# class Gpx - end
        
        
        
        
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
    gpx.write( "/tmp2/new.gpx" );
    
    
    
if __name__ == "__main__":
    autoTest();