<?php

  //$path_log = "./log/ogpfix.10.log";
  //$path_log = "./log/ogpfix.40.log";
  //$path_log = "./log/ogpfix.abcd.log";
  //$path_log = "./log/ogpfix.log";
  //$path_log = "./log/ogpfix_40md_6lg.log";
  //$path_log = "./log/ogpfix_61md_AI.log";
  $path_log = "../corpusalign/test2_collection1.log";

//  $id_multidoc = 3;
  $id_multidoc = 33;
  $lg1 = "es";
  $lg2 = "fr";
  $mesure = "docdistance";
  //$mesure = "docdistance";
  //$mesure = "cosinus";
  $dist_min = 0;
  $dist_max = 0.3; //beware : dist_max may be more than 1 in some .log files.


//chaînes de caract_res;
  $str_len_min1 = 0;
  $str_len_max1 = 1000000;
  $str_len_min2 = 0;
  $str_len_max2 = 1000000;

//fenetres

  $borne_min = 0;
  $borne_max = 0.1;
  $nb_occ_min1 = 1;
  $nb_occ_max1 = 20000;

  $nb_occ_rel_min1 = 1;
  $nb_occ_rel_max1 = 10000000000;
  
//  $score_min = 0;
//  $score_max = 1.0;
  $borne_min2 = 0.0;
  $borne_max2 = 1.0;


/*
  $gap1 = 0.01;
  $step1 = 0.005;

  $gap2 = 0.01;
  $step2 = 0.005;
*/
  $gap1 = 0.01;
  $step1 = 0.005;

  $gap2 = 0.01;
  $step2 = 0.005;

//matrice
  $zoom = 1;
  $discretisation_min = 0;
  $discretisation_max = 1;
?>
