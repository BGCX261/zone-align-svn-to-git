<?php
  include_once("./required/tool_files_dirs.php");

$array_files=tool_dir::dir_regexp("./","read.*\.php");

foreach($array_files["php"] as $path){
  $r=explode("/",$path);
  $file=array_pop($r);
  $dir=implode("/",$r)."/";
  $n=explode(".",$file);
  $i=explode("_",$n[0]);

  if($n[0] != "tool_read_log"){
    if($n[0] == "read2evolution_step_film" or $n[0] == "read2matrix"){
      $cmd = "php ".$n[0].".php";
    }
    else{
      ($n[0] == "read" or $n[0] == "read_step" or $n[0] == "read_csv") ? $ext = ".txt" : $ext = ".svg";
      $fileout = $dir . "out_" . $n[0] . $ext;
      $cmd = "php ".$n[0].".php > $fileout";
    }
    $ret = system($cmd);
    echo $cmd."\n";
  }
}

?>

