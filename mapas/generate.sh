
netgenerate.exe -g --grid.x-number 20 --perturb-x 23 --grid.y-number 2 --perturb-z 100 -o 0.net.xml --seed 5379479

netgenerate.exe -g --grid.x-number 20 --perturb-x 23 --grid.y-number 2 --perturb-z 100 -o 1.net.xml --seed 6831837

netgenerate.exe -g --grid.x-number 20 --perturb-x 23 --grid.y-number 2 --perturb-z 100 -o 2.net.xml --seed 9726976

netgenerate.exe -g --grid.x-number 20 --perturb-x 23 --grid.y-number 2 --perturb-z 100 -o 3.net.xml --seed 6106279

netgenerate.exe -g --grid.x-number 20 --perturb-x 23 --grid.y-number 2 --perturb-z 100 -o 4.net.xml --seed 9023093

netgenerate.exe -g --grid.x-number 20 --perturb-x 23 --grid.y-number 2 --perturb-z 100 -o 5.net.xml --seed 4310387

netgenerate.exe -g --grid.x-number 20 --perturb-x 23 --grid.y-number 2 --perturb-z 100 -o 6.net.xml --seed 8351704

netgenerate.exe -g --grid.x-number 20 --perturb-x 23 --grid.y-number 2 --perturb-z 100 -o 7.net.xml --seed 8419726

netgenerate.exe -g --grid.x-number 20 --perturb-x 23 --grid.y-number 2 --perturb-z 100 -o 8.net.xml --seed 1243412

netgenerate.exe -g --grid.x-number 20 --perturb-x 23 --grid.y-number 2 --perturb-z 100 -o 9.net.xml --seed 5982279



for i in 0 1 2 3 4 5 6 7 8 9
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