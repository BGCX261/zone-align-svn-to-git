<?php
  include_once("./required/tool_files_dirs.php");
  include_once("./required/tool_svg.php");
  include_once("./required/tool_read_log.php");
  include_once("./ini.php");

 ini_set('memory_limit',-1);

$time_start = microtime(true);

  $array_paquet = Tool_read_log::path2array_paquet($path_log,$lg1,$lg2,$mesure);

$time_end = microtime(true);
$time = $time_end - $time_start;
echo $time."\n";
$time_start = microtime(true);

  $a = Tool_read_log::filter_array_paquet($array_paquet, $lg1, $lg2, $id_multidoc,
                                          $borne_min, $borne_max,
                                          $dist_min, $dist_max,
                                          $nb_occ_min1, $nb_occ_max1,
                                          $nb_occ_rel_min1, $nb_occ_rel_max1,
                                          $str_len_min1, $str_len_max1,
                                          $str_len_min2, $str_len_max2);

$time_end = microtime(true);
$time = $time_end - $time_start;
echo $time."\n";

  $array_corres = array();
  for($i=$borne_min2;$i<$borne_max2;$i+=$gap2){
    $array_corres["$i"] = 0;
  }

  $res = array();

  foreach($a as $p){
    foreach($p[$lg2] as $v1){
      $id1 = floor($v1);
      $src1 = $v1 - $id1;
      if($id1 == $id_multidoc){
        $old_key = 0;
        foreach($array_corres as $key=>$aval){
          if($key >= $src1){
            ++$array_corres[$old_key];
            break;
          }
          $old_key = $key;
        }
      }
      elseif($id1 > $id_multidoc) break;
    }
  }
  print_r($array_corres);
?>

