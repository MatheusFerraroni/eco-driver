netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 0.net.xml --seed 959709305
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 1.net.xml --seed 473380937
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 2.net.xml --seed 817172493
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 3.net.xml --seed 209369489
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 4.net.xml --seed 554605868
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 5.net.xml --seed 516005735
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 6.net.xml --seed 871805786
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 7.net.xml --seed 261129122
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 8.net.xml --seed 343327165
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 9.net.xml --seed 786437055
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 10.net.xml --seed 353863383
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 11.net.xml --seed 382715298
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 12.net.xml --seed 964726590
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 13.net.xml --seed 788240171
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 14.net.xml --seed 145597396
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 15.net.xml --seed 565551761
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 16.net.xml --seed 395188401
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 17.net.xml --seed 360836588
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 18.net.xml --seed 750271093
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 19.net.xml --seed 815441608
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 20.net.xml --seed 946662148
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 21.net.xml --seed 576375862
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 22.net.xml --seed 588011720
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 23.net.xml --seed 424627479
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 24.net.xml --seed 487531011
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 25.net.xml --seed 916765594
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 26.net.xml --seed 380178501
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 27.net.xml --seed 734855156
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 28.net.xml --seed 828304848
netgenerate.exe -g --grid.x-number 51 --grid.y-number 2 --perturb-z 7 --default.speed 100 -o 29.net.xml --seed 296064566

for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 
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