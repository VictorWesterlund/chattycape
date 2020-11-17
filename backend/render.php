<?php

	class Layer {

		public function __construct($file) {
			$this->image = imagecreatefrompng($file);
			$this->size = list($width,$height,$type,$attr) = getimagesize($file);
		}

	}

	class Main {

		private $serversDir = "./servers/";

		public function __construct() {
			$this->config = $this->importConfig();
			$this->init();
		}

		private function importConfig() {
			$server = $_GET["server"];

			$config = $serversDir."config.json";

			if(!file_exists($config)) {
				throw new Exception(["400","Server not in config"]);
			}

			return json_decode(file_get_contents($config));
		}

		function init() {
			$bg = new Layer("background.png");

			# Prepare final image
			$cape = imagecreatetruecolor($bg->size[0],$bg->size[1]);
			imagealphablending($cape,true);
			imagesavealpha($cape,true);
		}

	}

	new Main();