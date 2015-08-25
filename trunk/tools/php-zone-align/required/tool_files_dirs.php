<?php

class Tool_files{

 public static function url_load($_url){
  $http_page = file_get_contents($_url);
  return $http_page;
 }

 public static function file_load($_path){
  if($id = @fopen($_path, "r")){
   $buffer = fread($id, filesize($_path));
   fclose($id);
  }
  return $buffer;
 }

 public static function file_write($_path,$_buffer){
  if($id = @fopen($_path, "w")){
   $res=fwrite($id,$_buffer);
   fclose($id);
  }
  return $res;
 }

 public static function file_add($_path,$_buffer){
  if($id = @fopen($_path, "a")){
   $res=fwrite($id,$_buffer);
   fclose($id);
  }
  return $res;
 }

 public static function file_load_csv($_path,$_sep_col,$_sep_line){
  $buffer=self::file_load($_path);
  return self::csv2array($buffer,$_sep_col,$_sep_line);
 }

 public static function csv2array($_data,$_sep_col,$_sep_line){
  $array_line=mb_split($_sep_line,$_data);
  $res=array();
  foreach($array_line as $num_line=>$line){
    if($line){
     $array_col=mb_split($_sep_col,$line);
     $res[$num_line]=$array_col;
    }
  }
  return $res;
 }

 public static function csv2array_line($_data,$_sep_line){
  $array_line=mb_split($_sep_line,$_data);
  return $array_line;
 }


 public static function json2array_acp($_data_json,&$_array_res){
  $js_decode=json_decode($_data_json,true);
  $entete=array_shift($js_decode);
  foreach($js_decode as $array_cmp){
    foreach($array_cmp as $id1=>$array_score){
      foreach($array_score as $id2=>$score){
        if($id2!=$id1 and !isset($_array_res["($id2.$id1)"]))
          $_array_res["($id1.$id2)"][]=$score;
      }
    }
  }
  return $entete;
 } 

 public static function array_acp2r($_array_acp){
  $count_col=count(current($_array_acp))+1;
  $entete="";
  for($i=0;$i<$count_col;++$i){
    if($i>0) $entete.="$i";
    $entete.="  ";
  }
  $entete=rtrim($entete)."\n";
  $res="";
  foreach($_array_acp as $id=>$scores){
    $ex=implode("  ",$scores);
    $res.="$id  ".$ex."\n";
  }
  return "$entete$res"; 
 }

}

class Tool_dir{
  public static function dir_getAll($_dir){
    $rep=opendir($_dir);
    $array=array();
    while($file=readdir($rep)){
      if($file != '..' && $file !='.' && $file !=''){
        array_push($array,"$_dir$file");
      }
    }
    closedir($rep);
    clearstatcache();
    return $array;
  }


  public static function dir_sort_type($_array_from_dir){
    $all_files_by_type=array();
    foreach($_array_from_dir as $path){
      $type=array_pop(@explode(".",$path));
      if(array_key_exists($type,$all_files_by_type))
        array_push($all_files_by_type[$type],$path);
      else $all_files_by_type[$type]=array($path);
    }
    return $all_files_by_type;
  }

  public static function dir_regexp($_dir,$_reg_exp,$_type=null){
    $array_type=self::dir_sort_type(self::dir_getAll($_dir));
    $array=array();
    foreach($array_type as $type=>$array_path){
      if($_type==null or $type==$_type)
      foreach($array_path as $path){
        $file=array_pop(@explode("/",$path));
//        if(ereg("$_reg_exp",$file,$out)){
        if(preg_match("/$_reg_exp/",$file,$out)){
           if(array_key_exists($type,$array)) array_push($array[$type],$path);
           else $array[$type]=array($path);
        }
      }
    }
    return $array;
  }



}


/*
function get_filtered_ids_multidocument($_dir,$_array_id_multidoc,$_array_lg){
 $array_res=array();
 foreach($_array_id_multidoc as $id_multidoc){
  $europa=new multidocument($id_multidoc,$_dir,array());
  $europa->__init();
  $array_doc=$europa->__get_array_doc();

  $flag=true;
  foreach($_array_lg as $lg){
   if(!array_key_exists($lg,$array_doc)){
    $flag=false;
    break;
   }
  }
  if($flag) $array_res[]=$id_multidoc;
 }
 return $array_res;
}

function get_all_ids_multidocument($_dir,$_rule){
 $array_path=dir_getAll($_dir);
 $all_ids_multidocs=array();
 foreach($array_path as $path)
  if(preg_match($_rule,$path,$id_multidoc)){
   //$id_doc=mb_strcut($document->__get_id(),-6,2);
   if(!in_array($id_multidoc[0],$all_ids_multidocs))array_push($all_ids_multidocs,$id_multidoc[0]);
  }
 return $all_ids_multidocs;
}

function mtg_get_all_ids_multidocuments($_dir){
 return get_all_ids_multidocument($_dir,'/[^_\/]+_/');
}

function europa_get_all_ids_multidocuments($_dir){
 return get_all_ids_multidocument($_dir,'/celex_IP-[0-9]+-[0-9]+./');
}

function dir_regexp($_dir,$_reg_exp,$_type=null){
 $array_type=sort_from_dir(dir_getAll($_dir));

 $array=array();
 foreach($array_type as $type=>$array_path){
  if($_type==null or $type==$_type)
  foreach($array_path as $path){
   $file=array_pop(explode("/",$path));
   if(ereg("$_reg_exp",$file,$out)){
    if(array_key_exists($type,$array)) array_push($array[$type],$path);
    else $array[$type]=array($path);
   }
  }
 }

 return $array;
}

function sort_from_dir($_array_from_dir){
 $all_files_by_type=array();
 foreach($_array_from_dir as $path){
  $type=array_pop(explode(".",$path));
  if(array_key_exists($type,$all_files_by_type)) array_push($all_files_by_type[$type],$path);
  else $all_files_by_type[$type]=array($path);
 }
 
 return $all_files_by_type;
}

function dir_getAll($_dir){
 $rep=opendir($_dir);
 $array=array();
 while($file=readdir($rep)) if($file != '..' && $file !='.' && $file !=''){array_push($array,"$_dir$file");}
 closedir($rep);
 clearstatcache();
 return $array;
}
*/
?>
