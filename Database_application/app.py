# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db

def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema)
    
    return con

def findAirlinebyAge(x,y):
    
    # Create a new connection
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()

    sql1="""select a.name,count(fhp.flights_id)
		from flights f, flights_has_passengers fhp,routes r,airlines a
		where f.id=fhp.flights_id and r.id=f.routes_id and r.airlines_id=a.id and f.id in
			(select distinct f.id
	 		from flights f,flights_has_passengers fhp,passengers p
	 		where f.id=fhp.flights_id and fhp.passengers_id=p.id and p.year_of_birth>'%d' and p.year_of_birth<'%d')
		group by fhp.flights_id 
		order by count(fhp.flights_id) desc;"""%(int(x),int(y))
    
    cur.execute(sql1)
    results1=cur.fetchone()
    airname=results1[0]
    
    sql2="""select count(ahp.airlines_id)
            from airlines a, airlines_has_airplanes ahp
            where a.id=ahp.airlines_id and a.name='%s'
            group by ahp.airlines_id;"""%(str(airname))
    cur.execute(sql2)
    results2=cur.fetchone()
    
    #print("findAirlinebyAge(%d,%d):\n airline_name=%s, num_of_passengers=%d, num_of_aircrafts=%d"%\
         #(int(x),int(y),results1[0],results1[1],results2[0]))
    
    return [("airline_name","num_of_passengers", "num_of_aircrafts"),(results1[0],results1[1],results2[0])]


def findAirportVisitors(x,a,b):
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()

    sql="""select a.name, count(*)
            from airports a,routes r,flights f, flights_has_passengers fhp
            where f.routes_id=r.id  and r.destination_id=a.id  and f.date>'%s' and f.date<'%s' and f.id=fhp.flights_id and a.name in(
            	select distinct a.name
            	from airlines ar,airports a,routes r,flights f
            	where f.routes_id=r.id and r.destination_id=a.id and r.airlines_id=ar.id and ar.name='%s' and f.date>'%s' and f.date<'%s')
            group by a.id
            order by count(*) desc;"""%(str(a),str(b),str(x),str(a),str(b))
    cur.execute(sql)
    results=cur.fetchall()

    #print("\nfindAirportVisitors(%s,%s,%s):\n"%(str(x),str(a),str(b)))
    airname=[]
    numvis=[]
    for row in results:
        airname.append(row[0])
        numvis.append(row[1])
        #print("aiport_name=%s, number_of_visitors=%d"%\
             #(airname,numvis))
        
    return [("aiport_name", "number_of_visitors"),(airname,numvis)]    
    

def findFlights(x,a,b):

    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()

    sql="""select f.id,air.alias,arp2.name,ap.model
           from flights f,airlines air,routes r,airlines_has_airplanes aha,airplanes ap,airports arp1,airports arp2
           where f.routes_id=r.id and r.source_id=arp1.id and arp1.city='%s' and r.destination_id=arp2.id and arp2.city='%s' and f.date='%s' and r.airlines_id=air.id and aha.airlines_id=air.id and aha.airplanes_id=ap.id and air.active='Y';"""%(str(a),str(b),str(x))

    cur.execute(sql)
    results=cur.fetchall()
    
    #print("\nfindFlights(%s,%s,%s):\n"%(str(x),str(a),str(b)))
    fid=[]
    altname=[]
    dest=[]
    mod=[]
    for row in results:
        fid.append(row[0])
        altname.append(row[1])
        dest.append(row[2])
        mod.append(row[3])
        #print("flight_id=%d, alt_name=%s, dest_name=%s, aircraft_model=%s"%\
             #(fid,altname,dest,mod))
    
    return [("flight_id", "alt_name", "dest_name", "aircraft_model"),(fid,altname,dest,mod)]
    

def findLargestAirlines(N):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    sql1="""select ar.name,ar.code,count(ar.id)
            from flights f,airlines ar,routes r
            where f.routes_id=r.id and r.airlines_id=ar.id
            group by ar.id
            order by count(ar.id) desc;"""
    cur.execute(sql1)
    results1=list(cur.fetchall())

    #print("\nfindLargestAirlines(%d):\n"%(int(N)))
    
    name=[]
    id=[]
    numf=[]
    numair=[]
    n=int(N)
    for x in range(0,n): 
        name.append(results1[x][0])
        id.append(results1[x][1])
        numf.append(results1[x][2])  
        sql2="""select count(ahp.airlines_id)
                from airlines a, airlines_has_airplanes ahp
                where a.id=ahp.airlines_id and a.name='%s'
                group by ahp.airlines_id;"""%(str(results1[x][0]))
        cur.execute(sql2)
        results2=cur.fetchone()
        numair.append(results2[0])
        #print("name=%s, id=%s, num_of_aircrafts=%s, num_of_flights=%s"%\
              #(str(name),str(id),str(numair),str(numf)))
    
    return [("name", "id", "num_of_aircrafts", "num_of_flights"),(name,id,numair,numf)]
        
   
    
def insertNewRoute(x,y):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    sql1="""select distinct a.id,ar1.id,ar2.id
           from routes r,airlines a,airports ar1,airports ar2
           where r.airlines_id=a.id and a.alias='%s' and r.source_id=ar1.id and ar1.name='%s' and ar2.id not in 
                   (select r.destination_id
                   from routes r,airlines a,airports ar
                   where r.airlines_id=a.id and a.alias='%s' and r.source_id=ar.id and ar.name='%s');"""%(str(x),str(y),str(x),str(y))
    cur.execute(sql1)
    results=cur.fetchone()    

    sql3="""select r.id 
            from routes r
            order by r.id desc;"""
    cur.execute(sql3)
    res=cur.fetchone()
    rid=int(res[0])+1

    sql2="""insert into routes(id,airlines_id, source_id, destination_id)
           values ('%d','%d','%d','%d');"""%(rid,int(results[0]),int(results[1]),int(results[2]))

    #print("\ninsertNewRoute(%s,%s):\n"%(str(x),str(y)))
    
    
    cur.execute(sql2)
    num=int(cur.rowcount)
    if (num==1):
        con.commit()
        return[" OK"]
    else:
        con.rollback
        return[" airline capacity full"]


    return [(),]


#findAirlinebyAge(1950,2010)
#findAirportVisitors("Aegean Airlines","2007-01-02","2019-10-28")
#findFlights("2014-12-12","Athens","London")
#findLargestAirlines(5)
#insertNewRoute("Air Asia","Kuala Lumpur Intl")
