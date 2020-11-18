<?php

	// Get Minotar from API
	class Minotar {

		public function __construct($username,$size) {
			$this->url = "https://minotar.net/armor/bust/{$username}/{$size}.png";

			$this->data = $this->curl();
			$this->image = imagecreatefromstring($this->data);
			$this->size = [imagesx($this->image),imagesy($this->image)];
		}

		private function curl() {
			$curl = curl_init();

			curl_setopt($curl, CURLOPT_URL, $this->url); 
			curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1); // good edit, thanks!
			curl_setopt($curl, CURLOPT_BINARYTRANSFER, 1); // also, this seems wise considering output is image.

			$data = curl_exec($curl);
			curl_close($curl);

			return $data;
		}
	
	}