<?php
  include_once("./required/tool_files_dirs.php");
  include_once("./required/tool_svg.php");
  include_once("./required/tool_read_log.php");
  include_once("./ini.php");

 ini_set("memory_limit",-1);

  $array_paquet = Tool_read_log::path2array_paquet($path_log,$lg1,$lg2,$mesure);

  $a = Tool_read_log::filter_array_paquet($array_paquet, $lg1, $lg2, $id_multidoc,
                                          $borne_min, $borne_max, $dist_min, $dist_max,
                                          $nb_occ_min1, $nb_occ_max1,
                                          $nb_occ_rel_min1, $nb_occ_rel_max1,
                                          $str_len_min1, $str_len_max1,
                                          $str_len_min2, $str_len_max2);

  $res = array();

  foreach($a as $p){
    $array2 = $p[$lg2];
      foreach($array2 as $v1){
        $id1 = floor($v1);
        $src1 = $v1 - $id1;
        if($id1 == $id_multidoc and Tool_read_log::btwn($src1,$borne_min,$borne_max)){
          foreach($array2 as $v2){
            $id2 = floor($v2);
            if($id2 == $id_multidoc){
              $nv1 = round($v1,3) - $id_multidoc;
              $nv2 = round($v2,3) - $id_multidoc;
              $res["$nv1"][] = $nv2;
            }
          elseif($id2 > $id_multidoc) break;
          }
        }
        elseif($id1 > $id_multidoc) break;
      }
  }

$margin_left = 10;
$margin_top = 10;
$x1 = $margin_top + 30;
$y1 = 0 + $margin_left;
$lg = 1000;

$x2 = $x1 + 300;
$y2 = $y1;

$line1 = Tool_svg::space($y1,$x1,$lg);
$line2 = Tool_svg::space($y2,$x2,$lg);
$inter1 = Tool_svg::inter($y1,$x1,$lg,$margin_left,$borne_min,$borne_max);
$inter2 = Tool_svg::inter($y2,$x2,$lg,$margin_left,0,1);

$links = "";
foreach($res as $k1=>$array_k2){
  foreach($array_k2  as $k2){
    $links .= Tool_svg::link($y1,$x1,$y2,$x2,$lg,$margin_left,$k1,$k2);
  }
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

print $out_svg;

?>

