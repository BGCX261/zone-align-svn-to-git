<?php
 mb_internal_encoding("utf-8");

  class Tool_read_log{
    public static function path2array_paquet($_path,$lg1,$lg2,$mesure){
      $array_lg = array($lg1,$lg2);
      sort($array_lg);
      $data = Tool_files::file_load($_path);
      $f = Tool_files::csv2array_line($data,"\n");

      $array_paquet = array();
      $tmp = array();

      $flag_vu = false;
      foreach($f as $line){
        if(mb_eregi("[:alnum:]",$line)) $tmp[] = trim($line);
        elseif(len($tmp)>0){
          list($dist,$rep) = mb_split(" : ",$tmp[0]);
          list($score,$l1,$l2) = mb_split(" ",$rep);
          $score = trim($score); $dist = trim($dist);
          $l1 = trim($l1); $l2 = trim($l2);

          if($dist == $mesure){
            if(($l1 == $lg2 and $l2 == $lg1) or ($lg1 == $l1 and $lg2 == $l2)){
             $flag_vu = true;
             list($str1,$rep1) = self::line2str_rep($tmp[1]);
             list($str2,$rep2) = self::line2str_rep($tmp[2]);
             $array_paquet[] = array('score'=>$score, $l1=>$rep1, $l2=>$rep2, 
                                     "str_$l1"=>$str1, "str_$l2"=>$str2);
             }
          }
          elseif($flag_vu) break;
          $tmp = array();
        }
      }
      return $array_paquet;
    }

    public static function filter_array_paquet($array_paquet, $lg1, $lg2, $id_multidoc,
                                               $borne_min, $borne_max, $dist_min, $dist_max,
                                               $nb_occ_min1, $nb_occ_max1,
                                               $nb_occ_rel_min1, $nb_occ_rel_max1,
                                               $str_len_min1, $str_len_max1,
                                               $str_len_min2, $str_len_max2){
      $a = array();
      foreach($array_paquet as $paquet){
      if(isset($paquet[$lg1]) and isset($paquet[$lg2])){
        $rep1 = $paquet[$lg1];
        $rep2 = $paquet[$lg2];

        $c = count($rep1);
        $c_relative = self::rep2count_relative($rep1,$id_multidoc);

        $b_in = self::is_in($rep1,$id_multidoc,$borne_min,$borne_max);
        $b2 = self::is_correct($rep2,$id_multidoc);
        $b_score = self::btwn($paquet['score'], $dist_min, $dist_max);
        $b_count_absolute = self::btwn($c, $nb_occ_min1, $nb_occ_max1);
        $b_count_relative = self::btwn($c_relative, $nb_occ_rel_min1, $nb_occ_rel_max1);
  
        if($b_in and $b2 and $b_score and $b_count_absolute and $b_count_relative){
          $len1 = mb_strlen($paquet["str_$lg1"]);
          $len2 = mb_strlen($paquet["str_$lg2"]);
          $b_len_str1 = self::btwn($len1,$str_len_min1,$str_len_max1);
          $b_len_str2 = self::btwn($len2,$str_len_min2,$str_len_max2);
          if($b_len_str1 and $b_len_str2) $a[] = $paquet;
        }
      }
      }
      return $a;
    }


    public static function line2str($_line){
      list($g,$d) = mb_split("' \([0-9]+\) : ",$_line);
      return ltrim($g,"'");
    }

    public static function line2rep($_line){
      list($g,$d) = mb_split("' \([0-9]+\) : ",$_line);
      $array_value = mb_split(" ",$d);
      $new_array_value = array();
      foreach($array_value as $v){
        list($id_multidoc,$pos_percent) = mb_split(":",$v);
        $pos = $pos_percent / 100;
        $new_array_value[] = $id_multidoc + $pos;
      }
      return $new_array_value;
    }

    public static function line2str_rep($_line){
      list($g,$d) = mb_split("' \([0-9]+\) : ",$_line);
      $str = ltrim($g);
      $array_value = mb_split(" ",$d);
      $new_array_value = array();
      foreach($array_value as $v){
        list($id_multidoc,$pos_percent) = mb_split(":",$v);
        $new_array_value[] = $id_multidoc + ($pos_percent / 100);
      }
      return array($str,$new_array_value);
    }


    public static function rep2count_relative($_array_d,$_id_document){
      $relative_count = 0;
      foreach($_array_d as $d){
        $pe = floor($d);
        if($pe > $_id_document) break;
        elseif($pe == $_id_document) ++$relative_count;
      }
      return $relative_count;
    }

    public static function is_correct($array_d,$_id_document){
        foreach($array_d as $d){
            $pe = floor($d);
            if($pe == $_id_document) return true;
        }
        return false;
    }

    public static function is_in($array_d, $_id_document, $_min, $_max){
      foreach($array_d as $d){
        $new_d = $d - $_id_document;
        if($new_d >= $_min and $new_d <= $_max) return true;
      }
      return false;
    }

    public static function btwn($_val, $_min, $_max){
      return ($_val >= $_min and $_val <= $_max);
    }

    public static function convert_dist2gray($_dist){
      return 255 - round(255*$_dist);
    }

    public static function dictionnaire_color(&$_image,&$_dict,$_dist){
      $color = self::convert_dist2gray($_dist);
      if(!isset($_dict[$color]))
        $_dict[$color] = imagecolorallocate($_image,$color,$color,$color);
      return $_dict[$color];
    }

/*
 * OLD
 */

    public static function OLD_line2rep($_line){
      list($g,$d) = mb_split("' \([0-9]+\) : ",$_line);
      return mb_split(" ",$d);
    }

  }

    function convert_dist2gray($_dist){
      return 255 - round(255*$_dist);
    }


    function test(&$_image,&$_dict,$_dist){
      $color = convert_dist2gray($_dist);
      $_dict[$color]++;
//      if(!isset($_dict[$color]))
//        $_dict[$color] = imagecolorallocate($_image,$color,$color,$color);
//      return $_dict[$color];
    }

    function dictionnaire_color(&$_image,&$_dict,$_dist){
      $color = convert_dist2gray($_dist);
      if(!isset($_dict[$color]))
        $_dict[$color] = imagecolorallocate($_image,$color,$color,$color);
      return $_dict[$color];
    }

?>
