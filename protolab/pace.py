import datetime


def secToStr( rSec ):
    strOut = "";
    if( rSec > 60*60 ):
        n = int(rSec/(60*60));
        strOut += "%dh" % n;
        rSec -= 60*60*n;
    if( rSec > 60 or 1 ):
        n = int(rSec/(60));
        strOut += "%02dm" % n;
        rSec -= 60*n;
    if( rSec > 0 ):
        strOut += "%02ds" % int(rSec);
        
    return strOut;

def pace( rPacePerKmInSec ):
    listI = range(1,43);
    listI.append( 42.195);
    for i in listI:
        rTime = rPacePerKmInSec * i;
        strTime = secToStr(rTime);
        print( "km: %s: t: %s" % (i, strTime) );
        #~ dt = datetime.datetime.strptime( rTime, "%Y-%m-%dT%H:%M:%SZ" );
        #~ print( str(dt))


def autotest():
    pace( 4*60+37 );
    pace( 4*60+45 );

if __name__ == "__main__":
    autotest();
    pass