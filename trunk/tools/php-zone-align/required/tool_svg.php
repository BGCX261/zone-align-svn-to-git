<?php

class Tool_svg{


  public static function heavy_line($_x1,$_y1,$_x2,$_y2){
    return "<line x1=\"$_x1\" y1=\"$_y1\" x2=\"$_x2\" y2=\"$_y2\" style=\"stroke:rgb(99,99,99);stroke-width:4\"/>";
  }

  public static function line($_x1,$_y1,$_x2,$_y2){
    return "<line x1=\"$_x1\" y1=\"$_y1\" x2=\"$_x2\" y2=\"$_y2\" style=\"stroke:rgb(99,99,99);stroke-width:2\"/>";
  }

  public static function thin_line($_x1,$_y1,$_x2,$_y2){
    return "<line x1=\"$_x1\" y1=\"$_y1\" x2=\"$_x2\" y2=\"$_y2\" style=\"stroke:rgb(99,99,99);stroke-width:0.3\"/>";
  }

  public static function space($_x,$_y,$_lg){
    $l = $_x + $_lg;
    return self::line($_x,$_y,$l,$_y);
  }

  public static function inter($_x,$_y,$_lg,$_margin_left,$_min,$_max){
    $tmin = $_lg * $_min + $_margin_left;
    $tmax = $_lg * $_max + $_margin_left;
    $ymax = $_y+5; $ymin = $_y-5;
    $lmin = self::line($tmin,$ymax,$tmin,$ymin);
    $lmax = self::line($tmax,$ymax,$tmax,$ymin);
    return "$lmin $lmax";
  }

  public static function link($_x1,$_y1,$_x2,$_y2,$_lg,$_margin_left,$_o1,$_o2){
    $t1 = $_lg * $_o1 + $_margin_left;
    $t2 = $_lg * $_o2 + $_margin_left;
    $l = self::thin_line($t1,$_y1,$t2,$_y2);
    return $l;
  }

  public static function barre($_x1,$_y1,$_x2,$_y2,$_lg,$_margin_left,$_o2,$_val){
    $t2 = $_lg * $_o2 + $_margin_left;
    $l = self::heavy_line($t2,$_val,$t2,$_y2);
    return $l;

  }


}

?>
