<?php
  include_once("./required/tool_files_dirs.php");
  include_once("./required/tool_svg.php");
  include_once("./required/tool_read_log.php");
  include_once("./ini.php");

  ini_set("memory_limit",-1);

  $array_paquet = Tool_read_log::path2array_paquet($path_log,$lg1,$lg2,$mesure);

$cpt = 0;
$matrice = array();
for($k=0;$k<1;$k+=$step1){
  $borne_min = $k;
  $borne_max = $borne_min + $gap1;  
  echo $cpt++."\r";

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
//    $array2 = Tool_read_log::line2rep($p[$lg2]);
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
  $ac = array_values($array_corres);
  $matrice[] = $ac;
}
$margin_left = 13;
$margin_top = 13;

$height = count($matrice)*$zoom + $margin_top;
$lengh  = count(reset($matrice))*$zoom + $margin_left;

$image = imagecreate($height,$lengh);
$dico_color = array();
dictionnaire_color($image,$dico_color,0);
$dico_color['red'] = imagecolorallocate($image,255,0,0);


//$max_matrice = 0;
//foreach($matrice as $ligne){
//  $max_matrice = max($max_matrice,max($ligne));
//}



foreach($matrice as $i=>$ligne){
  $max_ligne = max($ligne);
  foreach($ligne as $j=>$val){
    ($max_ligne == 0) ? $d = 0 : $d = $val / $max_ligne;
    if($d >= $discretisation_max) $d = 1;
    elseif($d <= $discretisation_min) $d = 0;

    $color = dictionnaire_color($image,$dico_color,$d);
    for($sc = $i*$zoom + $margin_left ; $sc < ($i+1)*$zoom + $margin_left; ++$sc){
      for($sl = $j*$zoom + $margin_top; $sl < ($j+1)*$zoom + $margin_top; ++$sl){
        imageSetPixel($image,$sc,$sl,$color);
      }
    }
  }
}

for($i=0; $i<10; ++$i){
  $x = (($height - $margin_top) / 10) * $i + $margin_top;
  $y = (($lengh - $margin_left) / 10) * $i + $margin_left;
  imagestring($image, 1, 0, $x+2, "$i".'0%', $dico_color['red']);
  for($j=0; $j<$margin_left; ++$j){
    imageSetPixel($image,$j,$x,$dico_color['red']);
  }
  imagestring($image, 1, $y+2, 0, "$i".'0%', $dico_color['red']);
  for($j=0; $j<$margin_top; ++$j){
    imageSetPixel($image,$y,$j,$dico_color['red']);
  }

}



imagepng($image,"out.png");
?>
