#1
select p.number
from airplanes p,airlines l,airlines_has_airplanes aha
where p.manufacturer='Airbus' and l.name='Lufthansa' and l.id=aha.airlines_id and p.id=aha.airplanes_id;

#2
select l.name
from airlines l,routes r,airports a1,airports a2
where a1.city='Athens' and a1.id=r.source_id and a2.city='Prague' and a2.id=r.destination_id and r.airlines_id=l.id;

#3
select count(*) as number
from passengers p, flights f, flights_has_passengers fhp, routes r, airlines a
where f.date='2012-02-19' and fhp.flights_id=f.id and fhp.passengers_id=p.id and f.routes_id=r.id and r.airlines_id=a.id and a.name='Aegean Airlines';

#4
(select 'yes' as result
from flights f,routes r, airlines a,airports a1, airports a2
where f.date='2014-12-12' and f.routes_id=r.id and r.airlines_id=a.id and a.name='Olympic Airways' and r.source_id=a1.id and a1.name='Athens El. Venizelos' and r.destination_id=a2.id and a2.name='London Gatwick'
group by a.id
having count(a.id)>0)
union
(select 'no' as result
from flights f,routes r, airlines a,airports a1, airports a2
where f.date='2014-12-12' and f.routes_id=r.id and r.airlines_id=a.id and a.name='Olympic Airways' and r.source_id=a1.id and a1.name='Athens El. Venizelos' and r.destination_id=a2.id and a2.name='London Gatwick'
group by a.id
having count(a.id)=0);

#5
select avg(2022-p.year_of_birth) as age
from passengers p,flights f,flights_has_passengers fhp,routes r,airports a
where p.id=fhp.passengers_id and fhp.flights_id=f.id and f.routes_id=r.id and r.destination_id=a.id and a.city='Berlin';

#6
(select p.name,p.surname
from passengers p,flights_has_passengers fhp
where p.id=fhp.passengers_id 
group by fhp.passengers_id
having count(fhp.passengers_id)=1)
union
(select p.name,p.surname
from passengers p,flights_has_passengers fhp,flights f,airplanes ap
where p.id=fhp.passengers_id and fhp.flights_id=f.id and f.airplanes_id=ap.id and exists
	(select *
    from airports ap2,flights f2
    where p.id=fhp.passengers_id and fhp.flights_id=f2.id and f2.airplanes_id=ap2.id )
group by fhp.passengers_id
having count(fhp.passengers_id)>1);
    
#7
select a1.city,a2.city
from airports a1, airports a2,routes r,flights f, flights_has_passengers fhp
where f.date>='2010-03-01' and f.date<='2014-07-17' and f.routes_id=r.id and r.destination_id=a2.id and r.source_id=a1.id and f.id=fhp.flights_id
group by fhp.flights_id
having count(fhp.flights_id)>5;

#8
select a.name,a.code,count(r.airlines_id) as num
from routes r,airlines a
where r.airlines_id=a.id and a.code in(
	select a.code
	from airlines a,airlines_has_airplanes aha
	where a.id=aha.airlines_id 
	group by aha.airlines_id
	having count(aha.airlines_id)=4)
group by r.airlines_id;

#9
select p.name,p.surname
from passengers p,flights f,flights_has_passengers fhp,airlines air,routes r
where p.id=fhp.passengers_id and fhp.flights_id=f.id and f.routes_id=r.id and r.airlines_id=air.id and air.id=any
	(select air.id
    from airlines air
    where air.active='Y')
group by fhp.passengers_id
having count(fhp.passengers_id)>=(select count(ar.id)
								from airlines ar
								where ar.active='Y');
                                
#10
(select p.name,p.surname
from passengers p,flights f,flights_has_passengers fhp,airlines a, routes r
where p.id=fhp.passengers_id and fhp.flights_id=f.id and f.routes_id=r.id and r.airlines_id=a.id and a.name='Aegean Airlines'
group by fhp.passengers_id
having count(fhp.passengers_id)=1)
union
(select p.name,p.surname
from passengers p,flights f,flights_has_passengers fhp
where p.id=fhp.passengers_id and fhp.flights_id=f.id and f.date>='2011-01-02' and f.date<='2013-12-31'
group by fhp.passengers_id
having count(fhp.passengers_id)>1);