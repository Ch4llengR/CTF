<?php

// Small script to find a value for loose comparison exploit

for ($x = 0; $x <= 1000000000; $x++) {
	$val = "0e".$x;
    if(md5($val) == $val)
	{
		echo "Found a value!! $val"; 
	}
}
?>
