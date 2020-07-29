
netgenerate.exe -g --grid.x-number 21 --grid.y-number 2 --perturb-z 25 --default.speed 100 -o 0.net.xml --seed 9523452

netgenerate.exe -g --grid.x-number 21 --grid.y-number 2 --perturb-z 25 --default.speed 100 -o 1.net.xml --seed 3452781

netgenerate.exe -g --grid.x-number 21 --grid.y-number 2 --perturb-z 25 --default.speed 100 -o 2.net.xml --seed 5462171

netgenerate.exe -g --grid.x-number 21 --grid.y-number 2 --perturb-z 25 --default.speed 100 -o 3.net.xml --seed 6437658

netgenerate.exe -g --grid.x-number 21 --grid.y-number 2 --perturb-z 25 --default.speed 100 -o 4.net.xml --seed 5512693



for i in 0 1 2 3 4
do
  rm "$i.sumo.cfg"
  touch "$i.sumo.cfg"
  echo "<configuration>\
	<input>\
		<net-file value=\"$i.net.xml\"/>\
		<route-files value=\"rota.rou.xml\"/>\
	</input>\
</configuration>" >> $i.sumo.cfg
done