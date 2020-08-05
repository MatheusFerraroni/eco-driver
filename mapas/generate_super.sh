netgenerate.exe -g --grid.x-number 301 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o super.net.xml --seed 8355201


rm "super.sumo.cfg"
touch "super.sumo.cfg"
echo "<configuration>\
<input>\
	<net-file value=\"super.net.xml\"/>\
	<route-files value=\"rota.rou.xml\"/>\
</input>\
</configuration>" >> super.sumo.cfg