<?php
  include_once("./required/tool_files_dirs.php");
  include_once("./required/tool_svg.php");
  include_once("./required/tool_read_log.php");
  include_once("./ini.php");

 ini_set("memory_limit",-1);

  $array_paquet = Tool_read_log::path2array_paquet($path_log,$lg1,$lg2,$mesure);

$cpt = 0;
//$step1 = 0.01;
for($k=0;$k<1;$k+=$step1){
  print $cpt."\r";
  $borne_min = $k;
  $borne_max = $borne_min + $gap1;  
  $out_file = vsprintf("./film/evol_rep_%04d.svg", array($cpt));
  ++$cpt;

  $a = Tool_read_log::filter_array_paquet($array_paquet, $lg1, $lg2, $id_multidoc,
                                          $borne_min, $borne_max, $dist_min, $dist_max,
                                          $nb_occ_min1, $nb_occ_max1,
                                          $nb_occ_rel_min1, $nb_occ_rel_max1,
                                          $str_len_min1, $str_len_max1,
                                          $str_len_min2, $str_len_max2);

  $array_corres = array();
  for($i=$borne_min2 ; $i<$borne_max2 ; $i+=$step2){
//    $array_corres["$i"] = array();
    $array_corres["$i"] = 0;
  }

  foreach($a as $p){
    $array2 = $p[$lg2];
    foreach($array2 as $v1){
      $id1 = floor($v1);
      $src1 = $v1 - $id1;
      if($id1 == $id_multidoc){
        foreach($array_corres as $key=>$aval){
          if(Tool_read_log::btwn($src1, $key, $key + $gap2)){
            ++ $array_corres[$key];
          }
        }
      }
      elseif($id1 > $id_multidoc) break;
    }
  }

//  print_r($array_corres);

$margin_left = 10;
$margin_top = 10;
$x1 = $margin_top + 30;
$y1 = 0 + $margin_left;
$lg = 1000;

$ecart = 300;

$x2 = $x1 + $ecart;
$y2 = $y1;

$line1 = Tool_svg::space($y1,$x1,$lg);
$line2 = Tool_svg::space($y2,$x2,$lg);
//$inter1 = Tool_svg::inter($y1,$x1,$lg,$margin_left,$borne_min,$borne_max);
$inter1 = Tool_svg::inter($y1,$x1,$lg,$margin_left,$borne_min,$borne_max);
$inter2 = Tool_svg::inter($y2,$x2,$lg,$margin_left,0,1);

$links = "";

$val_max = max($array_corres);

foreach($array_corres as $k2=>$nb_occ){
  if($val_max == 0) $val = $ecart;
  else{
    $val = $ecart - (($nb_occ/$val_max) * $ecart) + $x1;
  }
  $links .= Tool_svg::barre($y1,$x1,$y2,$x2,$lg,$margin_left,$k2,$val);
}

$out_svg = "<svg version=\"1.1\"
     baseProfile=\"full\"
     xmlns=\"http://www.w3.org/2000/svg\">

  $line1
  $line2

  $inter1
  $inter2

  $links
</svg>
";

Tool_files::file_write($out_file,$out_svg);
}
//print $out_svg;
?>
