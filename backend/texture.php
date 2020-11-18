<?php

	require "classes/Minotar.php"; // Player avatar
	require "classes/TextLayer.php";

	// Main class
	class Texture {

		public function __construct() {
			$this->input = [
				"server" => $_GET["server"],
				"username" => $_GET["username"],
				"tag" => $_GET["tag"].".png"
			];

			$this->path = "servers/{$this->input["server"]}/";

			$this->validate();
		}

		// Make sure all required urlparams are set
		private function validate() {
			foreach($this->input as $key => $value) {
				if(!$value) {
					$error[] = "Missing urlparam: '{$key}'.";
				}
			}

			if($error) {
				http_response_code("400 Bad Request");
				echo implode(" ",$error);
				die();
			}

			return true;
		}

		// Create a new texture
		function create($x,$y) {
			// Layers
			$bg = imagecreatefrompng($this->path."bg.png");
			$player = new Minotar($this->input["username"],100);
			$name = new TextLayer($this->input["username"],$this->path,30);
			$tag = imagecreatefrompng($this->path."tags/".$this->input["tag"]);
			
			// Create texture
			$image = imagecreatetruecolor($x,$y);
			$alpha = imagecolorallocatealpha($image,0,0,0,127);
			$color = imagecolorallocate($image,255,255,255);

			// Preserve transparency
			imagefill($image,0,0,$alpha);
			imagesavealpha($image,true);

			// Blend layers
			imagecopy($image,$bg,0,0,0,0,$x,$y); // Background
			imagecopy($image,$player->image,45,60,0,0,$player->size[0],$player->size[1]); // Player avatar
			$name->textcopy($image,110,210,$color); // Player name
			imagecopy($image,$tag,0,0,0,0,$x,$y); // Player rank

			// Output image
			header("Content-Type: image/png");
			echo imagepng($image);;
		}

	}

	$texture = new Texture();
	$texture->create(355,275);