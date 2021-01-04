netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 0.net.xml --seed 8355201
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 1.net.xml --seed 35245640
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 2.net.xml --seed 36572065
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 3.net.xml --seed 93085104
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 4.net.xml --seed 49116586
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 5.net.xml --seed 83628269
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 6.net.xml --seed 48322719
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 7.net.xml --seed 29067860
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 8.net.xml --seed 30343355
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 9.net.xml --seed 71396192
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 10.net.xml --seed 88472921
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 11.net.xml --seed 25133334
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 12.net.xml --seed 71111820
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 13.net.xml --seed 22195349
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 14.net.xml --seed 66047777
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 15.net.xml --seed 18797340
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 16.net.xml --seed 60564156
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 17.net.xml --seed 38478865
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 18.net.xml --seed 14708486
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 19.net.xml --seed 95225531
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 20.net.xml --seed 26270601
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 21.net.xml --seed 53429552
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 22.net.xml --seed 32134536
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 23.net.xml --seed 80386663
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 24.net.xml --seed 30345909
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 25.net.xml --seed 82331445
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 26.net.xml --seed 16009632
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 27.net.xml --seed 69779575
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 28.net.xml --seed 74866167
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 29.net.xml --seed 93463297
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 30.net.xml --seed 13594092
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 31.net.xml --seed 18875265
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 32.net.xml --seed 20413870
netgenerate -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 33.net.xml --seed 68992365

for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33
do
rm "$i.sumo.cfg"
touch "$i.sumo.cfg"
echo "<configuration>\
<input>\
	<net-file value=\"$i.net.xml\"/>\
</input>\
</configuration>" >> $i.sumo.cfg
done